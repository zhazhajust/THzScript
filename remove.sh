#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N bak_and_remove
#PBS -o $N.out
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script

#list=(45TW_new2/a2.5_w20/n0.2_half     45TW_new2/a2.5_w20/n0.5_half     45TW_new2/a2.5_w20/n0.4_half     45TW_new2/a2.5_w20/n0.3_half     45TW_new2/a2.5_w20/n0.6_half     45TW_new2/a2.5_w20/n0.25_half     45TW_new2/a2.5_w20/n0.35_half     45TW_new2/a2.5_w20/n0.45_half     45TW_new2/a2.5_w20/n1_half     45TW_new2/a2.5_w20/n0.7_half     45TW_new2/a2.5_w20/n0.55_half     45TW_new2/a2.5_w20/n0.3_dump1100     45TW_new2/a2.5_w20/n0.3_dump1200     45TW_new2/a2.5_w20/n0.3_spot500     45TW_new2/a2.5_w20/n0.3_spot1500)

#list=(45TW_new2/a2.6_w22.2/n0.14_plane 45TW_new2/a2.6_w22.2/n0.115_plane 45TW_new2/a2.6_w22.2/n0.075_plane 45TW_new2/a2.6_w22.2/n0.14_sharp 45TW_new2/a2.6_w22.2/n0.115_sharp 45TW_new2/a2.6_w22.2/n0.075_sharp 45TW_new2/a2.6_w22.2/n0.035_sharp)
list=(45TW_new2/a1.44_w40/n0.14_guass 45TW_new2/a2.6_w22.2/n0.3_theta8000)
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
                python fft.py $i
                python draw_freqs.py $i
                python draw_xt.py $i
		python remove.py $i
        done

