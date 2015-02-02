from os import listdir
from os.path import isfile, join, splitext, abspath
import pprint
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
                    ba = bytearray(f1.read())

                    img_data_dict = self.read_bly_line_bytearray(ba)

                    print pprint.pformat(img_data_dict)

            except Exception as e1:
                print e1

    # Do the real work
    def read_bly_line_bytearray(self, ba):

        # How long is our line/ bytearray?
        file_length = len(ba)

        # Get version
        version_bytes, ba = self.slice_bytearray(ba, 4)
        version = self.byte_to_uint(version_bytes)

        # Get image file url length
        img_path_len_bytes, ba = self.slice_bytearray(ba, 2)
        img_path_len_int = self.byte_to_ushort(img_path_len_bytes)

        # Get image url
        path_bytes, ba = self.slice_bytearray(ba, img_path_len_int)
        url_path = self.byte_arr_to_string(path_bytes, img_path_len_int)

        # Get tag list length
        tag_len, ba = self.slice_bytearray(ba, 2)
        tag_len_int = self.byte_to_ushort(tag_len)

        # Get tag list
        tags, ba = self.slice_bytearray(ba, tag_len_int)
        tag_tsv = self.byte_arr_to_string(tags, tag_len_int)

        # It's a TSV list, so split by \t
        tags = tag_tsv.split('\t')

         # Get normalised parameter list length, probably 127
        norm_param_len, ba = self.slice_bytearray(ba, 4)
        norm_param_len_int = self.byte_to_uint(norm_param_len)

        print norm_param_len_int

        norm_params = []
        for par_num in range(0, norm_param_len_int):
            # Get normalised parameter list
            norm_param_bytes, ba = self.slice_bytearray(ba, 8)
            norm_param = self.byte_to_double(norm_param_bytes)

            norm_params.append(norm_param)

        # Get parameter list length, probably 127
        param_len, ba = self.slice_bytearray(ba, 4)
        param_len_int = self.byte_to_uint(param_len)

        print param_len_int

        params = []
        for par_num in range(0, param_len_int):
            # Get parameter list
            param_bytes, ba = self.slice_bytearray(ba, 8)
            param = self.byte_to_double(param_bytes)

            params.append(param)

        #  Count of unique colours
        count_colours, ba = self.slice_bytearray(ba, 4)
        count_colours_int = self.byte_to_uint(count_colours)

        #  RGB
        colours = []
        for colour in range(0, count_colours_int):
            red_bytes, ba = self.slice_bytearray(ba, 8)
            red = self.byte_to_double(red_bytes)

            green_bytes, ba = self.slice_bytearray(ba, 8)
            green = self.byte_to_double(green_bytes)

            blue_bytes, ba = self.slice_bytearray(ba, 8)
            blue = self.byte_to_double(blue_bytes)
            colours.append([red, green, blue])

        return {
            'file_length': file_length,
            'version': version,
            'url_path_length': img_path_len_int,
            'url_path': url_path,
            'tag_list_length':tag_len_int,
            'tag_list': tags,
            'normalised_param_length': norm_param_len_int,
            'normalised_params': norm_params,
            'params_length': param_len_int,
            'params': params,
            'colours_length': count_colours_int,
            'colours': colours
        }

blyreader = BLYreader('./data')

blyreader.read_dir()