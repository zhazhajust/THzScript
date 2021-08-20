import sys
import Processing
from Processing import *
from clib.addTimeSequence import addFieldTheta
import constant as const
##########
##########
#########
#x_right = const.x_max/2
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
def PoolMap(thread,point,R):#,args):
    pool = multiprocessing.Pool()
    tasks = []
    try:
        start = int(const.window_stop_time/const.dt_snapshot)
        print('start',start)
    except:
        start = 1
    ###
    #start = 2499
    ###
    MapList = range(start,const.stop+const.step,const.step)
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

def getThetaTField(t,point,R):
    #pool.map()
    print('Processing number:',t)

    Field = Processing.Field
    if Field == 'Bz':
        data , title = getBz(t)
    if Field == 'Ey':
        data , title = getEy(t)
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
    TimeSequence = addFieldTheta(data,point,R)

    Mat = np.zeros(data.shape)
    for i in Mat:
        i * delta_x + const.x_min = x
        indexX = 
        indexY = (np.sqrt(R **2 - (x-x0)**2) + y0)/delta_y

        X**2 + Y ** 2 = R **2        

        
        Mat[indexX,indexY] = 1
    np.dot(data,Mat) 


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

    results = PoolMap(getThetaTField,point,R)#,args)

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
