import os

# s3://hmri-results/2016/12/27/book_events_bats_edga_2016-12-27.h5
files = []
for line in open('acutal_files_to_transfer.txt'):
    files.append(line)


tot = len(files)

for file in files:
  print('copying {}'.format(file))
  print('file {} of {}'.format(files.index(file),tot))
  os.system("aws s3 cp {} ~/data/. --profile uva_s3".format(file))
  os.system("rm -rf /tmp/*")