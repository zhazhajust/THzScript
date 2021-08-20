#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N FinalEff
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

#list=(MassLimit/new_a3_w9.1_n0.2/y50x300)
list=(MassLimit/new_a3_w9.1_n0.2/y20x300 MassLimit/new_a3_w9.1_n0.2/y40x300 MassLimit/new_a3_w9.1_n0.2/y50x300 MassLimit/new_a3_w9.1_n0.2/y10x300 MassLimit/new_a3_w9.1_n0.2/y7x300 MassLimit/new_a3_w9.1_n0.2/y2x300 MassLimit/new_a3_w9.1_n0.2/y4x300 MassLimit/new_a3_w9.1_n0.2/y5x300 MassLimit/new_a3_w9.1_n0.2/y3x700 MassLimit/new_a3_w9.1_n0.2/y3x500 MassLimit/new_a3_w9.1_n0.2/y3x300 MassLimit/new_a3_w9.1_n0.2/y3x200 MassLimit/new_a3_w9.1_n0.2/y3x100 MassLimit/new_a3_w9.1_n0.2/y3x50)

R=250e-6


for i in ${list[@]};
    do
        python getTimeSequence.py $i $R #$x #$y
        python EffFinal.py $i $R
        python plotFinalTHz.py $i $R
    done

