import logging
import sys
from websockets.sync.server import serve

def initWebSocket():
    logging.basicConfig(level=logging.DEBUG)
    addr, port = sys.argv[1].split(':')
    port = int(port)
    if addr == '':
        addr = 'localhost'

    with serve(addr, port) as server:
        logging.info(f'Listening on {addr}:{port}')
        server.serve_forever()
    