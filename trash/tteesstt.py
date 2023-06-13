import asyncio
import websockets
import logging

from threading import Queue
from threading import Thread

connected_clients = set()

async def notify_client():
    for client in connected_clients:
        await client.send("login")


class WRAgent(Thread):
	def __init__(self, conn):
		self.conn = conn
		Thread.__init__(self)
                
    def run(self):
        while True:
            message = websocket.recv()
            print(f"Received message: {message}")
            
            # Send the message to all connected clients
            for client in connected_clients:
                client.send(message)
                print(f"Sent message to client")
     

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    wrtr = WRAgent(connected_clients)
    wrtr.start()
    try:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            
            # Send the message to all connected clients
            for client in connected_clients:
                await client.send(message)
                print(f"Sent message to client")
    finally:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    start_server = websockets.serve(handle_client, '127.0.0.1', 8745, loop=loop)
    loop.run_until_complete(start_server)
    loop.run_forever()

# with websockets.serve(handle_client, "localhost", 8765) as websocket_server:
#     loop.run_forever()

# async def main():
#     print("WebSocket server started")
#     await server.wait_closed()

# asyncio.run(main())
