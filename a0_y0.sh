#!/bin/bash
lists=(12um_a2_n1_T6_w8 a2_n0.7 a2_n1_T2 a2_n1_T6_w10 a2_n1_w5 a2_n2 new_a2_n0.7 a2_n1 a2_n1_T20 a2_n1_T6_w8 a2_n1_w6  a2_n3 45tw_0.28_spot1 a2_n1.5 a2_n1_T4 a2_n1_w10 a2_n1_w7 a2_n4.5 a2_n0.4 a2_n1_T14 a2_n1_T6 a2_n1_w16 a2_n1_w8 a4_n1)
for i in ${list[@]};
	do
		python extract_parallel.py $i
		python fft.py $i
		python draw_freqs.py $i
		python efficiency_i.py $i
		python baktxt.py $i
		python my_a0.py $i
		python draw_E_w.py $i
		python gif_thz.py $i
	done
 
 
 
