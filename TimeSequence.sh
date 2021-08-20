#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N sequence
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

list=(MassLimit/new_a3_w9.1_n0.2/y50x300)
for i in ${list[@]};
        do
                python getTimeSequence.py $i > sequence.out
        done

