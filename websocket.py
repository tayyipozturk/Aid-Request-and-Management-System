import sys
import os
from socket import *
import asyncio
import websockets
import logging
import json
import http.cookies
from server_3 import ClientThread


# import django
# from django.contrib.session.models import Session
#
# def setupDjango(projectpath, projectname):
# 	'''call this once to setup django environment'''
# 	sys.path.append(projectpath)
# 	os.environ.setdefault('DJANGO_SETTINGS_MODULE',projectname + '.settings')
# 	django.setup()
#
# def checksession(sessionkey):
# 	'''check UDP/WS supplied id againts django session keys
# 	   for browser, 'sessionid' cookie will save this id
# 	   for django view request.session.session_key gives this id.
# 		simply view sends udp notifications with request.session.session_key and
# 		browser sends sessionid cookie. Note that they don't need to match.
# 		User A can send notification to user B. But both have session ids.
# 	'''
# 	try:
# 		Session.objects.get(session_key=sessionkey)
# 		return True
# 	except:
# 		return False

def singleton(cls):
    _instances = {}

    def getinstance():
        if cls not in _instances:
            _instances[cls] = cls()
        return _instances[cls]

    return getinstance


@singleton
class Notifications:
    def __init__(self):
        self.observers = {}
        self.broadcast = set()
        self.messages = {}

    def newconnection(self, ws):
        self.broadcast.add(ws)

    def closeconnection(self, ws):
        self.broadcast.discard(ws)

    def register(self, ws, cid):
        '''register a Lock and an id string'''
        if cid in self.observers:
            self.observers[cid].add(ws)
        else:
            self.observers[cid] = set([ws])
        print('Current observers', self.observers, self.broadcast)

    def unregister(self, ws, cid):
        '''remove registration'''
        if cid not in self.observers:
            return
        self.observers[cid].discard(ws)
        if self.observers[cid] == set():
            del self.observers[cid]
        print('Current observers', self.observers, self.broadcast)

    async def addNotification(self, oid, message):
        '''add a notification for websocket conns with id == oid
            the '*' oid is broadcast. Message is the dictionary
            to be sent to connected websockets.
        '''
        print(oid, message)
        if oid == '*':  # broadcast message
            for c in self.broadcast:
                await c.send(json.dumps(message))
        elif oid in self.observers:
            for c in self.observers[oid]:
                await c.send(json.dumps(message))


async def clienthandler(websocket, path):
    thread = ClientThread(websocket, websocket.remote_address)
    thread.start()


async def start_websocket_server():
    logging.basicConfig(level=logging.DEBUG)
    try:
        ws_addr = sys.argv[1].split(':', 1)
        if ws_addr[0] == '':
            ws_addr[0] = '0'
        ws_addr = getaddrinfo(ws_addr[0], ws_addr[1], AF_INET, SOCK_STREAM)
        ws_addr = ws_addr[0][4]

    except Exception as e:
        sys.stderr.write("{}\nusage: {} wsip:port\n".format(e, sys.argv[0]))
        sys.exit()

    # following creates a websocket handler
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    async with websockets.serve(clienthandler, ws_addr[0], ws_addr[1], loop=loop):
        logging.info("websocket server listening on {}:{}".format(ws_addr[0], ws_addr[1]))
        await asyncio.Future()  # run forever
