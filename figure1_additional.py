import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})

pol_thres=0.7

xlsx_filename='/home/ashindin/owncloud/0002_see_incl/Data_1_5.83.xlsx'
table=pd.read_excel(xlsx_filename, index_col=None, header=None) 
Ex, Ey, Ez, h, X, T, n2, labs =[],[],[],[],[],[],[],[]
for i in range(9):
    Ex.append(table[0+i*9][1::].values.astype(float))
    Ey.append(table[1+i*9][1::].values.astype(float))
    Ez.append(table[2+i*9][1::].values.astype(float))
    h.append(table[3+i*9][1::].values.astype(float))
    X.append(table[4+i*9][1::].values.astype(float))
    T.append(table[5+i*9][1::].values.astype(float))
    n2.append(table[6+i*9][1::].values.astype(float))
    labs.append(table[7+i*9][1])

fig=plt.figure(figsize=(9,6))
ax=plt.axes()
colors=['r','g','b','c','m', 'y', 'orange', 'brown', 'lime']
labels=[r'$\alpha=-28^\circ$',r'$\alpha=-21^\circ$',r'$\alpha=-14^\circ$',r'$\alpha=-7^\circ$',r'$\alpha=0^\circ$', 
r'$\alpha=7^\circ$', r'$\alpha=14^\circ$', r'$\alpha=21^\circ$', r'$\alpha=28^\circ$']
ind=0
for i in [0,2,3,4,5,7,6,8,1]:
    plt.plot(X[i],h[i],color=colors[ind],label='')
    plt.plot(X[i][np.where(Ez[i]>pol_thres)[0]],h[i][np.where(Ez[i]>pol_thres)[0]],color=colors[ind],label=labels[ind],lw=4)
    ind+=1
plt.legend(loc=3)
plt.title("5830 kHz")
plt.xlabel('X, km')
plt.ylabel('h, km')
ax.set_xticks([-300,-200,-100,0,100,200,300])
ax.set_ylim(80,230)

ann1 = ax.annotate('', xy=(11, 80), xycoords='data',
              xytext=(11, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann2 = ax.annotate('', xy=(82, 80), xycoords='data',
              xytext=(82, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann3 = ax.annotate('', xy=(113, 80), xycoords='data',
              xytext=(113, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))

ann4 = ax.annotate('A', Color='k', xy=(7, 90), xycoords='data',
              xytext=(7-3, 92), textcoords='data')

ann5 = ax.annotate('B', Color='k', xy=(78, 90), xycoords='data',
              xytext=(78-3, 92), textcoords='data')

ann4 = ax.annotate('C', Color='k', xy=(109, 90), xycoords='data',
              xytext=(109-3, 92), textcoords='data')

r=40
x0=50; y0=220
dx=-r*np.cos(75.822*np.pi/180); dy=-r*np.sin(75.822*np.pi/180)
# ~ print(dx,dy)

ann_mag = ax.annotate('', xy=(x0+dx, y0+dy), xycoords='data',
              xytext=(x0, y0), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))

ann_B = ax.annotate('B', Color='k', xy=(30, 200), xycoords='data',
              xytext=(27,200), textcoords='data',fontsize=16,fontweight='bold')    
ax.plot([-300,300],[223,223], "k--",lw=2)


ann_ns = ax.annotate('', xy=(150, 120), xycoords='data',
              xytext=(300, 120), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann_N = ax.annotate('N', Color='k', xy=(125, 120), xycoords='data',
              xytext=(132,118), textcoords='data',fontsize=16)    
ann_S = ax.annotate('S', Color='k', xy=(304, 120), xycoords='data',
              xytext=(305,118), textcoords='data',fontsize=16)

plt.savefig('figure1a_5830.pdf',dpi=600)
plt.savefig('figure1a_5830.png')
plt.close()

xlsx_filename='/home/ashindin/owncloud/0002_see_incl/sData_1_5.73.xlsx'
table=pd.read_excel(xlsx_filename, index_col=None, header=None) 
Ex, Ey, Ez, h, X, T, n2, labs =[],[],[],[],[],[],[],[]
for i in range(9):
    Ex.append(table[0+i*9][1::].values.astype(float))
    Ey.append(table[1+i*9][1::].values.astype(float))
    Ez.append(table[2+i*9][1::].values.astype(float))
    h.append(table[3+i*9][1::].values.astype(float))
    X.append(table[4+i*9][1::].values.astype(float))
    T.append(table[5+i*9][1::].values.astype(float))
    n2.append(table[6+i*9][1::].values.astype(float))
    labs.append(table[7+i*9][1])

fig=plt.figure(figsize=(9,6))
ax=plt.axes()
colors=['r','g','b','c','m', 'y', 'orange', 'brown', 'lime']
labels=[r'$\alpha=-28^\circ$',r'$\alpha=-21^\circ$',r'$\alpha=-14^\circ$',r'$\alpha=-7^\circ$',r'$\alpha=0^\circ$', 
r'$\alpha=7^\circ$', r'$\alpha=14^\circ$', r'$\alpha=21^\circ$', r'$\alpha=28^\circ$']
ind=0
for i in [0,1, 2,3,4,5,6,7,8]:
    plt.plot(X[i],h[i],color=colors[ind],label='')
    plt.plot(X[i][np.where(Ez[i]>pol_thres)[0]],h[i][np.where(Ez[i]>pol_thres)[0]],color=colors[ind],label=labels[ind],lw=4)
    ind+=1
plt.legend(loc=3)
plt.title("5730 kHz")
plt.xlabel('X, km')
plt.ylabel('h, km')
ax.set_xticks([-300,-200,-100,0,100,200,300])
ax.set_ylim(80,230)

ann1 = ax.annotate('', xy=(11, 80), xycoords='data',
              xytext=(11, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann2 = ax.annotate('', xy=(82, 80), xycoords='data',
              xytext=(82, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann3 = ax.annotate('', xy=(113, 80), xycoords='data',
              xytext=(113, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))

ann4 = ax.annotate('A', Color='k', xy=(7, 90), xycoords='data',
              xytext=(7-3, 92), textcoords='data')

ann5 = ax.annotate('B', Color='k', xy=(78, 90), xycoords='data',
              xytext=(78-3, 92), textcoords='data')

ann4 = ax.annotate('C', Color='k', xy=(109, 90), xycoords='data',
              xytext=(109-3, 92), textcoords='data')

r=40
x0=50; y0=220
dx=-r*np.cos(75.822*np.pi/180); dy=-r*np.sin(75.822*np.pi/180)
# ~ print(dx,dy)

ann_mag = ax.annotate('', xy=(x0+dx, y0+dy), xycoords='data',
              xytext=(x0, y0), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))

ann_B = ax.annotate('B', Color='k', xy=(30, 200), xycoords='data',
              xytext=(27,200), textcoords='data',fontsize=16,fontweight='bold')    
ax.plot([-300,300],[223,223], "k--",lw=2)


ann_ns = ax.annotate('', xy=(150, 120), xycoords='data',
              xytext=(300, 120), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann_N = ax.annotate('N', Color='k', xy=(125, 120), xycoords='data',
              xytext=(132,118), textcoords='data',fontsize=16)    
ann_S = ax.annotate('S', Color='k', xy=(304, 120), xycoords='data',
              xytext=(305,118), textcoords='data',fontsize=16)

plt.savefig('figure1a_5730.pdf',dpi=600)
plt.savefig('figure1a_5730.png')
plt.close()

xlsx_filename='/home/ashindin/owncloud/0002_see_incl/sData_1_5.93.xlsx'
table=pd.read_excel(xlsx_filename, index_col=None, header=None) 
Ex, Ey, Ez, h, X, T, n2, labs =[],[],[],[],[],[],[],[]
for i in range(9):
    Ex.append(table[0+i*9][1::].values.astype(float))
    Ey.append(table[1+i*9][1::].values.astype(float))
    Ez.append(table[2+i*9][1::].values.astype(float))
    h.append(table[3+i*9][1::].values.astype(float))
    X.append(table[4+i*9][1::].values.astype(float))
    T.append(table[5+i*9][1::].values.astype(float))
    n2.append(table[6+i*9][1::].values.astype(float))
    labs.append(table[7+i*9][1])

fig=plt.figure(figsize=(9,6))
ax=plt.axes()
colors=['r','g','b','c','m', 'y', 'orange', 'brown', 'lime']
labels=[r'$\alpha=-28^\circ$',r'$\alpha=-21^\circ$',r'$\alpha=-14^\circ$',r'$\alpha=-7^\circ$',r'$\alpha=0^\circ$', 
r'$\alpha=7^\circ$', r'$\alpha=14^\circ$', r'$\alpha=21^\circ$', r'$\alpha=28^\circ$']
ind=0
for i in [0,1, 2,3,4,5,6,7,8]:
    plt.plot(X[i],h[i],color=colors[ind],label='')
    plt.plot(X[i][np.where(Ez[i]>pol_thres)[0]],h[i][np.where(Ez[i]>pol_thres)[0]],color=colors[ind],label=labels[ind],lw=4)
    ind+=1
plt.legend(loc=3)
plt.title("5930 kHz")
plt.xlabel('X, km')
plt.ylabel('h, km')
ax.set_xticks([-300,-200,-100,0,100,200,300])
ax.set_ylim(80,230)

ann1 = ax.annotate('', xy=(11, 80), xycoords='data',
              xytext=(11, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann2 = ax.annotate('', xy=(82, 80), xycoords='data',
              xytext=(82, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann3 = ax.annotate('', xy=(113, 80), xycoords='data',
              xytext=(113, 90), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))

ann4 = ax.annotate('A', Color='k', xy=(7, 90), xycoords='data',
              xytext=(7-3, 92), textcoords='data')

ann5 = ax.annotate('B', Color='k', xy=(78, 90), xycoords='data',
              xytext=(78-3, 92), textcoords='data')

ann4 = ax.annotate('C', Color='k', xy=(109, 90), xycoords='data',
              xytext=(109-3, 92), textcoords='data')

r=40
x0=50; y0=220
dx=-r*np.cos(75.822*np.pi/180); dy=-r*np.sin(75.822*np.pi/180)
# ~ print(dx,dy)

ann_mag = ax.annotate('', xy=(x0+dx, y0+dy), xycoords='data',
              xytext=(x0, y0), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))

ann_B = ax.annotate('B', Color='k', xy=(30, 200), xycoords='data',
              xytext=(27,200), textcoords='data',fontsize=16,fontweight='bold')    
ax.plot([-300,300],[223,223], "k--",lw=2)


ann_ns = ax.annotate('', xy=(150, 120), xycoords='data',
              xytext=(300, 120), textcoords='data',
              arrowprops=dict(arrowstyle="->",
                              ec="k",lw=2))
ann_N = ax.annotate('N', Color='k', xy=(125, 120), xycoords='data',
              xytext=(132,118), textcoords='data',fontsize=16)    
ann_S = ax.annotate('S', Color='k', xy=(304, 120), xycoords='data',
              xytext=(305,118), textcoords='data',fontsize=16)

plt.savefig('figure1a_5930.pdf',dpi=600)
plt.savefig('figure1a_5930.png')
plt.close()