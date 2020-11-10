import threading
import queue


class _Operation(threading.Thread):
    def __init__(self, sem, qsem, *args, **kwds):
        self.sem = sem
        self.qsem = qsem
        self.method = kwds.pop('target')
        super().__init__(target=self.wrappedTarget, args=args, kwargs=kwds, daemon=True)

    def wrappedTarget(self, *args, **kwds):
        self.method(**kwds)
        if isinstance(self.sem, threading.Semaphore):
            self.sem.release()
            self.qsem.release()


class OperationQueue:
    def __init__(self, numberOfConcurrentTask=1, qsem=None):
        self.queue = queue.Queue()
        self.reservequeue = queue.Queue()
        self.sem = threading.Semaphore(numberOfConcurrentTask)
        self.qsem = qsem
        self.t = ''
        self.stoploop = False

    ## 작업 루프
    def mainloop(self):
        while True:
            oper = self.queue.get()
            self.qsem.acquire()
            self.sem.acquire()
            oper.start()
            if self.stoploop:
                break

    def mainloopinf(self):
        while True:
            if self.queue.empty():
                self.queue = self.reservequeue
            oper = self.queue.get()
            self.sem.acquire()
            oper.start()
            if self.stoploop:
                oper.join()
                break

    def add(self, method, *args, **kwds):
        task = _Operation(self.sem, self.qsem, target=method, *args, **kwds)
        self.queue.put(task)
        self.reservequeue.put(task)

    def start(self, **kwargs):
        run_async = kwargs.pop('run_async', False)
        infinite = kwargs.pop('infinite', False)
        if infinite:
            self.t = threading.Thread(target=self.mainloopinf, daemon=True)
        else:
            self.t = threading.Thread(target=self.mainloop, daemon=True)
        self.t.start()
        if not run_async:
            self.t.join()

    def stop(self):
        if self.t is not None:
            self.stoploop = True

    def flush(self):
        while not self.queue.empty():
            self.queue.get()






#source from https://soooprmx.com/archives/9693