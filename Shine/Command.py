# classes for transforming operations into unified messages
# @todo a lot of refactoring
class Command:
    def __init__(self):
        self.commands = []
        self.modules = {}
        parent = self
        self.modules['leds'] = Leds(parent)
        self.modules['media'] = Media(parent)
        self.modules['hue'] = Hue(parent)
        self.modules['cast'] = Chromecast(parent)
        

    def addCommand(self, command):
        self.commands.append(command)

    def getCommands(self):
        return self.commands
        


class Leds:
    def __init__(self, parent):
        self._module = 'leds'
        self.parent = parent

    def setCurLight(self, value):
        action = 'currentLight'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def setState(self, value):
        action = 'state'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def setColor(self, value):
        action = 'color'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def setBrightness(self, value):
        action = 'brightness'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def brightnessTo(self, value):
        action = 'brightnessTo'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

class Media:
    def __init__(self, parent):
        self._module = 'media'
        self.parent = parent

    def PauseLocal(self, value):
        action = 'pause'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def playSource(self, source):
        action = 'playSource'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"speakers", "source":"' + str(source)+ '"}}'
        self.parent.addCommand(r)

    def PauseForSpeaking(self):
        action = 'pauseForSpeaking'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{}}'
        self.parent.addCommand(r)

    def UnpauseForSpeaking(self):
        action = 'unPauseForSpeaking'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{}}'
        self.parent.addCommand(r)



class Hue:
    def __init__(self, parent):
        self._module = 'hue'
        self.parent = parent

    def setScene(self, value):
        action = 'setScene'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def toggleLights(self, value):
        action = 'toggleLights'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

    def slowOff(self, value):
        action = 'slowOff'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"value":"' + str(value)+ '"}}'
        self.parent.addCommand(r)

        
class Chromecast:
    def __init__(self, parent):
        self._module = 'chromecast'
        self.parent = parent

    def play(self, device):
        action = 'play'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)
        
    def pause(self, device):
        action = 'pause'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def unpause(self, device):
        action = 'unpause'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def stop(self, device):
        action = 'stop'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def mute(self, device):
        action = 'mute'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def unmute(self, device):
        action = 'unmute'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def volumeUp(self, device):
        action = 'volumeUp'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def volumeDown(self, device):
        action = 'volumeDown'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '"}}'
        self.parent.addCommand(r)

    def volumeTo(self, device, volume):
        action = 'stop'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '", "volume":"' + str(volume)+ '"}}'
        self.parent.addCommand(r)

    def status(self):
        action = 'status'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{}}'
        self.parent.addCommand(r)

    def playSource(self, device, source):
        action = 'playSource'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{"device":"' + str(device)+ '", "source":"' + str(source)+ '"}}'
        self.parent.addCommand(r)

    def turnOff(self):
        action = 'turnOff'
        r = '{"module":"' + self._module + '", "command": "' + action +'", "parameters":{}}'
        self.parent.addCommand(r)

