#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N python2
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script
#list=(45TW_new2/a2.5_w20/n0.25_half 45TW_new2/a2.5_w20/n0.45_half 45TW_new2/a2.5_w20/n0.7_half 45TW_new2/a2.5_w20/n1_half)
list=(45TW_new2/a2.5_w20/n0.3_half 45TW_new2/a2.5_w20/n0.4_half 45TW_new2/a2.5_w20/n0.5_half)
for i in ${list[@]};
        do
                python test_eff_bz.py $i
                python test_eff_ey.py $i
                #python gif_bz.py $i
        done


for i in ${list[@]};
        do
		python baktxt.py $i
	done
for i in ${list[@]};
        do
		python extract_from_bak.py $i
        done

for i in ${list[@]};
        do
                #python fft.py $i
                #python draw_freqs.py $i
                #python draw_xt.py $i

        done

