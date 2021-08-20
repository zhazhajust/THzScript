import os
import numpy as np
wkdir='/home/yujq/users/caijie/epoch2d/Data/45TW_new2/a2.6_w22.2'

dirlist=[]
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        if dirs == []:
            root = root[37:] 
            dirlist.append(str(root))
            print('root_dir:', root)  # 当前目录路径
            #print('sub_dirs:', dirs)  # 当前路径下所有子目录
        #print('files:', files)  # 当前路径下所有非目录子文件

file_name(wkdir)
print(dirlist)
np.save('txt/dirlist.npy',dirlist)
