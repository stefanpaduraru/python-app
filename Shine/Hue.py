#!/usr/bin/env python
from qhue import *
import requests
import json
import time

from Shine.ColorConverter import Converter
from Shine.ColorConverter import GamutA
from Shine.ColorConverter import GamutB
from Shine.ColorConverter import GamutC

# handle philips hue api interaction
class Hue:
    def __init__(self, logger):
        self._user = 'zn64uaWzazjqIaKCE2w4idKIVanomqQV-ClOQcqr';
        self._host = '192.168.1.201'
        self._bridge = Bridge(self._host, self._user)
        self.connected = True
        #self.createDefaults()
        self._logger = logger
        self._logger.info('Found HUE lights at '+self._host)

    def createDefaults(self):
        if (not self.connected):
            return False

        self._logger.info('Hue: Creating defaults ')    
        group = []
        #create group
        g = {'name': 'Shine: All Lights', 'lights': self.getAllLightsIndex(), 'type': 'LightGroup', 'recycle': False}
        url = self._bridge.groups.url
        r = self.postRequest(url, json.dumps(g))

        allLightsGroup = self.getAllLightsGroup()
        schedules = []

        s = {'localtime': 'PT00:00:01', 'name':'Shine: Dim lights', 'description':'Shine dim lights to 60 in 0.2s', 'command':{'address':'', 'body':{'bri':60, 'transitiontime':10}, 'method':'PUT'}, 'autodelete':False, 'recycle':False, 'status': 'disabled'}
        s['command']['address'] = self._bridge.groups[allLightsGroup['ID']].address+'/action/'
        print (json.dumps(s))
        r = self.postRequest(self._bridge.schedules.url, json.dumps(s))

        s = {'localtime': 'PT00:00:20', 'name':'Shine: Turn off', 'description':'Shine turn lamps slowly off', 'command':{'address':'', 'body':{'on':False, 'transitiontime':100}, 'method':'PUT'}, 'autodelete':False, 'recycle':False, 'status': 'disabled'}
        s['command']['address'] = self._bridge.groups[allLightsGroup['ID']].address+'/action/'
        r = self.postRequest(self._bridge.schedules.url, json.dumps(s))
        

    def getAllLightsGroup(self):
        if (not self.connected):
            return False
        
        groups = self._bridge.groups
        groups = groups()

        for g in groups:
            group = groups[g]
            
            if (group['name'] == 'Shine: All Lights'):
                return {'ID':g, 'group':group}

        return False

    def getSchedule(self, name):
        if (not self.connected):
            return False
        
        schedules = self._bridge.schedules
        schedules = schedules()

        for s in schedules:
            schedule = schedules[s]
            
            if (schedule['name'] == name):
                return {'ID':s, 'schedule':schedule}

        return False

    def getAllLightsIndex(self):
        if (not self.connected):
            return False
        
        lights = self._bridge.lights
        aux = []
        for light in lights():
            aux.append(light)

        return aux

    def searchScenes(self, keyword):
        if (not self.connected):
            return False
        
        keyword.replace(' ', '').lower()
        scenes = self._bridge.scenes()
        
        for s in scenes:
            scene = scenes[s]
            name = scene['name'].replace(' ', '').lower()
            
            if (keyword in name):
                #activate scene
                url = self._bridge.groups[4].url + '/action'
                r = self.putRequest(url + '', json.dumps({'scene': s}))
                return True
            
        return False

    def getScene(self, id):
        if (not self.connected):
            return False
        
        scene = self._bridge.scenes[id]
        return scene()

    def getSceneColors(self, id):
        if (not self.connected):
            return False

        scene = self.getScene(id)

    def setScene(self, q):
        if (not self.connected):
            return False

        self._logger.info('Hue: Switching lights to ' + q)
        q.replace(' ', '').lower()
        scenes = self._bridge.scenes()
        
        for s in scenes:
            scene = scenes[s]
            name = scene['name'].replace(' ', '').lower()

            if (q in name):
                #activate scene
                url = self._bridge.groups[4].url + '/action'
                r = self.putRequest(url + '', json.dumps({'scene': s}))
                return True
        
    def LightsOff(self):
        if (not self.connected):
            return False    

        url = self._bridge.groups[4].url + '/action'
        r = self.putRequest(url + '', json.dumps({'on': False}))

    def LightsOn(self):
        if (not self.connected):
            return False    

        url = self._bridge.groups[4].url + '/action'
        r = self.putRequest(url + '', json.dumps({'on': True}))
                
    def slowOff(self):
        if (not self.connected):
            return False
        
        schedules = self._bridge.schedules
        self._logger.info('Hue: Turning lights slowly off')
        
        if (not self.getSchedule('Shine: Dim lights')):
            self.createDefaults()
            
        #'command': {'address': '/api/zn64uaWzazjqIaKCE2w4idKIVanomqQV-ClOQcqr/groups/1/action', 'body': {'on': True}, 'method': 'PUT'}}}
        #r = self.postRequest('http://' + self._host + '/api/zn64uaWzazjqIaKCE2w4idKIVanomqQV-ClOQcqr/schedules', json.dumps(alarm))
        r = self.putRequest(schedules.url + '/' + self.getSchedule('Shine: Dim lights')['ID'], json.dumps({'status': 'enabled'}));
        r = self.putRequest(schedules.url + '/' + self.getSchedule('Shine: Turn off')['ID'], json.dumps({'status': 'enabled'}));        
        
    def getCurrentColors(self):
        lights = self._bridge.lights()

        colors = []
        for l in lights:
            light = lights[l]

            converterA = Converter(GamutA)
            converterB = Converter(GamutB)
            converterC = Converter(GamutC)
            
            col = converterA.xy_to_rgb(light['state']['xy'][0], light['state']['xy'][1])
            #print(light['name'])
            #light['state'][bri]/255
                        
            if (light['name'] == 'TVLightStrip' or light['name'] == 'Lamp' or light['name'] =='BureauLamp'):
                colors.append(col)
        
        return colors

    def convertXYToRGB(self, bulbType, coordinates, brightness):
        corners = {}
        corners['ecl']= {'red':{'hue':0, 'x':0.675, 'y':0.322}, 'green':{'hue':100, 'x':0.409, 'y':0.518}, 'blue':{'hue':184, 'x':0.167, 'y':0.04}}
        corners['cl']= {'red':{'hue':0, 'x':0.704, 'y':0.296}, 'green':{'hue':100, 'x':0.2151, 'y':0.7106}, 'blue':{'hue':184, 'x':0.138, 'y':0.08}}

        if (bulbType=='Extended color light'):
            limits = corners['ecl']
        else:
            limits = corners['cl']

        x = float(coordinates[0])
        y = float(coordinates[1])
    
        z = 1.0 - x - y;
        Y = brightness;
        X = (Y / y) * x;
        Z = (Y / y) * z;

        r =  X * 1.656492 - Y * 0.354851 - Z * 0.255038;
        g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152;
        b =  X * 0.051713 - Y * 0.121364 + Z * 1.011530;

        if (r <= 0.0031308):
            r = 12.92 * r
        else:
            r = (1.0 + 0.055) * pow(r, (1.0 / 2.4)) - 0.055
            
        if (g <= 0.0031308):
            g = 12.92 * g
        else:
            g = (1.0 + 0.055) * pow(g, (1.0 / 2.4)) - 0.055
                
        if (b <= 0.0031308):
            b = 12.92 * b
        else:
            b = (1.0 + 0.055) * pow(b, (1.0 / 2.4)) - 0.055;

        #print(r,g,b)
        return
        
    def postRequest(self, url, content):
        r = requests.post(url, content)
        return r.json()

    def putRequest(self, url, content):
        r = requests.put(url, content)
        return r.json()
