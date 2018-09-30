# light object to map led properties
class Light:
    def __init__(self):
        #curLight: 0 - normal, 1 - listening, 2 - alarm, 3 - brightness adjusting
        self._curLight = 0
        self._brightness = 100
        self._brightnessTo = 0
        self._color = 'rainbow'
        self._state = 'on'
   
    def setState(self, state):
        self._state = state
    
    def setCurLight(self, light):
        self._curLight = light

    def setBrightness(self, b):
        self._brightness = b

    def setBrightnessTo(self, b):
        self._brightnessTo = b
        
    def setColor(self, c):
        self._color = c

    def getState(self):
        return self._state
    
    def getBrightness(self):
        return self._brightness

    def getProps(self):
        return {'curLight': self._curLight, 'brightness': self._brightness, 'color': self._color, 'state': self._state}
