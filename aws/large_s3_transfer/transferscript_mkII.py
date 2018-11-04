import os

# s3://hmri-results/2016/12/27/book_events_bats_edga_2016-12-27.h5
files = []
for line in open('acutal_files_to_transfer.txt'):
    files.append(line)


tot = len(files)

files2 = []
for file in files:
    files2.append(file[:-1])


files2 = files2[3841:3843]
#print(files2)


if True:
    for file in files2:
        print('copying {} of {}'.format(files2.index(file),tot))
        filename = file[file.rfind('hmri-results/')+13:]
        print('copying {}'.format(filename))
        cmd1 = '{}'.format("aws s3 cp s3://hmri-results/{} s3://odl-hmtt/{} --profile uva_s3".format(filename,filename))
        print(cmd1)
        os.system(cmd1)
