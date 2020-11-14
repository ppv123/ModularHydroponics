import threading
import queue


class _Operation(threading.Thread):
    def __init__(self, sem, qsem, *args, **kwds):
        self.sem = sem
        #self.qsem = qsem
        self.method = kwds.pop('target')
        super().__init__(target=self.wrappedTarget, args=args, kwargs=kwds, daemon=True)

    def wrappedTarget(self, *args, **kwds):
        self.method(**kwds)
        if isinstance(self.sem, threading.Semaphore):
            self.sem.release()
            #self.qsem.release()


class OperationQueue:
    def __init__(self, numberOfConcurrentTask=1, **kwargs):
        self.queue = queue.Queue()
        '''
        self.sem = threading.Semaphore(numberOfConcurrentTask)
        self.t = ''
        self.stopmainloop = False
        self.stopaddloop = False
        '''
        self.reservequeue = queue.Queue()
        self.sem = threading.Semaphore(numberOfConcurrentTask)
        self.qsem = kwargs.pop('qsem', None)
        self.t = ''
        self.stoploop = False
        
    ## 작업 루프
    def mainloop(self):
        while True:
            oper = self.queue.get()
            #self.qsem.acquire()
            self.sem.acquire()
            oper.start()
            if self.stoploop:
                oper.join()
                break
    '''    
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
    '''
    def add(self, method, *args, **kwds):
        task = _Operation(self.sem, target=method, *args, **kwds)
        self.queue.put(task)
        self.reservequeue.put(task)

    def addloop(self, method, *args, **kwds):
        while True:
            task = _Operation(self.sem, target=method, *args, **kwds)
            self.queue.put(task)
            if self.stopaddloop:
                break
            
    def start(self, **kwargs):
        '''
        run_async = kwargs.pop('run_async', False)
        infinite = kwargs.pop('infinite', False)
        if infinite:
            self.t = threading.Thread(target=self.mainloopinf, daemon=True)
        else:
            self.t = threading.Thread(target=self.mainloop, daemon=True)
        self.t.start()
        if not run_async:
            self.t.join()
        '''
        self.t = threading.Thread(target=self.mainloop, daemon=True)
        self.t.start()
        if not run_async: # 옵션값에 따라 큐의 실행을 블럭킹으로 한다.
            self.t.join()

    def stop(self):
        if self.t is not None:
            self.stopmainloop = True
            #self.t.join()

'''
    def flush(self):
        while not self.queue.empty():
            self.queue.get()
            '''