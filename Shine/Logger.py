import logging
import sys
import requests
import json
import time

# logger class used to log info to main log file
class Logger:
    def __init__(self):

        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(format)
        #logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=format)
        logging.basicConfig(filename='/home/pi/assistant/assistant.log', level=logging.INFO, format=format)
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

        #fh = logging.FileHandler('/home/pi/assistant/assistant.log')
        #fh.setLevel(logging.DEBUG)
        #fh.setFormatter(formatter)
        #self._logger.addHandler(fh)

        #fh = logging.FileHandler('/home/pi/assistant/assistant.log')
        #fh.setLevel(logging.DEBUG)
        #fh.setFormatter(formatter)
        #self._logger.addHandler(fh)

        #ch = logging.StreamHandler(sys.stdout)
        #ch.setLevel(logging.INFO)
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #ch.setFormatter(formatter)
        #self._logger.addHandler(ch)

    def info(self, text):
        try:
            self._logger.info(text)
        except Exception as e:
            pass
