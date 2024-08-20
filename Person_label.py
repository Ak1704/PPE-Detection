import os
import glob
import shutil
def read_file(out_file,in_file):
    with open(in_file,'r') as file:
        r=[]
        for i in file.readlines():
            if i[0]=='0':
                print(i)
                r.append(i)
    with open(out_file,'w') as out:
        for i in r:
            out.write(i)

path= r"C:\Users\ADMIN\Desktop\tempdm\Py files\comp_vision\datasets\Test"
out_path=r"C:\Users\ADMIN\Desktop\tempdm\Py files\comp_vision\Person_det_data\Train\Labels"
os.chdir(path)
l=os.listdir()
for file in l[:399]:
    file_path = f"{path}\{file}"
    read_file(f'{out_path}\{file}',f'{path}\{file}')
out_path=r"C:\Users\ADMIN\Desktop\tempdm\Py files\comp_vision\Person_det_data\Val\Labels"
for file in l[399:]:
    file_path = f"{path}\{file}"
    read_file(f'{out_path}\{file}', f'{path}\{file}')
src_dir = r"C:\Users\ADMIN\Desktop\tempdm\Py files\comp_vision\datasets\images"
train_dir = r"C:\Users\ADMIN\Desktop\tempdm\Py files\comp_vision\Person_det_data\Train\Images"
Val_dir = r"C:\Users\ADMIN\Desktop\tempdm\Py files\comp_vision\Person_det_data\Val\Images"
os.chdir(src_dir)
l=os.listdir()
files= os.listdir()
for jpgfile in files[:399]:
    shutil.copy(jpgfile, train_dir)
for jpgfile in files[399:]:
    shutil.copy(jpgfile, Val_dir)