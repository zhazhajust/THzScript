# coding=utf-8
import time
import sys
import Processing
from Processing import *
from clib.addTimeSequence import addFieldTheta
import constant as const
##########
##########
#########
#x_right = const.x_max/2
#if const.move_window == T:
try:
    x_right = const.start_move_locate
    print('x_right = const.start_move_locate')
except:
    x_right = const.x_max/2
    print('x_right = const.x_max/2')
point = [x_right,0]
#global R 
R = 150e-6
##########
if len(sys.argv) > 2:
    R = float(sys.argv[2])

if len(sys.argv) > 3:
    x = float(sys.argv[3])
    y = float(sys.argv[4])
    point = [x,y]
    #R = float(sys.argv[4])
###########
##########
savedir = const.txtdir + 'x' + str(int(point[0]/1e-6)) + 'um' + str(int(R/1e-6)) + 'um'+ 'TimeSequence.npy'
##########
def timeit(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        end_time = time.time()
        print("%s函数运行时间为：%.8f" %(f.__name__, end_time - start_time))
        return res
    return wrapper  



##########
def PoolMap(thread,point,R):#,args):
    pool = multiprocessing.Pool()
    tasks = []
    if const.move_window == 'T':
        try:
            start = int(const.window_stop_time/const.dt_snapshot)
            print('start',start)
        except:
            pass
    else:
        start = 1
    ###
    stop = const.stop
    #start = 300
    #stop = 1000
    ###
    MapList = range(start,stop+const.step,const.step)
    #MapList = [2499]
    Time = np.array(MapList) * const.dt_snapshot
    np.save(const.txtdir + 'Sequencetime.npy',Time)
    for i in MapList:
        task = pool.apply_async(thread, (i,point,R))
        tasks.append(task)
    pool.close()
    pool.join()
    results = []
    for task in tasks:
        results.append(task.get())
    return results

@njit
def getCircle(data,point,R):
    x0 = point[0]
    y0 = point[1]
    
    #Mat = np.zeros(data.shape)
    result = np.zeros(data.shape[1])

    iterateY = np.arange(data.shape[1])

    #y = indexY * const.delta_y + const.y_min - y0 < R

    iterateY = iterateY[np.abs(iterateY * const.delta_y + const.y_min - y0) < R ]
    for indexY in range(data.shape[1]):
        indexY = int(indexY)
        y = indexY * const.delta_y + (const.y_min + const.delta_y/2)
        indexX = round((np.sqrt(R **2 - (y-y0)**2) + x0)/delta_x)
        #indexY = (np.sqrt(R **2 - (x-x0)**2) + y0)/delta_y
        #X**2 + Y ** 2 = R **2        
        #Mat[indexX,indexY] = 1
        if indexX * const.delta_x > const.x_min and indexX * const.delta_x < const.x_max:
            result[indexY] = data[indexX,indexY]

    #result = np.dot(data,Mat)
    return result

def getInterpData(data,point,R):
    x0 = point[0]
    y0 = point[1]
    dl = 1e-6
    dtheta = int(dl/R)
    theta = np.linspace(-pi/2,pi/2,dtheta)
    x = R * np.cos(theta) + x0
    y = R * np.sin(theta) + y0

    Y,X = np.meshgrid(np.linspace(-const.y_min,const.y_max,const.Ny),np.linspace(-const.x_min,const.x_max,const.Nx))

    points = np.stack([X.flatten(),Y.flatten()],axis = -1)
    InterpData = griddata(points,data.flatten(),(x,y),method = 'cubic')

    return theta , InterpData

def getThetaTField(t,point,R):
    #pool.map()
    print('Processing number:',t)

    Field = Processing.Field
    if Field == 'Bz':
        data , title = timeit(getBz)(t)
    if Field == 'Ey':
        data , title = timeit(getEy)(t)
    data = np.array(data)
    #####
    #point = [318e-6,0]
    #R = 200e-6
    point = np.array(point)
    ####
    #theta = np.arange(-90,91)
    #x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    #x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    #TimeSequence = addFieldTheta(data)#,TimeSequence)
    
    #TimeSequence = addFieldTheta(data,point,R)

    '''
    Mat = np.zeros(data.shape)
    for indexY in Mat.shape[1]:
        y = indexY * const.delta_y + const.y_min
        indexX = (np.sqrt(R **2 - (y-y0)**2) + x0)/delta_x
        #indexY = (np.sqrt(R **2 - (x-x0)**2) + y0)/delta_y
        #X**2 + Y ** 2 = R **2        
        Mat[indexX,indexY] = 1
    '''
    #result = np.dot(data,Mat) 
    #getCircleWrapper = timeit(getCircle)

    getCircleWrapper = timeit(getInterpData)
    theta , TimeSequence = getCircleWrapper(data,point,R)

    #TimeSequence = getCircle(data,point,R)    
    del data
    #TimeSequence = timeit(getCircle(data,point,R))

    return TimeSequence

def TimeSequence(point,R):
    #theta = np.arange(-90,91)
    #x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    #x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    #print(x,y)
    #stop = const.stop
    #step = 1
    #t = stop + step
    #TimeSequence= np.zeros((t,theta.shape[0]))
    #theta = np.arange(-90,91)
    #x,y = point[0] + R*np.cos(theta) , point[1] + R*np.sin(theta)
    #x ,y = x/delta_x,(y - (const.y_min+delta_y/2))/delta_y
    #args = [theta.shm.name,x.shm.name,y.shm.name]

    #results = PoolMap(getThetaTField,point,R)#,args)
    
    results = []
    if const.move_window == 'T':
        try:
            start = int(const.window_stop_time/const.dt_snapshot)
            print('start',start)
        except:
            pass
    else:
        start = 1
    stop = const.stop
    step = const.step
    for n in range(start,stop+step,step):
        results.append(getThetaTField(n,point,R))
    
    
    return results

if __name__ == '__main__':
    #point = [318e-6,0]
    #R = 200e-6
    #if len(sys.argv) > 3:
    #    x = float(sys.argv[2])
    #    y = float(sys.argv[3])
    #    point = [x,y]
    #    R = float(sys.argv[4])

    data = TimeSequence(point,R)
    data = np.array(data)
    np.save(savedir,data)
