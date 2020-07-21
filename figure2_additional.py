import numpy as np
import matplotlib.pyplot as plt

SPM_DB=np.load("../data/SPM_INLINE_DB_freq_res1kHz.npy", allow_pickle=True)
DM_DB=np.load("../data/DM_DB_freq_res1kHz.npy", allow_pickle=True)
BUM_DB=np.load("../data/BUM_DB_freq_res1kHz.npy", allow_pickle=True)
BUM2_DB=np.load("../data/BUM2_DB_freq_res1kHz_thin2.npy", allow_pickle=True)
BUMD_DB=np.load("../data/BUMD_DB_freq_res1kHz.pickle", allow_pickle=True)

db_offset=[-8.7,0,-2.5]
angle={0:"+28°",1:"+21°",2:"+14°",3:"+7°",4:"0°",5:"-7°",6:"-14°",7:"-21°",8:"-28°"}

ffilt=np.array([ 5705.,  5706.,  5707.,  5708.,  5709.,  5710.,  5711.,  5712.,
         5713.,  5714.,  5715.,  5716.,  5717.,  5718.,  5719.,  5720.,
         5721.,  5722.,  5723.,  5724.,  5725.,  5726.,  5727.,  5728.,
         5729.,  5730.,  5731.,  5732.,  5733.,  5734.,  5735.,  5736.,
         5737.,  5738.,  5739.,  5740.])
filt=np.array([  2.49690196e-03,   1.14594179e-03,   8.87009082e-04,
         1.30450145e-03,   2.48832010e-03,   4.41749953e-03,
         6.98679499e-03,   1.15913559e-02,   1.82360152e-02,
         2.83256235e-02,   4.19548090e-02,   6.01183251e-02,
         8.46387569e-02,   1.16327949e-01,   1.61554877e-01,
         2.29067958e-01,   2.68165878e-01,   3.26260806e-01,
         3.84012316e-01,   4.54077893e-01,   5.30090537e-01,
         5.99801779e-01,   6.69364589e-01,   7.35666093e-01,
         7.94395475e-01,   8.51966535e-01,   8.81451874e-01,
         9.14805494e-01,   9.30037487e-01,   9.50427290e-01,
         9.67660898e-01,   9.67894642e-01,   9.69793378e-01,
         9.73829792e-01,   9.82573770e-01,   1.00000000e+00])

DM_NOISE_DB=[]
BUM_NOISE_DB=[]
BUMD_NOISE_DB=[]
for site_ind in range(3):
    DM_NOISE_DB.append([])
    BUM_NOISE_DB.append([])
    BUMD_NOISE_DB.append([])    
    for angle_ind in range(9):
        DM_NOISE_DB[site_ind].append([])
        BUM_NOISE_DB[site_ind].append([])
        BUMD_NOISE_DB[site_ind].append([])
        for dir_ind in range(2):
            DM_NOISE_DB[site_ind][angle_ind].append([])
            BUM_NOISE_DB[site_ind][angle_ind].append([])
            BUMD_NOISE_DB[site_ind][angle_ind].append([])
            for series_ind in range(2):                
                DM_NOISE_DB[site_ind][angle_ind][dir_ind].append([])                
                BUM_NOISE_DB[site_ind][angle_ind][dir_ind].append([])                
                BUMD_NOISE_DB[site_ind][angle_ind][dir_ind].append([])                

site_ind=0; series_ind=1; angle_ind=0; dir_ind=0;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5761.,5762., 5763.,5764.,5765.,5777.,5837.,5927.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5824.,5825.,5826.,5827.,5828.,5829.,5830.,5832.,5833.,5835.,5836.,5837.,5838.]
site_ind=0; series_ind=1; angle_ind=0; dir_ind=1;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5843.,5761.,5762.,5763.,5764.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5833.,5834.,5827.,5829.,5830.,5831.,5832.,5835.,5836.,5837.,5838.]

site_ind=0; series_ind=1; angle_ind=2; dir_ind=0;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5762.,5763.,5764.,5765.,5766.,5767.]
# BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5824.,5825.,5826.,5827.,5828.,5829.,5830.,5832.,5833.,5835.,5836.,5837.,5838.]
BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5779.,  5780.,  5781., 5782.]

site_ind=0; series_ind=1; angle_ind=2; dir_ind=1;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5762.,5763.,5764.,5765.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5807.]
# BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=np.hstack((np.arange(5842.,5860.,1.),np.arange(5885.,5930.,1.)))
BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=np.arange(5885.,5887.,1.)


site_ind=0; series_ind=1; angle_ind=4; dir_ind=0;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5927.,5761.,5762.,5763.,5764.,5765.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5845.,5846.,5847.,5848.,5849.,5850.,5851.,5852.,5853.,5854.]
site_ind=0; series_ind=1; angle_ind=4; dir_ind=1;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5764.,5765.,5766.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5845.,5846.,5847.,5848.,5849.,5850.,5851.,5852.,5853.,5854.]

site_ind=0; series_ind=1; angle_ind=6; dir_ind=0;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5929.,5930.,5762.,5764.,5765.,5769.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5834.,5835.,5836.,5837.,5838.,5839.,5840.,5841.,5842.,5843.,5844.,5845.,5846.,5847.,5848.,5849.,5850.,5851.,5852.]
site_ind=0; series_ind=1; angle_ind=6; dir_ind=1;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5762.,5763.,5764.,5765.,5766.,5767.,5768.,5769.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5834.,5835.,5836.,5837.,5838.,5839.,5840.,5841.,5842.,5843.,5844.,5845.,5846.,5847.,5848.,5849.,5850.,5851.,5852.]

site_ind=0; series_ind=1; angle_ind=8; dir_ind=0;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5761.,5762.,5763.,5764.,5765.,5766.,5767.,5768.,5769.,5823.,5929.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5778.]
site_ind=0; series_ind=1; angle_ind=8; dir_ind=1;
DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5858.,5917.,5819.,5820.,5821.,5822.,5761.,5762.,5763.,5764.,5765.,5766.,5767.,5768.,5769.]
BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind]=[5754.,5755.,5756.,5757.,5758.,5759.,5760.,5761.]

# FIGURE
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
        axs1[-1].set_ylabel('$\Delta f$, kHz')
    else:
        axs1[-1].set_yticks([])
    axs1[-1].set_ylim(-25,150)
    
cbaxes = plt.axes((left_board,bottom_1-0.06,width_1*18+sshift*16,0.01))
cbaxes.set_xlim(-110,-75)
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
    axs2[-1].set_ylim(-110,-75)
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
        axs3[-1].set_ylabel('$\Delta f$, kHz')
    else:
        axs3[-1].set_yticks([])
    axs3[-1].set_xlabel('$f_0$, MHz')
    axs3[-1].set_ylim(0,100)
    axs3[-1].set_xlim(5.700,5.930)
    axs3[-1].set_xticks([5.730,5.830,5.930])
# 


angle_inds=[8,7,6,5,4,3,2,1,0]

# png_filename = 'fig2_spm_all_angles_ser1_Riverview.png'
# site_ind=0
# series_ind=1

# png_filename = 'fig2_spm_all_angles_ser1_Tonsina.png'
# site_ind=1
# series_ind=1

# png_filename = 'fig2_spm_all_angles_ser0_Tiekel.png'
site_ind=1
series_ind=0

#SPM
for angle_ind2 in range(9):
    for dir_ind in range(2):
        angle_ind=angle_inds[angle_ind2]        
        ind=angle_ind2*2+dir_ind
        f0_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][0]
        f_axe=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][1]
        spectrogram=SPM_DB[site_ind][angle_ind][dir_ind][series_ind][2]                
        pcm=axs1[ind].pcolormesh(f0_axe/1000, f_axe/1000,10*np.log10(spectrogram.T)+db_offset[site_ind],vmax=-75,vmin=-110,cmap='jet')
cb = plt.colorbar(pcm, cax = cbaxes, orientation='horizontal')  
cbaxes.set_xlabel('Intensity, dB')

###### ax2
for angle_ind2 in range(9):
                
    angle_ind=angle_inds[angle_ind2]
    ind=angle_ind2
    
    dir_ind=0
    dm_f0= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    dm_freq= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    dm_int= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    bum_f0= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    bum_freq= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    bum_int= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]

    proc_filename = 'C:\\Users\\ashindin\\git\\see_proc\\proc_'+str(site_ind)+str(series_ind)+str(angle_ind)+str(dir_ind)+'.npz'
    print(proc_filename)
    proc_data = np.load(proc_filename)
    bum_f0 = proc_data['bum_f0']
    bum_int = proc_data['bum_int']

    print(bum_f0)
    print(bum_int)
    #
    if site_ind==0:
        for i in range(len(ffilt)):
            if ffilt[i] in dm_f0+(dm_freq/1000).astype(int):
                dm_int[np.where(dm_f0+(dm_freq/1000).astype(int)==ffilt[i])[0][0]]/=filt[i]
    #
    
    if type(BUMD_DB[site_ind][angle_ind][dir_ind][series_ind])!=bool:
        bumd_f0= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
        bumd_freq= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
        bumd_int= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
        for i in range(len(BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
            bumd_int[np.where(bumd_f0==BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan
        if ind==6:
            axs2[ind].plot(bumd_f0/1000,10*np.log10(bumd_int)+db_offset[site_ind],'g',lw=1, label='BUM$_D$/d')
        
    # for i in range(len(DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
    #     dm_int[np.where(dm_f0==DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan
    # for i in range(len(BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
    #     bum_int[np.where(bum_f0==BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan

    if ind==0:
        axs2[ind].plot(dm_f0/1000,10*np.log10(dm_int)+db_offset[site_ind],'r',lw=1,label='DM/d')
        axs2[ind].plot(bum_f0/1000,10*np.log10(bum_int)+db_offset[site_ind],'m',lw=1,label='BUM/d')
    else:
        axs2[ind].plot(dm_f0/1000,10*np.log10(dm_int)+db_offset[site_ind],'r',lw=1)
        axs2[ind].plot(bum_f0/1000,10*np.log10(bum_int)+db_offset[site_ind],'m',lw=1)
    
    dir_ind=1;
    dm_f0= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    dm_freq= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    dm_int= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    for i in range(len(ffilt)):
        if ffilt[i] in dm_f0+(dm_freq/1000).astype(int):
            dm_int[np.where(dm_f0+(dm_freq/1000).astype(int)==ffilt[i])[0][0]]/=filt[i]
    #
    bum_f0= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    bum_freq= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    bum_int= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    if type(BUMD_DB[site_ind][angle_ind][dir_ind][series_ind])!=bool:
        bumd_f0= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
        bumd_freq= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
        bumd_int= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
        for i in range(len(BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
            bumd_int[np.where(bumd_f0==BUMD_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan
        if ind==6:
            axs2[ind].plot(bumd_f0/1000,10*np.log10(bumd_int)+db_offset[site_ind],'c',lw=1,label='BUM$_D$/u')
        else:
            axs2[ind].plot(bumd_f0/1000,10*np.log10(bumd_int)+db_offset[site_ind],'c',lw=1)
        
    # for i in range(len(DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
    #     dm_int[np.where(dm_f0==DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan
    # for i in range(len(BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
    #     bum_int[np.where(bum_f0==BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan

    if ind==0:
        axs2[ind].plot(dm_f0/1000,10*np.log10(dm_int)+db_offset[site_ind],'b',lw=1, label= 'DM/u')
        axs2[ind].plot(bum_f0/1000,10*np.log10(bum_int)+db_offset[site_ind],'k',lw=1, label= 'BUM/u')
        axs2[ind].set_ylabel("SEE intensity, dB", labelpad=0)
    else:
        axs2[ind].plot(dm_f0/1000,10*np.log10(dm_int)+db_offset[site_ind],'b',lw=1)
        axs2[ind].plot(bum_f0/1000,10*np.log10(bum_int)+db_offset[site_ind],'k',lw=1)
    
    axs2[ind].set_ylim([-110,-73])


axs2[0].legend(loc=2, handlelength=1)
axs2[6].legend(loc=3, handlelength=1)

#AXS3
fgyro=[5733.52,5738.6,5731.5,5751.5,5721.] # ВЕРА ПРОВЕРИЛА!!
fgyro=[5725, 5738, 5734, 5749, 5730] # А СЕРГЕЕВ ПЕРЕДЕЛАЛ!!!

for angle_ind2 in range(9):
                
    angle_ind=angle_inds[angle_ind2]
    ind=angle_ind2
    
    dir_ind=0;
    dm_f0= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    dm_freq= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    dm_int= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    bum_f0= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    bum_freq= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    bum_int= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    
    if type(BUM2_DB[site_ind][angle_ind][dir_ind][series_ind])!=bool:
        bum2_f0= BUM2_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
        bum2_freq= BUM2_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
        bum2_int= BUM2_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
        col='y'
        bum2_int[np.where(bum2_int<1e-49)]=np.nan
        bum2_freq[np.where(bum2_int<1e-49)]=np.nan
    
    if type(BUMD_DB[site_ind][angle_ind][dir_ind][series_ind])!=bool:
        bumd_f0= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
        bumd_freq= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
        bumd_int= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
        axs3[ind].plot(bumd_f0/1000,bumd_freq/1000,'g',lw=1)
        
    for i in range(len(DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
        dm_int[np.where(dm_f0==DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan
    for i in range(len(BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
        bum_int[np.where(bum_f0==BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan

    if ind in [0]:
#     if ind in [0,3]:
        bum_f02=np.arange(5700,5800)
    else:
        bum_f02=np.arange(5700,5850)
    
#     axs[ind].plot(bum_f02,bum_f02*bum_coeffs[ind][dir_ind][0]+bum_coeffs[ind][dir_ind][1],'m',lw=1)
    axs3[ind].plot(bum_f0/1000,bum_freq/1000,color=(0.75, 0.0, 0.75, .5),lw=1)
#     axs3[ind].plot(bum_f02,bum_f02*bum_coeffs[ind][dir_ind][0]+bum_coeffs[ind][dir_ind][1],color=(0.75, 0.0, 0.75, .5),lw=1)
    axs3[ind].plot(bum_f0/1000,bum_freq/1000,'m',lw=1)
    
    
    dir_ind=1;
    dm_f0= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    dm_freq= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    dm_int= DM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    bum_f0= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
    bum_freq= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
    bum_int= BUM_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
    if type(BUM2_DB[site_ind][angle_ind][dir_ind][series_ind])!=bool:
        bum2_f0= BUM2_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
        bum2_freq= BUM2_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
        bum2_int= BUM2_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
        col='orange'
        bum2_int[np.where(bum2_int<1e-49)]=np.nan
        bum2_freq[np.where(bum2_int<1e-49)]=np.nan
        
        
    if type(BUMD_DB[site_ind][angle_ind][dir_ind][series_ind])!=bool:
        bumd_f0= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,0]
        bumd_freq= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,1]
        bumd_int= BUMD_DB[site_ind][angle_ind][dir_ind][series_ind][:,2]
#      
        bumd_f03=np.arange(5750,5900)

        axs3[ind].plot(bumd_f0/1000,bumd_freq/1000,color=(0.0, 0.75, 0.75, 1.),lw=1)
        
        
    for i in range(len(DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
        dm_int[np.where(dm_f0==DM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan
    for i in range(len(BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind])):
        bum_int[np.where(bum_f0==BUM_NOISE_DB[site_ind][angle_ind][dir_ind][series_ind][i])[0][0]]=np.nan

        
    axs3[ind].plot(bum_f0/1000,bum_freq/1000,'k',lw=1)
    
# plt.savefig(png_filename,dpi=300)
plt.show() 