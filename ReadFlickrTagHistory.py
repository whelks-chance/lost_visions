import csv

__author__ = 'lostvisions'

# flickrid	enteredtext	from	to	tagid	author	tag	mode
# 12403504@N02

class ReadFlickrTagHistory:
    def __init__(self, file):
        self.file = file

    def is_metadata_tag(self, tag):
        return True

    def removeCommonMetadata(self, human_tag_file):

        total_read = 0
        total_human = 0

        with open(self.file, 'rb') as csvfile:
            rowreader = csv.reader(csvfile, delimiter='\t', quotechar='|')

            with open(human_tag_file, 'wb') as human_file:
                human_writer = csv.writer(human_file, delimiter='\t', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

                for row in rowreader:
                    total_read += 1
                    # print row
                    # print ', '.join(row)

                    try:
                        if len(row) > 1 and row[5] != '12403504@N02' and row[7] == 'add':
                            # print row
                            # print row[0], row[1], '\n'
                            total_human += 1
                            human_writer.writerow(row)

                        if total_read%100 == 0:
                            print '.',
                        if total_human%100 == 0:
                            print '#',
                        if total_read%1000 == 0:
                            print '\n'
                    except:
                        print '\n', row, '\n'


tag_file = '/media/New Volume/taghistory.tsv'
human_tag_file = '/media/New Volume/humantaghistory.tsv'

rfth = ReadFlickrTagHistory(tag_file)
rfth.removeCommonMetadata(human_tag_file)