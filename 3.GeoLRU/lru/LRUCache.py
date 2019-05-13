import asyncio
import time
from datetime import datetime, timedelta
import json
import pickle
from threading import Thread, Lock, Event
import websockets

from lru.lru_socket import SocketServer


def LRUCache(function=None, cache_size=100, validity_in_minutes=60, is_master_node=False, master_node_hostname=None):
    """Wrapper function to the main decorator class _LRUCache. _LRUCache stores records in
    key,value pairs. Records expire after validity_in_minutes(default=60 minutes) is reached.
    The cache is Geo distributed and broadcasts changes and updates to replica nodes via
    websocket on port 6789.

    Keyword arguments:
        cache_size  : the maximum size of the cache. (default = 100) 
        validity_in_minutes  : cache validity in minutes. This can be a decimal value. (default = 1year)
        is_master_node  : specifies if the current instance is the master node in its cluster. (default = False)
        master_node_hostname: specify the hostname of the master node if this cache is not the master ( default = None)
    """

    # Start a websocket server if this cache is the master
    # TODO: verify that there isn't an already existing master node before starting the webserver
    # if is_master_node:
    #     event_loop = asyncio.new_event_loop()
    #     t = Thread(target=SocketServer.serve, kwargs={'loop': event_loop},daemon=True)
    #     t.start()
    

    if function:
        return _LRUCache(function)
    else:
        def wrapper(function):
            return _LRUCache(function, cache_size, validity_in_minutes, master_node_hostname, is_master_node)

        return wrapper


class _LRUCache:
    """Main decorator for the LRU(Least Recently Used) Cache. This stores records in
    key,value pairs. Records expire after validity_in_minutes(default=60 minutes) is reached.
    The cache is Geo distributed and broadcasts changes and updates to replica nodes via
    websocket on port 6789.

    Keyword arguments:
        cache_size  : the maximum size of the cache. If this limit is reached the least recently accessed record is deleted to make roam for new records. (default = 100) 
        validity_in_minutes  : cache validity in minutes. This can be a decimal value. (default = 60)
        is_master_node  : specifies if the current instance is the master node in its cluster. (default = False)
    """

    MASTER_HOST_NAME = None
    VALIDITY = None
    WEB_SOCKET_PORT = 6789


    def __init__(self, func, cache_size=100, validity_in_minutes=60, master_node_hostname=None, is_master_node=False):
        self.func = func
        self.cache = {
            "creation_time":datetime.now().timestamp(),
            "data":{},
            }
        # access list of the keys- most recently accessed keys are infront
        self.access_list = []
        self.limit = cache_size

        

        # set validity_in_minutes 
        _LRUCache.VALIDITY = validity_in_minutes * 60

        # set SocketServer hostname 
        _LRUCache.MASTER_HOST_NAME = master_node_hostname

        # if it is not the master then start a listener to 
        # listen for updates
        if not is_master_node:
            event_loop = asyncio.new_event_loop()
            t = Thread(target=self._listen_for_updates, kwargs={'loop': event_loop})
            t.start()
        else:
            _LRUCache.MASTER_HOST_NAME = "localhost"


    def __call__(self, *args, **kwargs):

        # First try to expire the cache
        self._attempt_to_expire(self.cache)


        # if the args already exist in the cache
        if args in self.cache.get("data"):
            self._move_to_front(args)
    
            self.publish_update()
            return self.cache["data"][args]
        
        # if the cache limit is reached - remove the oldest record
        if len(self.cache["data"]) == self.limit:
            oldest_key = self.access_list.pop(0)

            # delete record from self.cache
            del self.cache["data"][oldest_key]

        
        # compute the cache and node - if not in cache
        result = self.func(*args, **kwargs)
        self.cache["data"][args] = result

        # add new keys to the top of the access_list register
        self.access_list.append(args)

        self.publish_update()

        return result


    def _move_to_front(self, args):
        """This function moves the most recently accessed key to the front
        of the access_list

        Params:
            args: the key of the Key-Value pair to be read.
        """

        for index in range(len(self.access_list)):
            if self.access_list[index] == args:
                self.access_list += [self.access_list.pop(index)]
                break

    def _attempt_to_expire(self, cache):
        """This method expires _LRUCache if the validity_in_minutes time as elapsed.
        It will return True if it expired the Cache and False if it did not
        because the time has not elapsed.
        """
        diff = datetime.now().timestamp() - self.cache["creation_time"]
        if diff >= _LRUCache.VALIDITY:
            self.cache["creation_time"] = datetime.now().timestamp()
            self.cache["data"] = dict()

            self.access_list = []

            return True
        else:
            return False

    def publish_update(self):
        
        asyncio.get_event_loop().run_until_complete(self._publisher())


    # TODO: Make publisher re-establish connection to network if connection breaks
    async def _publisher(self):
        """THis method publishes updates to LRUCache so that other distributed Caches can receive it """
        async with websockets.connect(f"ws://{_LRUCache.MASTER_HOST_NAME}:{_LRUCache.WEB_SOCKET_PORT}") as socket:
            message = {
                "cache": self.cache,
                "access_list": self.access_list
            }
            message_bytes = pickle.dumps(message)
            await socket.send(message_bytes)

    def _listen_for_updates(self, loop):
        """this methods makes _listener run perpetually in the background """
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._listener())
        loop.run_forever()

    # TODO: Make listener re-establish connection to network if connection breaks
    async def _listener(self):
        """This method listens for updates to the cache state and replicates updates locally"""
        if _LRUCache.MASTER_HOST_NAME:
            async with websockets.connect(f"ws://{_LRUCache.MASTER_HOST_NAME}:{_LRUCache.WEB_SOCKET_PORT}") as socket:
                while True:
                    raw_response = await socket.recv()
                    response = pickle.loads(raw_response)
                    with Lock():
                        self.cache = response.get("cache")
                        self.access_list = response.get("access_list")
        else:
            raise Exception("[FATAL] master_node_hostname value is required for non-master LRUCache")

