import subprocess
import multiprocessing

#import alsaaudio

#used for playing audio on device
class Speakers:
    def __init__(self, logger):
        self._logger = logger
    
        self.playing = 0
        self.stopped = 1
        self.paused = 0
        self.sources = {'blue':'http://s2.voscast.com:8964/stream', 'red':'http://s2.voscast.com:8968/stream', 'green':'http://s2.voscast.com:8966/stream'}
        self.pid = 0
        self.proc = 0
        self.speaker = 0 # 0 - none, 1 - locally, 2 - chromecast
        self.speakerVolume = 0.3
        

    #----------control----------#
    def PlaySource(self, source):
        self._logger.info('AUDIO: Playing ' + source + ' on speaker\n')
        if (not self.pid):
            #self.proc = subprocess.call(["mpg123", self.selectedSource])
            self.proc = subprocess.Popen(["mpg123", self.sources[source]], stdout=subprocess.PIPE)
            self.pid = self.proc.pid

    def Pause(self):
        if (self.playing):
            if (self.speaker == 1):
                self.PauseLocal()
                self._logger.info('AUDIO: Pausing on speaker\n')
                
        self.playing = 0
        self.stopped = 0
        self.paused = 1
        
    def PauseForSpeaking(self):
        if (self.speaker == 1):
            if (self.playing):
                self.PauseLocal()
                
            self.playing = 0
            self.stopped = 0
            self.paused = 1
            self._logger.info('AUDIO: Pausing speaker to talk\n')

    def unPauseForSpeaking(self):
        if (self.speaker == 1):
            if (self.paused):
                self.Play(self.selectedSource)
                self._logger.info('AUDIO: Unpausing speaker\n')


    #----------speakers----------#
    def PlayGreen(self):
        self.selectedSource = self.sources['green']
        self.PlaySource()
        
    def PauseLocal(self):
        if (self.proc):
            self.proc.kill()
            
        self.pid = 0
        self.playing = 0
        self.stopped = 1
        self.paused = 1
        self.speaker = 1
        self._logger.info('AUDIO: Pausing play on speaker\n')
        
    def StopLocal(self):
        if (self.proc):
            self.proc.kill()
            
        self.pid = 0
        self.playing = 0
        self.stopped = 1
        self.paused = 0
        self.speaker = 0
        self._logger.info('AUDIO: Stoppping play on speaker\n')

    def VolumeToOnSpeakers(self, v):
        #m = alsaaudio.Mixer()
        #vol = m.getvolume()
        self._logger.info('AUDIO: volume to '+v+' on speakers')
        #m.setvolume(v)
        
    def VolumeUpOnSpeakers():
        self._logger.info('AUDIO: volume up speakers')
        #m = alsaaudio.Mixer()
        #vol = m.getvolume() + 10
        #m.setvolume(vol)

    def VolumeDownOnSpeakers():
        self._logger.info('AUDIO: volume down speakers')
        #m = alsaaudio.Mixer()
        #vol = m.getvolume() - 10
        #m.setvolume(vol) 
        
   

    
