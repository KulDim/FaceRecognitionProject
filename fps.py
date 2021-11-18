import time

class FPS:

    print('initialization class FPS')

    def __init__(self):
        self.counterFPS = 0
        self.start_time = time.time()

    def counter(self):
        self.counterFPS += 1
        if (time.time() - self.start_time) > 1 :
            self.fps = self.counterFPS / (time.time() - self.start_time)
            self.counterFPS = 0
            self.start_time = time.time()
            return(self.fps)