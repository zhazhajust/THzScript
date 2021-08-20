import sys
import Processing
from Processing import *
from clib.addTimeSequence import addFieldTheta
import constant as const
##########
##########
#########
#x_right = const.x_max/2
NTheta = 2 * const.Ny
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
savedir = const.txtdir  + 'x' + str(int(point[0]/1e-6)) + 'um' + str(int(R/1e-6)) + 'um'+ 'TimeSequence.npy'
##########
def PoolMap(thread,point,R):#,args):
    pool = multiprocessing.Pool()
    tasks = []
    #try:
    #    start = int(const.window_stop_time/const.dt_snapshot)
    #    print('start',start)
    #except:
    start = 1
    ###
    #start = 2499
    ###
    stop = const.stop
    #stop = 666
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

def plotCircle():
    x0 = point[0]
    y0 = point[1]
    maxY = (const.y_max - const.y_min)/2
    if R > maxY:
        thetaMax = np.arcsin(maxY/R)
    else:
        thetaMax = pi
    theta = np.linspace(- thetaMax,thetaMax,NTheta)
    x = (x0 + R*np.cos(theta))/delta_x
    y = (y0 + R*np.sin(theta))/delta_y
    plt.plot(x,y)
    savedir = const.figdir
    plt.savefig(savedir + 'circle.jpg',dpi=160)

if __name__ == '__main__':
    #point = [318e-6,0]
    #R = 200e-6
    #if len(sys.argv) > 3:
    #    x = float(sys.argv[2])
    #    y = float(sys.argv[3])
    #    point = [x,y]
    #    R = float(sys.argv[4])
    plotCircle()
    data = TimeSequence(point,R)
    data = np.array(data)
    np.save(savedir,data)
