import threading
import queue


class _Operation(threading.Thread):
    def __init__(self, sem, *args, **kwds):
        self.sem = sem
        self.method = kwds.pop('target')
        super().__init__(target=self.wrappedTarget, args=args, kwargs=kwds, daemon=True)

    def wrappedTarget(self, *args, **kwds):
        self.method(**kwds)
        if isinstance(self.sem, threading.Semaphore):
            self.sem.release()


class OperationQueue:
    def __init__(self, numberOfConcurrentTask=1):
        self.queue = queue.Queue()
        self.sem = threading.Semaphore(numberOfConcurrentTask)
        self.t = ''
        self.stopmainloop = False
        self.stopaddloop = False

    ## 작업 루프
    def mainloop(self):
        while True:
            oper = self.queue.get()
            self.sem.acquire()
            oper.start()
            if self.stopmainloop:
                oper.join()
                break

    def add(self, method, *args, **kwds):
        task = _Operation(self.sem, target=method, *args, **kwds)
        self.queue.put(task)

    def addloop(self, method, *args, **kwds):
        while True:
            task = _Operation(self.sem, target=method, *args, **kwds)
            self.queue.put(task)
            if self.stopaddloop:
                break

    def start(self, run_async=False):
        self.t = threading.Thread(target=self.mainloop, daemon=True)
        self.t.start()
        if not run_async: # 옵션값에 따라 큐의 실행을 블럭킹으로 한다.
            self.t.join()

    def stop(self):
        if self.t is not None:
            self.stopmainloop = True
            #self.t.join()






#source from https://soooprmx.com/archives/9693