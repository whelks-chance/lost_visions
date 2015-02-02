from os import listdir, walk
from os.path import isfile, join, splitext, abspath
import pprint
import struct
from graphs import create_img_graph
from matrix_distance import PictureDetails, find_dists

__author__ = 'ubuntu'

table_headers = ['grad1_energy', 'grad1_entropy', 'grad1_correlation', 'grad1_inverseDifferenceMoment',
                 'grad1_inertia', 'grad1_clusterShade', 'grad1_clusterProminence', 'grad2_energy', 'grad2_entropy',
                 'grad2_correlation', 'grad2_inverseDifferenceMoment', 'grad2_inertia', 'grad2_clusterShade',
                 'grad2_clusterProminence', 'energy', 'entropy', 'correlation', 'inverseDifferenceMoment',
                 'inertia', 'clusterShade', 'clusterProminence', 'laplace_energy', 'laplace_entropy',
                 'laplace_correlation', 'laplace_inverseDifferenceMoment', 'laplace_inertia',
                 'laplace_clusterShade', 'laplace_clusterProminence', 'segment_energy', 'segment_entropy',
                 'segment_correlation', 'segment_inverseDifferenceMoment', 'segment_inertia',
                 'segment_clusterShade', 'segment_clusterProminence', 'segmentDistances_energy',
                 'segmentDistances_entropy', 'segmentDistances_correlation',
                 'segmentDistances_inverseDifferenceMoment', 'segmentDistances_inertia',
                 'segmentDistances_clusterShade', 'segmentDistances_clusterProminence', 'threshold_Y_Q0',
                 'threshold_U_Q0', 'threshold_V_Q0', 'threshold_Y_Q1', 'threshold_U_Q1', 'threshold_V_Q1',
                 'threshold_Y_Q2', 'threshold_U_Q2', 'threshold_V_Q2', 'threshold_Y_Q3', 'threshold_U_Q3',
                 'threshold_V_Q3', 'threshold_Y_Q4', 'threshold_U_Q4', 'threshold_V_Q4', 'thresholdOtsu_Y',
                 'thresholdOtsu_U', 'thresholdOtsu_V', 'median_Y', 'median_U', 'median_V', 'variance_Y',
                 'standardDeviation_Y', 'skewness_Y', 'kurtosis_Y', 'errorOnAverage_Y', 'variance_U',
                 'standardDeviation_U', 'skewness_U', 'kurtosis_U', 'errorOnAverage_U', 'variance_V',
                 'standardDeviation_V', 'skewness_V', 'kurtosis_V', 'errorOnAverage_V', 'variance_SegmentSize',
                 'standardDeviation_SegmentSize', 'skewness_SegmentSize', 'kurtosis_SegmentSize',
                 'errorOnAverage_SegmentSize', 'thresholdOtsu_SegmentSize', 'median_SegmentSize',
                 'variance_SegmentDistances', 'standardDeviation_SegmentDistances', 'skewness_SegmentDistances',
                 'kurtosis_SegmentDistances', 'errorOnAverage_SegmentDistances', 'thresholdOtsu_SegmentDistances',
                 'median_SegmentDistances', 'originalWidth', 'originalHeight', 'proportion', 'orientation',
                 'segmentCount', 'jpegCompressionRatio', 'pngCompressionRatio', 'variance_grad1',
                 'standardDeviation_grad1', 'skewness_grad1', 'kurtosis_grad1', 'errorOnAverage_grad1',
                 'thresholdOtsu_grad1', 'median_grad1', 'variance_grad2', 'standardDeviation_grad2',
                 'skewness_grad2', 'kurtosis_grad2', 'errorOnAverage_grad2', 'thresholdOtsu_grad2',
                 'median_grad2', 'variance_hough', 'standardDeviation_hough', 'skewness_hough',
                 'kurtosis_hough', 'errorOnAverage_hough', 'thresholdOtsu_hough', 'median_hough',
                 'hough_energy', 'hough_entropy', 'hough_correlation', 'hough_inverseDifferenceMoment',
                 'hough_inertia', 'hough_clusterShade', 'hough_clusterProminence']

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
        # onlyfiles = [ f for f in walk(self.dir_path)
        #               if isfile(join(self.dir_path, f)) and splitext(join(self.dir_path, f))[1].split('.')[-1] == 'bly' ]

        only_files = []
        count = 0
        file_count = 200

        for root, dirs, files in walk(self.dir_path, topdown=False):
            if count > file_count:
                break
            for name in files:
                if count > file_count:
                    break
                if isfile(join(root, name)) and splitext(join(root, name))[1].split('.')[-1] == 'bly':
                    only_files.append(join(root, name))
                    count += 1

        print len(only_files)
        pic_details = []

        for bly in only_files:
            try:
                # print '\n\n'
                # print abspath(bly)

                with open(abspath(bly)) as f1:
                    ba = bytearray(f1.read())

                    img_data_dict = self.read_bly_line_bytearray(ba)

                    # print pprint.pformat(img_data_dict)

                    pd = PictureDetails(img_data_dict['flickr_id'], img_data_dict['normalised_params'])
                    pd.url = img_data_dict['url_path']
                    # print img_data_dict['flickr_id']
                    pic_details.append(pd)

            except Exception as e1:
                print e1

        print len(pic_details)
        dists, closests = find_dists(pic_details)

        print len(dists)

        create_img_graph(closests)

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

        flickr_id = url_path.split('/')[-1].split('_')[0]

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

        norm_params = []
        for par_num in range(0, norm_param_len_int):
            # Get normalised parameter list
            norm_param_bytes, ba = self.slice_bytearray(ba, 8)
            norm_param = self.byte_to_double(norm_param_bytes)

            norm_params.append(norm_param)

        # Get parameter list length, probably 127
        param_len, ba = self.slice_bytearray(ba, 4)
        param_len_int = self.byte_to_uint(param_len)

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
            'flickr_id': flickr_id,
            'tag_list_length':tag_len_int,
            'tag_list': tags,
            'normalised_param_length': norm_param_len_int,
            'normalised_params': norm_params,
            'params_length': param_len_int,
            'params': params,
            'colours_length': count_colours_int,
            'colours': colours
        }

blyreader = BLYreader('./bly-data/')

blyreader.read_dir()