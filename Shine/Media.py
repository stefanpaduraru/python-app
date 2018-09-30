from Shine.Speakers import Speakers
from Shine.Cast import Cast
from Shine.LGWebOSTV import LGWebOSTV
import pychromecast

# media class used to handle device speakers and chromecast devices
class Media:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info('Searching for LAN devices')
        devices = pychromecast.get_chromecasts()
        
        self.speakers = Speakers(logger)
        #self.video = Video(devices)
        self.tv = LGWebOSTV(logger)
        self.cast = Cast(devices, logger)

    def turnOff(self):
        self.tv.turnoff()
        for cast in self.cast.getDevices():
            self.cast.Stop(cast)
        
