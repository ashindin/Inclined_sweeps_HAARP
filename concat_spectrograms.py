#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np
import matplotlib.pyplot as plt


# In[29]:


def view_spectrogram_dbshift(t_axe,f_axe,spectrogram,tit='',min_int=-120,max_int=-90,ymin=0,ymax=0,db_shift=0,savefile="",close_fig=False):
    fig=plt.figure(figsize=(9,6))
    plt.pcolormesh(t_axe,f_axe,10*np.log10(spectrogram.T)+db_shift,vmax=max_int,vmin=min_int,cmap='jet')
    plt.xlim(t_axe[0],t_axe[-1])
    #if ymin==0:
    if ymax==0:
        ymin=f_axe[0]
        ymax=f_axe[-1]
    plt.ylim(ymin,ymax)
    plt.grid()
    plt.colorbar()
    plt.title(tit)    
    if savefile!="":
        plt.savefig(savefile)
        plt.close()
    if close_fig==False:
        plt.show()


# # Site A

# In[30]:


sr=500000; period_samples=int(0.2*sr); duration_samples=int(0.15*sr)
npz_fnames=[
'spew_110330_012948_05830_0250_01_01_spm_n250.npz',
'spew_110330_013028_05830_0250_01_01_spm_n250.npz',
'spew_110330_013456_05830_0250_01_01_spm_n250.npz',
'spew_110330_013925_05830_0250_01_01_spm_n250.npz',
'spew_110330_014353_05830_0250_01_01_spm_n250.npz',
'spew_110330_014821_05830_0250_01_01_spm_n250.npz',
'spew_110330_015250_05830_0250_01_01_spm_n250.npz',
'spew_110330_015718_05830_0250_01_01_spm_n250.npz',
'spew_110330_020147_05830_0250_01_01_spm_n250.npz',
'spew_110330_020615_05830_0250_01_01_spm_n250.npz',
'spew_110330_021044_05830_0250_01_01_spm_n250.npz']
nfft=int(npz_fnames[0].split('.')[0].split('_')[-1][1::]) # 250
npz_fname_out='spectrogram_A_n'+str(nfft)+'.npz'
png_fname_out='spectrogram_A_n'+str(nfft)+'.png'
npz_fname_out


# In[31]:


SP=[]

fname_ind=0
t_crop_ind_right=0
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
# SP.append(spectrogram[0:-t_crop_ind_right])
SP.append(spectrogram[0::])

fname_ind=1
t_crop_ind_right=10
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=2
t_crop_ind_right=10
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=3
t_crop_ind_right=10
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=4
t_crop_ind_right=11
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=5
t_crop_ind_right=10
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=6
t_crop_ind_right=11
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=7
t_crop_ind_right=0
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0::])

fname_ind=8
t_crop_ind_right=10
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=9
t_crop_ind_right=11
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])

fname_ind=10
t_crop_ind_right=11
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
SP.append(spectrogram[0:-t_crop_ind_right])


# In[32]:


SPCAT=np.vstack((
    SP[0],np.ones((3,250))*1e-50,SP[1],np.ones((3,250))*1e-50,SP[2],
    np.ones((2,250))*1e-50,SP[3],
    np.ones((3,250))*1e-50,SP[4],
    np.ones((3,250))*1e-50,SP[5],
    np.ones((3,250))*1e-50,SP[6],
    np.ones((3,250))*1e-50,SP[7],
    np.ones((3,250))*1e-50,SP[8],
    np.ones((3,250))*1e-50,SP[9],
    np.ones((3,250))*1e-50,SP[10],
                ))

SPCAT[138:141,125]=0.19
SPCAT[1480:1483,125]=0.19
SPCAT[2823:2826,125]=0.19
SPCAT[4165:4168,125]=0.19
SPCAT[5507:5510,125]=0.19
SPCAT[6849:6852,125]=0.19
SPCAT[8191:8194,125]=0.19
SPCAT[9534:9537,125]=0.19
SPCAT[10876:10879,125]=0.19
SPCAT[12218:12221,125]=0.19

t_axe=np.array([i*period_samples/sr for i in range(SPCAT.shape[0])])


# In[37]:


view_spectrogram_dbshift(t_axe,f_axe/1000,SPCAT,tit="Spectrogram A (nfft="+str(nfft)+")",
                             min_int=-120,max_int=-80,ymin=-125,ymax=125,
                             db_shift=-8.5,savefile=png_fname_out)


# In[36]:


npz_fname_out


# In[34]:


np.savez(npz_fname_out,
     spectrogram=SPCAT,
     f_axe=f_axe, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)


# # Site B

# In[38]:


sr=500000; period_samples=int(0.2*sr); duration_samples=int(0.15*sr)
npz_fnames=['2903201114_spm_n500.npz','2903201115_spm_n500.npz']
nfft=int(npz_fnames[0].split('.')[0].split('_')[-1][1::]) # 500
npz_fname_out='spectrogram_B_n'+str(nfft)+'.npz'
png_fname_out='spectrogram_B_n'+str(nfft)+'.png'
# npz_fname_out


# In[39]:


fname_ind=0
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
t_axe=npz_data["t_axe"];
SP1=np.vstack((np.copy(spectrogram[23::,:]),np.ones((53,len(f_axe)))*1e-50))
SP1[-53::,249]=np.max(spectrogram)


# In[40]:


fname_ind=1
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
t_axe=npz_data["t_axe"];
SP2=np.vstack((np.ones((4,len(f_axe)))*1e-50,np.copy(spectrogram[0::,:])))
SP2[0:4,399]=np.max(spectrogram)


# In[41]:


SPCAT=np.vstack((SP1,SP2,np.ones((26,len(f_axe)))*1e-50))
SPCAT[13474::,249]=np.max(spectrogram)
t_axe=np.array([i*period_samples/sr for i in range(SPCAT.shape[0])])


# In[42]:


view_spectrogram_dbshift(t_axe,f_axe/1000,SPCAT,tit="Spectrogram B (nfft="+str(nfft)+")",
                             min_int=-120,max_int=-80,ymin=-75,ymax=175,
                             db_shift=0,savefile=png_fname_out)


# In[43]:


np.savez(npz_fname_out,
     spectrogram=SPCAT,
     f_axe=f_axe, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)


# # Site C

# In[47]:


sr=333333; period_samples=32772; duration_samples=11000
npz_fnames=['rxdsp-haarp-20110330-012352-p01_spm_n333.npz']
nfft=int(npz_fnames[0].split('.')[0].split('_')[-1][1::]) # 500
npz_fname_out='spectrogram_C_n'+str(nfft)+'.npz'
png_fname_out='spectrogram_C_n'+str(nfft)+'.png'
npz_fname_out


# In[48]:


fname_ind=0
fname=npz_fnames[fname_ind]
npz_data=np.load(fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
t_axe=npz_data["t_axe"];


# In[51]:


view_spectrogram_dbshift(t_axe,f_axe/1000,spectrogram,tit="Spectrogram C (nfft="+str(nfft)+")",
                             min_int=-120,max_int=-80,ymin=-125,ymax=125,
                             db_shift=-2.5,savefile=png_fname_out)


# In[50]:


np.savez(npz_fname_out,
     spectrogram=spectrogram,
     f_axe=f_axe, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)

