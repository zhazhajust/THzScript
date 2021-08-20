from lib.ey.extract_y0 import run
import constant as const
import os
import sys
savedir=const.txtdir   #"./txt/a0_1_2e-2/"
savename="xt.npy"
if os.path.exists(savedir+savename) == True:
        sys.exit()
run()
