import asyncio
import websockets
from threading import Thread

class SocketServer:
    # clients/minions list 
    CLIENTS = set()

    @staticmethod
    def serve(port=6789, loop=None):
        if loop is None:
            asyncio.get_event_loop().run_until_complete(
                websockets.serve(SocketServer.server_function, 'localhost', port))
            asyncio.get_event_loop().run_forever()
        else:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                websockets.serve(SocketServer.server_function, 'localhost', port))
            print("Cache Server started")
            loop.run_forever()


    @staticmethod
    async def server_function(websocket, path):
        # register(websocket) sends user_event() to websocket
        await SocketServer.register(websocket)
        try:
            async for message in websocket:

                await SocketServer.broadcast_update(message)

        finally:
            await SocketServer.unregister(websocket)
    
    @staticmethod
    async def register(websocket):
        SocketServer.CLIENTS.add(websocket)
    
    @staticmethod
    async def unregister(websocket):
        SocketServer.CLIENTS.remove(websocket)
    
    @staticmethod
    async def broadcast_update(message):
        # asyncio.wait doesn't accept an empty list
        if SocketServer.CLIENTS:
            await asyncio.wait([user.send(message) for user in SocketServer.CLIENTS])

if __name__ == "__main__":
    event_loop = asyncio.new_event_loop()
    print("Starting Cache server...")
    SocketServer.serve()