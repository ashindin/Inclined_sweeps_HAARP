#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


plt.rcParams.update({'font.size': 18})


# In[3]:


site={0:"A", 1:"B", 2:"C"}
series={0:"I", 1:"II"}
angle={0:"28°",1:"21°",2:"14°",3:"7°",4:"0°",5:"-7°",6:"-14°",7:"-21°",8:"-28°"}
angle_ar=np.array([28,21,14,7,0,-7,-14,-21,-28])
direction={0:"↓", 1:"↑"}

bum_proc_table_fname='bum_proc_100Hz.csv'
bum_proc_table=np.loadtxt(bum_proc_table_fname,skiprows=1,delimiter=',')
step=0
BUM_PROC_DB=[]
for site_ind in range(3):
    BUM_PROC_DB.append([])
    for angle_ind in range(9):
        BUM_PROC_DB[site_ind].append([])
        for dir_ind in range(2):
            BUM_PROC_DB[site_ind][angle_ind].append([])
            for series_ind in range(2):
                BUM_PROC_DB[site_ind][angle_ind][dir_ind].append((bum_proc_table[step,5],bum_proc_table[step,6],bum_proc_table[step,7]))
                step+=1


# In[7]:


dm_proc_table_fname='dm_proc_100Hz.csv'
dm_proc_table=np.loadtxt(dm_proc_table_fname,skiprows=1,delimiter=',')


# In[8]:


step=0
DM_PROC_DB=[]
for site_ind in range(3):
    DM_PROC_DB.append([])
    for angle_ind in range(9):
        DM_PROC_DB[site_ind].append([])
        for dir_ind in range(2):
            DM_PROC_DB[site_ind][angle_ind].append([])
            for series_ind in range(2):
                DM_PROC_DB[site_ind][angle_ind][dir_ind].append((dm_proc_table[step,5],dm_proc_table[step,6],dm_proc_table[step,7],dm_proc_table[step,8]))
                step+=1   


# In[9]:


fig3_x_axe=[-28,-21,-14,-7,0,7,14,21,28]
fig3_4fc_A, fig3_4fc_B, fig3_4fc_C=[],[],[]
fig3_DMmin_A, fig3_DMmin_B, fig3_DMmin_C=[],[],[]
fig3_DMmax_A, fig3_DMmax_B, fig3_DMmax_C=[],[],[]
fig3_BUMmax_A, fig3_BUMmax_B, fig3_BUMmax_C=[],[],[]
fig3_dfBUMmax_A, fig3_dfBUMmax_B, fig3_dfBUMmax_C=[],[],[]
for series_ind in range(1,2):
    for angle_ind in [8,7,6,5,4,3,2,1,0]:
        for dir_ind in range(1):
            fig3_4fc_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
            fig3_4fc_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
            fig3_4fc_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
            fig3_DMmin_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
            fig3_DMmin_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
            fig3_DMmin_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])
            fig3_DMmax_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][3])
            fig3_DMmax_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][3])
            fig3_DMmax_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][3])            
            fig3_BUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
            fig3_BUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
            fig3_BUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])            
            fig3_dfBUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]-fig3_4fc_A[-1])
            fig3_dfBUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]-fig3_4fc_B[-1])
            fig3_dfBUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]-fig3_4fc_C[-1])


# In[10]:


fig,axs=plt.subplots(figsize=(16,10),nrows=2, ncols=2)
plt.subplots_adjust(left=0.07, bottom=0.15, right=0.93, top=0.94, wspace=0.22, hspace=None)
axs[1][0].plot(fig3_x_axe,fig3_BUMmax_A,'bo-', label='site A')
axs[1][0].plot(fig3_x_axe,fig3_BUMmax_B,'ro-', label='site B')
axs[1][0].plot(fig3_x_axe,fig3_BUMmax_C,'go-', label='site C')
axs[1][0].set_xticks([-28,-14,0,14,28])
axs[1][0].grid()
axs[1][0].set_xlabel(r'$\alpha$, $^\circ$')
axs[1][0].set_ylabel('BUM intensity, dB')

axs[1][1].set_ylabel(r'$\delta f_{\mathrm{BUMmax}}$, kHz')

axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_A,'bs-')
axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_B,'rs-')
axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_C,'gs-')
axs[1][1].set_xlabel(r'$\alpha$, $^\circ$')
axs[1][1].set_xticks([-28,-14,0,14,28])
axs[1][1].grid()

axs[0][1].plot(fig3_x_axe,fig3_DMmax_A,'bo-')
axs[0][1].plot(fig3_x_axe,fig3_DMmax_B,'ro-')
axs[0][1].plot(fig3_x_axe,fig3_DMmax_C,'go-')
axs[0][1].set_xticks([-28,-14,0,14,28])

axs[0][1].plot(fig3_x_axe,fig3_DMmin_A,'bo--')
axs[0][1].plot(fig3_x_axe,fig3_DMmin_B,'ro--')
axs[0][1].plot(fig3_x_axe,fig3_DMmin_C,'go--')
axs[0][1].set_xticks([-28,-14,0,14,28])

axs[0][1].grid()
axs[0][1].set_ylabel('DM intensity, dB')

axs[0][0].plot(fig3_x_axe,fig3_4fc_A,'bo-',label='site A')
axs[0][0].plot(fig3_x_axe,fig3_4fc_B,'ro-',label='site B')
axs[0][0].plot(fig3_x_axe,fig3_4fc_C,'go-',label='site C')
axs[0][0].set_xticks([-28,-14,0,14,28])
axs[0][0].set_yticks([5725,5735,5745])
axs[0][0].grid()
axs[0][0].set_ylabel('$4f_c$, kHz')

axs[0][0].legend()

x_shift=0.48
y_shift=0.45
x0=0.002
y0=0.965
fig.text(x0,y0,'a)',fontsize=18)
fig.text(x0+x_shift-0.01,y0,'b)',fontsize=18)
fig.text(x0,y0-y_shift,'c)',fontsize=18)
fig.text(x0+x_shift-0.01,y0-y_shift,'d)',fontsize=18)


plt.savefig('figure3.pdf',dpi=600)
plt.savefig('figure3.png')
#plt.show()
plt.close()

