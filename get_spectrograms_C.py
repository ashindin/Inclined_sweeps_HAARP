#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, sys
import numpy as np
import scipy.signal as ss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# In[11]:


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the
def get_raw_data_from_binary_file(fname,offset_samples,duration_samples,bit_depth,num_of_channels):
    f=open(fname,'rb')
    offset_bytes=int(offset_samples*int(bit_depth/8)*num_of_channels)
#     print(offset_bytes)
    f.seek(offset_bytes,0)
    data_raw=f.read(int(duration_samples*int(bit_depth/8)*num_of_channels))
    f.close()
    return data_raw
def raw_to_complex_volts(data_raw,nc,v_range,bit_depth=16):
    if bit_depth==16:
        data=np.frombuffer(data_raw,dtype='>i2')
        data=np.reshape(data,(nc,int(len(data_raw)/nc/2)),'F')*v_range/32767
        data_complex=np.zeros((int(nc/2),int(len(data_raw)/nc/2)),dtype=np.complex128)
        for i in range(int(nc/2)):
            data_complex[i,:]=data[2*i,:]+1j*data[2*i+1,:]
    elif bit_depth==32:
        data=np.fromstring(data_raw,dtype=np.int32)
        data=np.reshape(data,(nc,int(len(data_raw)/nc/4)),'F')*v_range/2147483647
        data_complex=np.zeros((int(nc/2),int(len(data_raw)/nc/4)),dtype=np.complex128)
        for i in range(int(nc/2)):
            data_complex[i,:]=data[2*i,:]+1j*data[2*i+1,:]
    return data_complex
def raw_to_int16(data_raw):
    data=np.frombuffer(data_raw,dtype='>i2')
    return data
def get_spectrogram(fname, offset_samples, period_samples, duration_samples, sr,bd,nc, channel=0, nfft=0, num_of_pulses=0,v_range=0.5,waitbar=True):    
#     sr,bd,nc,ns=get_wv_file_parameters(fname)
    fsize=os.path.getsize(fname) # file size
    ns=int(fsize/int(bd/8)/nc)
    if nfft==0:
        nfft=int(sr/1000) # freq. res. 1kHz
    if num_of_pulses==0:
        num_of_pulses=int((ns-offset_samples)/period_samples)
#     t_axe=np.array([i*period_samples/sr for i in range(num_of_pulses)])
    SPECTROGRAM=np.zeros((num_of_pulses,nfft))
    if waitbar==True:
        for i in range(num_of_pulses):
            progress(i, num_of_pulses, status='Calculating spectrogram')
#             data_raw=get_raw_data_from_wv_file(fname,offset_samples+i*period_samples,duration_samples)
            data_raw=get_raw_data_from_binary_file(fname,offset_samples+i*period_samples,duration_samples,bd,nc)
            data_complex=raw_to_complex_volts(data_raw,nc,v_range,bit_depth=bd)[channel,:]
            f_axe,spec=ss.welch(data_complex,fs=sr,nperseg=nfft,noverlap = nfft-1,scaling='spectrum',window='hanning',detrend=None,return_onesided=False)
            SPECTROGRAM[i,:]=np.hstack((spec[int(nfft/2)::],spec[0:int(nfft/2)]))    
    else:
        for i in range(num_of_pulses):
#             data_raw=get_raw_data_from_wv_file(fname,offset_samples+i*period_samples,duration_samples)
            data_raw=get_raw_data_from_binary_file(fname,offset_samples+i*period_samples,duration_samples,bd,nc)
            data_complex=raw_to_complex_volts(data_raw,nc,v_range,bit_depth=bd)[channel,:]
            f_axe,spec=ss.welch(data_complex,fs=sr,nperseg=nfft,noverlap = nfft-1,scaling='spectrum',window='hanning',detrend=None,return_onesided=False)
            SPECTROGRAM[i,:]=np.hstack((spec[int(nfft/2)::],spec[0:int(nfft/2)])) 
    f_axe=np.hstack((f_axe[int(nfft/2)::],f_axe[0:int(nfft/2)]))
    if nfft % 2 != 0:
        f_axe=np.roll(f_axe,-1)
        spec=np.roll(f_axe,-1)
    t_axe=np.arange(0,SPECTROGRAM.shape[0]*0.4,0.4)
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


# In[7]:


fname="rxdsp-haarp-20110330-012352-p01.data"
print(fname)
bd=16; nc=2; sr=333333; v_range=0.5;
nfft=3330


# In[9]:


npz_fnames=fname.split('.')[0]+"_spm_n"+str(nfft)+".npz"
# print(npz_fnames)
png_fnames=fname.split('.')[0]+"_spm_n"+str(nfft)+".png"
# print(png_fnames)


# In[ ]:


offset_samples=23215; period_samples=32772; duration_samples=11000
SP1, f_axe1, t_axe1=get_spectrogram(fname, offset_samples, period_samples, duration_samples, sr,bd,nc, channel=0, nfft=nfft, num_of_pulses=0,v_range=0.5,waitbar=True)
offset_samples=8215; period_samples=32772; duration_samples=11000
SP2, f_axe2, t_axe2=get_spectrogram(fname, offset_samples, period_samples, duration_samples, sr,bd,nc, channel=0, nfft=nfft, num_of_pulses=0,v_range=0.5,waitbar=True)   


# In[ ]:


SP1=SP1[919:-1,:]
SP2=SP2[920::,:]
SPCAT=np.zeros((SP1.shape[0]+SP2.shape[0],SP1.shape[1]))
for i in range(SP1.shape[0]):
    SPCAT[2*i,:]=SP1[i,:]
    SPCAT[2*i+1,:]=SP2[i,:]
SPCAT=SPCAT[0:13500,:]
t_axe=np.array([i*0.4 for i in range(SPCAT.shape[0])])


# In[ ]:


np.savez(npz_fnames,
     spectrogram=SPCAT,
     f_axe=f_axe1, t_axe=t_axe, nfft=nfft,     
     duration_samples=duration_samples,
     period_samples=period_samples)


# In[ ]:


view_spectrogram_dbshift(t_axe,f_axe1/1000,SPCAT,tit=fname,
                             min_int=-120,max_int=-80,ymin=-125,ymax=165,
                             db_shift=0,savefile=png_fnames)

