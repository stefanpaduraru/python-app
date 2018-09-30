import pychromecast

# cast class for controlling google chromecast devices
class Cast:
    def __init__(self, devices, logger):
        self._sources = {'blue':'http://s2.voscast.com:8964/stream', 'red':'http://s2.voscast.com:8968/stream', 'green':'http://s2.voscast.com:8966/stream'}
        self._logger = logger

        #devices = pychromecast.get_chromecasts()
        self.devices = {}
        for cast in devices:
            cast.wait()
            self.devices[cast.device.friendly_name.lower()] = cast
            self.devices[cast.device.friendly_name.lower()].mc = cast.media_controller
            self._logger.info('Found cast device '+cast.device.friendly_name+' at '+cast.host)
        #print(self.devices)

    def getDevices(self):
        devices = {}
        for cast in self.devices:
            devices[cast] = cast
        return devices

    def Status(self):
        for cast in self.devices:
            print (cast)
            print(self.devices[cast].status)
            print ('---------------------------------------------------')

    def MCStatus(self):
        for cast in self.devices:
            print (cast)
            print(self.devices[cast].mc.status)
            print ('---------------------------------------------------')

    def getPlayingDevices(self):
        playing = list()
        self.Status()
        self.MCStatus()
        for device in self.devices:
            if (self.devices[device] and self.devices[device].mc):
                cast = self.devices[device]
                #print (cast.status.app_id)
                #or cast.status.app_id != 'None'
            if (cast.mc.status.player_state == "PLAYING"):
                playing.append(device)

        print (playing)
        return playing


    def Play(self, device):
        if (self.devices[device] and self.devices[device].mc):
            cast = self.devices[device]
            self.Unmute(device)
            if (cast.status.volume_muted):
                # unmute
                self.Unmute(device)
            else:
                # play
                self._logger.info('Playing '+device)
                cast.mc.play()

    def Pause(self, device):
        if (self.devices[device] and self.devices[device].mc):
            cast = self.devices[device]
            if (cast.mc.status.supports_pause):
                # pause if it supports
                cast.mc.pause()
            else:
                # mute
                self.Mute(device)

    def Unpause(self, device):
        if (self.devices[device] and self.devices[device].mc):
            cast = self.devices[device]
            if (cast.mc.status.player_state == 'PAUSED'):
                self._logger.info('VIDEO: Unpausing chromecast '+device)
                cast.mc.play();
            elif (cast.status.volume_muted):
                self.Unmute(device)

    def Stop(self, device):
        if (self.devices[device] and self.devices[device].mc):
            cast = self.devices[device]
            if (cast.mc.status.player_state == "PLAYING"):
                cast.mc.stop()
                self._logger.info('CAST: Stopping play on '+device)

    def Mute(self, device):
        if (self.devices[device]):
            cast = self.devices[device]
            cast.set_volume_muted(True)

    def Unmute(self, device):
        if (self.devices[device] and self.devices[device].mc):
            cast = self.devices[device]
            cast.set_volume_muted(False)

    def VolumeUp(self, device):
        if (self.devices[device]):
            cast = self.devices[device]
            cast.volume_up()

    def VolumeDown(self, device):
        if (self.devices[device]):
            cast = self.devices[device]
            cast.volume_down()

    def VolumeTo(self, device, v):
        if (self.devices[device]):
            cast = self.devices[device]
            cast.set_volume(v)

    def playSource(self, device, src):
        self.devices[device].mc.play_media(self._sources[src], 'audio/mp3')
        self.devices[device].mc.block_until_active()
        self._logger.info('CAST: Playing '+src+' on '+device)

    def turnOff(self):
        for device in self.devices:
            self.Stop(device)
