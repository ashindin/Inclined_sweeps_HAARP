#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


def get_st_t_indxs(series_ind=0,angle_ind=0,dir_ind=0):
    if series_ind==0:
        if dir_ind==0:            
            st_ind=300+angle_ind*750
        else:
            st_ind=500+angle_ind*750
    else:
        if dir_ind==0:            
            st_ind=13050-angle_ind*750
        else:
            st_ind=13250-angle_ind*750   
    
    return st_ind


# In[4]:


f0_axe_up=np.linspace(5730,5929,200)
f0_axe_down=np.flip(np.linspace(5731,5930,200),axis=0)
t_axe_local=np.arange(0.,40.,.2)


# In[3]:


inline_spm_fnames=[
'f0shifted_spm_A_n2500.npz',
'f0shifted_spm_B_n5000.npz',
'f0shifted_spm_C_n3330.npz'
]
output_fname='spm_database_100Hz.npy'


# In[7]:


SPM_DB=[]
for site_ind in range(3):
    npz_data=np.load(inline_spm_fnames[site_ind]);
    spectrogram=npz_data["spectrogram"];
    f_axe=npz_data["f_axe"];
    t_axe=npz_data["t_axe"];
    nfft=npz_data["nfft"];
#     f_center=npz_data["f_center"];
#     site_file=npz_data["site"];
    
    SPM_DB.append([])
    for angle_ind in range(9):
        SPM_DB[site_ind].append([])
        for dir_ind in range(2):
            SPM_DB[site_ind][angle_ind].append([])
            for series_ind in range(2):
                st_ind=get_st_t_indxs(series_ind=series_ind,angle_ind=angle_ind,dir_ind=dir_ind)
                if dir_ind==0:
                    SPM_DB[site_ind][angle_ind][dir_ind].append((f0_axe_down,f_axe,spectrogram[st_ind:st_ind+200,:]))                
                else:
                    SPM_DB[site_ind][angle_ind][dir_ind].append((f0_axe_up,f_axe,spectrogram[st_ind:st_ind+200,:]))        

np.save(output_fname,SPM_DB)





