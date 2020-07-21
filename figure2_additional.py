#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

# plt.rcParams.update({'font.size': 18})
SITE = 2
SERIES = 1


def get_k_b(xy1,xy2):
    k=(xy2[1]-xy1[1])/(xy2[0]-xy1[0])
    b=xy1[1]-k*xy1[0]
    return k,b
def moving_average(a, n):    
    ret=np.copy(a)
    for i in range(n//2,len(a)-n//2):
        ret[i]=np.mean(a[i-n//2:i+n//2+1])
    return ret
def get_see_ranges(roi_xy):
    roi_xy_new_0=np.append(roi_xy[:,0],roi_xy[0,0])
    roi_xy_new_1=np.append(roi_xy[:,1],roi_xy[0,1])
    roi_xy_new=np.vstack((roi_xy_new_0,roi_xy_new_1)).T
#     print(roi_xy_new)
    bum_f_axe=np.arange(np.min(np.array(roi_xy)[:,0])+1,np.max(np.array(roi_xy_new)[:,0]))
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
    bum_ranges=[]
    for jj in range(len(bum_f_axe)):
        f=bum_f_axe[jj]
        dfs=[]
        for j in range(len(f0_arange)):
            if f in f0_arange[j]:
                f_ind=np.where(f0_arange[j]==f)[0][0]
                dfs.append(df_arange[j][f_ind])
        bum_ranges.append((f,sorted(dfs)))
    return bum_ranges

db_offset=[-8.7,0,-2.5]
angle={0:"+28°",1:"+21°",2:"+14°",3:"+7°",4:"0°",5:"-7°",6:"-14°",7:"-21°",8:"-28°"}

spec_db_file="spm_database_100Hz.npy"
spec_file="spectrogram_A_n2500.npz"
# proc_files=[
#     'proc_0100.npz',
#     'proc_0101.npz',
#     'proc_0120.npz',
#     'proc_0121.npz',
#     'proc_0140.npz',
#     'proc_0141.npz',
#     'proc_0160.npz',
#     'proc_0161.npz',
#     'proc_0180.npz',
#     'proc_0181.npz',
# ]
proc_files=[
    'proc_'+str(SITE)+'100.npz',
    'proc_'+str(SITE)+'101.npz',
    'proc_'+str(SITE)+'110.npz',
    'proc_'+str(SITE)+'111.npz',
    'proc_'+str(SITE)+'120.npz',
    'proc_'+str(SITE)+'121.npz',
    'proc_'+str(SITE)+'130.npz',
    'proc_'+str(SITE)+'131.npz',
    'proc_'+str(SITE)+'140.npz',
    'proc_'+str(SITE)+'141.npz',
    'proc_'+str(SITE)+'150.npz',
    'proc_'+str(SITE)+'151.npz',
    'proc_'+str(SITE)+'160.npz',
    'proc_'+str(SITE)+'161.npz',
    'proc_'+str(SITE)+'170.npz',
    'proc_'+str(SITE)+'171.npz',
    'proc_'+str(SITE)+'180.npz',
    'proc_'+str(SITE)+'181.npz',
]


SPM_DB=np.load(spec_db_file, allow_pickle=True)

data=np.load(spec_file)
spectrogram=data['spectrogram']
f_axe=data['f_axe']
t_axe=data['t_axe']

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

for angle_ind in range(9):
    for dir_ind in range(2):
        for session_ind in range(2):            
            for i in range(len(SPM_DB[0][angle_ind][dir_ind][session_ind][0])):
                ind=np.where(SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,0:2500]==1e-50)[0][-1]+1
                SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,ind:ind+351]=SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,ind:ind+351]/temp

DM_F0, DM_INT, DM_FREQS =[],[],[]
BUM_F0, BUM_INT, BUM_FREQS =[],[],[]
BUMD_F0, BUMD_INT, BUMD_FREQS =[],[],[]


# file_ind=0
# for file_ind in range(len(proc_files)):
# for file_ind in [8,9,6,7,4,5,2,3,0,1]:
for file_ind in [16,17,14,15,12,13,10,11,8,9,6,7,4,5,2,3,0,1]:
# for file_ind in [7]:
# for file_ind in range(9,10):
    filename=proc_files[file_ind]
    proc_data=np.load(filename)
    list(proc_data.keys())

    temp_name=filename.split('.')[0].split('_')[-1]
    site_ind=int(temp_name[0])
    series_ind=int(temp_name[1])
    angle_ind=int(temp_name[2])
    dir_ind=int(temp_name[3])
    # site_ind, series_ind, angle_ind, dir_ind
    interference_mask=proc_data['interference_mask']
    if dir_ind==0: interference_mask=np.flipud(interference_mask)

    roi_bum_xy=proc_data['roi_bum_xy']
    roi_bumd_xy=proc_data['roi_bumd_xy']
    roi_dm_xy=proc_data['roi_dm_xy']

    spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][session_ind][2]
    spec_log=10*np.log10(spectrogram)
    spec_filt=spec_log*(1-interference_mask)-200*interference_mask
    f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][session_ind][0]
    f_axe=SPM_DB[site_ind][angle_ind][dir_ind][session_ind][1]
    if dir_ind==0: 
        spec_filt=np.flipud(spec_filt)
        f0_axe=np.flip(f0_axe)

    bum_ranges=get_see_ranges(roi_bum_xy)      
    bum_int=np.ones(len(bum_ranges))*np.nan
    bum_f0=np.zeros(len(bum_ranges))
    bum_freqs=np.ones(len(bum_ranges))*np.nan
    for j in range(len(bum_ranges)):
        f0=bum_ranges[j][0]
        f0_ind=np.where(np.abs(f0_axe-f0)==np.min(np.abs(f0_axe-f0)))[0][0]
        df_min=bum_ranges[j][1][0]
        df_max=bum_ranges[j][1][1]
        df_min_ind=np.where(np.abs(f_axe/1000-df_min)==np.min(np.abs(f_axe/1000-df_min)))[0][0]
        df_max_ind=np.where(np.abs(f_axe/1000-df_max)==np.min(np.abs(f_axe/1000-df_max)))[0][0]
        bum_f0[j]=f0
        bum_int[j]=np.max(spec_filt[f0_ind,df_min_ind:df_max_ind+1],axis=0)
        bum_freqs[j]=f_axe[df_min_ind+np.argmax(spec_filt[f0_ind,df_min_ind:df_max_ind+1],axis=0)]/1000
    BUM_F0.append(bum_f0), BUM_INT.append(bum_int), BUM_FREQS.append(bum_freqs)
    
    bumd_ranges=get_see_ranges(roi_bumd_xy)      
#     print(len(bumd_ranges),bumd_ranges)
    bumd_int=np.ones(len(bumd_ranges))*np.nan
    bumd_f0=np.zeros(len(bumd_ranges))
    bumd_freqs=np.ones(len(bumd_ranges))*np.nan
    for j in range(len(bumd_ranges)):
        f0=bumd_ranges[j][0]
        f0_ind=np.where(np.abs(f0_axe-f0)==np.min(np.abs(f0_axe-f0)))[0][0]
        df_min=bumd_ranges[j][1][0]
        df_max=bumd_ranges[j][1][1]
        df_min_ind=np.where(np.abs(f_axe/1000-df_min)==np.min(np.abs(f_axe/1000-df_min)))[0][0]
        df_max_ind=np.where(np.abs(f_axe/1000-df_max)==np.min(np.abs(f_axe/1000-df_max)))[0][0]
        bumd_f0[j]=f0
        bumd_int[j]=np.max(spec_filt[f0_ind,df_min_ind:df_max_ind+1],axis=0)
        bumd_freqs[j]=f_axe[df_min_ind+np.argmax(spec_filt[f0_ind,df_min_ind:df_max_ind+1],axis=0)]/1000
    BUMD_F0.append(bumd_f0), BUMD_INT.append(bumd_int), BUMD_FREQS.append(bumd_freqs)

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
    
    if site_ind==0 and series_ind==1 and angle_ind==0 and dir_ind==0:
        dm_f0[np.where(dm_f0==5777.)]=np.nan
        dm_f0[np.where(dm_f0==5837.)]=np.nan
        dm_f0[np.where(dm_f0==5927.)]=np.nan
        
    if site_ind==0 and series_ind==1 and angle_ind==4 and dir_ind==0:
        dm_f0[np.where(dm_f0==5927.)]=np.nan
    
    if site_ind==0 and series_ind==1 and angle_ind==8 and dir_ind==0:
        dm_f0[np.where(dm_f0==5929.)]=np.nan
        
    if site_ind==0 and series_ind==1 and angle_ind==8 and dir_ind==1:
        dm_f0[np.where(dm_f0==5917.)]=np.nan
        
#DM_PROC=np.load("dm_proc.npy")
dm_proc_table_fname='dm_proc_100Hz.csv'
dm_proc_table=np.loadtxt(dm_proc_table_fname,skiprows=1,delimiter=',')

step=0
DM_PROC=[]
for site_ind in range(3):
    DM_PROC.append([])
    for angle_ind in range(9):
        DM_PROC[site_ind].append([])
        for dir_ind in range(2):
            DM_PROC[site_ind][angle_ind].append([])
            for series_ind in range(2):
               DM_PROC[site_ind][angle_ind][dir_ind].append((dm_proc_table[step,5],dm_proc_table[step,6],dm_proc_table[step,7],dm_proc_table[step,8]))
               step+=1

# text_size=16
# dx=0.011

# fig=plt.figure(figsize=(16,15))
# axs1=[]
# i_sh1=0.001
# i_sh2=0.001
# for i in range(len(bb)):
#     if i in [1,3,5,7,9]:
#         axs1.append(plt.axes(position=[bb[i][0]-dx+0.02-i_sh1*i,bb[i][1]+0.267*2-0.02,bb[i][2]-0.008,bb[i][3]/3]))
# #         print(i)
#     else:        
#         axs1.append(plt.axes(position=[bb[i][0]+0.0199-i_sh2*i,bb[i][1]+0.267*2-0.02,bb[i][2]-0.008,bb[i][3]/3]))
# cbaxes = plt.axes([0.060000000000000005, 0.05+0.269*2+0.10-0.02, 0.9769152542372881-0.060000000000000005, 0.05/3]) 

fig = plt.figure(figsize=(11.69333333334,8.2667),dpi=102) # A4 - format

sshift=0.014

left_board = 0.06
width_1 = 0.039
height_1 = 0.25
x_shift_1 = width_1+sshift

bottom_1 = 0.72
axs1 = []
for i in range(18):
    if i%2==0:
        axs1.append(plt.axes((left_board + i*x_shift_1, bottom_1, width_1, height_1)))
        axs1[-1].set_xlim(5.930,5.730)
        axs1[-1].set_xticks([5.730,5.930])
    else:
        axs1.append(plt.axes((left_board + i*x_shift_1-sshift, bottom_1, width_1, height_1)))
        axs1[-1].set_xlim(5.730,5.930)
        axs1[-1].set_xticks([5.930])
    if i==0: 
        axs1[-1].set_yticks([0,25,50,75,100,125,150])
        axs1[-1].set_ylabel(r'$\Delta f$, kHz')
    else:
        axs1[-1].set_yticks([])
    axs1[-1].set_ylim(-25,150)
    
cbaxes = plt.axes((left_board,bottom_1-0.06,width_1*18+sshift*16,0.01))
# cbaxes.set_xlim(-110,-75)
cbaxes.set_yticks([])
cbaxes.set_xticks([-110,-105,-100,-95,-90,-85,-80,-75])


width_2 = width_1*2
x_shift_2 = width_2+sshift*2
bottom_2 = 0.35

axs2 = []
for i in range(9):
    axs2.append(plt.axes((left_board + i*x_shift_2, bottom_2, width_2, height_1)))
    if i==0:
        axs2[-1].set_yticks([-110,-100,-90,-80])
        axs2[-1].set_ylabel('SEE intensity, dB')
    else:
        axs2[-1].set_yticks([])
    axs2[-1].set_ylim(-120,-80)
    axs2[-1].set_xlim(5.700,5.930)
    axs2[-1].set_xticks([5.730,5.830,5.930])
    fig.text(left_board + i*x_shift_2 +0.045,0.98,
    r'$\alpha=$'+str(angle[8-i]),
    horizontalalignment='center', verticalalignment='center')

bottom_3 = 0.06

axs3 = []
for i in range(9):
    axs3.append(plt.axes((left_board + i*x_shift_2, bottom_3, width_2, height_1)))
    if i==0: 
        axs3[-1].set_yticks([0,20,40,60,80,100])
        axs3[-1].set_ylabel(r'$\Delta f$, kHz')
    else:
        axs3[-1].set_yticks([])
    axs3[-1].set_xlabel('$f_0$, MHz')
    axs3[-1].set_ylim(0,100)
    axs3[-1].set_xlim(5.700,5.930)
    axs3[-1].set_xticks([5.730,5.830,5.930])
# 


angle_inds=[8,7,6,5,4,3,2,1,0]

site_ind=SITE
series_ind=SERIES

#SPM
for angle_ind2 in range(9):
    for dir_ind in range(2):
        angle_ind=angle_inds[angle_ind2]        
        ind=angle_ind2*2+dir_ind
        f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][0]
        f_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][1]
        spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][2]                
        pcm=axs1[ind].pcolormesh(f0_axe/1000, f_axe/1000,10*np.log10(spectrogram.T)+db_offset[site_ind],vmax=-80,vmin=-120,cmap='jet')
cb = plt.colorbar(pcm, cax = cbaxes, orientation='horizontal')  
cbaxes.set_xlabel('Intensity, dB')


######

# axs2=[]
# i_sh=0.002
# for i in range(0,len(bb),2):
#     axs2.append(plt.axes(position=[bb[i][0]+0.02-i_sh*i,bb[i][1]+0.267-0.08-0.03,bb[i][2]*2-0.008,bb[i][3]/3]))

# angle_inds=[8,6,4,2,0]
# site_ind=0 
# series_ind=1
for angle_ind2 in range(9):
                
    angle_ind=angle_inds[angle_ind2]
    ind=angle_ind2
    
    dir_ind=0
    dm_f0= DM_F0[angle_ind2*2]
    dm_freq= DM_FREQS[angle_ind2*2]
    dm_int= DM_INT[angle_ind2*2]
    bum_f0= BUM_F0[angle_ind2*2]
    bum_freq= BUM_FREQS[angle_ind2*2]
    bum_int= BUM_INT[angle_ind2*2]

    if angle_ind in [1,2,3]:     
        bumd_f0= BUMD_F0[angle_ind2*2]
        bumd_freq= BUMD_FREQS[angle_ind2*2]
        bumd_int= BUMD_INT[angle_ind2*2]
        axs2[ind].plot(bumd_f0,bumd_int+db_offset[site_ind],'g',lw=1, label=r'BUM$_\mathrm{D}$/d')
        
    if ind==0:
        axs2[ind].plot(dm_f0,dm_int+db_offset[site_ind],'r',lw=1,label='DM/d')
        axs2[ind].plot(bum_f0,bum_int+db_offset[site_ind],'m',lw=1,label='BUM/d')
    else:
        axs2[ind].plot(dm_f0,dm_int+db_offset[site_ind],'r',lw=1)
        axs2[ind].plot(bum_f0,bum_int+db_offset[site_ind],'m',lw=1)
    
    dir_ind=1
    
    dm_f0= DM_F0[angle_ind2*2+1]
    dm_freq= DM_FREQS[angle_ind2*2+1]
    dm_int= DM_INT[angle_ind2*2+1]
    bum_f0= BUM_F0[angle_ind2*2+1]
    bum_freq= BUM_FREQS[angle_ind2*2+1]
    bum_int= BUM_INT[angle_ind2*2+1]
    
    if angle_ind in [1,2,3]:    
        bumd_f0= BUMD_F0[angle_ind2*2+1]
        bumd_freq= BUMD_FREQS[angle_ind2*2+1]
        bumd_int= BUMD_INT[angle_ind2*2+1]        
        if ind==3:
            axs2[ind].plot(bumd_f0,bumd_int+db_offset[site_ind],'c',lw=1,label=r'BUM$_\mathrm{D}$/u')
        else:
            axs2[ind].plot(bumd_f0,bumd_int+db_offset[site_ind],'c',lw=1)
        
    if ind==0:
        axs2[ind].plot(dm_f0,dm_int+db_offset[site_ind],'b',lw=1, label= 'DM/u')
        axs2[ind].plot(bum_f0,bum_int+db_offset[site_ind],'k',lw=1, label= 'BUM/u')
        axs2[ind].set_ylabel("SEE intensity, dB", labelpad=0)
    else:
        axs2[ind].plot(dm_f0,dm_int+db_offset[site_ind],'b',lw=1)
        axs2[ind].plot(bum_f0,bum_int+db_offset[site_ind],'k',lw=1)
    
    # axs2[ind].set_ylim([-110,-75])

    axs2[ind].set_xlim([5700,5930])
    axs2[ind].set_xticks([5730,5830,5930])
    if ind>0:
        axs2[ind].set_yticklabels({''})

axs2[0].legend(loc=2, handlelength=1)
axs2[3].legend(loc=3, handlelength=1)    
######
    
# axs3=[]
# i_sh=0.002
# for i in range(0,len(bb),2):
#     axs3.append(plt.axes(position=[bb[i][0]+0.02-i_sh*i,bb[i][1]-0.08-0.05,bb[i][2]*2-0.008,bb[i][3]/3]))

# angle_inds=[8,6,4,2,0]
# site_ind=0 
# series_ind=1
for angle_ind2 in range(9):
                
    angle_ind=angle_inds[angle_ind2]
    ind=angle_ind2
    
    dir_ind=0
    dm_f0= DM_F0[angle_ind2*2]
    dm_freq= DM_FREQS[angle_ind2*2]
    dm_int= DM_INT[angle_ind2*2]
    bum_f0= BUM_F0[angle_ind2*2]
    bum_freq= BUM_FREQS[angle_ind2*2]
    bum_int= BUM_INT[angle_ind2*2]
      
    if angle_ind in [1,2,3]:    
        bumd_f0= BUMD_F0[angle_ind2*2]
        bumd_freq= BUMD_FREQS[angle_ind2*2]
        bumd_int= BUMD_INT[angle_ind2*2]
        axs3[ind].plot(bumd_f0,bumd_freq,'g',lw=1)
        
    axs3[ind].plot(bum_f0,bum_freq,color=(0.75, 0.0, 0.75, .5),lw=1)
    axs3[ind].plot(bum_f0,bum_freq,'m',lw=1)
    
    dir_ind=1
    dm_f0= DM_F0[angle_ind2*2+1]
    dm_freq= DM_FREQS[angle_ind2*2+1]
    dm_int= DM_INT[angle_ind2*2+1]
    bum_f0= BUM_F0[angle_ind2*2+1]
    bum_freq= BUM_FREQS[angle_ind2*2+1]
    bum_int= BUM_INT[angle_ind2*2+1]          
        
    if angle_ind in [1,2,3]:    
        bumd_f0= BUMD_F0[angle_ind2*2+1]
        bumd_freq= BUMD_FREQS[angle_ind2*2+1]
        bumd_int= BUMD_INT[angle_ind2*2+1] 
        axs3[ind].plot(bumd_f0,bumd_freq,color=(0.0, 0.75, 0.75, 1.),lw=1)
        bumd_f0_full=np.arange(5700,5850)
        bumd_coefs=np.polyfit(bumd_f0[10::],bumd_freq[10::],1)
        axs3[ind].plot(bumd_f0_full,bumd_f0_full*bumd_coefs[0]+bumd_coefs[1],color=(0.0, 0.75, 0.75, 1.),lw=1)
    axs3[ind].plot(bum_f0,bum_freq,'k',lw=1)
    
    bum_f0_full=np.arange(5700,5800)
    bum_coefs=np.polyfit(bum_f0[10::],bum_freq[10::],1)
    if ind==3:
        bum_coefs=np.polyfit(bum_f0[10:-10],bum_freq[10:-10],1)
    if ind==4:
        bum_coefs=np.polyfit(bum_f0[10:-10],bum_freq[10:-10],1)
        
    axs3[ind].plot(bum_f0_full,bum_f0_full*bum_coefs[0]+bum_coefs[1],color=(0., 0.0, 0., .5),lw=1)
#     print(bum_coefs)
        
    axs3[ind].set_ylim([0,100])
    axs3[ind].set_xlim([5700,5930])
    axs3[ind].set_xticks([5730,5830,5930])
    axs3[ind].set_xlabel('$f_0$, kHz')
    if ind==0:
        axs3[ind].set_ylabel(r'$\Delta f_{\mathrm{BUM}}$, kHz')

    if ind>0:
        axs3[ind].set_yticklabels({''})
    
    # ann = axs3[ind].annotate('', xy=(DM_PROC[site_ind][angle_ind][1][series_ind][0]+DM_PROC[site_ind][angle_ind][1][series_ind][1], 0), xycoords='data',
    #               xytext=(DM_PROC[site_ind][angle_ind][1][series_ind][0]+DM_PROC[site_ind][angle_ind][1][series_ind][1], 9), textcoords='data',
    #               arrowprops=dict(arrowstyle="->",                                  
    #                               ec="r",lw=2))
                                  
# fig.text(0.01,0.33,'c)',horizontalalignment='center', verticalalignment='center', fontsize=18)
# fig.text(0.01,0.66-0.05,'b)',horizontalalignment='center', verticalalignment='center', fontsize=18)
# fig.text(0.01,0.98,'a)',horizontalalignment='center', verticalalignment='center', fontsize=18)

    
# plt.savefig('figure2.pdf',dpi=600)
plt.savefig('temp_figure2_site'+str(site_ind)+'_series'+str(series_ind)+'.png',dpi=300)
# plt.show()
plt.close()
