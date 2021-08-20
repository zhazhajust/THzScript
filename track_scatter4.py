import happi 
import numpy as np 
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt 
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import sys, getopt
import os,time


q0        =     1.602176565e-19 # C
m0        =     9.10938291e-31  # kg
v0        =     2.99792458e8    # m/s^2


matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'

# #matplotlib.rcParams['font.family'] = 'arial'
# # matplotlib.rcParams['font.weight'] = 'normal'
# # matplotlib.rcParams['font.size'] = 17

matplotlib.rcParams['lines.linewidth'] = 2

matplotlib.rcParams['axes.linewidth'] = 2
matplotlib.rcParams['axes.labelsize'] = 20
# matplotlib.rcParams['axes.titlesize'] = 17
# matplotlib.rcParams['axes.titlepad'] = 15
# matplotlib.rcParams['axes.facecolor'] = 'none'

matplotlib.rcParams['xtick.major.width'] = 1.5
matplotlib.rcParams['xtick.major.size'] = 6
matplotlib.rcParams['ytick.major.width'] = 1.5
matplotlib.rcParams['ytick.major.size'] = 6.0
matplotlib.rcParams['ytick.labelsize'] = 20
matplotlib.rcParams['xtick.labelsize'] = 20.0
matplotlib.rcParams['ytick.right'] = True
matplotlib.rcParams['legend.framealpha'] = 1.0
matplotlib.rcParams['legend.fontsize'] = 15.0

matplotlib.rcParams['ytick.minor.pad'] = 2

matplotlib.rcParams['legend.fancybox'] = False

matplotlib.rcParams['legend.edgecolor'] = 'black'

matplotlib.rcParams['xtick.minor.width'] = 1.0
matplotlib.rcParams['xtick.minor.size'] = 4

matplotlib.rcParams['ytick.minor.width'] = 1.0
matplotlib.rcParams['ytick.minor.size'] = 4

matplotlib.rcParams['ytick.minor.visible'] = False
matplotlib.rcParams['xtick.minor.visible'] = False


matplotlib.rcParams['figure.figsize'] = 9,7 ##one 
matplotlib.rcParams['figure.dpi'] = 100

matplotlib.rcParams['figure.subplot.wspace'] = 0.05
matplotlib.rcParams['figure.subplot.hspace'] = 0.0


matplotlib.rcParams['figure.subplot.left'] = 0.25
matplotlib.rcParams['figure.subplot.right'] = 0.85
matplotlib.rcParams['figure.subplot.bottom'] = 0.15
matplotlib.rcParams['figure.subplot.top'] = 0.9



font = {'family' : 'Times New Roman',  
 		'color'  : 'black',  
          'weight' : 'normal',  
          'size'   : 25,  
          }  

font1 = {'family' : 'Times New Roman',  
          'weight' : 'normal',  
          'size'   : 10,  
          } 


data_dir = './Data/'
txt_dir = data_dir+'txt16/'
# txt_dir = data_dir+'txt11_1/'

Img_dir  = txt_dir+'track_y_2/' 


# S = happi.Open(data_dir,scan=False)
# diag1 = S.Field(0,"Ey")
# # diag2 = S.Field(0,"Ez")
# diag3 = S.Field(0,"Bz")


# diag4 = S.Field(0,"-Rho_electron")

# diag5 = S.Field(0,"Ex")

# diag6 = S.Field(0,"Rho_proton")
# # diag7 = S.Field(0,"Bz_m")
# # diag8 = S.Field(0,"Jx")
# # diag9 = S.Field(0,"Jx_electron")
# # diag10 = S.Field(0,"Jx_proton")

# # diag11 = S.Field(0,"By")
# # diag12 = S.Field(0,'Env_E_abs')


# Ex = np.array(diag5.getData()) 
# Ey = np.array(diag1.getData()) 
# # Ez = np.array(diag2.getData()) 

# Bz = np.array(diag3.getData()) 
# # By = np.array(diag11.getData()) 

# ne = np.array(diag4.getData()) 
# nion = np.array(diag6.getData()) 

# X = diag6.getAxis('x')
# time1 = diag6.getTimes()/(2*np.pi)

# X = np.array(X)/(2*np.pi)


xx = np.loadtxt(txt_dir+'xx1d.txt')
yy = np.loadtxt(txt_dir+'yy1d.txt')
print(xx[0,0])
# px = np.loadtxt(txt_dir+'px1d.txt')
py = np.loadtxt(txt_dir+'py1d.txt')
# pz = np.loadtxt(txt_dir+'pz1d.txt')


# np.savetxt(txt_dir1+'xx1d.txt',xx[:,::100])
# np.savetxt(txt_dir1+'yy1d.txt',yy[:,::100])
# # np.savetxt(txt_dir1+'px1d.txt',px[:,::100])
# np.savetxt(txt_dir1+'py1d.txt',py[:,::100])


# # Ex = np.loadtxt(txt_dir+'Ex1d.txt')
# Ey = np.loadtxt(txt_dir+'Ey1d.txt')
# # Ez = np.loadtxt(txt_dir+'Ez1d.txt')

# Bx = np.loadtxt(txt_dir+'Bx1d.txt')
# # By = np.loadtxt(txt_dir+'By1d.txt')
# Bz = np.loadtxt(txt_dir+'Bz1d.txt')

# Id = np.loadtxt(txt_dir+'Id1d.txt')

# time = np.loadtxt(txt_dir+'tt1d.txt')
# print(len(time))

cmap=plt.get_cmap('rainbow')

#test Id
# for i in range(1,timesteps,100):

# 	if (Id[i,:].all==Id[i-1,:]).all():
# 		print('True')

if not os.path.isdir(Img_dir):
	os.makedirs(Img_dir)
# if not os.path.isdir(Img_dir):
# 	os.makedirs(Img_dir)

# px =px/1836

py =py/1836

# pz =pz/1836

# gamma = (1+px**2+py**2+pz**2)**0.5


# vx = px/gamma
# vy = py/gamma
# vz = pz/gamma

id_num = np.shape(xx)[1]
print(id_num)
# timesteps =  np.shape(xx)[0]
tt = np.linspace(5,23,1656)

fig, axs = plt.subplots(1, 1)

for num in range(0,id_num,100):
# if (py[1228,num]>0):
# 	print(num)
	x = yy[0:1228,num]- yy[0,num]
	y = py[0:1228,num]
	t = tt[0:1228]
	dydx = (0.5 * (t[:-1] + t[1:]))

	points = np.array([x, y]).T.reshape(-1, 1, 2)
	segments = np.concatenate([points[:-1], points[1:]], axis=1)


	# Create a continuous norm to map from data points to colors
	norm = plt.Normalize(dydx.min(), dydx.max())
	lc = LineCollection(segments, cmap='rainbow', norm=norm)
	# Set the values used for colormapping
	lc.set_array(dydx)
	lc.set_linewidth(0.5)
	line = axs.add_collection(lc)
	axs.set_xlabel('y')
	axs.set_ylabel('py')

	axs.set_xlim(-0.006,0.006)
	axs.set_ylim(-0.002,0.002 )

fig.colorbar(line, ax=axs)
plt.savefig(Img_dir+'track_e'+'%04d'%num+'.png')
plt.close('all')

# plt.scatter(yy[739:740,168],py[739:740,168],s=10,color='blue')
# plt.scatter(yy[0,168],py[0,168],s=50,color='green',marker='*')

# plt.scatter(yy[739:740,180],py[739:740,180],s=10,color='black')
# plt.scatter(yy[739:740,246],py[739:740,246],s=10,color='red')

	# for num in range(id_num):
	# 	if (yy[i,num]>6.08) and (yy[i,num]<6.15):
	# 		print(num)
	# 	# plt.plot(time,yy[:,i]-yy[0,i],c='black',lw=0.01)
	# 	plt.plot(time,yy[:,i],lw=1,color=cmap((yy[0,i]-3)*2))
	# plt.subplot(211)
	# plt.scatter(yy[i,:],xx[i,:],s=10,color=cmap(i/1196))
	# plt.xlim(6,7)
	# plt.ylim(5,9)

	# plt.title('t='+str(tt[i]))

	# plt.subplot(212)
	# plt.scatter(yy[i,:],py[i,:],s=10,color=cmap(i/1196))
	# plt.scatter(yy[i,168],py[i,168],s=10,color='blue')
	# plt.scatter(yy[i,180],py[i,180],s=10,color='pink')
	# plt.scatter(yy[i,246],py[i,246],s=10,color='black')

	# plt.scatter(yy[i,171],py[i,171],s=10,color='black')
	# plt.scatter(yy[i,172],py[i,172],s=10,color='red')

	# plt.ylim(-0.001,0.001)
	# plt.xlim(6,7)
	# plt.scatter(xx[0,:]-np.mean(xx[0,:]),py[i,:],s=10,marker='x')
	# plt.ylim(-10,10)
	# plt.scatter((xx[0,:]-np.mean(xx[0,i])),yy[i,:]-yy[0,:],s=10,marker='x')
	# plt.scatter(xx[i,19],yy[i,19],s=10,c='red',label='19')
	# plt.scatter(xx[i,10],yy[i,10],s=10,c='yellow',label='10')
	# plt.scatter(xx[i,5],yy[i,5],s=10,c='purple',label='5')
	# plt.scatter(xx[i,50],yy[i,50],s=10,c='black',label='50')
	# plt.scatter(xx[i,11],yy[i,11],s=10,c='orange',label='11')
	# plt.hlines(yy[0,10],5,5.6,lw=0.1)
	# plt.hlines(yy[0,20],5,5.6,lw=0.1)
	# plt.hlines(yy[0,50],5,5.6,lw=0.1)

	# plt.legend()

	# plt.grid()
	# plt.xlim(4,)
	# plt.ylim(2.75,3.75)
	# plt.ylim(4,6)

	# plt.twinx()
	# xx_tr = X[xx1:xx2]
	# nion_tr = np.mean(nion[ii,xx1:xx2,yy1:yy2],axis=1)
	# Ey_tr = np.mean(Ey[ii,xx1:xx2,yy1:yy2],axis=1)
	# Ex_tr = np.mean(Ex[ii,xx1:xx2,yy1:yy2],axis=1)

	# plt.plot(xx_tr,nion_tr/4,c='green',lw=4,label='np/4')
	# plt.plot(xx_tr,Ey_tr*4,c='red',lw=4,label='Ey*4')
	# plt.plot(xx_tr,Ex_tr,c='black',lw=4,label='Ex')
	# plt.legend()
	# plt.ylim(-20,20)
	# plt.xlim(5,5.6)

# plt.title(time[i])






# for num in range(90,91):

# 	fig,ax = plt.subplots(2,1)
# 	ax1 =ax[0]
# 	# ax1.plot(time,F_y_l[:,num],c='red',label=r"$-v_x \times B_z$",lw=2)
# 	# ax1.plot(time,F_y_e[:,num],c='blue',label=r'$E_y$',lw=2)
# 	# ax1.plot(time,F_y_e[:,num]+F_y_l[:,num],c='black',label=r'$F$',lw=2,ls='--',alpha=0.5)

# 	# ax1.plot(time,F_y[:,num]+F_ey[:,num],c='red',label='F_y',lw=2)
# 	ax1.plot(time,Bz[:,num],c='red',label='Bz',lw=2)
# 	ax1.plot(time,Ey[:,num],c='blue',label='Ey',lw=2)
# 	ax1.plot(time,(Bz[:,num]+Ey[:,num])/2,label='E',lw=2,color='black')
# 	ax1.set_xlim(5,20)
# 	# ax1.set_ylim(-15,15)
# 	ax1.set_xticklabels('')
# 	ax1.set_ylabel('Force',fontdict=font)
# 	ax1.legend(loc='best',prop=font1)
# 	# plt.grid()

# 	ax2 = ax[1]
# 	# ax2.plot(time,gamma[:,num],c='black',label='vx',lw=2)
# 	ax2.plot(time,vy[:,num],c='orange',label='vy',lw=2)
# 	# ax2.plot(time,vx[:,num],c='black',label='vx',lw=2)
# 	ax3 = ax2.twinx()

# 	ax3.plot(time,(yy[:,num]-yy[0,num]),c='green',label='x',lw=2)
# 	print("num",num)
# 	print("y_intial",yy[0,num])
# 	print("y_final",yy[-1,num])
# 	print("y_delta",yy[-1,num]-yy[0,num])
# 	ax2.text(10,0.0005,str(yy[-1,num])+'-'+str(yy[0,num]))
# 	ax2.set_xlim(5,20)
# 	ax2.set_ylim(-0.001,0.001)
# 	ax3.set_ylim(-0.001,0.001)
# 	ax2.set_xlabel('t [T]',fontdict=font)
# 	ax2.set_ylabel(r'$v_y$ [c]',fontdict=font)
# 	ax3.set_ylabel(r'$\delta y$ [um]',fontdict=font)


# 	plt.savefig(Img_dir+'track_EyBz'+'%04d'%num+'.png')
# 	plt.close('all')


















