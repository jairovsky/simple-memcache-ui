import mem
import screen
import logging

client = mem.connect()

def getkeys():
    k = client.get_all_keys()
    i = 0
    r = []
    for kk in k:
        r.append((kk, i))
        i += 1
    return r
def getkey(k, data):
    
    return client.get(k.label)

screen.start(on_update=getkeys, on_get_key=getkey)


