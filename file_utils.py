import os

__author__ = 'lostvisions'


# Walks folders looking for files
# Does not return xxyyzz.xyz.sift files
# Array of file paths returned will have maximum of max_files entries
# With filter_sift=True does not return xxyyzz.xyz if xxyyzz.xyz.sift already exists
def find_files(folders, max_files=100, filter_sift=False):
    all_files = []

    for folder in folders:
        all_files = walk_folder(folder, all_files, max_files, filter_sift)
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
def walk_folder(folder, all_files, max_files, filter_sift=False):

    for a_file in os.listdir(folder):
        if len(all_files) > max_files:
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
            else:
                all_files.append(os.path.join(folder, a_file))

        if os.path.isdir(os.path.join(folder, a_file)):
            all_files = walk_folder(os.path.join(folder, a_file), all_files, max_files, filter_sift)
    return all_files

