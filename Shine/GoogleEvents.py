import time
import json
from google.assistant.library.event import EventType
from Shine.Command import Command

# get google events and commands and transform them to unified messages
class GoogleEvents:
    def __init__(self, assistant, utils):
        self._assistant = assistant
        self.command = Command()
        self._utils = utils
        self._logger = self._utils._logger


        #self._queue = queue
        #self._media = media
        #self._light = light
        #self._hue= hue


    def getEvent(self, event):
        # assistant listening
        if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self.command.modules['leds'].setCurLight(1)
            self.command.modules['leds'].setState(1)
            self._logger.info('Google Event: conversation started');

        # assistant finished listening
        if event.type == EventType.ON_END_OF_UTTERANCE:
            #self.command.modules['leds'].setCurLight(1)
            self._logger.info('Google Event: end of utterance');

        # assistant recognized speech
        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
            self.command.modules['leds'].setCurLight(1)
            self.processEvent(event)
            self._logger.info('Google Event: speech recognized: ' + json.dumps(event.args));

        # assistant started responding
        if event.type == EventType.ON_RESPONDING_STARTED:
            self.command.modules['leds'].setCurLight(1)
            self._logger.info('Google Event: respoding ');

        # assistant finished
        if event.type == EventType.ON_RESPONDING_FINISHED:
            #self.command.modules['leds'].setCurLight(0)
            self._logger.info('Google Event: finished respoding');

        if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
                event.args and not event.args['with_follow_on_turn']):
            self.command.modules['leds'].setCurLight(0)
            self.command.modules['media'].UnpauseForSpeaking()
            self._logger.info('Google Event: conversation turn ended: no follow up');

        if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
                event.args and event.args['with_follow_on_turn']):
            self.command.modules['leds'].setCurLight(1)
            self._logger.info('Google Event: conversation turn ended: with follow up' );

        if (event.type == EventType.ON_ALERT_STARTED):
            self.command.modules['leds'].setCurLight(2)
            self.command.modules['leds'].setColor('alarm')
            self._logger.info('Google Event: alert started ' + json.dumps(event.args));

        if (event.type == EventType.ON_ALERT_FINISHED):
            self.command.modules['leds'].setCurLight(0)
            self.command.modules['leds'].setColor('rainbow')
            self._logger.info('Google Event: alert finished');
            #self._logger.info('ON_ALERT_FINISHED: ' + json.dumps(event.args));

        if (event.type == EventType.ON_ASSISTANT_ERROR):
            self.command.modules['leds'].setCurLight(0)
            #self.command.modules['leds'].setColor('red')
            self._logger.info('Google Event: assistant error : ' + json.dumps(event.args));

        commands = self.command.getCommands()
        return commands
        #print (self.command.getCommands())
        #self._queue.put(self._light)




    def processEvent(self, event):
        stop = 0
        strings = {}

        command = ''
        if (event.args['text']):
            command = event.args['text'].lower()

        commands = command.split('and')

        #misc commands
        strings["less_light"] = "less light"
        strings["more_light"] = "more light"
        strings["dim_to"] = "dim to"
        strings["light_up"] = "light up"
        strings["color_to"] = "change color to"

        for command in commands:
            #search in hue scenes and activate
            if (command != '' and self._utils._hue.searchScenes(command)):
                self._assistant.stop_conversation()
                #de revenit


            if (event.args['text'].lower().find(strings["dim_to"]) != -1):
                b = [int(s) for s in event.args['text'].replace('%', '').split() if s.isdigit()]
                self._assistant.stop_conversation()

                bri = int((int(b[0])*255)/100)
                self.animateLights('', bri)


            if (event.args['text'].lower().find(strings["color_to"]) != -1):
                color = event.args['text'].replace('change color to ', '')
                self.command.modules['leds'].setColor(color.lower())
                self.command.modules['leds'].setCurLight(0)
                stop = 1

            if (event.args['text'].lower().find(strings["light_up"]) != -1):
                self.command.modules['leds'].setColor('white')
                self.command.modules['hue'].setScene('lightup')
                self.animateLights('white', 255)

                #stop = 1
            if (event.args['text'].lower().find(strings["less_light"]) != -1):
                self.animateLights('', 'less')

            if (event.args['text'].lower().find(strings["more_light"]) != -1):
                self.animateLights('', 'more')

            if (event.args['text'].lower().find('test') != -1):
                #self._hue.createDefaults()
                stop = 1


        #----------cast----------#
        #get devices and create commands
        devices = self._utils._media.cast.getDevices()
        #devices = ['video', 'music']
        for command in commands:
            #play, pause, stop, mute simple commands
            if (command == 'play'):
                devices = self._utils._media.cast.getPlayingDevices()
                if (len(devices) == 1):
                    cast = devices[0]
                    self.command.modules['cast'].play(cast)
                    stop = 1

            if (command == 'stop'):
                devices = self._utils._media.cast.getPlayingDevices()
                if (len(devices) == 1):
                    cast = devices[0]
                    self.command.modules['cast'].stop(cast)
                    stop = 1

            if (command == 'pause'):
                devices = self._utils._media.cast.getPlayingDevices()
                if (len(devices) == 1):
                    cast = devices[0]
                    self.command.modules['cast'].pause(cast)
                    stop = 1

            if (command == 'mute'):
                devices = self._utils._media.cast.getPlayingDevices()
                if (len(devices) == 1):
                    cast = devices[0]
                    self.command.modules['cast'].mute(cast)
                    stop = 1

            if (command == 'unmute'):
                devices = self._utils._media.cast.getPlayingDevices()
                if (len(devices) == 1):
                    cast = devices[0]
                    self.command.modules['cast'].unmute(cast)
                    stop = 1




            if (command.startswith('play ')):
                terms = command.split()
                device = terms[-1]
                #gotta check if device in devices
                if (device in devices):
                    #self._media.cast.Play(device)
                    self.command.modules['cast'].play(device)
                    stop = 1

            if (command.startswith('stop ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    #self._media.cast.Stop(device)
                    self.command.modules['cast'].stop(device)
                    #stop = 1

            if (command.startswith('pause ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    #self._media.cast.Pause(device)
                    self.command.modules['cast'].pause(device)
                    #stop = 1

            if (command.startswith('unpause ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    #self._media.cast.Unpause(device)
                    self.command.modules['cast'].unpause(device)
                    #stop = 1

            if (command.startswith('mute ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    #self._media.cast.Mute(device)
                    self.command.modules['cast'].mute(device)

            if (command.startswith('unmute ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    #self._media.cast.Unmute(device)
                    self.command.modules['cast'].unmute(device)

            if (command.startswith('volume up on ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    #self._media.cast.VolumeUp(device)
                    self.command.modules['cast'].volumeUp(device)

            if (command.startswith('volume down on ')):
                terms = command.split()
                device = terms[-1]
                if (device in devices):
                    self.command.modules['cast'].volumeDown(device)
                    #self._media.cast.VolumeDown(device)

            if (command.find('volume to on ') != -1):
                terms = command.split()
                device = terms[-1]
                b = [int(s) for s in command.replace('%', '').split() if s.isdigit()]
                if (device in devices):
                    self._media.cast.VolumeTo(device, b[0])
                    self.command.modules['cast'].volumeTo(device)
                    stop = 1

            if (command.find('status') != -1):
                self._assistant.stop_conversation()
                self.command.modules['cast'].status()


        #----------music----------#
        strings["play_green"] = "play green"
        strings["play_green_music"] = "play green on music"
        strings["play_red_music"] = "play red on music"
        strings["play_blue_music"] = "play blue on music"

        for command in commands:
            if (event.args['text'].lower() == strings["play_green"]):
                #self._media.speakers.PlayGreen()
                self.command.modules['media'].playSource('green')
                #self._assistant.stop_conversation()
                #stop = 1

            if (event.args['text'].lower() == strings["play_green_music"]):
                #self._assistant.stop_conversation()
                self.command.modules['cast'].playSource(device, 'green')

            if (event.args['text'].lower() == strings["play_red_music"]):
                #self._assistant.stop_conversation()
                self.command.modules['cast'].playSource(device, 'red')

            if (event.args['text'].lower() == strings["play_blue_music"]):
                #self._assistant.stop_conversation()
                self.command.modules['cast'].playSource(device, 'blue')


        #----------lights----------#
        strings["movie_time"] = "movie time"
        strings["im_home"] = "i'm home"
        strings["goodbye"] = "goodbye"
        strings["goodnight"] = "good night"
        strings["goodmorning"] = "good morning"

        strings["lights_off"] = "lights off"
        strings["lights_on"] = "lights on"

        strings["turn_off"] = "turn off"
        strings["turn_on"] = "turn on"

        #print (commands)
        for command in commands:
            if (event.args['text'].lower().find(strings["movie_time"]) != -1):
                self.command.modules['hue'].setScene('movie')
                self.command.modules['leds'].setColor('rainbow')
                self.animateLights('rainbow', 5)

            if (event.args['text'].lower().find(strings["im_home"]) != -1):
                self.command.modules['hue'].toggleLights(True)
                self.command.modules['hue'].setScene('home')
                self.command.modules['leds'].setColor('rainbow')
                self.command.modules['leds'].setState(1)
                self.animateLights('rainbow', 128)

            if (event.args['text'].lower().find(strings["goodbye"]) != -1):
                self.command.modules['hue'].setScene('out')
                self.command.modules['leds'].setColor('rainbow')
                self.animateLights('rainbow', 64)

            if (event.args['text'].lower().find(strings["goodnight"]) != -1):
                self.command.modules['leds'].setCurLight(0)
                self.command.modules['leds'].setColor('rainbow')
                self.animateLights('rainbow', 1)
                self.command.modules['hue'].slowOff(True)
                #self._media.turnOff()
                self.command.modules['cast'].turnOff()

            if (event.args['text'].lower().find(strings["goodmorning"]) != -1):
                self.command.modules['hue'].setScene('home')
                self.command.modules['leds'].setColor('rainbow')
                self.animateLights('rainbow', 250)

            if (event.args['text'].lower().find(strings["lights_on"]) != -1):
                self.command.modules['hue'].toggleLights(True)
                self.command.modules['hue'].setScene('home')
                self.command.modules['leds'].setColor('rainbow')
                self.command.modules['leds'].setCurLight(0)
                self.command.modules['leds'].setState(1)
                self.command.modules['leds'].setBrightness(128)
                stop = 1

            if (event.args['text'].lower().find(strings["lights_off"]) != -1):
                self.command.modules['hue'].toggleLights(False)
                self.command.modules['leds'].setCurLight(0)
                self.command.modules['leds'].setState(0)
                stop = 1

            if (event.args['text'].lower().find(strings["turn_off"]) != -1):
                self.command.modules['leds'].setState(0)
                self.command.modules['leds'].setCurLight(0)
                stop = 1

            if (event.args['text'].lower().find(strings["turn_on"]) != -1):
                self.command.modules['leds'].setCurLight(0)
                self.command.modules['leds'].setState(1)
                self.command.modules['leds'].setBrightness(128)
                stop = 1


        #----------TV----------#
        strings["turn_on_tv"] = "tv on"
        strings["turn_off_tv"] = "tv off"
        strings["turn_on_the_tv"] = "turn on the tv"
        strings["turn_off_the_tv"] = "turn off the tv"
        strings["mute_tv"] = "mute tv"
        strings["unmute_tv"] = "unmute tv"
        strings["mute_the_tv"] = "mute the tv"
        strings["unmute_the_tv"] = "unmute the tv"
        strings["volume_up_tv"] = "volume up on tv"
        strings["volume_down_tv"] = "volume down on tv"
        strings["volume_to_on_tv"] = "volume on tv to"
        strings["prevent_sleep"] = "don't sleep"
        strings["tv_hdmi1"] = "turn the tv on hdmi 1"
        strings["tv_hdmi2"] = "turn the tv on hdmi 2"
        strings["tv_hdmi3"] = "turn the tv on hdmi 3"

        for command in commands:
            if (event.args['text'].lower().find(strings["turn_on_tv"]) != -1):
                self._media.tv.turnon()
                stop = 1

            if (event.args['text'].lower().find(strings["turn_off_tv"]) != -1):
                self._media.tv.turnoff()
                stop = 1

            if (event.args['text'].lower().find(strings["turn_on_the_tv"]) != -1):
                self._media.tv.turnon()
                stop = 1

            if (event.args['text'].lower().find(strings["turn_off_the_tv"]) != -1):
                self._media.tv.turnoff()
                stop = 1

            if (event.args['text'].lower().find(strings["mute_tv"]) != -1):
                self._media.tv.mute()
                stop = 1

            if (event.args['text'].lower().find(strings["mute_the_tv"]) != -1):
                self._media.tv.mute()
                stop = 1

            if (event.args['text'].lower().find(strings["unmute_tv"]) != -1):
                self._media.tv.unmute()
                stop = 1

            if (event.args['text'].lower().find(strings["unmute_the_tv"]) != -1):
                self._media.tv.unmute()
                stop = 1

            if (event.args['text'].lower().find(strings["volume_up_tv"]) != -1):
                self._media.tv.volumeUp()
                stop = 1

            if (event.args['text'].lower().find(strings["volume_down_tv"]) != -1):
                self._media.tv.volumeDown()
                stop = 1

            if (event.args['text'].lower().find(strings["prevent_sleep"]) != -1):
                self._media.tv.preventSleep()
                stop = 1

            if (event.args['text'].lower().find(strings["volume_to_on_tv"]) != -1):
                b = [int(s) for s in event.args['text'].replace('%', '').split() if s.isdigit()]
                self._media.tv.VolumeTo(b[0])
                stop = 1

            if (event.args['text'].lower().find(strings["tv_hdmi1"]) != -1):
                self._media.tv.hdmi1()
                stop = 1

            if (event.args['text'].lower().find(strings["tv_hdmi2"]) != -1):
                self._media.tv.hdmi2()
                stop = 1

            if (event.args['text'].lower().find(strings["tv_hdmi3"]) != -1):
                self._media.tv.hdmi3()
                stop = 1

        if (stop == 1):
            self._assistant.stop_conversation()

        #self._queue.put(self._light)


    def animateLights(self, color, brightness):
        if (color):
            self.command.modules['leds'].setColor(color)
        self.command.modules['leds'].brightnessTo(brightness)
        self.command.modules['leds'].setCurLight(3)
