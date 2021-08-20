import numpy as np
import constant as const
savedir = const.txtdir
eff=np.load(savedir+'EffBz.npy')
#distance = np.load (savedir + 'EffLocated.npy')
#a0=np.load(savedir+'a0.npy')
#a0_3 = np.loadtxt(savedir+'3.5Thz_a0.txt')

#time1 =  np.load(const.txtdir + 'a0.npy').argmax()+1   #sdf_locate
#locate1 = (time1*const.dt_snapshot - const.window_start_time)*3e8*1e6

###
time2 = np.load(const.txtdir + 'EffBz.npy').argmax()+1
locate2 = (time2*const.dt_snapshot - const.window_start_time)*3e8*1e6
#print('a0.argmax():',time1,locate1,a0.max())
print('eff.argmax():',time2,locate2,np.nanmax(eff))
#print('a0_3.argmax():',a0_3.argmax(),(a0_3.argmax()*const.dt_snapshot - const.window_start_time)*3e8*1e6)
