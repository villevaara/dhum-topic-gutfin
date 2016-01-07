import time


class Timer(object):
    def __init__(self):
        self.start_time = time.time()
        self.end_time = 0.0
        print '\n    Starting timer!\n'

    def reset(self):
        self.start_time = time.time()
        print('\n   Timer reset to 0!\n')

    def get_lap(self):
        laptime = time.time() - self.start_time
        return laptime

    def print_lap(self):
        rawtime = self.get_lap()
        mins = int(rawtime / 60)
        secs = int(rawtime - (mins * 60))
        print '\n    Time elapsed: %d minutes, %d seconds.\n' % (mins, secs)
        if mins > 4:
            print '        TOO LONG!\n'
