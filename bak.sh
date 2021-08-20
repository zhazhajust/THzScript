#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N baktxt
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
#list=(2color/a5.8_w50_t110/ez_a0.1 2color/a5.8_w50_t110/ex_n2.7e23)
#list=(2color/a2_w50_t100/ez_a0.1)
list=(2color/a3_w50_t100/ez_a0.1 2color/a2_w50_t100/ez_a0.5 2color/a2_w50_t100/ez_a0.1)


for i in ${list[@]};
        do
		python baktxt.py $i
	done

for i in ${list[@]};
        do
		python extractEz.py $i
                python fftEz.py $i
                python drawEzFreqs.py $i
                python drawEzXt.py $i
	done
