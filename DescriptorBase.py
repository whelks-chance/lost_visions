__author__ = 'ubuntu'


class DescriptorBase():
    def __init__(self):
        self.name = 'generic base descriptor - zero functions'

    def touch_descriptor(self, img_path, detector_ext=None, output_path=None):
        raise NotImplementedError

    def compare_descriptors(self, d1, d2, thresh):
        raise NotImplementedError

    def pickle_keypoints(self, keypoints, descriptors):
        raise NotImplementedError

    def unpickle_keypoints(self, array):
        raise NotImplementedError


class DescriptorCreationResponse():
    def __init__(self, descriptor_path, had_to_create):
        self.had_to_create = had_to_create
        self.descriptor_path = descriptor_path
        self.error = None

    def error(self):
        return self.error