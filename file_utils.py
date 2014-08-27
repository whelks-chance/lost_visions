import os

__author__ = 'lostvisions'


def find_files(folders, max_files=100):
    all_files = []
    for folder in folders:
        # print folder
        count = 0
        for a_file in os.listdir(folder):
                # print a_file
            fileName, fileExtension = os.path.splitext(a_file)

            if os.path.isfile(os.path.join(folder, a_file)) and '.sift' not in fileExtension:
                all_files.append(os.path.join(folder, a_file))
        all_files = walk_folder(folder, all_files)

    # print 'Found ' + str(len(all_files)) + ' files'
    files_dict = {}
    for f in all_files[:max_files]:
        files_dict[int(len(files_dict))] = f

    # print str(files_dict) + '\n\n****\n'
    # print 'Loading ' + str(len(files_dict)) + ' files.'
    return files_dict

def walk_folder(folder, all_files):
    for a_file in os.listdir(folder):
        # print a_file
        fileName, fileExtension = os.path.splitext(a_file)

        if os.path.isfile(os.path.join(folder, a_file)) and '.sift' not in fileExtension:
            all_files.append(os.path.join(folder, a_file))

        if os.path.isdir(os.path.join(folder, a_file)):
            all_files = walk_folder(os.path.join(folder, a_file), all_files)
    return all_files

