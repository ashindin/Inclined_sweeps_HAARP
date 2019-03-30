#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, sys
import numpy as np
import scipy.signal as ss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# In[10]:


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the
def get_raw_data_from_binary_file(fname,offset_samples,duration_samples,bit_depth,num_of_channels):
    f=open(fname,'rb')
    offset_bytes=offset_samples*(bit_depth//8)*num_of_channels
    f.seek(offset_bytes,0)
    data_raw=f.read(int(duration_samples*int(bit_depth/8)*num_of_channels))
    f.close()
    return data_raw
def raw_to_complex_volts(data_raw,nc,v_range,bit_depth=16):
    if bit_depth==16:
        data=np.frombuffer(data_raw,dtype=np.int16)
        data=np.reshape(data,(nc,int(len(data_raw)/nc/2)),'F')*v_range/32767
        data_complex=np.zeros((int(nc/2),int(len(data_raw)/nc/2)),dtype=np.complex128)
        for i in range(int(nc/2)):
            data_complex[i,:]=data[2*i,:]+1j*data[2*i+1,:]
    elif bit_depth==32:
        data=np.frombuffer(data_raw,dtype=np.int32)
        data=np.reshape(data,(nc,int(len(data_raw)/nc/4)),'F')*v_range/2147483647
        data_complex=np.zeros((int(nc/2),int(len(data_raw)/nc/4)),dtype=np.complex128)
        for i in range(int(nc/2)):
            data_complex[i,:]=data[2*i,:]+1j*data[2*i+1,:]
    return data_complex
def get_spectrogram(fname, offset_samples, period_samples, duration_samples, sr,bd,nc, channel=0, nfft=0, num_of_pulses=0,v_range=0.5,waitbar=True):    
#     sr,bd,nc,ns=get_wv_file_parameters(fname)
    fsize=os.path.getsize(fname) # file size
    ns=fsize//(bd//8)//nc
    
    if nfft==0:
        nfft=int(sr/1000) # freq. res. 1kHz
    if num_of_pulses==0:
        num_of_pulses=int((ns-offset_samples)/period_samples)
    t_axe=np.array([i*period_samples/sr for i in range(num_of_pulses)])
    SPECTROGRAM=np.zeros((num_of_pulses,nfft))
    if waitbar==True:
        for i in range(num_of_pulses):
            progress(i, num_of_pulses, status='Calculating spectrogram')
#             data_raw=get_raw_data_from_wv_file(fname,offset_samples+i*period_samples,duration_samples)
            data_raw=get_raw_data_from_binary_file(fname,offset_samples+i*period_samples,duration_samples,bd,nc)
            data_complex=raw_to_complex_volts(data_raw,nc,v_range,bit_depth=bd)[channel,:]
            f_axe,spec=ss.welch(data_complex,fs=sr,nperseg=nfft,noverlap = nfft-1,scaling='spectrum',window='hanning',detrend=None, return_onesided=False)
            SPECTROGRAM[i,:]=np.hstack((spec[int(nfft/2)::],spec[0:int(nfft/2)]))    
    else:
        for i in range(num_of_pulses):
#             data_raw=get_raw_data_from_wv_file(fname,offset_samples+i*period_samples,duration_samples)
            data_raw=get_raw_data_from_binary_file(fname,offset_samples+i*period_samples,duration_samples,bd,nc)
            data_complex=raw_to_complex_volts(data_raw,nc,v_range,bit_depth=bd)[channel,:]
            f_axe,spec=ss.welch(data_complex,fs=sr,nperseg=nfft,noverlap = nfft-1,scaling='spectrum',window='hanning',detrend=None, return_onesided=False)
            SPECTROGRAM[i,:]=np.hstack((spec[int(nfft/2)::],spec[0:int(nfft/2)])) 
    f_axe=np.hstack((f_axe[int(nfft/2)::],f_axe[0:int(nfft/2)]))
    return SPECTROGRAM, f_axe, t_axe
def view_spectrogram_dbshift(t_axe,f_axe,spectrogram,tit='',min_int=-120,max_int=-90,ymin=0,ymax=0,db_shift=0,savefile="",close_fig=False):
    fig=plt.figure(figsize=(9,6))
    plt.pcolormesh(t_axe,f_axe,10*np.log10(spectrogram.T)+db_shift,vmax=max_int,vmin=min_int,cmap='jet')
    plt.xlim(t_axe[0],t_axe[-1])
    #if ymin==0:
    if ymax==0:
        ymin=f_axe[0]
        ymax=f_axe[-1]
    plt.ylim(ymin,ymax)
#     plt.grid()
    plt.colorbar()
    plt.title(tit)    
    if savefile!="":
        plt.savefig(savefile)
        plt.close()
    if close_fig==False:
        plt.show()


# In[16]:


bin_fnames=[
'spew_110330_012948_05830_0250_01_01.DRXS12.raw', # 00
'spew_110330_013028_05830_0250_01_01.DRXS12.raw', # 01
'spew_110330_013456_05830_0250_01_01.DRXS12.raw', # 02
'spew_110330_013925_05830_0250_01_01.DRXS12.raw', # 03
'spew_110330_014353_05830_0250_01_01.DRXS12.raw', # 04
'spew_110330_014821_05830_0250_01_01.DRXS12.raw', # 05
'spew_110330_015250_05830_0250_01_01.DRXS12.raw', # 06
'spew_110330_015718_05830_0250_01_01.DRXS12.raw', # 07
'spew_110330_020147_05830_0250_01_01.DRXS12.raw', # 08
'spew_110330_020615_05830_0250_01_01.DRXS12.raw', # 09
'spew_110330_021044_05830_0250_01_01.DRXS12.raw', # 10
# 'spew_110330_021500_06900_0250_01_01.DRXS12.raw', # 11
# 'spew_110330_021509_04850_0016_01_00.DRXS12.raw', # 12
]
bd=32; nc=2; sr=250000;v_range=0.5;


# In[17]:


f_center=np.ones(len(bin_fnames),dtype=np.int)*5830000;
start_offsets=np.array([
    2970000, # 00 - spew_110330_012948_05830_0250_01_01.DRXS12.bin
    32000, # 01 - spew_110330_013028_05830_0250_01_01.DRXS12.bin
    5000, # 02 - spew_110330_013456_05830_0250_01_01.DRXS12.bin
    0, # 03 - spew_110330_013925_05830_0250_01_01.DRXS12.bin
    22000, # 04 - spew_110330_014353_05830_0250_01_01.DRXS12.bin
    32000, # 05 - spew_110330_014821_05830_0250_01_01.DRXS12.bin
    25000, # 06 - spew_110330_015250_05830_0250_01_01.DRXS12.bin
    23000, # 07 - spew_110330_015718_05830_0250_01_01.DRXS12.bin
    29000, # 08 - spew_110330_020147_05830_0250_01_01.DRXS12.bin
    16000, # 09 - spew_110330_020615_05830_0250_01_01.DRXS12.bin
    10000, # 10 - spew_110330_021044_05830_0250_01_01.DRXS12.bin
#     0, # 11 - spew_110330_021500_06900_0250_01_01.DRXS12.bin
#     0, # 12 - spew_110330_021509_04850_0016_01_00.DRXS12.bin
])


# In[18]:


nfft=2500
period_samples=int(0.2*sr)
duration_samples=int(0.15*sr)


# In[19]:


npz_fnames=[os.path.split(bin_fnames[i])[1].split('.')[0]+"_spm_n"+str(nfft)+".npz" for i in range(len(bin_fnames))]
# print(npz_fnames)
png_fnames=[os.path.split(bin_fnames[i])[1].split('.')[0]+"_spm_n"+str(nfft)+".png" for i in range(len(bin_fnames))]
# print(png_fnames)


# In[ ]:


# SP_RAW=[]
for i in range(len(bin_fnames)):
    print("Processing "+bin_fnames[i])
    SP_temp, f_axe, t_axe=get_spectrogram(bin_fnames[i], start_offsets[i], period_samples, duration_samples, sr,bd,nc, channel=0, nfft=nfft, num_of_pulses=0,v_range=0.5,waitbar=True)    
#     SP_RAW.append(SP_temp)
    save_filename=npz_fnames[i]    
    np.savez(save_filename,
         source_filename=os.path.split(bin_fnames[i])[1],
         spectrogram=SP_temp,
         f_axe=f_axe, t_axe=t_axe, nfft=nfft,
         offset_samples=start_offsets[i],
         duration_samples=duration_samples,
         period_samples=period_samples)
    view_spectrogram_dbshift(t_axe,f_axe/1000,SP_temp,tit=bin_fnames[i],
                             min_int=-120,max_int=-60,ymin=-125,ymax=125,
                             db_shift=0,savefile=png_fnames[i])


# In[ ]:




