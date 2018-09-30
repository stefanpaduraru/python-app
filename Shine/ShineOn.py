# to do next: multiprocess queue for passing errors from child processes to main process. Message should include process id, exception type, def, line

from __future__ import print_function
import multiprocessing
import subprocess
import time

from Shine.PersonalAssistant import PersonalAssistant
from Shine.LED import LED
from Shine.Logger import Logger
from Shine.Media import Media
from Shine.Hue import Hue
from Shine.Server import Server
from Shine.Utils import Utils
from Shine.Config import Config
from Shine.Interpreter import Interpreter

import argparse
import json
import os
import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.file_helpers import existing_file

# ShineOn class create queues and threads for g assistant, socket server, device leds
# and manages the messages passed by sub threads, interprets and executes them
class ShineOn:
    def __init__(self):
        self._logger = Logger()
        self._logger.info(' ')
        self._logger.info('ShineOn: Starting up')
        self._logger.info('ShineOn PID: '+str(os.getpid()))
        self.commands = []

        self._config = Config()
        self._hue = Hue(self._logger)
        self._media = Media(self._logger)
        self._utils = Utils(self._config, self._hue, self._media, self._logger)
        self._lastRead = 0

	# create queues and threads for g assistant, socket server, device leds
    def start(self):
        #open process for assistent
        _pa = False
        _pa = PersonalAssistant(self._logger)
        self._assistantQueue = multiprocessing.Queue()
        self._assistantProcess_ = multiprocessing.Process(target=_pa.run, args=(self._assistantQueue, self._utils))
        self._assistantProcess_.start()

        #open process for LEDS
        _leds = LED(self._logger)
        self._ledsQueue = multiprocessing.Queue()
        self._ledsProcess_ = multiprocessing.Process(target=_leds.LightUP, args=(self._ledsQueue, self._utils))
        self._ledsProcess_.start()

        #open process for server
        _server = Server(self._logger)
        self._serverQueue = multiprocessing.Queue()
        self._serverProcess_ = multiprocessing.Process(target=_server.ServerStart, args=(self._serverQueue, self._utils))
        self._serverProcess_.start()

        #open process for media

        #open interpreter for processing commands and execute. proxy
        self._interpreter = Interpreter(_pa, self._ledsQueue, self._media, self._utils)

    def run(self):
        while (True):
            #read queues 5 times / sec
            currentTime = int(round(time.time() * 1000))
            if (currentTime - self._lastRead > 200):
                self._lastRead = int(round(time.time() * 1000))

                #read personal assistant messages
                self.getMessages(self._assistantQueue)

                #read socket server messages
                self.getMessages(self._serverQueue)

                #read buttons messages
                #@todo

                if (len(self.commands)):
                    #send commands to interpreter
                    results = self._interpreter.execute(self.commands)
                    #print (results)
                    for result in results:
                        #get result for each command and return it
                        if (result['source'] == 'socket'):
                            #return to socket server
                            self._serverQueue.put(result)

                        #if (result['source'] == 'assistant'):
                            #return to socket server
                            #self._assistantQueue.put(result)

                    self.commands = []
            time.sleep(190/1000.0)
			
	#red messages from queue argument
    def getMessages(self, queue):
        while queue.qsize():
            msg = queue.get()
            self.commands.append(msg)
