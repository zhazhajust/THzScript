#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N ProcessFigEff2
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

#list=(MassLimit/new_a3_w9.1_n0.2/y50x300)
list=(MassLimit/new_a3_w9.1_n0.2/y100x200)


x=218e-6
y=0
R=150e-6

for i in ${list[@]};
        do
                python gifTHzPlot.py $i
                python Eff.py $i
                python gifElectron.py $i
                python gifKpolar.py $i 218e-6
                python EffAll.py $i
                #python getTimeSequence.py $i $R $x $y ########no move window
                #python EffFinal.py $i $R
                #python plotFinalTHz.py $i $R
        done

