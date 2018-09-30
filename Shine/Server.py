# TODO send diagnostics message back to main process
import socket
import sys
import time
import ast
import multiprocessing
import threading
import json
from Shine.Config import Config
from Shine.Logger import Logger

# class Server creates a socket server listening on several ports, gets messages from connected clients
# and sends them to main process. The main process passes the messages to proxy command interpreter for execution
class Server:
    def __init__(self, logger):
        self.config = Config()
        self.settings = self.config.getSection('SERVER')
        self.logger = logger
        self.params = {}
        self.messages = []
	
	# creates socket server and starts listening
	# each client that connects is given a child thread
    def ServerStart(self, queue, utils):
        p = multiprocessing.current_process()
        self.logger.info('Server PID: '+str(p.pid))

        self._queue = queue
        self._utils = utils

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #check ports available
        ok = False
        ports = json.loads(self.settings['ports'])
        for port in ports:
            if (not ok):
                try :
                    server_address = ('', int(port))
                    self.sock.bind(server_address)
                    ok = True
                except socket.error as msg:
                    ok = False
                    continue

        self.logger.info ('Server: Starting up on %s port %s' % self.sock.getsockname())
        self.sock.listen(5)
        self.logger.info ('Server: Started')
        while True:
            #self.logger.info ('Server: waiting for a connection')
            client, address = self.sock.accept()
            client.settimeout(60)
            try:
                self.logger.info ('Server: client connected: ' + str(address))
                threading.Thread(target = self.listenToClient,args = (client, address, self._queue, self.logger)).start()
            except:
                print (sys.exc_info())
                pass

	# reads messages from argument queue
    def getMessages(self, queue):
        while queue.qsize():
            msg = queue.get()
            self.messages.append(msg)

	# gets messages sent specifically to the socket server
    def getMyMessages(self, queue, address):
        self.getMessages(queue)
        messages = []
        #if (len(self.messages)):
        #    print (self.messages)

        for message in self.messages:
            msg = json.loads(message)
            if (msg['address'] == address):
                messages.append(message)
                self.messages.remove(message)

        return messages

	# listens to messages sent by client and passes them to the main process through a queue
    def listenToClient(self, client, address, mainQueue, logger):
        size = 1024
        message = ''
        while True:
            try:
                data = client.recv(8192)
                data = str(data.decode('utf-8'))
                if data != '':
                    if data.find('_EOC_'):
                        if ("_EOC_" not in data):
                            message += data
                        else:
                            if message == '':
                                message = data
                            #message = message.strip().replace('\n', '').replace('\r', '')
                            message = message.strip().replace('_EOC_', '')

                            if (len(message)):
                                logger.info ('Server: message from (' + str(address) + '): ' + message)
                                #return command to parent
                                command = '{"source":"socket", "address":"'+str(address)+'", "message":'+message+'}'
                                mainQueue.put(command)

                                #send response to client
                                ok = 'OK'
                                client.send(ok.encode())

                            message = ''

            except (RuntimeError, TypeError, NameError):
                print (repr(NameError))
                pass

            #read message from parent
            #messages = self.getMyMessages(mainQueue, address)

            #if (len(messages)):
            #    print (messages)
            #    for message in messages:
            #        msg = json.loads(message)
            #        msg = msg['return']
            #        client.send(msg.encode())
