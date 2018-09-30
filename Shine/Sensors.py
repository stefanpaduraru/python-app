from __future__ import print_function
import smbus
import time
import os
import json
from Shine.CapacitiveButtons import CapacitiveButtons
from Shine.Config import Config

# used for reading data from embedded sensors (ambient light brightness, capacitive touch sensor)
class Sensors:
    def __init__(self):
        self.config = Config()
        self.settings = self.config.getSection('SENSORS')
        if (self.settings['capacitive']):
            self.initCapButtons()
        

    def run (self):
        #self.queue = queue

        if (self.settings['brightness']):
            bri = self.readBrightness()
            message = "{'module': 'sensors', 'command': 'brightness', 'parameters': {'full': '"+str(bri['full'])+"', 'infrared':'"+str(bri['infrared'])+"', 'visible':'"+str(bri['visible'])+"'}}"
            #self.queue.put(message)
            print (message)

        if (self.settings['capacitive']):
            pressed = self.readCapButtons()
            message = "{'module': 'sensors', 'command': 'cap', 'parameters': {'buttons': "+str(pressed)+"}}"
            print (message)
            #self.queue.put(message)
            #construct message
            
        if (self.settings['push']):
            pressed = self.readPushButtons()
            message = "{'module': 'sensors', 'command': 'push', 'parameters': {'pressed': '"+str(pressed)+"'}}"
            print (message)
            #self.queue.put(message)
            
        time.sleep(1)


    def readBrightness(self):
        # Get I2C bus
        bus = smbus.SMBus(1)
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)
        time.sleep(0.5)

        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
        data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

        full = data[1] * 256 + data[0]
        infrared = data1[1] * 256 + data1[0]
        visible = full - infrared

        return {'visible': visible, 'infrared': infrared, 'full': full}

    def initCapButtons(self):
        bus = smbus.SMBus(1)
        self.capButtons = CapacitiveButtons(0x29, bus, touch_offset = 0)

    def readCapButtons(self):
        self.capButtons.multitouch_enabled = False
        self.capButtons.leds_linked = True
        self.capButtons.write_register(CapacitiveButtons.STANDBYCFG, 0x30)

        touched = list()
        touched = self.capButtons.touched
        return touched

    def readPushButtons(self):
        return False

