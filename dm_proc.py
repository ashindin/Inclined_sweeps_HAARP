#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


# In[2]:


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 


# In[3]:


# plt.rcParams.update({'font.size': 18})


# In[4]:


site={0:"A", 1:"B", 2:"C"}
series={0:"I", 1:"II"}
angle={0:"28°",1:"21°",2:"14°",3:"7°",4:"0°",5:"-7°",6:"-14°",7:"-21°",8:"-28°"}
angle_ar=np.array([28,21,14,7,0,-7,-14,-21,-28])
direction={0:"↓", 1:"↑"}


# In[14]:


def get_k_b(xy1,xy2):
    k=(xy2[1]-xy1[1])/(xy2[0]-xy1[0])
    b=xy1[1]-k*xy1[0]
    return k,b
def moving_average(a, n):    
    ret=np.copy(a);
    for i in range(n//2,len(a)-n//2):
        ret[i]=np.mean(a[i-n//2:i+n//2+1])
    return ret
def get_see_ranges(roi_xy):
    roi_xy_new_0=np.append(roi_xy[:,0],roi_xy[0,0])
    roi_xy_new_1=np.append(roi_xy[:,1],roi_xy[0,1])
    roi_xy_new=np.vstack((roi_xy_new_0,roi_xy_new_1)).T
#     print(roi_xy_new)
    dm_f_axe=np.arange(np.min(np.array(roi_xy)[:,0])+1,np.max(np.array(roi_xy_new)[:,0]))
    f0_arange=[]
    df_arange=[]
    for j in range(len(roi_xy_new)-1):
        p1=roi_xy_new[j]
        p2=roi_xy_new[j+1]
        f0_arange.append(np.arange(np.minimum(roi_xy_new[j][0],roi_xy_new[j+1][0]),np.maximum(roi_xy_new[j][0],roi_xy_new[j+1][0])))            
        #~ print(j,p1,p2)
        k,b=get_k_b(p1,p2)

        df_arange.append((k*f0_arange[j]+b).astype(np.int))    

    #~ print("WOW")
    dm_ranges=[]
    for jj in range(len(dm_f_axe)):
        f=dm_f_axe[jj]
        dfs=[]
        for j in range(len(f0_arange)):
            if f in f0_arange[j]:
                f_ind=np.where(f0_arange[j]==f)[0][0]
                dfs.append(df_arange[j][f_ind])
        dm_ranges.append((f,sorted(dfs)))
    return dm_ranges


# # Fix filter band issue for site A (at f0 ~ 5730 kHz)

# In[6]:


data=np.load("spectrogram_A_n2500.npz")
spectrogram=data['spectrogram']
f_axe=data['f_axe']
t_axe=data['t_axe']


# In[7]:


rngs=[[600+i*750,1150+i*750] for i in range(18)]
rngs[-1][1]=13500
rngs.insert(0,[0,400])
spm_mean=np.zeros(2500)
for i in range(len(rngs)):
    spm_mean+=np.mean(spectrogram[rngs[i][0]:rngs[i][1],:],axis=0)
spm_mean/=len(rngs)
# plt.figure()
temp=spm_mean[0:360]/spm_mean[350]
# plt.plot(temp)
k,b=get_k_b([124,temp[124]],[127,temp[127]]); temp[125:127]=np.array([125,126])*k+b
k,b=get_k_b([148,temp[148]],[152,temp[152]]); temp[149:152]=np.array(range(149,152))*k+b
k,b=get_k_b([167,temp[167]],[171,temp[171]]); temp[168:171]=np.array(range(168,171))*k+b
k,b=get_k_b([196,temp[196]],[200,temp[200]]); temp[197:200]=np.array(range(197,200))*k+b
k,b=get_k_b([229,temp[229]],[231,temp[231]]); temp[230:231]=np.array(range(230,231))*k+b
k,b=get_k_b([248,temp[248]],[252,temp[252]]); temp[249:252]=np.array(range(249,252))*k+b
k,b=get_k_b([267,temp[267]],[271,temp[271]]); temp[268:271]=np.array(range(268,271))*k+b
k,b=get_k_b([298,temp[298]],[302,temp[302]]); temp[299:302]=np.array(range(299,302))*k+b
k,b=get_k_b([348,temp[348]],[352,temp[352]]); temp[349:352]=np.array(range(349,352))*k+b
temp=moving_average(temp, 11)
temp=temp[0:351]


# In[8]:


db_offset=[-8.7,0,-2.5]


# In[9]:


spec_db_file="spm_database_100Hz.npy"
SPM_DB=np.load(spec_db_file, allow_pickle=True)


# In[10]:


for angle_ind in range(9):
    for dir_ind in range(2):
        for session_ind in range(2):            
            for i in range(len(SPM_DB[0][angle_ind][dir_ind][session_ind][0])):
                ind=np.where(SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,0:2500]==1e-50)[0][-1]+1
                SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,ind:ind+351]=SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,ind:ind+351]/temp


# In[11]:


dm_proc_table_fname='dm_proc_100Hz.csv'
dm_proc_table=np.loadtxt(dm_proc_table_fname,skiprows=1,delimiter=',')

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


# In[18]:


with PdfPages('dm_proc.pdf') as pdf:
    fig3_x_axe=[-28,-21,-14,-7,0,7,14,21,28]
    # I down
    fig3_4fc_A, fig3_4fc_B, fig3_4fc_C=[],[],[]
    fig3_DMmin_A, fig3_DMmin_B, fig3_DMmin_C=[],[],[]
    fig3_DMmax_A, fig3_DMmax_B, fig3_DMmax_C=[],[],[]
#     fig3_BUMmax_A, fig3_BUMmax_B, fig3_BUMmax_C=[],[],[]
#     fig3_dfBUMmax_A, fig3_dfBUMmax_B, fig3_dfBUMmax_C=[],[],[]
    for series_ind in range(1):
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
#                 fig3_BUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])            
#                 fig3_dfBUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]-fig3_4fc_A[-1])
#                 fig3_dfBUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]-fig3_4fc_B[-1])
#                 fig3_dfBUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]-fig3_4fc_C[-1])

    fig,axs=plt.subplots(figsize=(16,5),nrows=1, ncols=2)
    plt.subplots_adjust(left=0.07, bottom=0.15, right=0.93, top=0.94, wspace=0.22, hspace=None)
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_A,'bo-', label='site A')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_B,'ro-', label='site B')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_C,'go-', label='site C')
#     axs[1][0].set_xticks([-28,-14,0,14,28])
#     axs[1][0].grid()
#     axs[1][0].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][0].set_ylabel('BUM intensity, dB')

#     axs[1][1].set_ylabel('$\delta f_{\mathrm{BUMmax}}$, kHz')

#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_A,'bs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_B,'rs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_C,'gs-')
#     axs[1][1].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][1].set_xticks([-28,-14,0,14,28])
#     axs[1][1].grid()

    axs[1].plot(fig3_x_axe,fig3_DMmax_A,'bo-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_B,'ro-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_C,'go-')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].plot(fig3_x_axe,fig3_DMmin_A,'bo--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_B,'ro--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_C,'go--')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].grid()
    axs[1].set_ylabel('DM intensity, dB')

    axs[0].plot(fig3_x_axe,fig3_4fc_A,'bo-',label='site A')
    axs[0].plot(fig3_x_axe,fig3_4fc_B,'ro-',label='site B')
    axs[0].plot(fig3_x_axe,fig3_4fc_C,'go-',label='site C')
    axs[0].set_xticks([-28,-14,0,14,28])
    axs[0].set_yticks([5725,5735,5745])
    axs[0].grid()
    axs[0].set_ylabel('$4f_c$, kHz')
    tit=series[series_ind]+" "+direction[dir_ind]
    axs[0].set_title(tit)

    axs[0].legend()

    x_shift=0.48
    y_shift=0.45
    x0=0.002
    y0=0.965
    fig.text(x0,y0,'a)',fontsize=18)
    fig.text(x0+x_shift-0.01,y0,'b)',fontsize=18)
#     fig.text(x0,y0-y_shift,'c)',fontsize=18)
#     fig.text(x0+x_shift-0.01,y0-y_shift,'d)',fontsize=18)

    pdf.savefig(dpi=600)
    plt.close()
    
    # I up
    fig3_4fc_A, fig3_4fc_B, fig3_4fc_C=[],[],[]
    fig3_DMmin_A, fig3_DMmin_B, fig3_DMmin_C=[],[],[]
    fig3_DMmax_A, fig3_DMmax_B, fig3_DMmax_C=[],[],[]
#     fig3_BUMmax_A, fig3_BUMmax_B, fig3_BUMmax_C=[],[],[]
#     fig3_dfBUMmax_A, fig3_dfBUMmax_B, fig3_dfBUMmax_C=[],[],[]
    for series_ind in range(1):
        for angle_ind in [8,7,6,5,4,3,2,1,0]:
            for dir_ind in range(1,2):
                fig3_4fc_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
                fig3_4fc_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
                fig3_4fc_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
                fig3_DMmin_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
                fig3_DMmin_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
                fig3_DMmin_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])
                fig3_DMmax_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][3])
                fig3_DMmax_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][3])
                fig3_DMmax_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][3])            
#                 fig3_BUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])            
#                 fig3_dfBUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]-fig3_4fc_A[-1])
#                 fig3_dfBUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]-fig3_4fc_B[-1])
#                 fig3_dfBUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]-fig3_4fc_C[-1])

    fig,axs=plt.subplots(figsize=(16,5),nrows=1, ncols=2)
    plt.subplots_adjust(left=0.07, bottom=0.15, right=0.93, top=0.94, wspace=0.22, hspace=None)
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_A,'bo-', label='site A')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_B,'ro-', label='site B')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_C,'go-', label='site C')
#     axs[1][0].set_xticks([-28,-14,0,14,28])
#     axs[1][0].grid()
#     axs[1][0].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][0].set_ylabel('BUM intensity, dB')

#     axs[1][1].set_ylabel('$\delta f_{\mathrm{BUMmax}}$, kHz')

#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_A,'bs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_B,'rs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_C,'gs-')
#     axs[1][1].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][1].set_xticks([-28,-14,0,14,28])
#     axs[1][1].grid()

    axs[1].plot(fig3_x_axe,fig3_DMmax_A,'bo-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_B,'ro-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_C,'go-')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].plot(fig3_x_axe,fig3_DMmin_A,'bo--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_B,'ro--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_C,'go--')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].grid()
    axs[1].set_ylabel('DM intensity, dB')

    axs[0].plot(fig3_x_axe,fig3_4fc_A,'bo-',label='site A')
    axs[0].plot(fig3_x_axe,fig3_4fc_B,'ro-',label='site B')
    axs[0].plot(fig3_x_axe,fig3_4fc_C,'go-',label='site C')
    axs[0].set_xticks([-28,-14,0,14,28])
    axs[0].set_yticks([5725,5735,5745])
    axs[0].grid()
    axs[0].set_ylabel('$4f_c$, kHz')
    tit=series[series_ind]+" "+direction[dir_ind]
    axs[0].set_title(tit)

    axs[0].legend()

    x_shift=0.48
    y_shift=0.45
    x0=0.002
    y0=0.965
    fig.text(x0,y0,'a)',fontsize=18)
    fig.text(x0+x_shift-0.01,y0,'b)',fontsize=18)
#     fig.text(x0,y0-y_shift,'c)',fontsize=18)
#     fig.text(x0+x_shift-0.01,y0-y_shift,'d)',fontsize=18)

    pdf.savefig(dpi=600)
    plt.close()
    
    # II down
    fig3_4fc_A, fig3_4fc_B, fig3_4fc_C=[],[],[]
    fig3_DMmin_A, fig3_DMmin_B, fig3_DMmin_C=[],[],[]
    fig3_DMmax_A, fig3_DMmax_B, fig3_DMmax_C=[],[],[]
#     fig3_BUMmax_A, fig3_BUMmax_B, fig3_BUMmax_C=[],[],[]
#     fig3_dfBUMmax_A, fig3_dfBUMmax_B, fig3_dfBUMmax_C=[],[],[]
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
#                 fig3_BUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])            
#                 fig3_dfBUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]-fig3_4fc_A[-1])
#                 fig3_dfBUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]-fig3_4fc_B[-1])
#                 fig3_dfBUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]-fig3_4fc_C[-1])

    fig,axs=plt.subplots(figsize=(16,5),nrows=1, ncols=2)
    plt.subplots_adjust(left=0.07, bottom=0.15, right=0.93, top=0.94, wspace=0.22, hspace=None)
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_A,'bo-', label='site A')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_B,'ro-', label='site B')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_C,'go-', label='site C')
#     axs[1][0].set_xticks([-28,-14,0,14,28])
#     axs[1][0].grid()
#     axs[1][0].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][0].set_ylabel('BUM intensity, dB')

#     axs[1][1].set_ylabel('$\delta f_{\mathrm{BUMmax}}$, kHz')

#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_A,'bs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_B,'rs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_C,'gs-')
#     axs[1][1].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][1].set_xticks([-28,-14,0,14,28])
#     axs[1][1].grid()

    axs[1].plot(fig3_x_axe,fig3_DMmax_A,'bo-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_B,'ro-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_C,'go-')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].plot(fig3_x_axe,fig3_DMmin_A,'bo--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_B,'ro--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_C,'go--')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].grid()
    axs[1].set_ylabel('DM intensity, dB')

    axs[0].plot(fig3_x_axe,fig3_4fc_A,'bo-',label='site A')
    axs[0].plot(fig3_x_axe,fig3_4fc_B,'ro-',label='site B')
    axs[0].plot(fig3_x_axe,fig3_4fc_C,'go-',label='site C')
    axs[0].set_xticks([-28,-14,0,14,28])
    axs[0].set_yticks([5725,5735,5745])
    axs[0].grid()
    axs[0].set_ylabel('$4f_c$, kHz')
    tit=series[series_ind]+" "+direction[dir_ind]
    axs[0].set_title(tit)

    axs[0].legend()

    x_shift=0.48
    y_shift=0.45
    x0=0.002
    y0=0.965
    fig.text(x0,y0,'a)',fontsize=18)
    fig.text(x0+x_shift-0.01,y0,'b)',fontsize=18)
#     fig.text(x0,y0-y_shift,'c)',fontsize=18)
#     fig.text(x0+x_shift-0.01,y0-y_shift,'d)',fontsize=18)

    pdf.savefig(dpi=600)
    plt.close()
    
    # II up
    fig3_4fc_A, fig3_4fc_B, fig3_4fc_C=[],[],[]
    fig3_DMmin_A, fig3_DMmin_B, fig3_DMmin_C=[],[],[]
    fig3_DMmax_A, fig3_DMmax_B, fig3_DMmax_C=[],[],[]
#     fig3_BUMmax_A, fig3_BUMmax_B, fig3_BUMmax_C=[],[],[]
#     fig3_dfBUMmax_A, fig3_dfBUMmax_B, fig3_dfBUMmax_C=[],[],[]
    for series_ind in range(1,2):
        for angle_ind in [8,7,6,5,4,3,2,1,0]:
            for dir_ind in range(1,2):
                fig3_4fc_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
                fig3_4fc_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
                fig3_4fc_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]+DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1])            
                fig3_DMmin_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
                fig3_DMmin_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
                fig3_DMmin_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])
                fig3_DMmax_A.append(DM_PROC_DB[0][angle_ind][dir_ind][series_ind][3])
                fig3_DMmax_B.append(DM_PROC_DB[1][angle_ind][dir_ind][series_ind][3])
                fig3_DMmax_C.append(DM_PROC_DB[2][angle_ind][dir_ind][series_ind][3])            
#                 fig3_BUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][2])
#                 fig3_BUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][2])            
#                 fig3_dfBUMmax_A.append(BUM_PROC_DB[0][angle_ind][dir_ind][series_ind][0]-fig3_4fc_A[-1])
#                 fig3_dfBUMmax_B.append(BUM_PROC_DB[1][angle_ind][dir_ind][series_ind][0]-fig3_4fc_B[-1])
#                 fig3_dfBUMmax_C.append(BUM_PROC_DB[2][angle_ind][dir_ind][series_ind][0]-fig3_4fc_C[-1])

    fig,axs=plt.subplots(figsize=(16,5),nrows=1, ncols=2)
    plt.subplots_adjust(left=0.07, bottom=0.15, right=0.93, top=0.94, wspace=0.22, hspace=None)
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_A,'bo-', label='site A')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_B,'ro-', label='site B')
#     axs[1][0].plot(fig3_x_axe,fig3_BUMmax_C,'go-', label='site C')
#     axs[1][0].set_xticks([-28,-14,0,14,28])
#     axs[1][0].grid()
#     axs[1][0].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][0].set_ylabel('BUM intensity, dB')

#     axs[1][1].set_ylabel('$\delta f_{\mathrm{BUMmax}}$, kHz')

#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_A,'bs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_B,'rs-')
#     axs[1][1].plot(fig3_x_axe,fig3_dfBUMmax_C,'gs-')
#     axs[1][1].set_xlabel(r'$\alpha$, $^\circ$')
#     axs[1][1].set_xticks([-28,-14,0,14,28])
#     axs[1][1].grid()

    axs[1].plot(fig3_x_axe,fig3_DMmax_A,'bo-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_B,'ro-')
    axs[1].plot(fig3_x_axe,fig3_DMmax_C,'go-')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].plot(fig3_x_axe,fig3_DMmin_A,'bo--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_B,'ro--')
    axs[1].plot(fig3_x_axe,fig3_DMmin_C,'go--')
    axs[1].set_xticks([-28,-14,0,14,28])

    axs[1].grid()
    axs[1].set_ylabel('DM intensity, dB')

    axs[0].plot(fig3_x_axe,fig3_4fc_A,'bo-',label='site A')
    axs[0].plot(fig3_x_axe,fig3_4fc_B,'ro-',label='site B')
    axs[0].plot(fig3_x_axe,fig3_4fc_C,'go-',label='site C')
    axs[0].set_xticks([-28,-14,0,14,28])
    axs[0].set_yticks([5725,5735,5745])
    axs[0].grid()
    axs[0].set_ylabel('$4f_c$, kHz')
    tit=series[series_ind]+" "+direction[dir_ind]
    axs[0].set_title(tit)

    axs[0].legend()

    x_shift=0.48
    y_shift=0.45
    x0=0.002
    y0=0.965
    fig.text(x0,y0,'a)',fontsize=18)
    fig.text(x0+x_shift-0.01,y0,'b)',fontsize=18)
#     fig.text(x0,y0-y_shift,'c)',fontsize=18)
#     fig.text(x0+x_shift-0.01,y0-y_shift,'d)',fontsize=18)

    pdf.savefig(dpi=600)
    plt.close()

    step=0
#     BUM_F0, BUM_INT, BUM_FREQS =[],[],[]
    DM_F0, DM_INT, DM_FREQS =[],[],[]
    for site_ind in range(3):
        for series_ind in range(2):
            for angle_ind in range(9):
                for dir_ind in range(2):
#     for site_ind in range(1):
#         for series_ind in range(1,2):
#             for angle_ind in range(1):
#                 for dir_ind in range(1):
                    progress(step, 107, status='Save pictures to pdf')
                    step+=1
                    proc_filename='proc_'+str(site_ind)+str(series_ind)+str(angle_ind)+str(dir_ind)+'.npz'
                    proc_data=np.load(proc_filename)
                    interference_mask=proc_data['interference_mask']
                    if dir_ind==0: interference_mask=np.flipud(interference_mask);
#                     roi_bum_xy=proc_data['roi_bum_xy']
#                     roi_bumd_xy=proc_data['roi_bumd_xy']
                    roi_dm_xy=proc_data['roi_dm_xy']
                    spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][2]
                    spec_log=10*np.log10(spectrogram)
                    spec_filt=spec_log*(1-interference_mask)-200*interference_mask
                    f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][0]
                    f_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][1]
                    if dir_ind==0: 
                        spec_filt=np.flipud(spec_filt)
                        spec_log=np.flipud(spec_log)
                        f0_axe=np.flip(f0_axe)

                    dm_ranges=get_see_ranges(roi_dm_xy)      
                    dm_int=np.ones(len(dm_ranges))*np.nan
                    dm_f0=np.zeros(len(dm_ranges))
                    dm_freqs=np.ones(len(dm_ranges))*np.nan
                    for j in range(len(dm_ranges)):
                        f0=dm_ranges[j][0]
                        f0_ind=np.where(np.abs(f0_axe-f0)==np.min(np.abs(f0_axe-f0)))[0][0]
                        df_min=dm_ranges[j][1][0]
                        df_max=dm_ranges[j][1][1]
                        df_min_ind=np.where(np.abs(f_axe/1000-df_min)==np.min(np.abs(f_axe/1000-df_min)))[0][0]
                        df_max_ind=np.where(np.abs(f_axe/1000-df_max)==np.min(np.abs(f_axe/1000-df_max)))[0][0]
                        dm_f0[j]=f0
                        dm_int[j]=np.max(spec_filt[f0_ind,df_min_ind:df_max_ind+1],axis=0)
                        dm_freqs[j]=f_axe[df_min_ind+np.argmax(spec_filt[f0_ind,df_min_ind:df_max_ind+1],axis=0)]/1000
                    DM_F0.append(dm_f0), DM_INT.append(dm_int), DM_FREQS.append(dm_freqs)

                    f0_DMmin=DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][0]
                    df_DMmin=DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][1]                    
                    DMmin=DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][2]
                    DMmax=DM_PROC_DB[site_ind][angle_ind][dir_ind][series_ind][3]

    #                 fig = plt.figure(figsize=(16,5))
                    fig = plt.figure(figsize=(16,4.8))
                    axs0 = plt.subplot('131')                
                    axs0.pcolormesh(f0_axe, f_axe/1000,
                                   spec_filt.T+db_offset[site_ind],vmax=-80,vmin=-125,cmap='jet',rasterized=True)
    #                 axs0.plot([5730,5930],[dm_min_offset_kHz,dm_min_offset_kHz],"k",lw=3)
    #                 axs0.plot([5730,5930],[dm_max_offset_kHz,dm_max_offset_kHz],"k",lw=3)
                    axs0.plot(dm_f0,dm_freqs,"k:",lw=1)
                    axs0.set_ylim(-15,0)
                    axs0.set_xlim([5730,5930])
                    tit=str(step)+" "+site[site_ind]+" "+series[series_ind]+" "+angle[angle_ind]+" "+direction[dir_ind]
                    axs0.set_title(tit)


                    axs1 = plt.subplot('132')
                    axs1.plot(dm_f0,dm_int+db_offset[site_ind],"r",lw=2)
                    axs1.plot([f0_DMmin, f0_DMmin],[-200,0],"k",lw=2)
                    axs1.plot([5730, 5930],[DMmin,DMmin],"k",lw=2)
                    axs1.plot([5730, 5930],[DMmax,DMmax],"k",lw=2)                    
                    axs1.set_xlim([5730,5930])
                    axs1.set_title("{:.2f}".format(DMmin)+" dB, "+"{:.2f}".format(DMmax)+" dB")
                    axs1.plot()
    #                 axs1.set_title(str(np.max(10*np.log10(dm_int[0:50])+db_offset[site_ind])))
                    axs1.set_ylim([-125,-80])
                    axs1.grid()

                    axs2 = plt.subplot('133')
                    axs2.plot(dm_f0,dm_freqs,"b",lw=2)
                    axs2.plot([f0_DMmin,f0_DMmin],[-200,0],"k",lw=2)
                    axs2.plot([5730,5930],[df_DMmin,df_DMmin],"k",lw=2)
                    axs2.set_xlim([5730,5930])
                    axs2.set_ylim([-15,0])
#                     axs2.set_title("BUM freq offset, kHz")
                    axs2.set_title("{:.0f}".format(f0_DMmin)+" kHz, "+"{:.1f}".format(df_DMmin)+" kHz")
                    axs2.grid()                    
                    
                    pdf.savefig(dpi=600)
                    plt.close()
                

