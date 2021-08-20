import numpy as np
#import constant as const
#savedir = const.txtdir

urls=np.load('txt/dirlist.npy')

for url in urls:
	txtdir='/home/yujq/users/caijie/epoch2d'+'/txt/'+url+'/'	
	try:
		eff=np.load(txtdir+'eff_bz.npy')
		with open("txt/getEff.txt","a") as f:
			f.write(str(url[21:]) + ','  + str(np.nanmax(eff))+"\n")
	except:
		eff=np.zeros(100)*np.nan
