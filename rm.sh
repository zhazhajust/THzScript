#!/bin/bash
#PBS -l walltime=999:00:00
#PBS -l nodes=1:ppn=96
#PBS -N remove
#PBS -V
#PBS -q opt

#list=(test     test2     45tw_0.25     45tw_0.28_spot1     test_subset     a2_n1_T6_w8     a2_n1_T6_w10     a2_n1.5     a2_n2     a2_n1_T14     a2_n1_T20     a2_n1_w6     a2_n0.45     a2_n4.5     a2_n0.7     a2_n3     a4_n1     a2_n1_T6     a2_n1     new_a2_n0.7     a2_n1_w7     a2_n1_w8     a2_n1_w10     a2_n1_w16     a2_n1_w5     a2_n1_T2     a2_n1_T4     12um_a2_n1_T6_w8     a1_n1     2_color_test     2_color_test2     fangda     half_45TW     infra     ion_acceleration/3     ion_acceleration/5     masslimit     mass_limit     mass_limit2     amp_infra     mass_limit_a0_20     45TW_1500um_n0.28_half     2color     Infra     45TW/a0_3     45TW/a0_1.5     45TW/a3_n0.29_half     45TW/a3_n0.3_guass_spot2     45TW/a3_n0.2_guass_spot2     45TW/a3_n0.28_guass_spot2     45TW/a1.5_w14.3/45TW_n0.1     45TW/a1.5_w14.3/45TW_n0.15     45TW/a1.5_w14.3/45TW_n0.25     45TW/a1.5_w14.3/45TW_n0.2     45TW/a1.5_w14.3/45TW_n0.28     45TW/a1.5_w14.3/45TW_n0.3     45TW/a1.5_w14.3/45TW_n0.5     45TW_new/a3_n0.28_half     45TW_new/a3_w7.17/n0.28_half)

#list=(45TW_new2/a2.6_w22.2/n0.14_plane 45TW_new2/a2.6_w22.2/n0.115_plane 45TW_new2/a2.6_w22.2/n0.075_plane 45TW_new2/a2.6_w22.2/n0.14_sharp 45TW_new2/a2.6_w22.2/n0.115_sharp 45TW_new2/a2.6_w22.2/n0.075_sharp 45TW_new2/a2.6_w22.2/n0.035_sharp)

#list=(45TW_new2/a1.44_w40/n0.14_guass)

#list=(45TW_new2/a1.44_w40/n0.14_plane 45TW_new2/a2.6_w22.2/n0.035_plane 45TW_new2/a1.44_w40/n0.005_plane 45TW_new2/a1.44_w40/n0.14_guass 45TW_new2/a2.6_w22.2/n0.14_spot0_650 45TW_new2/a2.6_w22.2/n0.14_spot0 45TW_new2/a2.6_w22.2/n0.14_spot600_1400 45TW_new2/a2.6_w22.2/n0.14_spot0_1500 45TW_new2/a2.6_w22.2/n0.14_spot0_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_1200 45TW_new2/a2.6_w22.2/n0.075_spot0_1000 45TW_new2/a2.6_w22.2/n0.115_spot0_1000 45TW_new2/a2.6_w22.2/n0.115_spot0_1500 45TW_new2/a2.6_w22.2/n0.075_spot0_1500 45TW_new2/a2.6_w22.2/n0.14_spot600_1000 45TW_new2/a2.6_w22.2/n0.14_spot300_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_1000 45TW_new2/a2.6_w22.2/n0.14_spot-300_1000 45TW_new2/a2.6_w22.2/n0.14_spot-600_1000 45TW_new2/a2.6_w22.2/n0.3_spot0_1000 45TW_new2/a2.6_w22.2/n0.5_spot0_1000)
#list=('2color/a5.8_w50_t110/n2.7e23' '2color/a2_w100_t160/test' 2color/a5.8_w50_t110/new_n2.7e23 2color/a5.8_w50_t110/ex_n2.7e23 2color/a5.8_w50_t110/4T0_n2.7e23)
#list=(45TW_new2/a1.44_w40/n0.0035_plane 45TW_new2/a1.44_w40/n0.005_plane 45TW_new2/a1.44_w40/n0.14_guass 45TW_new2/a1.44_w40/n0.14_plane 45TW_new2/a2.6_w22.2/n0.14_spot1000_1000 45TW_new2/a2.6_w22.2/n0.5_spot0_1000 45TW_new2/a2.6_w22.2/n0.3_spot0_1000 45TW_new2/a2.6_w22.2/n0.14_spot-600_1000 45TW_new2/a2.6_w22.2/n0.14_spot-300_1000 45TW_new2/a2.6_w22.2/n0.075_spot0_1500 45TW_new2/a2.6_w22.2/n0.115_spot0_2000 45TW_new2/a2.6_w22.2/n0.75_spot0_2000 45TW_new2/a2.6_w22.2/n0.115_spot0_1500 45TW_new2/a2.6_w22.2/n0.115_spot0_800 45TW_new2/a2.6_w22.2/n0.075_spot0_1000 45TW_new2/a2.6_w22.2/n0.115_spot0_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_800 45TW_new2/a2.6_w22.2/n0.14_spot300_1000 45TW_new2/a2.6_w22.2/n0.14_spot600_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_2000 45TW_new2/a2.6_w22.2/n0.14_spot0_500 45TW_new2/a2.6_w22.2/n0.14_spot0_1400 45TW_new2/a2.6_w22.2/n0.14_spot0_1200 45TW_new2/a2.6_w22.2/n0.14_spot0_1000 45TW_new2/a2.6_w22.2/n0.14_spot0_1300 45TW_new2/a2.6_w22.2/n0.14_spot0_1600 45TW_new2/a2.6_w22.2/n0.14_spot0_1500 45TW_new2/a2.6_w22.2/n0.01_spot0 45TW_new2/a2.6_w22.2/n0.14_spot600_650 45TW_new2/a2.6_w22.2/n0.14_spot300_650 45TW_new2/a2.6_w22.2/n0.075_spot0/n0.075_spot0_2000 45TW_new2/a2.6_w22.2/n0.01_spot0_2000 45TW_new2/a2.6_w22.2/n0.03_spot0_2000 45TW_new2/a2.6_w22.2/n0.05_spot0_2000 45TW_new2/a2.6_w22.2/n0.14_spot0_650 45TW_new2/a2.6_w22.2/n0.14_spot300 45TW_new2/a2.6_w22.2/n0.14_spot600 45TW_new2/a2.6_w22.2/n0.14_spot0 45TW_new2/a2.6_w22.2/n5e24_plane_spot0 45TW_new2/a2.6_w22.2/n0.14_1400 45TW_new2/a2.6_w22.2/n0.14_spot600_1400 45TW_new2/a2.6_w22.2/n0.03_plane 45TW_new2/a2.6_w22.2/n0.025_plane 45TW_new2/a2.6_w22.2/n0.005_plane 45TW_new2/a2.6_w22.2/n0.02_plane 45TW_new2/a2.6_w22.2/n0.015_plane 45TW_new2/a2.6_w22.2/n0.01_plane 45TW_new2/a2.6_w22.2/bak_0.115 45TW_new2/a2.6_w22.2/bak_0.14 45TW_new2/a2.6_w22.2/n0.035_sharp 45TW_new2/a2.6_w22.2/n0.075_sharp 45TW_new2/a2.6_w22.2/n0.115_sharp 45TW_new2/a2.6_w22.2/n0.14_sharp 45TW_new2/a2.6_w22.2/n0.035_plane 45TW_new2/a2.6_w22.2/n0.075_plane 45TW_new2/a2.6_w22.2/n0.115_plane 45TW_new2/a2.6_w22.2/n0.14_plane 45TW_new2/a2.6_w22.2/n0.3_theta8000 45TW_new2/a2.6_w22.2/n0.3_theta6000 45TW_new2/a2.6_w22.2/n0.3_theta3800 45TW_new2/a2.6_w22.2/n0.3_theta3600 45TW_new2/a2.6_w22.2/n0.3_theta3400 45TW_new2/a2.6_w22.2/n0.3_theta3200 45TW_new2/a2.6_w22.2/n0.3_theta3000 45TW_new2/a2.6_w22.2/n0.3_theta4000 45TW_new2/a2.5_w20/n0.3_spot1500 45TW_new2/a2.5_w20/n0.3_spot500 45TW_new2/a2.5_w20/n0.3_dump1200 45TW_new2/a2.5_w20/n0.3_dump1100 45TW_new2/a2.5_w20/n0.55_half 45TW_new2/a2.5_w20/n0.7_half 45TW_new2/a2.5_w20/n1_half 45TW_new2/a2.5_w20/n0.45_half 45TW_new2/a2.5_w20/n0.35_half 45TW_new2/a2.5_w20/n0.25_half 45TW_new2/a2.5_w20/n0.6_half 45TW_new2/a2.5_w20/n0.3_half 45TW_new2/a2.5_w20/n0.4_half 45TW_new2/a2.5_w20/n0.5_half 45TW_new2/a2.5_w20/n0.2_half )
#list=(2color/a2_w85_t100/n10e22_T18 2color/a2_w50_t30/n3e23_a0.1 2color/a2_w100_t30/n1e23_a0.1 2color/a5_w50_t110 2color/a3_w50_t100/n1e22_a0.1 2color/a3_w50_t100/n15e22_a0.1 2color/a3_w50_t100/ez_a0.1 2color/a2_w50_t100/n10e22_T10 2color/a2_w50_t100/n15e22_a0.1 2color/a2_w50_t100/ez_a0.5 2color/a2_w50_t100/ez_a0.1 2color/a2_w100_t160/n1e23_a0.1 2color/a2_w100_t160/ez_a0.1 2color/a2_w100_t160/ez_a0.5/ez_a0.1 2color/a2_w100_t160/ey_a0.5 2color/a2_w100_t160/test 2color/a5.8_w50_t110/ez_a0.5 2color/a5.8_w50_t110/ez_a0.1 2color/a5.8_w50_t110/ex_n2.7e23 2color/a5.8_w50_t110/4T0_n2.7e23 2color/a5.8_w50_t110/new_n2.7e23 2color/a5.8_w50_t110/n2.7e23 2color/2_color_test2 2color/2_color_test)
#list=(cascade/a2_w50_t110/guass_n1e25_n10e22 cascade/a2_w50_t110/n5e25_n10e22)

list=(MassLimit/new_a3_w9.1_n0.2/y20x300 MassLimit/new_a3_w9.1_n0.2/y40x300 MassLimit/new_a3_w9.1_n0.2/y7x300 MassLimit/new_a3_w9.1_n0.2/y2x300 MassLimit/new_a3_w9.1_n0.2/y4x300 MassLimit/new_a3_w9.1_n0.2/y3x700 MassLimit/new_a3_w9.1_n0.2/y3x500 MassLimit/new_a3_w9.1_n0.2/y3x300 MassLimit/new_a3_w9.1_n0.2/y3x200 MassLimit/new_a3_w9.1_n0.2/y3x100 MassLimit/new_a3_w9.1_n0.2/y3x50)


for i in ${list[@]};
        do
		#python extract_y0.py $i		
		#python fft.py $i
		#python draw_freqs.py $i
		#python draw_xt.py $i
		
		#python baktxt.py $i
		#python test_eff_bz.py $i
		#python test_eff_ey.py $i
		python rm.py $i
	done

