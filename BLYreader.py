from os import listdir
from os.path import isfile, join, splitext, abspath
import struct

__author__ = 'ubuntu'


class BLYreader():
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def slice_bytearray(self, b_arr,  n_bytes):
        start_bytes = b_arr[0: n_bytes]

        for a in range(0, n_bytes):
            b_arr.pop(0)
        return start_bytes, b_arr

    def byte_to_uint(self, b_arr):
        return struct.unpack('>I', str(b_arr))[0]

    def read_dir(self):
        onlyfiles = [ f for f in listdir(self.dir_path)
                      if isfile(join(self.dir_path, f)) and splitext(join(self.dir_path, f))[1].split('.')[-1] ]

        for bly in onlyfiles:
            print abspath(join(self.dir_path, bly))

            with open(abspath(join(self.dir_path, bly))) as f1:
                ba = bytearray(f1.readline())

                self.read_bly_line_bytearray(ba)

    def read_bly_line_bytearray(self, ba):
        print len(ba)

        version, ba = self.slice_bytearray(ba, 4)

        print self.byte_to_uint(version)

        print len(ba)


blyreader = BLYreader('./data')

blyreader.read_dir()