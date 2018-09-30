import time
import ast
import sys
import multiprocessing
from neopixel import *

from Shine.Light  import Light
from Shine.Config import Config
from Shine.BendingColors import BendingColors


LED_STRIP      = ws.SK6812_STRIP_GRBW   # Strip type and colour ordering

# led class for performing operations on the device leds (color animation, brightness, state)
class LED:
    def __init__(self, logger):
        self.config = Config()
        leds = self.config.getSection('LEDS')
        self.logger = logger
        self.logger.info('LEDS: Starting')
        self.params = Light()
        #self.strip = Adafruit_NeoPixel(int(leds['count']), int(leds['pin']), int(leds['freq_hz']), int(leds['dma']), bool(leds['invert']), int(leds['brightness']), int(leds['channel']), LED_STRIP)
        self.strip = Adafruit_NeoPixel(int(leds['count']), int(leds['pin']), int(leds['freq_hz']), int(leds['dma']), ast.literal_eval(leds['invert']), int(leds['brightness']), int(leds['channel']), LED_STRIP)
        #self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
        self.strip.begin()
        self.delay = 2.5

	# read queue messages
    def readMessages(self):
        messages = []
        while self.queue.qsize():
            msg = self.queue.get()
            messages.append(msg)

        if (len(messages)):
            for message in messages:
                for key in message:
                    if (key == 'curLight'):
                        self.params.setCurLight(message[key])

                    if (key == 'brightness'):
                        self.params.setBrightness(message[key])

                    if (key == 'color'):
                        self.params.setColor(message[key])

                    if (key == 'state'):
                        self.params.setState(message[key])

                    if (key == 'brightnessTo'):
                        self.params.setBrightnessTo(message[key])

	# main function. called when starting the subthread from the main file
    def LightUP(self, queue, utils):
        p = multiprocessing.current_process()
        self.logger.info('LEDS PID: '+str(p.pid))

        self._utils = utils
        self.queue = queue

        brightness = int(self.config.getSection('LEDS')['brightness'])
        self.strip.setBrightness(brightness)

        self.strip.show()
        self.logger.info('LEDS: Started')
        self.readMessages()

        while True:
            self.readMessages()
            self.checkBrightness()

            while self.params.getState() == 'off':
                #assistant is off
                self.readMessages()
                self.checkBrightness()
                self.offAnimation()

            one = False
            while (self.params.getState() == 'on' and (self.params._curLight == 0 or self.params._curLight == 1) and not self.params._brightnessTo):
                self.readMessages()
                self.checkBrightness()
                if (self.params._curLight == 0 or self.params._curLight == 1):

                    if (self.params._color == "rainbow" or self.params._curLight == 1):
                        #self.rainbowAnimation()
                        self.frozenAnimation()
                        #print ('Exiting')
                        #sys.exit()

                        #to remove
                        #if (not one):
                        #    print ('animating once')
                        #    self.rainbowAnimation()
                        #    one = True

                    if (self.params._curLight == 0):
                        self.delay = 25
                    elif(self.params._curLight == 1):
                        self.delay = 10
                    else:
                        self.delay = 10

                if (self.params._curLight == 0):
                    if (self.params._color == 'red'):
                        self.delay = 50
                        self.colorAnimation('red')

                    if (self.params._color == 'white'):
                        self.delay = 50
                        self.colorAnimation('white')

                    if (self.params._color == 'blue'):
                        self.delay = 50
                        self.colorAnimation('blue')

                    if (self.params._color == 'yellow'):
                        self.delay = 50
                        self.colorAnimation('yellow')

                    if (self.params._color == 'green'):
                        self.delay = 50
                        self.colorAnimation('green')

                    if (self.params._color == "party"):
                        self.delay = 50
                        self.partyAnimation()
                        exit

            while (self.params.getState() == 'on' and (self.params._curLight == 2)):
                self.readMessages()
                self.checkBrightness()
                self.alarmAnimation()

            self.checkBrightness()

    def checkBrightness(self):
        if(self.params._brightnessTo > 0):
            b = self.params._brightness
            t = self.params._brightnessTo
            self.params._brightnessTo = 0
            self.animateBrightness(b, t)
            self.params._curLight = 0

    def partyAnimation(self):
        colors = self._utils._hue.getCurrentColors()
        self.strip.setBrightness(40)
        for i in range(1, 8):
            c = colors[0]
            self.strip.setPixelColor(i, Color(c[0], c[1], c[2]))
            #self.strip.setBrightness(c['bri'])

        for i in range(9, 16):
            c = colors[1]
            self.strip.setPixelColor(i, Color(c[0], c[1], c[2]))
            #self.strip.setBrightness(c['bri'])

        for i in range(16, 24):
            c = colors[2]
            self.strip.setPixelColor(i, Color(c[0], c[1], c[2]))
            #self.strip.setBrightness(c['bri'])

        self.strip.show()
        time.sleep(500/1000.0)

    def alarmAnimation(self):
        self.checkBrightness()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(255, 128, 0))
        self.strip.show()

        for k in range (self.params.getBrightness(), int(self.params.getBrightness()/2), -1):
            if (k % 5 == 0):
                self.readMessages()
                self.checkBrightness()

            if (self.params._curLight != 2):
                break
            self.strip.setBrightness(k)
            self.strip.show()
            time.sleep(self.delay/1000.0)

        for j in range(int(self.params.getBrightness()/2), self.params.getBrightness()):
            if (k % 5 == 0):
                self.readMessages()
                self.checkBrightness()

            if (self.params._curLight != 2):
                break

            self.strip.setBrightness(j)
            self.strip.show()
            time.sleep(self.delay/1000.0)

    def frozenAnimation(self):
        count = int(self.strip.numPixels())
        bc = BendingColors()
        steps = 50
        #colors = bc.gradient('#00ffcb', '#004eff', steps)
        colors = bc.gradient('#ff0000', '#0000ff', steps)
        #colors = bc.gradient('#0090ff', '#00ff00', steps)
        rcolors = []
        for x in range(len(colors) - 1, 0, -1):
            rcolors.append(colors[x])
            
        idx = 0

        #for i in range(int(self.strip.numPixels())):
            #c = colors[0]
            #self.strip.setPixelColor(i, Color(c['red'], c['green'], c['blue']))
        #    self.strip.setPixelColor(i, Color(0, 0, 0))

        animationFinished = False
        offset = 0
        while (not animationFinished):
            for i in range(int(self.strip.numPixels() - 1)):
                c = colors[offset + i]
                self.strip.setPixelColor(i, Color(c['red'], c['green'], c['blue']))
				#strip.setPixelColor(i + int(count/2), Color(c['red'], c['green'], c['blue']))

            colorIdx = 1
            colorIdx2 = 1
            t = 0
            self.delay = 50
            for c in colors:
                #if (colorIdx2 % 5 == 0):
                    #self.readMessages()
                    #self.checkBrightness()

                for i in range(0, colorIdx - 1):
                    currentColor = colors[colorIdx2 - i - 1]
                    self.strip.setPixelColor(i, Color(currentColor['red'], currentColor['green'], currentColor['blue']))
    				#strip.setPixelColor(i + int(count/2), Color(currentColor['red'], currentColor['green'], currentColor['blue']))
                    #print (colorIdx2, colorIdx, i)

                if (self.params._curLight == 0):
                    t += 1
                    p = t/25
                    self.delay = self.easeInOutQuint(p, 5, 50, 1)
                elif(self.params._curLight == 1):
                    self.delay = 1
                else:
                    self.delay = 1

                time.sleep(self.delay/1000.0)
                self.strip.show()

                colorIdx2 += 1
                if (colorIdx >= 18):
                    colorIdx = 18
                else:
                    colorIdx += 1

            colorIdx = 0
            colorIdx2 = 0
            self.delay = 50
            t = 0

            for c in colors:
                #if (colorIdx2 % 5 == 0):
                    #self.readMessages()
                    #self.checkBrightness()

                for i in range(colorIdx - 1, 0, -1):
                    currentColor = colors[colorIdx2]
                    self.strip.setPixelColor(i, Color(currentColor['red'], currentColor['green'], currentColor['blue']))
    				#strip.setPixelColor(i + int(count/2), Color(currentColor['red'], currentColor['green'], currentColor['blue']))
                    #print (colorIdx2, colorIdx, i)

                if (self.params._curLight == 0):
                    t += 1
                    p = t/25
                    self.delay = self.easeInOutQuint(p, 5, 50, 1)
                elif(self.params._curLight == 1):
                    self.delay = 1
                else:
                    self.delay = 1

                time.sleep(self.delay/1000.0)
                self.strip.show()

                colorIdx2 += 1
                if (colorIdx >= 18):
                    colorIdx = 18
                else:
                    colorIdx += 1

            animationFinished = True


            #offset += 1
            #if (offset + count/2 >= steps):
            #    animationFinished = True




    def colorAnimation(self, color):
        if (color == "red"):
            c = Color(255, 0, 0)
            #c = Color(255, 0, 176)

        if (color == "white"):
            c = Color(243, 247, 218)

        if (color == "green"):
            c = Color(0, 255, 12)

        if (color == "blue"):
            c = Color(0, 229, 255)

        if (color == "yellow"):
            c = Color(255, 241, 0)


        for i in range (self.strip.numPixels()):
            self.strip.setPixelColor(i, c)
        self.strip.setBrightness(self.params._brightness)
        self.strip.show()
        time.sleep(self.delay/1000.0);

    def rainbowAnimation(self):
        #part = 0
        #if (part == 0):
        j = 0
        t = 0
        switch = False
        end = False
        while (j <= 255 and not end):
            if (j % 5 == 0):
                self.readMessages()
                self.checkBrightness()

            for i in range (self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))

            self.strip.setBrightness(self.params._brightness)
            if (j % 5 == 0):
                self.strip.show()

            if (self.params._curLight == 0):
                t += 1
                if (not switch):
                    #self.delay = 50
                    p = t/383
                else:
                    p = t/75
                self.delay = self.easeInOutQuint(p, 5, 50, 1)
            elif(self.params._curLight == 1):
                self.delay = 1
            else:
                self.delay = 1

            time.sleep(self.delay/1000.0)

            if (j == 255):
                t = 0
                switch = True

            if (switch and j == 129):
                end = True

            if (not switch):
                j += 1
            else:
                j -= 1

            #print (j)

        j = 128
        t = 0
        while (j >= 0):
            if (j % 5 == 0):
                self.readMessages()
                self.checkBrightness()

            #for i in range (self.strip.numPixels()):
            #    self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))

            #self.strip.setBrightness(self.params._brightness)
            #self.strip.show()

            if (self.params._curLight == 0):
                self.delay = 50
                t += 1
                p = t/255
                self.delay = self.easeInOutQuint(p, 5, 50, 1)
            elif(self.params._curLight == 1):
                self.delay = 1
            else:
                self.delay = 1

            time.sleep(self.delay/1000.0)
            j -= 1

    def animateBrightness(self, current, to):
        #print ('animating brightness '+str(current)+' '+str(to))
        if (current == to):
            self.strip.setBrightness(to)
            self.strip.show()
            return

        #delay = 1000/(current-to)
        #delay = self.easeInOutQuint(p, current, to, 1)
        #if (delay < 0):
        #    delay = -1 * delay

        #print ('starting at '+str(current))
        j = 0
        c = self.params.getBrightness()
        t = to
        if (current > to):
            c = to
            t = self.params.getBrightness()
        step = 1000/(t - c)
        #print (t, c, step)
        while (self.params.getBrightness() != to):
            j += step
            if (to > self.params.getBrightness()):
                nxt = self.params.getBrightness() + 1
            else:
                nxt = self.params.getBrightness() - 1

            self.params.setBrightness(nxt)
            self.strip.setBrightness(nxt)
            delay = self.easeInQuint(j, 1, 200, 1700)
            #print (j, self.params.getBrightness(), delay)
            self.strip.show()
            time.sleep(delay/1000)
        #print ('ending at '+str(nxt))


    def offAnimation(self):
        if (self.params.getBrightness() >= 0):
            self.animateBrightness(self.params.getBrightness(), 0)
            #animate brightness
            #while (self.params.getBrightness() >= 0 and self.params.getState() == 'off'):
            #    self.readMessages()

            #    if (self.params.getBrightness() > 0):
            #        self.params.setBrightness(self.params.getBrightness() - 1)
            #        self.strip.setBrightness(self.params.getBrightness())
            #        self.strip.show()
            #        time.sleep(10/1000.0)
            #    else:
            #        self.params.setBrightness(0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def easeInOutQuint(self, t, b, c, d):
        if (t > 0):
            t /= d/2
        else:
            t = 0

        if (t < 1):
            return c/2*t*t*t*t*t + b

        t -= 2
        return c/2*(t*t*t*t*t + 2) + b

    def easeInQuint(self, t, b, c, d):
        t /= d
        return c*t*t*t*t*t + b
