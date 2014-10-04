import datetime
from time import sleep

__author__ = 'ubuntu'

class TimeInstant():
    def __init__(self, time, description):
        self.time = time
        self.description = description


class TimeKeeper():

    def __init__(self):
        self.times = []
        self.time_now('start')

    def time_now(self, description, print_out=False):
        now = datetime.datetime.now()
        current_instant = TimeInstant(now, description)

        if print_out:
            print '\n****************'
            print 'Event : ' + description
            print 'Time : ' + str(now.isoformat())
        if len(self.times) > 0:
            recent = self.times[-1]
            delta = current_instant.time - recent.time

            if print_out:
                print 'Time delta : ' + str(delta.total_seconds())

                start = self.times[0]
                start_delta = current_instant.time - start.time
                print 'Time since start : ' + str(start_delta.total_seconds())
                print '****************\n'

            self.times.append(current_instant)
            return delta.total_seconds()
        else:
            if print_out:
                print '****************\n'

            self.times.append(current_instant)
            return 0