# How to install Geo LRU library
**Version**: Python3.X 
```bash
$ cd 3.GeoLRU
$ sudo python setup.py install
```

## How to Use
After the library has been installed. You can import it and start using in your projects as a decorator. First you have to start the websocket server to allow for communication between distributed caches.
Example:
1. start websocket server
```bash
$ python lru/lru_socket.py
```
***NOTE** : There should be only one websocket server for a single cache.
gotten from test/test_lru.py
```python 
import time
from lru.LRUCache import LRUCache

@LRUCache(cache_size=9, validity_in_minutes=0.5,is_master_node=True)
def expensive_function(num):

    print("computing...")
    time.sleep(2)
    result = num * num
    return result


@LRUCache(master_node_hostname="localhost")
def not_so_expensive_function(num):

    print("computing...")
    time.sleep(2)
    result = num * num
    return result

while True:
    print(expensive_function(2))
    print(not_so_expensive_function(4))
    print(expensive_function(5))
```

## Contributing
