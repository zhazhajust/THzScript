#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N testEff
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
list=(MassLimit/tracer/y100x250 MassLimit/tracer/y10x250 MassLimit/tracer/y30x250 MassLimit/tracer/y50x250 MassLimit/tracer/y3x250 MassLimit/tracer/y5x250 MassLimit/tracer/y7x250)
#list=(MassLimit/tracer/y20x50 MassLimit/tracer/y20x150 MassLimit/tracer/y20x250 MassLimit/tracer/y20x400)

R1=430e-6
x1=-150e-6

R2=350e-6
x2=100e-6

for i in ${list[@]};
    do
        #python getTimeSequence.py $i 50e-6  #$x #$y

        #python getTimeSequence.py $i 350e-6 -150e-6 0 

        python getCircle.py $i $R1 $x1 0
        #python getTimeSequence.py $i 140e-6

        #python EffFinal.py $i 60e-6

        python EffCircle.py $i $R1 $x1 0 

        #python EffFinal.py $i 140e-6

        #python plotFinalTHz.py $i 60e-6

        python plotCircle.py $i $R1 $x1 0 

        #python plotFinalTHz.py $i 140e-6

        python getCircle.py $i $R2 $x2 0
        #python getTimeSequence.py $i 140e-6

        #python EffFinal.py $i 60e-6

        python EffCircle.py $i $R2 $x2 0

        #python EffFinal.py $i 140e-6

        #python plotFinalTHz.py $i 60e-6

        #python plotFinalTHz.py $i 200e-6 100e-6 0

        python plotCircle.py $i $R2 $x2 0

    done
