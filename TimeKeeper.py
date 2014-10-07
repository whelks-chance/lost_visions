import datetime
from time import sleep

__author__ = 'ubuntu'

class TimeInstant():
    def __init__(self, time, description):
        self.time = time
        self.description = description


def write_file(text):
    with open('timekeeper.txt', 'a') as f1:
        f1.writelines(line + '\n' for line in text)
    f1.close()


class TimeKeeper():

    def __init__(self):
        self.times = []
        self.time_now('start')

    def time_now(self, description, print_out=False):
        now = datetime.datetime.now()
        current_instant = TimeInstant(now, description)

        text = []

        if print_out:
            text.append('\n****************')
            text.append('Event : {}'.format(description))
            text.append('Time : {}'.format(str(now.isoformat())))

        if len(self.times) > 0:
            recent = self.times[-1]
            delta = current_instant.time - recent.time

            if print_out:
                text.append('Time delta : {}'.format(str(delta.total_seconds())))

                start = self.times[0]
                start_delta = current_instant.time - start.time
                text.append('Time since start : {}\n'.format(str(start_delta.total_seconds())))
                text.append('****************\n')
                write_file(text)

            self.times.append(current_instant)
            return delta.total_seconds()
        else:
            if print_out:
                text.append('****************\n')
                write_file(text)
            self.times.append(current_instant)
            return 0