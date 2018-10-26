import os

# s3://hmri-results/2016/12/27/book_events_bats_edga_2016-12-27.h5
files = []
for line in open('acutal_files_to_transfer.txt'):
    files.append(line)


tot = len(files)

files2 = []
for file in files:
    files2.append(file[:-1])

files2 = files2[0:3]
print(files2)

for file in files2:
  print('copying {}'.format(file))
  print('file {} of {}'.format(files2.index(file),tot))
  os.system("rm -rf /tmp/*")
  os.system("aws s3 cp {} ~/data/. --profile uva_s3".format(file))
  os.system("rm -rf /tmp/*")