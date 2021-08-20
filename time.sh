#!/bin/bash

starttime=`date +'%Y-%m-%d %H:%M:%S'`

python baktxt.py 45TW_new2/a2.6_w22.2/n0.075_plane
endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
end_seconds=$(date --date="$endtime" +%s);
echo "本次运行时间： "$((end_seconds-start_seconds))"s"
