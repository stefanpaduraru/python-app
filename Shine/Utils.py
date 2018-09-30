from __future__ import print_function
import json
import os
import socket
import fcntl
import struct

# this class is used for diagnostics of the device
# builds an object with properties such as local ip address, connected network ssid, wifi card mac, device temp, led status (color animation, brightness, state) etc
class Utils:
    def __init__(self, config, hue, media, logger):
        self._config = config
        self._hue = hue
        self._media = media
        self._logger = logger
        self._status = {'color':'rainbow', 'brightness':128, 'state':'on', 'volume':0, 'mute':False, 'network':'', 'ipaddress':'', 'temp':'0'}

    def getStatus(self):
        #current volume
        #mute or not
        #wifi network
        #ip address
        self._status['ipaddress'] = self.getIPAddress('wlan0')
        self._status['network'] = self.getCurrentNetwork()
        self._status['mac'] = self.getMacAddress()
        #led color
        #led intesity

        #temperature
        self._status['temp'] = self.getTemperature()
        return json.dumps(self._status)

    def setStatus(self, prop, val):
        self._status[prop] = val

    def rebootDevice(self):
        command = 'reboot now'

        data = os.popen(command)

    def turnoffDevice(self):
        command = 'shutdown now'

        data = os.popen(command)

    def getMacAddress(self):
        command = 'cat /sys/class/net/wlan0/'

        data = os.popen(command)
        mac = str(data.read()).replace('\n', '').upper()
        return mac

    def getTemperature(self):
        command = '/opt/vc/bin/vcgencmd measure_temp'

        data = os.popen(command)
        temp = str(data.read()).replace('temp=', '').replace('\'C', '').replace('\n', '')
        return temp

    def getIPAddress(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        str = ifname[:15]
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', str.encode())
        )[20:24])

    def getCurrentNetwork(self):
        f = os.popen('iwgetid')
        network = str(f.read()).replace('wlan0     ESSID:', '').replace('"', '').replace('\n', '')
        return network
