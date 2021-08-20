#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N Ey
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
#list=(MassLimit/a10_w6 MassLimit/a20_w3)
#list=(cascade/a2_w50_t110/n5e25_n10e22)
#list=(cascade/a2_w50_t110/guass_n1e25_n10e22)
#list=(MassLimit/a0.38_T17.5fs/x100y60)
#list=(MassLimit/a10_w6/y6x30 MassLimit/a10_w6/y6x100)
#list=(MassLimit/a2.6_w22.2/y20x100 MassLimit/a2.6_w22.2/y20x300)
#list=(deceleration/10.6um/a2_n1_T2ps_w100)
#list=(deceleration/3.9um/a1.1_T90_w12/n10e22 deceleration/3.9um/a1.1_T90_w12/n7e23)
#list=(deceleration/3.9um/a2_T90_w8/n7e23)
#list=(deceleration/3.9um/a2_T90_w24/n7e23)
#list=(deceleration/10.6um/a2_n1_w8_T5 deceleration/10.6um/a2_n1_w7_T6 deceleration/10.6um/a2_n1_w7_T5)
#list=(deceleration/10.6um/a2_2ps_w120)
list=(MassLimit/solidTarget)
for i in ${list[@]};
    do
        python test_eff_bz.py $i
        #python test_eff_ey.py $i
		#python eff_2d_ez.py $i
		python eff_2d_ey.py $i
        #python gif_bz.py $i
		python gifEyDensity.py $i
		#python gifEzthz.py $i
		#python gifEythz.py $i
		#python gifKOfEy.py $i
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

