#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N test
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script
#python gifEz2color.py 2color/a2_w50_t100/n10e22_T10
python plotTracer2.py MassLimit/tracer/y20x50 

python plotTracer2.py MassLimit/tracer/y20x150

python plotTracer2.py MassLimit/tracer/y20x400

