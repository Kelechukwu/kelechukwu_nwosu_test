import time
import sys
import os

# Add grandparent directory to sys.path 
# this is so that version module can be imported
# when running tests directly 
sys.path.append(os.path.abspath(__file__ + "/../../"))
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
    # print(not_so_expensive_function(4))
    print(expensive_function(5))
    print(expensive_function(6))
    print(expensive_function(5))
    print(expensive_function(4))