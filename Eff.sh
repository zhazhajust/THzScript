#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N CircleEff
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

#list=(MassLimit/New/y600x250 MassLimit/New/y300x250 MassLimit/New/y100x250)
#i='MassLimit/new_a3_w9.1_n0.2/y50x300'
#list=(MassLimit/new_a3_w9.1_n0.2/y20x300 MassLimit/new_a3_w9.1_n0.2/y40x300 MassLimit/new_a3_w9.1_n0.2/y50x300 MassLimit/new_a3_w9.1_n0.2/y10x300 MassLimit/new_a3_w9.1_n0.2/y7x300 MassLimit/new_a3_w9.1_n0.2/y2x300 MassLimit/new_a3_w9.1_n0.2/y4x300 MassLimit/new_a3_w9.1_n0.2/y5x300 MassLimit/new_a3_w9.1_n0.2/y3x700 MassLimit/new_a3_w9.1_n0.2/y3x500 MassLimit/new_a3_w9.1_n0.2/y3x300 MassLimit/new_a3_w9.1_n0.2/y3x200 MassLimit/new_a3_w9.1_n0.2/y3x100 MassLimit/new_a3_w9.1_n0.2/y3x50)
#list=(MassLimit/tracer/y20x250)
#list=(MassLimit/tracer/y30x250 MassLimit/tracer/y50x250 MassLimit/tracer/y10x250 MassLimit/tracer/y120x250)
#list=(MassLimit/tracer/y20x250 MassLimit/tracer/y50x250)

#list=(MassLimit/tracer/theta30/y10x250)
#list=(Data/MassLimit/tracer/y3x250 Data/MassLimit/tracer/y5x250 Data/MassLimit/tracer/y7x250)
#list=(MassLimit/tracer/y3x250 MassLimit/tracer/y5x250 MassLimit/tracer/y7x250)
#list=(MassLimit/tracer/y10x250 MassLimit/tracer/y30x250 MassLimit/tracer/y50x250 MassLimit/tracer/y3x250 MassLimit/tracer/y5x250 MassLimit/tracer/y7x250)


#list=(MassLimit/tracer/y20x50 MassLimit/tracer/y20x150 MassLimit/tracer/y20x250 MassLimit/tracer/y20x400 MassLimit/tracer/y20x50 MassLimit/tracer/y20x150 MassLimit/tracer/y20x250 MassLimit/tracer/y20x400)
#list=(MassLimit/tracerNew/y5x250 MassLimit/tracerNew/y10x250 MassLimit/tracerNew/y30x250 MassLimit/tracerNew/y50x250 MassLimit/tracerNew/y5x250 MassLimit/tracerNew/y10x250 MassLimit/tracerNew/y30x250 MassLimit/tracerNew/y50x250)
#list=(MassLimit/tracer/y20x600 MassLimit/tracer/y20x800)
#list=(MassLimit/tracerNew/y20x800 MassLimit/tracerNew/y20x1200 MassLimit/tracerNew/y20x1600)
list=(MassLimit/tracer/y20x600 MassLimit/tracer/y20x800 MassLimit/tracer/y20x1000)

#list=(MassLimit/tracer/n0.1 MassLimit/tracer/n0.3 MassLimit/tracer/n0.4)

R=(620e-6 820e-6 1010e-6)
x=(-450e-6 -650e-6 -850e-6)

#R=150e-6
#x=150e-6

for i in $(seq 0 ${#list[@]}); do

        echo ${list[$i]}
        echo ${R[$i]}
        echo ${x[$i]}
        python initialEnerge.py ${list[$i]} ${R[$i]} ${x[$i]} 0
        python EffCircle.py ${list[$i]} ${R[$i]} ${x[$i]} 0

#e=${variable[$i]}


done

