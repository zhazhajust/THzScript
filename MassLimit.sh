#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N python
#PBS -o $N.out
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script
python gifEyDenthz.py MassLimit/a10_w6
python gifEyDenthz.py MassLimit/a20_w3
