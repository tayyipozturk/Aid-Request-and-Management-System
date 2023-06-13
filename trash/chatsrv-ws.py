#!/usr/bin/python


import logging 
from threading import Thread,Lock,Condition
import socket
import websockets
from websockets.sync.server import serve
import sys

class Chat:
	def __init__(self):
		self.buf = []
		self.lock = Lock()
		self.newmess = Condition(self.lock)
	def newmessage(self,mess):
		self.lock.acquire()
		self.buf.append(mess)
		self.newmess.notifyAll()
		self.lock.release()
	def getmessages(self,after=0):
		self.lock.acquire()
		if len(self.buf) < after:
			a = []
		else:
			a = self.buf[after:]
		self.lock.release()
		return a
		
		
	

class WRAgent(Thread):
	def __init__(self, conn, chat):
		self.conn = conn
		self.chat = chat
		self.current = 0
		Thread.__init__(self)
	def run(self):
		oldmess = self.chat.getmessages()
		self.current += len(oldmess)
		self.conn.send('\n'.join([i for i in oldmess]))
		notexit = True
		while notexit:
			self.chat.lock.acquire()
			self.chat.newmess.wait()
			self.chat.lock.release()
			oldmess = self.chat.getmessages(self.current)
			self.current += len(oldmess)
			try:
				self.conn.send('\n'.join([i for i in oldmess]))
			except:
				notexit = False
			

if len(sys.argv) != 2:
	print('usage: ',sys.argv[0],'port')
	sys.exit(-1)

def serveconnection(cr, sc):
	print("started")
	wrtr = WRAgent(sc, cr)
	wrtr.start()
	try:
		inp = sc.recv(1024)
		while inp:
			cr.newmessage(inp)
			print('waiting next')
			inp = sc.recv(1024)
		print('client is terminating')
		sc.close()
	except websockets.exceptions.ConnectionClosed:
		sc.close()
		wrtr.terminate()


HOST = ''         
PORT = int(sys.argv[1] )
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST, PORT))

chatroom = Chat()

with serve(lambda nc:serveconnection(chatroom,nc) , host = HOST, port = PORT, 
			logger = logging.getLogger("chatsrv") ) as server:
	print("serving")
	server.serve_forever()


