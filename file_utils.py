import os
import math

__author__ = 'lostvisions'


# Walks folders looking for files
# Does not return xxyyzz.xyz.sift files
# Array of file paths returned will have maximum of max_files entries
# With filter_sift=True does not return xxyyzz.xyz if xxyyzz.xyz.sift already exists
def find_files(folders, max_files=100, filter_sift=False, folder_spread=False):
    all_files = []

    print max_files
    folder_count = None
    if folder_spread:
        print "non-ceil {}".format(str(max_files/ len(folders)))
        folder_count = math.ceil(max_files / float(len(folders)))
        print "{} files per folder. {} folders total".format(folder_count, len(folders))


    for folder in folders:
        all_files = walk_folder(folder, all_files, max_files, filter_sift, folder_count)
        print all_files
        if len(all_files) > max_files:
            break

    # print 'Found ' + str(len(all_files)) + ' files'
    files_dict = {}
    for f in all_files[:max_files]:
        files_dict[int(len(files_dict))] = f

    # print str(files_dict) + '\n\n****\n'
    # print 'Loading ' + str(len(files_dict)) + ' files.'
    return files_dict


# Walks folders looking for files
# Array of file paths returned will have maximum of max_files entries
# Does not return xxyyzz.xyz.sift files
#  With filter_sift=True does not return xxyyzz.xyz if xxyyzz.xyz.sift already exists
def walk_folder(folder, all_files, max_files, filter_sift=False, folder_count = None):
    found_count = 0
    for a_file in os.listdir(folder):
        if len(all_files) > max_files:
            return all_files
        if folder_count is not None and found_count == folder_count:
            return all_files

        fileName, fileExtension = os.path.splitext(a_file)

        if os.path.isfile(os.path.join(folder, a_file)) \
                and '.sift' not in fileExtension \
                and '.jpg' in fileExtension:
            if filter_sift:
                if os.path.isfile(os.path.join(folder, (a_file + '.sift'))):
                    pass
                else:
                    all_files.append(os.path.join(folder, a_file))
                    found_count += 1
            else:
                all_files.append(os.path.join(folder, a_file))
                found_count += 1

        if os.path.isdir(os.path.join(folder, a_file)):
            all_files = walk_folder(os.path.join(folder, a_file), all_files, max_files, filter_sift)
    return all_files

