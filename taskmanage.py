import threading
import queue


class _Operation(threading.Thread):
    def __init__(self, sem, *args, **kwds):
        self.sem = sem
        self.method = kwds.pop('target')
        super().__init__(target=self.wrappedTarget, args=args, kwargs=kwds, daemon=True)

    def wrappedTarget(self, *args, **kwds):
        self.method()
        if isinstance(self.sem, threading.Semaphore):
            self.sem.release()


class OperationQueue:
    def __init__(self, numberOfConcurrentTask=1):
        self.queue = queue.Queue()
        self.sem = threading.Semaphore(numberOfConcurrentTask)

  ## 함수와 인자를 받아서 큐에 추가한다.
    def add(self, method, *args, **kwds):
        task = _Operation(self.sem, method, *args, **kwds)
        self.queue.put(task)

  ## 작업 루프
    def mainloop(self):
        while True:
            t = self.queue.get()
            self.sem.acquire()
            t.start()

  ## 루프를 돌리는 명령
    def start(self, run_async=False):
        t = threading.Thread(target=self.mainloop, daemon=True)
        t.start()
        if not run_async: # 옵션값에 따라 큐의 실행을 블럭킹으로 한다.
            t.join()

#source from https://soooprmx.com/archives/9693