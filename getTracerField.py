#import numpy as np
#cimport numpy as np

#cdef double[:, :] ProcessTracerField(double[:, :] Ex, double[:, :] Ey, double[:] X, double[:] Y):

import numpy as np
import constant as const
######
delta_x = const.delta_x
delta_y = const.delta_y
pi = 3.1415926

######
def MoveData(Ex,Ey,X,Y):
    #Field = np.zeros((2, len(X)))
    TracerField = np.zeros((2, len(X)))
    # cdef double[:] TracerEy = np.zeros(len(X))
    for i, x, y in zip(np.arange(len(X)), X, Y):
        indexX = int(round((x - const.x_min - const.delta_x/2)/const.delta_x))
        indexY = int(round((y - const.y_min - const.delta_y/2)/const.delta_y))
        try:
            TracerField[0, i] = Ex[indexX, indexY]
            TracerField[1, i] = Ey[indexX, indexY]
        except:
            print('deltax,y',const.delta_x,const.delta_y)
            print('x,indexX:',x,indexX)
            print('y,indexY:',y,indexY)
    return TracerField

def getTracerField(Ex, Ey, X, Y):
    Ex = np.array(Ex)
    Ey = np.array(Ey)
    X = np.array(X)
    Y = np.array(Y)
    TracerField = MoveData(Ex, Ey, X, Y)
    TracerField = np.array(TracerField)
    TracerEx = TracerField[0, :]
    TracerEy = TracerField[1, :]

    return TracerEx, TracerEy

