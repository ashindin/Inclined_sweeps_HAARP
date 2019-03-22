#!/usr/bin/env python
# coding: utf-8

# In[57]:


import numpy as np
import matplotlib.pyplot as plt


# In[58]:


def view_spectrogram_dbshift(t_axe,f_axe,spectrogram,tit='',min_int=-120,max_int=-90,ymin=0,ymax=0,db_shift=0,savefile="",close_fig=False):
    fig=plt.figure(figsize=(20,6))
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

# In[59]:


full_spm_fname='spectrogram_A_n250.npz'
npz_fname_out=full_spm_fname.replace('spectrogram','f0shifted_spm')
png_fname_out=npz_fname_out.replace('.npz','.png')
npz_fname_out2=npz_fname_out.replace('.npz','_filt.npz')
png_fname_out2=png_fname_out.replace('.png','_filt.png')
# png_fname_out2


# In[60]:


npz_data=np.load(full_spm_fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
t_axe=npz_data["t_axe"];
nfft=npz_data["nfft"];
duration_samples=npz_data["duration_samples"];
period_samples=npz_data["period_samples"];


# In[61]:


f0_ind=np.argmax(spectrogram,1)
fm=f_axe[f0_ind]/1000+5830


# In[62]:


f_axe_new=np.linspace(-249,250,500)
spm_inline=np.ones((len(f0_ind),len(f_axe_new)))*1e-50
for i in range(len(f0_ind)):
    temp=-f0_ind[i]+250
    spm_inline[i,temp:temp+250]=spectrogram[i,:]


# In[63]:


view_spectrogram_dbshift(t_axe,f_axe_new,spm_inline,tit="$f_0$-shifted spectrogram A (nfft="+str(nfft)+")",
                             min_int=-120,max_int=-80,ymin=-50,ymax=150,
                             db_shift=-8.7,savefile=png_fname_out)


# In[64]:


np.savez(npz_fname_out,
     spectrogram=spm_inline,
     f_axe=f_axe_new*1000, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)

# Filtering
def denoise(data,inds,rad):
    data_filt=np.copy(data)
    for ind in inds:
#         data_filt[ind-rad:ind+rad+1]=0.5*(data_filt[ind-rad-1]+data_filt[ind+rad+1])
        data_filt[ind-rad:ind+rad+1]=1e-50
    return data_filt
f_int_inds=[50, 105, 185, 214, 225, 230, 235, 245]
rad=3;
spectrogram_filt=np.zeros_like(spectrogram)
for i in range(len(t_axe)):
    spectrogram_filt[i,:]=denoise(spectrogram[i,:],f_int_inds,rad)
f_axe_new=np.linspace(-249,250,500)
spm_inlinef=np.ones((len(f0_ind),len(f_axe_new)))*1e-50
for i in range(len(f0_ind)):
    temp=-f0_ind[i]+250
    spm_inlinef[i,temp:temp+250]=spectrogram_filt[i,:]
np.savez(npz_fname_out2,
     spectrogram=spm_inlinef,
     f_axe=f_axe_new*1000, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)
     
# # Site B

# In[65]:


full_spm_fname='spectrogram_B_n500.npz'
npz_fname_out=full_spm_fname.replace('spectrogram','f0shifted_spm')
png_fname_out=npz_fname_out.replace('.npz','.png')
# png_fname_out


# In[66]:


npz_data=np.load(full_spm_fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
t_axe=npz_data["t_axe"];
nfft=npz_data["nfft"];
duration_samples=npz_data["duration_samples"];
period_samples=npz_data["period_samples"];


# In[67]:


f0_ind=np.argmax(spectrogram,1)
fm=f_axe[f0_ind]/1000+5780


# In[68]:


f_axe_new=np.linspace(-499,500,1000)
spm_inline=np.ones((len(f0_ind),len(f_axe_new)))*1e-50
for i in range(len(f0_ind)):
    temp=-f0_ind[i]+500
    spm_inline[i,temp:temp+500]=spectrogram[i,:]


# In[69]:


view_spectrogram_dbshift(t_axe,f_axe_new,spm_inline,tit="$f_0$-shifted spectrogram B (nfft="+str(nfft)+")",
                             min_int=-120,max_int=-80,ymin=-50,ymax=150,
                             db_shift=0,savefile=png_fname_out)


# In[70]:


np.savez(npz_fname_out,
     spectrogram=spm_inline,
     f_axe=f_axe_new*1000, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)


# # Site C

# In[71]:


full_spm_fname='spectrogram_C_n333.npz'
npz_fname_out=full_spm_fname.replace('spectrogram','f0shifted_spm')
png_fname_out=npz_fname_out.replace('.npz','.png')
png_fname_out


# In[72]:


npz_data=np.load(full_spm_fname);    
spectrogram=npz_data["spectrogram"];
f_axe=npz_data["f_axe"];
t_axe=npz_data["t_axe"];
nfft=npz_data["nfft"];
duration_samples=npz_data["duration_samples"];
period_samples=npz_data["period_samples"];


# In[73]:


f0_ind=np.argmax(spectrogram,1)
fm=f_axe[f0_ind]/1000+5830


# In[74]:


f_axe_new=np.linspace(-332,333,666)
spm_inline=np.ones((len(f0_ind),len(f_axe_new)))*1e-50
for i in range(len(f0_ind)):
    temp=-f0_ind[i]+333
    spm_inline[i,temp:temp+333]=spectrogram[i,:]


# In[75]:


view_spectrogram_dbshift(t_axe,f_axe_new,spm_inline,tit="$f_0$-shifted spectrogram C (nfft="+str(nfft)+")",
                             min_int=-120,max_int=-80,ymin=-50,ymax=150,
                             db_shift=-2.5,savefile=png_fname_out)


# In[76]:


np.savez(npz_fname_out,
     spectrogram=spm_inline,
     f_axe=f_axe_new*1000, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)

