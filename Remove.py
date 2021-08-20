import numpy as np
import constant as const
import os
import multiprocessing
import lists
import Processing
savedir = const.txtdir


def getflist():
    filedict = []
    filename = sdfdir + 'normal.visit'
    with open(filename,'r') as f:
        filedict = f.readlines()
        filedict = [i.rstrip('\n') for i in filedict]
    return filedict

flist = getflist() #Processing.flist()
savefile = flist[::int(len(arr)/100)]
print(arr)
#b = const.x_max/3e8/const.dt_snapshot/2
try:
	b = (const.las_t_fwhm1/const.dt_snapshot)*2
except:
	b = 0
b = int(b)
#print('b',b)
#dirsdf  = const.sdfdir
#dirsize =  const.filenumber
####
#stay=lists.line[::int(len(lists.line)/100)]
#stay=np.arange(start,stop+int(stop)/100,int(stop)/100)

#stay = arr
#print('1=2',stay/stay2)
def rm(n):
	save = 0

	#index_max = efficiency.argmax()+1
	#a0_max    = a0.argmax()+1
	#print('a0',a0.max())
	#print('eff',efficiency.max())

	str_n = str(n).zfill(const.filenumber)

	#if str_n in stay:
	if n in stay:
		save = 1
		print(str_n)
	if n == b: 
		save = 1
	if n == stop:
                save = 1
	#####remove
	
	if save == 0:
		if os.path.exists(dirsdf + flist[n])==True:
			print('begin_remove')
            os.remove(dirsdf + flist[n])
			#os.remove(dirsdf+str(n).zfill(dirsize)+".sdf")
			print('remove:',n)
	if save == 1:
		print('save_sdf:',n)
	
	return
print('len(lists.line)',len(lists.line))
if len(lists.line) < const.stop:
	print('has been removed')


pool = multiprocessing.Pool(processes=96)
results=pool.map(rm,range(start,stop+step,step))
#print(len(results))


