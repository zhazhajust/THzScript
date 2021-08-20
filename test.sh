#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N test
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script
#python gifEz2color.py 2color/a2_w50_t100/n10e22_T10


python plotTracer3.py MassLimit/a3New/y40x1000

python plotTracer3.py MassLimit/a3New/y60x1000
#MassLimit/tracer/y20x1200new

#python plotTracer2.py MassLimit/tracerOld/y30x250

#python plotTracer2.py MassLimit/tracerOld/y50x250


#python plotTracer2.py MassLimit/tracerOld/a0.5y30

#python plotTracer2.py MassLimit/tracerOld/a1y30

#python plotTracer2.py MassLimit/tracerOld/a5y30


#python plotTracer2.py MassLimit/tracerNew/y30x250

#python plotTracer2.py MassLimit/tracerNew/y50x250


#python plotTracer2.py MassLimit/tracerNew/y20x50

#python plotTracer2.py MassLimit/tracerNew/y20x150

#python plotTracer2.py MassLimit/tracerNew/y20x250

#python plotTracer2.py MassLimit/tracerNew/y20x400
