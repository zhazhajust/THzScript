# -- coding: utf-8 --
import os
import sys
import numpy as np
#case_name = ''
def getValue(x):
    try:
        x = eval(x)
    except:
        return
    return x


def sefDirName(DirName):
    case_name = DirName
case_name = 'MassLimit/tracer/y20x250new'#'MassLimit/new_a3_w9.1_n0.2/y50x300'#'45TW/new_a3_n0.29_half'#'MassLimit/new_a3_w9.1_n0.2/y10x300'

#constant
nperseg = 256
if len(sys.argv) > 1:
    case_name    = sys.argv[1]
data_name = case_name+"/"
#filenumber = 4
####
####
wkdir = os.path.abspath(os.path.join(os.getcwd(), ".."))
print(os.path.abspath(os.path.join(os.getcwd(), "..")))
epochdir = wkdir #'/home/yujq/users/caijie/epoch2d'

####
####

sdfdir  =  epochdir+"/Data/"+data_name
#sdfdir  =  "../Data/"+data_name
txtdir  =  epochdir+"/txt/"+data_name
figdir  =  epochdir+"/fig/"+data_name
gifdir  =  epochdir+"/gif/"+data_name
pngdir  =  epochdir+"/gif/png/"
####stop
a=os.listdir(sdfdir)
a=[i.split('.') for i in a]
loop=[i for i in a if i[1] == 'sdf']
loop=np.array(loop)
#loop=np.sort(loop)
loop=loop[:,0]
loop=np.sort(loop)

b=loop

start=1
stop=int(b[-1])
step=1
print(stop)
filenumber = len(str(b[-1]))

def checkdir():
    
    if (os.path.isdir(txtdir) == False):
            os.makedirs(txtdir,exist_ok = True)
    if (os.path.isdir(figdir) == False):
            os.makedirs(figdir,exist_ok = True)
    os.makedirs(gifdir,exist_ok = True)
    os.makedirs(pngdir,exist_ok = True)
checkdir()

######

fb=open(sdfdir+'deck.status','r')
www = fb.readlines()
#print(www)
#www = set(www)
ConstDict = www #{}
#for key,value in www:
#    if ConstDict.has_key(key):
#        continue    
#    ConstDict[key] = value 
ConstDict = [i.replace(' \tElement ','').replace(' handled OK\n','') for i in ConstDict]
ConstDict = [i.split('=') for i in ConstDict]
new_dict={}
for i in ConstDict:
    if len(i) == 2:
        if i[0] in new_dict:
            continue
        new_dict[i[0]] = i[1]
#del www
locals().update(new_dict)
#####
#####
name=case_name






######
######
micron=1e-6
c=3e8
femto=1e-15

Nx=eval(nx)
laser_lamada=eval(laser_lamada)

x_spot = eval(x_spot)
T0=eval(T0)
Ny=eval(ny)
#Nz=eval(nz)
y_min=eval(y_min)
y_max=eval(y_max)
x_min=eval(x_min)
x_max=eval(x_max)
#print(x_max,x_min)
print('x_spot',x_spot)
#x_spot= eval(x_spot)
x_length = eval(x_length)
x_right = eval(x_right)
print('RightTimeStart',(x_right - x_min) / c/1e-15)
#print('Nx',Nx)
#z_min=eval(z_min)
#z_max=eval(z_max)
dt_snapshot=eval(dt_snapshot)

#start_move_locate = getValue(start_move_locate)
#stop_move_locate = getValue(stop_move_locate)
#move_window = getValue(move_window)

#print('window_start_time',window_start_time)
#window_start_time=eval(window_start_time)


#print('window_start_time',window_start_time)
try:
    start_move_locate = eval(start_move_locate)
    stop_move_locate = eval(stop_move_locate)
except:
    pass
try:
    window_start_time = eval(window_start_time)
    window_stop_time = eval(window_stop_time)
except:
    pass
print('Time:',window_start_time,window_stop_time)
las_t_fwhm1=eval(las_t_fwhm1)


print('fwhm,dt:',las_t_fwhm1,dt_snapshot)
lamada=laser_lamada
########
####stop
#a=os.listdir(sdfdir)
#a=[i.split('.') for i in a]
#b=[i for i in a if i[1] == 'sdf']
#stop=int(b[-1][0])
#print(stop)
###
###
start   =  1
###
'''
c       =  3e8
micron  =  1e-6
lamada  =  10.6 * micron 
gridnumber = 1908
Ny      =  235
Nx      =  gridnumber
Nz      =  235

start   =  1
stop    =  4000
step    =  1
'''


dt      =  dt_snapshot*1e15      #fs
x_end   =  x_max - x_min 
x_lenth =  x_end
y_lenth =  y_max - y_min #lamada
#z_lenth =  z_max - z_min 
#print(window_start_time)
#window_start_time =  (x_max - x_min) / c
delta_x =  x_end/Nx
delta_y =  y_lenth/Ny
t_end   =  stop * dt_snapshot
x_interval=1
t_total=1e15*x_end/c         #fs
#print(t_total,dt_snapshot)
t_size=t_total/(dt_snapshot*1e15)+1+1           #t_grid_number
######t_size=int(1e15*gridnumber*delta_x/c)+1

if t_end-window_start_time<0:
      xgrid   =  int(Nx)
else:
      xgrid   =  int(Nx + c*(t_end-window_start_time)/delta_x)
#####fft freqs


