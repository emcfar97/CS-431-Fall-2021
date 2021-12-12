def main(initialize=1):

    import threading 

    from .. import sankaku
    from . import flickr, posespace, elitebabes, instagram, blogspot
    
    threads = [
        threading.Thread(target=flickr.start, args=(initialize,)),
        threading.Thread(target=elitebabes.start, args=(initialize,)),
        # threading.Thread(target=instagram.start, args=(initiailze,)),
        # threading.Thread(target=posespace.start, args=(initiailze,))
        threading.Thread(target=sankaku.start, args=(initialize, True, 0)),
        ]
    for thread in threads: thread.main()
    for thread in threads: thread.join()