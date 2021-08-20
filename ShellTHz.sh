#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N ShellTHz
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

#list=(MassLimit/new_a3_w9.1_n0.2/y50x300)
#list=(MassLimit/new_a3_w9.1_n0.2/y20x300 MassLimit/new_a3_w9.1_n0.2/y40x300 MassLimit/new_a3_w9.1_n0.2/y50x300 MassLimit/new_a3_w9.1_n0.2/y10x300 MassLimit/new_a3_w9.1_n0.2/y7x300 MassLimit/new_a3_w9.1_n0.2/y2x300 MassLimit/new_a3_w9.1_n0.2/y4x300 MassLimit/new_a3_w9.1_n0.2/y5x300 MassLimit/new_a3_w9.1_n0.2/y3x700 MassLimit/new_a3_w9.1_n0.2/y3x500 MassLimit/new_a3_w9.1_n0.2/y3x300 MassLimit/new_a3_w9.1_n0.2/y3x200 MassLimit/new_a3_w9.1_n0.2/y3x100 MassLimit/new_a3_w9.1_n0.2/y3x50)
#list=(MassLimit/New/y600x250 MassLimit/New/y300x250 MassLimit/New/y100x250)
#list=(MassLimit/tracer/y20x250 MassLimit/tracer/y50x250)
#list=(MassLimit/tracer/y30x250 MassLimit/tracer/y20x250 MassLimit/tracer/y50x250 MassLimit/tracer/y10x250 MassLimit/tracer/y120x250)
#list=(MassLimit/tracer/theta30/y10x250)
#list=(MassLimit/tracer/y3x250 MassLimit/tracer/y5x250 MassLimit/tracer/y7x250)
#list=(MassLimit/tracerstatic/y3x250  MassLimit/tracerstatic/y5x250 MassLimit/tracerstatic/y7x250)
#list=(MassLimit/tracerNew/y5x250 MassLimit/tracerNew/y10x250 MassLimit/tracerNew/y30x250 MassLimit/tracerNew/y50x250 MassLimit/tracer/y3x250 MassLimit/tracer/y5x250 MassLimit/tracer/y7x250 MassLimit/tracer/y10x250 MassLimit/tracer/y20x250 MassLimit/tracer/y30x250 MassLimit/tracer/y50x250 MassLimit/tracer/y100x250 MassLimit/tracer/y120x250)
#list=(MassLimit/tracer/y20x600 MassLimit/tracer/y20x800)
#list=(MassLimit/a1 MassLimit/a0.7)
#list=(MassLimit/tracer/y20x30 MassLimit/tracer/y20x50new MassLimit/tracer/y20x100 MassLimit/tracer/y20x75)
list=(MassLimit/tracer/y20x250new)
R=150e-6

echo $R

for i in ${list[@]};
        do
                python gifTHzPlot.py $i
                python Eff.py $i
                python gifElectron.py $i

                #python gifKpolar.py $i #x
                #python EffAll.py $i


                #python getTimeSequence.py $i $R  #$x #$y
                #python EffFinal.py $i $R
                #python plotFinalTHz.py $i $R
        done

#for i in ${list[@]};
#    do
#        python getTimeSequence.py $i $R #$x #$y
#        python EffFinal.py $i $R
#        python plotFinalTHz.py $i $R
#    done

