#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N 2_col_Ey
#PBS -V
#PBS -q opt
cd /home/yujq/users/caijie/epoch2d/THz_script
#list=(45TW_new2/a2.6_w22.2/n0.14_plane 45TW_new2/a2.6_w22.2/n0.115_plane 45TW_new2/a2.6_w22.2/n0.075_plane 45TW_new2/a2.6_w22.2/n0.14_sharp 45TW_new2/a2.6_w22.2/n0.115_sharp 45TW_new2/a2.6_w22.2/n0.075_sharp 45TW_new2/a2.6_w22.2/n0.035_sharp)
#list=(45TW_new2/a1.44_w40/n0.14_guass)
#list=(45TW_new2/a1.44_w40/n0.14_plane 45TW_new2/a2.6_w22.2/n0.035_plane 45TW_new2/a1.44_w40/n0.005_plane)
#list=(45TW_new2/a2.6_w22.2/n0.14_spot0_650 45TW_new2/a2.6_w22.2/n0.14_spot0 45TW_new2/a2.6_w22.2/n0.14_spot600_1400 45TW_new2/a2.6_w22.2/n0.14_spot0_1500 45TW_new2/a2.6_w22.2/n0.14_spot0_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_1200)
#list=(45TW_new2/a2.6_w22.2/n0.075_spot0_1000 45TW_new2/a2.6_w22.2/n0.115_spot0_1000)
#list=(45TW_new2/a2.6_w22.2/n0.115_spot0_1500 45TW_new2/a2.6_w22.2/n0.075_spot0_1500)
#list=(45TW_new2/a2.6_w22.2/n0.14_spot600_1000 45TW_new2/a2.6_w22.2/n0.14_spot300_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_1000)


#list=(45TW_new2/a2.6_w22.2/n0.14_spot-300_1000 45TW_new2/a2.6_w22.2/n0.14_spot-600_1000)
#list=(45TW_new2/a2.6_w22.2/n0.3_spot0_1000 45TW_new2/a2.6_w22.2/n0.5_spot0_1000)
#list=('2color/a5.8_w50_t110/n2.7e23' '2color/a2_w100_t160/test')
#list=(2color/a5.8_w50_t110/new_n2.7e23 2color/a5.8_w50_t110/ex_n2.7e23 2color/a5.8_w50_t110/4T0_n2.7e23)
#list=(2color/a2_w100_t160/ey_a0.5 MassLimit/a2.6_w22.2/y20_x30)
list=(MassLimit/a10_w6 MassLimit/a20_w3)
for i in ${list[@]};
        do
                #python test_eff_bz.py $i
                #python test_eff_ey.py $i
		#python eff_2d_ez.py $i
		python eff_2d_ey.py $i
                #python gif_bz.py $i
		#python gifEzthz.py $i
		python gifEy2color.py $i
		python gifKOfEy.py $i
		python gifDensity.py $i
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

        done

