import logging 
from threading import Thread,Lock,Condition
from queue import Queue
import socket
import websockets
from websockets.sync.server import serve
import sys

class NotifyCentre:
    def __init__(self):
        self.queue = Queue()
        self.lock = Lock()
        self.cond = Condition(self.lock)
        self.broadcast = set()


    def newconnection(self, ws):
        self.broadcast.add(ws)

    def closeconnection(self, ws):
        self.broadcast.discard(ws)

    def newmessage(self,mess):
        self.lock.acquire()
        self.sendmessage(mess)
        self.cond.notify_all()
        self.lock.release()


    def getmessages(self):
        self.lock.acquire()
        res = None
        if not self.queue.empty():
            res = self.queue.get()
        self.lock.release()
        return res
    
    def isempty(self):
        return self.queue.empty()
    
    def sendmessage(self, mess):
        for i in self.broadcast:
            i.send(mess)

def serveconnection(sc,nc):
    nc.newconnection(sc)
    try:
        notexit = True
        while notexit:
            try:
                msg = sc.recv()
            except:
                notexit = False
                break
    except Exception as e:
        print("ws exception: ",e)
    finally:
        nc.closeconnection(sc)
        sc.close()


class WebSocketThread(Thread):
    def __init__(self, nc):
        self.nc = nc
        Thread.__init__(self)
    def run(self):
        with serve(lambda sc:serveconnection(sc,self.nc) , host = '127.0.0.1', port = 1999, 
                logger = logging.getLogger("chatsrv") ) as server:
            print("> Notification server started.")
            server.serve_forever()

