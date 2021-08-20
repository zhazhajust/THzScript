import os
import numpy as np
dirlist=[]
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        if dirs == []:
            dirlist.append(str(root))
            print('root_dir:', root)  # 当前目录路径
            #print('sub_dirs:', dirs)  # 当前路径下所有子目录
        #print('files:', files)  # 当前路径下所有非目录子文件
#wkdir = '/home/yujq/users/caijie/epoch2d/Data/45TW_new2/a2.5_w20'
#wkdir = '/home/yujq/users/caijie/epoch2d/Data/45TW_new2'
#wkdir = '/home/yujq/users/caijie/epoch2d/Data/2color'
#wkdir ='/home/yujq/users/caijie/epoch2d/Data/cascade'
wkdir = '/home/yujq/users/caijie/epoch2d/Data/MassLimit/new_a3_w9.1_n0.2'
file_name(wkdir)
#print(tuple(dirlist))
s=''
for i in dirlist:
	s=i[37:]+' '+s	
print(s)
np.save('txt/dirlist.npy',dirlist)
