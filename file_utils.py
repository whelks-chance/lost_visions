import os
import math
import pprint

__author__ = 'lostvisions'


# Walks folders looking for files
# Does not return xxyyzz.xyz.sift files
# Array of file paths returned will have maximum of max_files entries
# With filter_sift=True does not return xxyyzz.xyz if xxyyzz.xyz.sift already exists
def find_files(folders, max_files=100, filter_descriptors=None, output_path=None, folder_spread=False):
    all_files = []
    files_dict = {}

    print 'Finding max ' + str(max_files) + ' files'
    folder_count = None
    if folder_spread:
        # print "non-ceil {}".format(str(max_files/ len(folders)))
        folder_count = math.ceil(max_files / float(len(folders)))
        print "Max {} files per folder." \
              " {} folders total. May be less due to rounding".format(folder_count, len(folders))

    for folder in folders:
        all_files = walk_folder(folder,
                                all_files,
                                max_files,
                                filter_descriptors,
                                output_path, folder_count, base_path=os.path.abspath(os.path.join(folder, '..')))
        if len(all_files) > max_files:
            break

    # print 'Found ' + str(len(all_files)) + ' files'
    for f in all_files[:max_files]:
        files_dict[int(len(files_dict))] = f

    print pprint.pformat(files_dict, indent=1, width=80, depth=None)

    # print 'Loading ' + str(len(files_dict)) + ' files.'
    return files_dict


# Walks folders looking for files
# Array of file paths returned will have maximum of max_files entries
# Does not return xxyyzz.xyz.sift files
#  With filter_sift=True does not return xxyyzz.xyz if xxyyzz.xyz.sift already exists
def walk_folder(folder, all_files, max_files, filter_descriptors=None,
                output_folder=None, folder_count=None, base_path=None):

    # print 'Searching folder {}'.format(folder)
    # print('base folder {}'.format(base_path))
    found_count = 0
    for file_name in os.listdir(folder):
        a_file = os.path.join(folder, file_name)
        if len(all_files) > max_files:
            return all_files
        if folder_count is not None and found_count == folder_count:
            return all_files

        fileName, fileExtension = os.path.splitext(file_name)

        if os.path.isfile(a_file) and a_file[-4:] == '.jpg':
            if filter_descriptors:
                should_add = False
                for descriptor in filter_descriptors:

                    #TODO move output folder check to OUTPUT_FOLDER

                    # 'folder' is the folder we are searching
                    # 'a_file' is the current file we've found, ending with .jpg

                    # rel_path is the relative path from the current files name from the folders parent
                    # so ~/images/maps/a_map0001.jpg
                    # is maps/a_map0001.jpg
                    parent_parent = os.path.abspath(os.path.dirname(folder))
                    rel_path = os.path.relpath(os.path.abspath(a_file), base_path)
                    # print '*{}*\n *{}*\n *{}*,\n *{}*\n\n'.format(parent_parent, folder, rel_path, os.path.abspath(a_file))

                    # join the output_folder folder from settings to this relative path
                    # ~/output/maps/a_map.jpg
                    new_path = os.path.join(output_folder, rel_path)

                    #
                    descriptor_path = os.path.join(new_path, 'desc' + descriptor['ext'])

                    # print 'File {}\nlooking for {}'.format(os.path.abspath(a_file), os.path.abspath(descriptor_path))

                    if os.path.isfile(descriptor_path):
                        # print 'found {} \n'.format(descriptor_path)
                    # if os.path.isfile(os.path.join(folder, (a_file + '.sift'))):
                        pass

                    else:
                        # Missing a descriptor, so we add it to the list
                        # TODO this means for any missing descriptor, we calculate all descriptors again.
                        should_add = True
                if should_add:
                    all_files.append(a_file)
                    found_count += 1
            else:
                all_files.append(a_file)
                found_count += 1

        if os.path.isdir(a_file):
            all_files = walk_folder(a_file,
                                    all_files,
                                    max_files=max_files,
                                    filter_descriptors=filter_descriptors,
                                    output_folder=output_folder,
                                    base_path=base_path)
    return all_files

