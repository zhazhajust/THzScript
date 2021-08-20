import sys
from Processing import *
from clib.addTimeSequence import addFieldTheta

##########
##########
#########
point = [318e-6,0]
#global R 
R = 250e-6
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
savedir = const.txtdir +'Start'+ 'TimeSequence.npy'
##########
def PoolMap(thread,point,R):#,args):
    results = 0
    with SharedMemoryManager() as smm:
        '''
        sl = []
        #for arg in args:
        #    shm = shared_memory.SharedMemory(create=True, size=arg.nbytes)
        #    arg_shm = np.ndarray(arg.shape, dtype=arg.dtype, buffer=shm.buf)
        #    arg_shm[:] = arg[:]
        #    #print(arg)
            #sl.append(smm.ShareableList(name = arg.shm.name))
            #a = shared_memory.ShareableList(arg)
        #    sl.append(shm.name)

        #sl = smm.ShareableList(range(2000))
        # Divide the work among two processes, storing partial results in sl

        pool = multiprocessing.Pool(processes=96)   #,initargs=(ss1,ss2))
        #MapList = range(const.stop+const.step)
        MapList = range(10)
        results = pool.map(func,MapList,args = (point,R))
        pool.close()
        pool.join()
        '''

        #input_file = np.zeros(3000, dtype=np.intc)

        pool = multiprocessing.Pool()
        tasks = []

        try:
            start = int(const.window_stop_time/const.dt_snapshot)
        except:
            start = 1
        #MapList = range(start,const.stop+const.step,const.step)
        
        #Time = np.array(MapList) * const.dt_snapshot

        Time = np.arange(0,18e-6/3e8,const.dt_snapshot)

        MapList = np.arange(0,int(Time[-1]/const.dt_snapshot)+1)

        np.save(const.txtdir + 'Sequencetime.npy',Time)
        #MapList = range(10)
        for i in MapList:
            task = pool.apply_async(thread, (i,point,R))
            tasks.append(task)

        pool.close()
        pool.join()
        results = []
        for task in tasks:
            results.append(task.get())
            #print(task.get())


        #total_result = sum(sl)  # Consolidate the partial results now in sl
    return results

def getThetaTField(t,point,R):
    #pool.map()
    print('Processing number:',t)
    data , title = getBz(t)
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
    TimeSequence = data[0,:]
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
