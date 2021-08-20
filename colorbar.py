import matplotlib.pyplot as plt
import numpy as  np

def reg_cmap():
    iname = 'rainbow'
    oname = 'dist'    
    low = 0.1        
    high = 1.0

    #(position, [r,g,b,a] or #rrggbb)
    special = [(0,[1,1,1,1])]      
    cmap = plt.get_cmap(iname)
    N = int((high - low) * 256)
    values = np.linspace(low,high,N)
    colors = cmap(values)
    colorlist = [(values[i],colors[i]) for i in range(N)]
    colorlist = special + colorlist
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list(oname,colorlist)
    #An other example: plt.cm.colors.LinearSegmentedColormap.from_list(‘cmap’, [‘#FFFFFF’, ‘#98F5FF’, ‘#00FF00’, ‘#FFFF00’,’#FF0000’, ‘#8B0000’], 256)
    plt.cm.register_cmap(cmap=cmap)
    return cmap

def reg_cmap_transparent(iname,alpha):
    oname = iname + '_transparent'
    cmap = plt.get_cmap(iname)
    values = np.linspace(0,1,256)
    colors = cmap(values)
    for i in range(256):
        colors[i][3] = alpha[i]
    colorlist = [(values[i],colors[i]) for i in range(256)]
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list(oname,colorlist)
    plt.cm.register_cmap(cmap=cmap)
    return cmap

def create_alpha(func):
    return [ 1 if func(i)>1 else 0 if func(i)<0 else func(i) for i in range(256)]

#iname = 'jet'
#lambda x:(0.7 + (1/256*x) *0.3)
#lambda x:(np.exp(x/(256))-0.7)

def getTransCmap(func,iname = 'jet'):#lambda x:(0.7 + (1/256*x) *0.3)):
    plt.set_cmap(reg_cmap_transparent(iname,create_alpha(func)))#lambda x:(0.7 + (1/256*x) *0.3))))
    cmap_trans = plt.get_cmap()
    return cmap_trans

if __name__ == '__main__':
    iname = 'jet'
    plt.set_cmap(reg_cmap_transparent(iname,create_alpha(lambda x:(0.7 + (1/256*x) *0.3))))
    cmap_trans = plt.get_cmap()
