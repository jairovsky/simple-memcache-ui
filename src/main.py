import mem
from ui import MainUI
import logging
from sys import argv

logging.basicConfig(filename='log.txt',level=logging.DEBUG,format='%(asctime)s %(message)s')

client = mem.connect(argv[1], int(argv[2]))

if __name__ == '__main__':
    ui = MainUI()
    ui.refresh_items = lambda: client.get_all_keys()
    ui.get_item = lambda k: client.get(k)
    ui.del_item = lambda k: client.delete(k)

    ui.start()


