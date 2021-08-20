import os
import re
flist=os.listdir()
print(flist)
err='[a-zA-Z0-9]*\.e[a-zA-Z0-9]*'
for i in flist:
	e=re.findall(err,i)
	print(e)
	try:
		os.rename(str(e[0]),'err/'+str(e[0]))
	except:
		print(e)
out='[a-zA-Z0-9]*\.o[a-zA-Z0-9]*'

for i in flist:
        o=re.findall(out,i)
        print(o)
        try:
                os.rename(str(o[0]),'err/'+str(o[0]))
        except:
                print(o)
