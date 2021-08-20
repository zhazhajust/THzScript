import sdf
a= sdf.read('0010.sdf',dict=True)
b=a['Electric Field/Ey/Core_centre'].data[:,0]
c=a['Electric Field/Ey'].data[:,749]
print(b==c)
np.sum(b==c)
