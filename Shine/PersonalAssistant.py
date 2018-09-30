import argparse
import json
import os
import multiprocessing

import google.auth.transport.requests
import google.oauth2.credentials
from google.assistant.library import Assistant
from google.assistant.library.file_helpers import existing_file


from Shine.GoogleEvents import GoogleEvents

# personal assistant class (Google Assistant for now)
# creates and runs the assistant in subprocess
# gets events, passes them through the GoogleEvents to get the uniform commands
# passes commands through main queue to parent process

class PersonalAssistant:
    def __init__(self, logger):
        self.logger = logger
        self.device_api_url = 'https://embeddedassistant.googleapis.com/v1alpha2'

    def run(self, mainQueue, utils):
        p = multiprocessing.current_process()
        self.logger = utils._logger
        self.logger.info('Google Assistant PID: '+str(p.pid))

        with open(os.path.join(os.path.expanduser('~/.config'),'google-oauthlib-tool','credentials.json'), 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))

        self.logger.info('Google Assistant: Starting')
        _assistant =  Assistant(credentials, 'homepi-177214-shineon-1s9b88')
        self._assistant = _assistant

        self.register_device('homepi-177214', credentials, 'homepi-177214-shineon-1s9b88', self._assistant.device_id)
        count = 0
        for event in _assistant.start():
            #print(event)
            _events = GoogleEvents(_assistant, utils)
            if (count == 0):
                self.logger.info('Google Assistant: Started')
            messages = _events.getEvent(event)
            self.sendMessages(mainQueue, messages)
            count += 1

	# sends commands back to parent
    def sendMessages(self, mainQueue, messages):
        if (len(messages)):
            for message in messages:
                command = '{"source":"assistant", "address":"", "message":'+message+'}'
                mainQueue.put(command)

	#registers device if needed
    def register_device(self, project_id, credentials, device_model_id, device_id):
        base_url = '/'.join([self.device_api_url, 'projects', project_id, 'devices'])
        device_url = '/'.join([base_url, device_id])
        session = google.auth.transport.requests.AuthorizedSession(credentials)
        r = session.get(device_url)
        #print(device_url, r.status_code)
        if r.status_code == 404:
            print('Registering....')
            r = session.post(base_url, data=json.dumps({
                'id': device_id,
                'model_id': device_model_id,
                'client_type': 'SDK_LIBRARY'
            }))
            if r.status_code != 200:
                raise Exception('failed to register device: ' + r.text)
            print('\rDevice registered.')
