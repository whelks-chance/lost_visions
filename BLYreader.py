from os import listdir
from os.path import isfile, join, splitext, abspath
import struct

__author__ = 'ubuntu'


class BLYreader():
    def __init__(self, dir_path):
        self.dir_path = dir_path

    # Returns two arrays, the first of length n_bytes, the second the remainder
    def slice_bytearray(self, b_arr,  n_bytes):
        start_bytes = b_arr[0: n_bytes]

        for a in range(0, n_bytes):
            b_arr.pop(0)
        return start_bytes, b_arr

    # Convert the bytes to an unsigned integer
    def byte_to_uint(self, b_arr):
        return struct.unpack('>I', str(b_arr))[0]

    # Convert to a double
    def byte_to_double(self, b_arr):
        return struct.unpack('>d', str(b_arr))[0]

    # Convert to unsigned short
    def byte_to_ushort(self, b_arr):
        return struct.unpack('>H', str(b_arr))[0]

    # Return s string of length string_len_int from the byte array
    def byte_arr_to_string(self, b_arr, string_len_int):
        return struct.unpack(str(string_len_int) + 's', str(b_arr))[0]

    # Work through each .bly file in a directory, no recursion
    def read_dir(self):
        onlyfiles = [ f for f in listdir(self.dir_path)
                      if isfile(join(self.dir_path, f)) and splitext(join(self.dir_path, f))[1].split('.')[-1] == 'bly' ]

        for bly in onlyfiles:
            try:
                print '\n\n'
                print abspath(join(self.dir_path, bly))

                with open(abspath(join(self.dir_path, bly))) as f1:
                    ba = bytearray(f1.readline())

                    self.read_bly_line_bytearray(ba)

            except Exception as e1:
                print e1

    # Do the real work
    def read_bly_line_bytearray(self, ba):

        # How long is our line/ bytearray?
        print len(ba)

        # Get version
        version, ba = self.slice_bytearray(ba, 4)
        print self.byte_to_uint(version)

        # Get image file url length
        img_path_len, ba = self.slice_bytearray(ba, 2)
        img_path_len_int = self.byte_to_ushort(img_path_len)
        print img_path_len_int

        # Get image url
        path_bytes, ba = self.slice_bytearray(ba, img_path_len_int)
        url_path = self.byte_arr_to_string(path_bytes, img_path_len_int)
        print url_path

        # Get tag list length
        tag_len, ba = self.slice_bytearray(ba, 2)
        tag_len_int = self.byte_to_ushort(tag_len)

        # Get tag list
        tags, ba = self.slice_bytearray(ba, tag_len_int)
        tag_tsv = self.byte_arr_to_string(tags, tag_len_int)

        # It's a TSV list, so split by \t
        tags = tag_tsv.split('\t')

        print tags

         # Get normalised parameter list length, probably 127
        norm_param_len, ba = self.slice_bytearray(ba, 4)
        norm_param_len_int = self.byte_to_uint(norm_param_len)

        print norm_param_len_int

        for par_num in range(0, norm_param_len_int):
            # Get normalised parameter list
            norm_param_bytes, ba = self.slice_bytearray(ba, 8)
            norm_param = self.byte_to_double(norm_param_bytes)

            print norm_param



blyreader = BLYreader('./data')

blyreader.read_dir()