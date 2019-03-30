#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np
import scipy.signal as ss
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


site={0:"A", 1:"B", 2:"C"}
series={0:"I", 1:"II"}
angle={0:"28°",1:"21°",2:"14°",3:"7°",4:"0°",5:"-7°",6:"-14°",7:"-21°",8:"-28°"}
direction={0:"↓", 1:"↑"}
db_offset=[-8.7,0,-2.5]


# # Fix filter band issue for site A (at f0 ~ 5730 kHz)

# In[4]:


data=np.load("spectrogram_A_n2500.npz")
spectrogram=data['spectrogram']
f_axe=data['f_axe']
t_axe=data['t_axe']


# In[5]:


# fig=plt.figure()
# plt.pcolormesh(range(len(t_axe)),f_axe/1000,10*np.log10(spectrogram.T),vmin=-120, vmax=-80)
# plt.xlim([0,350])
# plt.show()


# In[6]:


# temp=np.zeros(36)
# fig=plt.figure()
# for i in range(18):
#     temp+=spectrogram[300+750*i,0:36]/spectrogram[300+750*i,35]
#     plt.plot(f_axe[0:36]/1000+5830,spectrogram[300+750*i,0:36]/spectrogram[300+750*i,35])

# temp_mean=temp/18
# plt.plot(f_axe[0:36]/1000+5830,temp_mean,'k',lw=3)
# plt.xlim(f_axe[0]/1000+5830,5740)
# plt.show()


# In[7]:


# %matplotlib notebook


# In[8]:


def get_k_b(xy1,xy2):
    k=(xy2[1]-xy1[1])/(xy2[0]-xy1[0])
    b=xy1[1]-k*xy1[0]
    return k,b
def moving_average(a, n):    
    ret=np.copy(a);
    for i in range(n//2,len(a)-n//2):
        ret[i]=np.mean(a[i-n//2:i+n//2+1])
    return ret


# In[9]:


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
# plt.plot(temp,lw=2)
# plt.ylim(0,1)
# plt.show()


# In[10]:


SPM_DB=np.load("spm_database_100Hz.npy")
# SPM_DB=np.load("spm_database_filt.npy")


# In[11]:


for angle_ind in range(9):
    for dir_ind in range(2):
        for session_ind in range(2):            
            for i in range(len(SPM_DB[0][angle_ind][dir_ind][session_ind][0])):
                ind=np.where(SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,0:2500]==1e-50)[0][-1]+1
                SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,ind:ind+351]=SPM_DB[0][angle_ind][dir_ind][session_ind][2][i,ind:ind+351]/temp


# In[12]:


# site_ind, series_ind, angle_ind, dir_ind = 1,1,0,0

# f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][0]
# f_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][1]
# spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][2]

# np.savez("test_inline_ton_s2_28d_100Hz.npz", spectrogram=spectrogram, f_axe=f_axe, t_axe=f0_axe)


# In[13]:


# angle_ind=0; dir_ind=0; session_ind=0
# f0_axe = SPM_DB[0][angle_ind][dir_ind][session_ind][0]
# f_axe = SPM_DB[0][angle_ind][dir_ind][session_ind][1]
# spectrogram = SPM_DB[0][angle_ind][dir_ind][session_ind][2]

                
# plt.pcolormesh(f0_axe,f_axe/1000,10*np.log10(spectrogram.T),vmin=-120,vmax=-80)
# plt.ylim([-15,0])
# plt.show()

# plt.plot(10*np.log10(spectrogram[0,:]))
# plt.show()


# In[14]:


dm_min_offset_kHz=-11.
dm_max_offset_kHz=-8.


# In[15]:


csv=np.loadtxt('dm_proc_100Hz.csv',delimiter=',', skiprows=1)
# csv


# In[16]:


DM_PROC=[]
step=0
for site_ind in range(3):
    DM_PROC.append([])
    for angle_ind in range(9):
        DM_PROC[site_ind].append([])
        for dir_ind in range(2):
            DM_PROC[site_ind][angle_ind].append([])
            for series_ind in range(2):                
                step+=1
                DM_PROC[site_ind][angle_ind][dir_ind].append((csv[step-1,5],csv[step-1,6],csv[step-1,7],csv[step-1,8]))


# In[ ]:


np.save("dm_proc.npy",DM_PROC)


# In[22]:


DM_DB=[]
step=0
with PdfPages('dm_proc.pdf') as pdf:
    for series_ind in range(2):
        for dir_ind in range(2):
        #     series_ind=1; dir_ind=1; 
            angle_axe=[28,21,14,7,0,-7,-14,-21,-28]
            fig = plt.figure(figsize=(9.9,3))
            axs1 = plt.subplot('122')

            site_ind=0
            test=[]; test1=[]; test_x=[]
            for angle_ind in range(9):
                test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
                test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
                test_x.append(angle_axe[angle_ind])    
            plt.plot(test_x,test,'bo--')
            plt.plot(test_x,test1,'bo-')
            site_ind=1
            test=[]; test1=[]; test_x=[]
            for angle_ind in range(9):
                test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
                test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
                test_x.append(angle_axe[angle_ind])
            plt.plot(test_x,test,'ro--')
            plt.plot(test_x,test1,'ro-')
            site_ind=2
            test=[]; test1=[]; test_x=[]
            for angle_ind in range(9):
                test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
                test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
                test_x.append(angle_axe[angle_ind])
            plt.plot(test_x,test,'go--')
            plt.plot(test_x,test1,'go-')

            plt.ylim([-125,-80])
            axs1.set_xticks([-28,-14,0,14,28])
            tit=series[series_ind]+" "+direction[dir_ind]
            axs1.set_title(tit)
            plt.grid()

            axs2 = plt.subplot('121')
            site_ind=0
            test=[]; test_x=[]
            for angle_ind in range(9):
                test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1])    
                test_x.append(angle_axe[angle_ind])    
            plt.plot(test_x,test,'bo-')
            site_ind=1
            test=[]; test_x=[]
            for angle_ind in range(9):
                test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1])    
                test_x.append(angle_axe[angle_ind])    
            plt.plot(test_x,test,'ro-')
            site_ind=2
            test=[]; test_x=[]
            for angle_ind in range(9):
                test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1]-1)    
                test_x.append(angle_axe[angle_ind])    
            plt.plot(test_x,test,'go-')

            axs2.set_xticks([-28,-14,0,14,28])
            axs2.set_yticks([5725,5735,5745,5755])
            axs2.set_ylim(5720,5757)
            axs2.set_title(tit)
            plt.grid()
            pdf.savefig(dpi=300) 
            plt.close()
    
    for site_ind in range(3):
        DM_DB.append([])
        for angle_ind in range(9):
            DM_DB[site_ind].append([])
            for dir_ind in range(2):
                DM_DB[site_ind][angle_ind].append([])
                for series_ind in range(2):                                       
                    progress(step, 107, status='Save pictures to pdf')
                    step+=1                    
                    dm_min_freq=DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]
                    dm_offset_freq=DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1]
                    dm_min_int=DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2]
                    dm_max_int=DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3]
                    
                    f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][0]
                    f_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][1]
                    spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][2]
                    dm_fmin_ind=np.where(f_axe==dm_min_offset_kHz*1000)[0][0]
                    dm_fmax_ind=np.where(f_axe==dm_max_offset_kHz*1000)[0][0]
                    dm_int=np.max(spectrogram[:,dm_fmin_ind:dm_fmax_ind+1],axis=1)
                    dm_freq=f_axe[np.argmax(spectrogram[:,dm_fmin_ind:dm_fmax_ind+1],axis=1)+dm_fmin_ind]
                    DM_DB[site_ind][angle_ind][dir_ind].append(np.vstack((f0_axe,dm_freq,dm_int)).T)                    
                    fig, axs = plt.subplots(1, 3, figsize=(9.9,3))           
                    axs[0].pcolormesh(f0_axe, f_axe/1000,
                                   10*np.log10(spectrogram.T)+db_offset[site_ind],vmax=-80,vmin=-125,cmap='jet',rasterized=True)
                    axs[0].plot([5730,5930],[dm_min_offset_kHz,dm_min_offset_kHz],"k",lw=3)
                    axs[0].plot([5730,5930],[dm_max_offset_kHz,dm_max_offset_kHz],"k",lw=3)
                    axs[0].plot(f0_axe,dm_freq/1000,"w",lw=3)
                    axs[0].set_ylim(-15,0)
                    axs[0].set_xlim([5730,5930])
                    tit=str(step)+" "+site[site_ind]+" "+series[series_ind]+" "+angle[angle_ind]+" "+direction[dir_ind]
                    axs[0].set_title(tit)

                    axs[1].plot(f0_axe,10*np.log10(dm_int)+db_offset[site_ind],"r",lw=3)                    
                    axs[1].set_ylim([-125,-80])
                    axs[1].plot([5730,5930],[dm_min_int,dm_min_int],'g:')
                    axs[1].plot([5730,5930],[dm_max_int,dm_max_int],'g:')
                    axs[1].plot([dm_min_freq,dm_min_freq],[-135,-70],'g:')
                    axs[1].set_title("{:.2f}".format(dm_min_int)+" dB, "+"{:.2f}".format(dm_max_int)+" dB")
#                     axs[1].grid()
                    axs[2].plot(f0_axe,dm_freq/1000,"b",lw=3)
                    axs[2].plot([5730,5930],[dm_offset_freq,dm_offset_freq],'g:')
                    axs[2].set_title("{:.0f}".format(dm_min_freq)+" kHz, "+"{:.1f}".format(dm_offset_freq)+" kHz")
#                     axs[2].grid()
                    pdf.savefig(dpi=300) 
                    plt.close()
                    
    #                 plt.show()


# In[18]:


# for series_ind in range(2):
#     for dir_ind in range(2):
#     #     series_ind=1; dir_ind=1; 
#         angle_axe=[28,21,14,7,0,-7,-14,-21,-28]
#         fig = plt.figure(figsize=(9.9,3))
#         axs1 = plt.subplot('122')

#         site_ind=0
#         test=[]; test1=[]; test_x=[]
#         for angle_ind in range(9):
#             test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
#             test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
#             test_x.append(angle_axe[angle_ind])    
#         plt.plot(test_x,test,'bo--')
#         plt.plot(test_x,test1,'bo-')
#         site_ind=1
#         test=[]; test1=[]; test_x=[]
#         for angle_ind in range(9):
#             test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
#             test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
#             test_x.append(angle_axe[angle_ind])
#         plt.plot(test_x,test,'ro--')
#         plt.plot(test_x,test1,'ro-')
#         site_ind=2
#         test=[]; test1=[]; test_x=[]
#         for angle_ind in range(9):
#             test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
#             test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
#             test_x.append(angle_axe[angle_ind])
#         plt.plot(test_x,test,'go--')
#         plt.plot(test_x,test1,'go-')

#         plt.ylim([-125,-80])
#         axs1.set_xticks([-28,-14,0,14,28])
#         tit=series[series_ind]+" "+direction[dir_ind]
#         axs1.set_title(tit)
#         plt.grid()

#         axs2 = plt.subplot('121')
#         site_ind=0
#         test=[]; test_x=[]
#         for angle_ind in range(9):
#             test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1])    
#             test_x.append(angle_axe[angle_ind])    
#         plt.plot(test_x,test,'bo-')
#         site_ind=1
#         test=[]; test_x=[]
#         for angle_ind in range(9):
#             test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1])    
#             test_x.append(angle_axe[angle_ind])    
#         plt.plot(test_x,test,'ro-')
#         site_ind=2
#         test=[]; test_x=[]
#         for angle_ind in range(9):
#             test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1]-1)    
#             test_x.append(angle_axe[angle_ind])    
#         plt.plot(test_x,test,'go-')

#         axs2.set_xticks([-28,-14,0,14,28])
#         axs2.set_yticks([5725,5735,5745,5755])
#         axs2.set_ylim(5720,5757)
#         axs2.set_title(tit)
#         plt.grid()
#         plt.show()


# In[19]:


# series_ind=1; dir_ind=0; 
# angle_axe=[28,21,14,7,0,-7,-14,-21,-28]
# fig = plt.figure(figsize=(9.9,3))
# axs1 = plt.subplot('122')

# site_ind=0
# test=[]; test1=[]; test_x=[]
# for angle_ind in range(9):
#     test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
#     test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
#     test_x.append(angle_axe[angle_ind])    
# plt.plot(test_x,test,'bo--')
# plt.plot(test_x,test1,'bo-')
# site_ind=1
# test=[]; test1=[]; test_x=[]
# for angle_ind in range(9):
#     test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
#     test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
#     test_x.append(angle_axe[angle_ind])
# plt.plot(test_x,test,'ro--')
# plt.plot(test_x,test1,'ro-')
# site_ind=2
# test=[]; test1=[]; test_x=[]
# for angle_ind in range(9):
#     test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][2])
#     test1.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][3])
#     test_x.append(angle_axe[angle_ind])
# plt.plot(test_x,test,'go--')
# plt.plot(test_x,test1,'go-')

# plt.ylim([-122,-80])
# axs1.set_xticks([-28,-14,0,14,28])
# plt.grid()

# axs2 = plt.subplot('121')
# site_ind=0
# test=[]; test_x=[]
# for angle_ind in range(9):
#     test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1])    
#     test_x.append(angle_axe[angle_ind])    
# plt.plot(test_x,test,'bo-')
# site_ind=1
# test=[]; test_x=[]
# for angle_ind in range(9):
#     test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1])    
#     test_x.append(angle_axe[angle_ind])    
# plt.plot(test_x,test,'ro-')
# site_ind=2
# test=[]; test_x=[]
# for angle_ind in range(9):
#     test.append(DM_PROC[site_ind][angle_ind][dir_ind][series_ind][0]+DM_PROC[site_ind][angle_ind][dir_ind][series_ind][1]-1)    
#     test_x.append(angle_axe[angle_ind])    
# plt.plot(test_x,test,'go-')

# axs2.set_xticks([-28,-14,0,14,28])
# axs2.set_yticks([5725,5735,5745,5755])
# axs2.set_ylim(5722,5757)
# plt.grid()
# plt.show()


# In[20]:


# DM_DB=[]
# DM_PROC=[]
# step=0
# for site_ind in range(3):
#     DM_DB.append([])
#     DM_PROC.append([])
#     for angle_ind in range(9):
#         DM_DB[site_ind].append([])
#         DM_PROC[site_ind].append([])
#         for dir_ind in range(2):
#             DM_DB[site_ind][angle_ind].append([])
#             DM_PROC[site_ind][angle_ind].append([])
#             for series_ind in range(2):                                                       
#                 step+=1
#                 f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][0]
#                 f_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][1]
#                 spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][2]
#                 dm_fmin_ind=np.where(f_axe==dm_min_offset_kHz*1000)[0][0]
#                 dm_fmax_ind=np.where(f_axe==dm_max_offset_kHz*1000)[0][0]
#                 dm_int=np.max(spectrogram[:,dm_fmin_ind:dm_fmax_ind+1],axis=1)
#                 dm_freq=f_axe[np.argmax(spectrogram[:,dm_fmin_ind:dm_fmax_ind+1],axis=1)+dm_fmin_ind]

#                 DM_DB[site_ind][angle_ind][dir_ind].append(np.vstack((f0_axe,dm_freq,dm_int)).T)
#                 DM_PROC[site_ind][angle_ind][dir_ind].append((csv[step-1,5],csv[step-1,6],csv[step-1,7],csv[step-1,8]))

#                 fig = plt.figure(figsize=(9.9,3))
#                 axs0 = plt.subplot('131')                
#                 axs0.pcolormesh(f0_axe, f_axe/1000,
#                                10*np.log10(spectrogram.T)+db_offset[site_ind],vmax=-75-7,vmin=-100-7,cmap='jet',rasterized=True)
#                 axs0.plot([5730,5930],[dm_min_offset_kHz,dm_min_offset_kHz],"k",lw=3)
#                 axs0.plot([5730,5930],[dm_max_offset_kHz,dm_max_offset_kHz],"k",lw=3)
#                 axs0.plot(f0_axe,dm_freq/1000,"w",lw=3)
#                 axs0.set_ylim(-15,0)
#                 axs0.set_xlim([5730,5930])
#                 tit=str(step)+" "+site[site_ind]+" "+series[series_ind]+" "+angle[angle_ind]+" "+direction[dir_ind]
#                 axs0.set_title(tit)
                
                
#                 axs1 = plt.subplot('132')
#                 axs1.plot(f0_axe,10*np.log10(dm_int)+db_offset[site_ind],"r",lw=3)
#                 axs1.plot([5730,5930],[csv[step-1,7],csv[step-1,7]],'g:')
#                 axs1.plot([5730,5930],[csv[step-1,8],csv[step-1,8]],'g:')
#                 axs1.plot([csv[step-1,5],csv[step-1,5]],[-115,-70],'g:')
#                 axs1.set_title(str(np.max(10*np.log10(dm_int[0:50])+db_offset[site_ind])))
#                 axs1.set_ylim([-115-9,-70-8])
#                 axs1.grid()
                
#                 axs2 = plt.subplot('133')
#                 axs2.plot(f0_axe,dm_freq/1000,"b",lw=1)
#                 axs2.plot([5730,5930],[csv[step-1,6],csv[step-1,6]],'g:')
#                 axs2.set_title("DM freq offset, kHz")
#                 axs2.grid()                    
#                 plt.show()

