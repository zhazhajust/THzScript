import constant as const
import numpy as np

lists=const.b
bbb=np.arange(len(lists))
for i in range(len(lists)):
        bbb[i]=int(lists[i])



def find_nearest(value , array = bbb):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#lists=np.array(const.b)
#bbb=np.arange(len(lists))
#for i in range(len(lists)):
#	bbb[i]=int(lists[i][0])

###example
###
array=bbb
value=3.5
print(find_nearest(value, array))	

