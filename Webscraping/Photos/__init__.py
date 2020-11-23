import threading
from .. import sankaku
from . import flickr, posespace, erotica, imagefap, instagram, pinterest, blogspot

def start():

    threads = [
        # threading.Thread(target=erotica.start, args=(0,)),
        # threading.Thread(target=erotica.start, args=(1,)),
        # threading.Thread(target=erotica.start, args=(2,))
        ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    threads = [
        threading.Thread(target=flickr.start),
        # threading.Thread(target=instagram.start),
        # threading.Thread(target=posespace.start)
        ]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    
    threading.Thread(target=sankaku.start, args=(0,)),