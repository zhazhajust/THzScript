#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N Ey
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

list=(45TW_new2/a2.6_w22.2/n0.14_spot0_1000 45TW_new2/a2.6_w22.2/n0.3_spot0_1000 45TW_new2/a2.6_w22.2/n0.5_spot0_1000)
#MassLimit/a2.6_w22.2/y20x300 MassLimit/a2.6_w22.2/y20x100 MassLimit/a10_w6/y6x100 MassLimit/new_a3_w9.1_n0.2/y3x50 MassLimit/new_a3_w9.1_n0.2/y3x100 MassLimit/new_a3_w9.1_n0.2/y3x200 MassLimit/new_a3_w9.1_n0.2/y3x300 MassLimit/new_a3_w9.1_n0.2/y3x500 MassLimit/new_a3_w9.1_n0.2/y3x700 MassLimit/new_a3_w9.1_n0.2/y2x300 MassLimit/new_a3_w9.1_n0.2/y5x300 MassLimit/new_a3_w9.1_n0)
for i in ${list[@]};
    do
        python AllKpolar.py $i > gif.out
    done

#python gifKpolar.py MassLimit/new_a3_w9.1_n0.2/y3x300
