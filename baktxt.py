import constant as const
import sdf
import os
import numpy as np
import multiprocessing
start=const.start
stop=const.stop
step=const.step

savedir="baktxt/"+const.data_name

#if (os.path.isdir(savedir) == False):
#	os.makedirs(savedir,exist_ok = True)
os.makedirs(savedir,exist_ok = True)
def baktxt(n):
	print(n)
	if os.path.exists("baktxt/"+const.data_name+str(n)+"Ey_y0.npy") == True:
		print("baktxt/"+const.data_name+str(n)+"Ey_y0.npy"+" exists")
		return

	try:
		#print("save file:"+str(n))
		sdfdir=const.sdfdir +str(n).zfill(const.filenumber)+".sdf"
		data = sdf.read(sdfdir,dict=True)
		Ey_y0=data["Electric Field/Ey"].data[:,int(const.Ny/2)]
		np.save("baktxt/"+const.data_name+str(n)+"Ey_y0.npy",Ey_y0)
		Ez_y0=data["Electric Field/Ez"].data[:,int(const.Ny/2)]		
		np.save("baktxt/"+const.data_name+str(n)+"Ez_y0.npy",Ez_y0)
	except:
		return

pool = multiprocessing.Pool(processes=96)
#for i in range(start,stop+step,step):
#       results.append(pool.apply_async(extract, (i, ))) 

def bak_txt(i):
	baktxt(i)
	return
#results = pool.map_async(baktxt,range(int(start),int(stop+step)))

results = pool.map(baktxt,range(int(start),int(stop+step)))

pool.close()
pool.join()

print('finished')
