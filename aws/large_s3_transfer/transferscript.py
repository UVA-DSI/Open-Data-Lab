import os

# s3://hmri-results/2016/12/27/book_events_bats_edga_2016-12-27.h5
files = []
for line in open('acutal_files_to_transfer.txt'):
    files.append(line)

folders = []
for line in open('folders_to_make.txt'):
    folders.append(line)


tot = len(files)

files2 = []
for file in files:
    files2.append(file[:-1])

folders2 = []
for folder in folders:
    folders2.append(folder[18:-1])


files2 = files2[0:2]
print(files2)
print("path ~/data/{}/".format(files2[0][18:files2[0].rfind("/")]))
##folders2 = folders2[0:3]
##print(folders2)

print("making file structure")

if True:
    os.system('rm -rf ~/data/*')
    for folder in folders2: os.system("mkdir ~/data/{}".format(folder))

    for file in files2:
        print('copying {}'.format(file))
        path = '~/data/{}/'.format(file[18:file.rfind("/")])
        print('to {}'.format(path))
        print('file {} of {}'.format(files2.index(file),tot))
        os.system("rm -rf /tmp/*")
        os.system("aws s3 cp {} {} --profile uva_s3".format(file,path))
        os.system("rm -rf /tmp/*")
