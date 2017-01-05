from linslens import EELsModels_huge as L
import numpy as np
import pylab as pl
from linslens import EELsKeckModels as K
from linslens.Plotter import *
import colorImage
from scipy import ndimage
from jeans.makemodel import deproject
import lenslib
import glob
from linslens.Profiles import *
from astLib import astCalc


def clip(arr,nsig=3.5):
    a = arr.flatten()
    m,s,l = a.mean(),a.std(),a.size
    while 1:
        a = a[abs(a-m)<s*nsig]
        if a.size==l:
            return m,s
        m,s,l = a.mean(),a.std(),a.size


def MakeTab(model,kmodel,name):
    model.Initialise()
    imgs,sigs,mods = model.imgs, model.sigs,model.models
    xm,ym = int(imgs[0].shape[1]/2.),int(imgs[0].shape[0]/2.)
    if name == 'J1606':
        ym -= 10
    for i in range(len(imgs)):
        imgs[i] = imgs[i][ym-30:ym+30,xm-30:xm+30]
        sigs[i] = sigs[i][ym-30:ym+30,xm-30:xm+30]
        mods[i] = mods[i][ym-30:ym+30,xm-30:xm+30]
    pl.figure(figsize=(30,6))
    
    xx,yy = np.arange(5,26,1), np.ones(21)*5.
    pl.subplot(143)
    ###
    ###
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])
    resid = (imgs[0]-mods[0])/sigs[0]
    m,s = clip(resid)
    resid-=m
    pl.imshow(resid,interpolation='nearest',origin='lower',cmap='gray_r',vmin=-1*s,vmax=7.5*s)
    ###
    kmodel.Initialise()
    img,sig,mod = kmodel.img,kmodel.sig,kmodel.model
    if name in ['J1218','J1347','J1606','J2228']:
        scale = 5./3
    elif name in ['J0837','J0901','J0913','J1125','J1144','J1323','J1446','J1605','J1619']:
        scale = 5.
    xm,ym = int(img.shape[1]/2.), int(img.shape[0]/2.)
    if name == 'J1606':
        ym -= 10*scale

    img = img[ym-30*scale:ym+30*scale,xm-30*scale:xm+30*scale]
    sig = sig[ym-30*scale:ym+30*scale,xm-30*scale:xm+30*scale]
    mod = mod[ym-30*scale:ym+30*scale,xm-30*scale:xm+30*scale]
    pl.subplot(144)
    ###
    
    pl.subplot(141)
    CI = colorImage.ColorImage()
    CI.nonlin = 40.
    V,I,K = imgs[0],imgs[1],img
    dxi,dyi = model.Ddic['xoffset'],model.Ddic['yoffset']
    dxk,dyk = kmodel.Ddic['xoffset']+kmodel.Dx,kmodel.Ddic['yoffset']+kmodel.Dy
    I = ndimage.shift(I,[dyi,dxi])
    
    K = ndimage.zoom(K,1./scale)

    K = ndimage.shift(K,[-shifts[name][1],-shifts[name][0]])

    vki = CI.createModel(V,I,K)
    pl.imshow(vki,interpolation='nearest',origin='lower')
    pl.plot(xx,yy,color='White',lw=4)
    pl.imshow(vki,interpolation='nearest',origin='lower')  
    pl.figtext(0.065,0.24,"$1''$",color='White',fontsize=45,weight=1000,family='sans-serif',stretch='ultra-expanded')  
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])
    
    # colour model
    pl.subplot(142)
    V,I,K = mods[0],mods[1],mod
    I = ndimage.shift(I,[dyi,dxi])
    K = ndimage.zoom(K,1./scale)
    K = ndimage.shift(K,[-shifts[name][1],-shifts[name][0]])

    vki = CI.createModel(V,I,K)
    pl.imshow(vki,interpolation='nearest',origin='lower')
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])

    ## FINALLY, lug in the DM slope thing!
    dir = '/data/ljo31b/EELs/galsub/emceeruns/'
    
    file = glob.glob(dir+name+'_parametric_DPL*')
    file.sort()
    f = file[-1]
    result_DPL = np.load(f)
    lp_DPL,trace_DPL,dic_DPL,_ = result_DPL
    a1_DPL,a3_DPL = np.unravel_index(lp_DPL[:,0].argmax(),lp_DPL[:,0].shape)
    zl = lz[name][0]
    scale = astCalc.da(zl)*np.pi/180./3600 * 1e3
    
    gamma = dic_DPL['Lens 1 gamma'][a1_DPL,0,a3_DPL]
    rs = dic_DPL['Lens 1 rs'][a1_DPL,0,a3_DPL]*0.05*scale
    gamma_l = np.percentile(dic_DPL['Lens 1 gamma'][:,0].ravel(),16)
    gamma_u = np.percentile(dic_DPL['Lens 1 gamma'][:,0].ravel(),84)
    rs_l = np.percentile(dic_DPL['Lens 1 rs'][:,0].ravel(),16)
    rs_u = np.percentile(dic_DPL['Lens 1 rs'][:,0].ravel(),84)

    r = np.logspace(-7,3,3500)
    dpdr_DPL = dlogrho_dlogr_gNFW(r,gamma,rs)
    dpdr_DPL_l = dlogrho_dlogr_gNFW(r,gamma_l,rs)
    dpdr_DPL_u = dlogrho_dlogr_gNFW(r,gamma_u,rs)

    pl.subplot(144)
    pl.plot(r,dpdr_DPL,color='SteelBlue',label='dark matter')
    pl.legend(loc='lower right',ncol=2,fontsize=15)
    pl.ylabel('density slope')
    pl.xlabel('radius (kpc)')
    pl.fill_between(r,dpdr_DPL_l, dpdr_DPL_u, color='LightBlue',alpha=0.5)
    pl.locator_params(axis='y',nbins=3)
    pl.locator_params(axis='x',nbins=3)

    cat = np.load('/data/ljo31/Lens/LensParams/Structure_lensgals_2src.npy')[0]
    rein = cat[name]['Lens 1 b']*0.05*scale

    pl.axvline(rein,color='k',ls='--',label='Einstein radius',lw=2) # Einstein radius

    pl.xlim([0,10])
    pl.ylim([-2.4,-2.1])

    pl.figtext(0.05,0.8,'data',fontsize=30,color='white')
    pl.figtext(0.3,0.8,'model',fontsize=30,color='white')
    pl.figtext(0.55,0.8,'S/N residuals',fontsize=30,color='k')
    pl.savefig('/home/ljo31/Documents/Proposals/EEL'+name+'.pdf')
    pl.show()
 

dir = '/data/ljo31/Lens/LensModels/twoband/'
sz = np.load('/data/ljo31/Lens/LensParams/SourceRedshiftsUpdated.npy')[()]
names = sz.keys()
names.sort()
shifts = [['J0837',[1.3,2.9]],['J0901',[0,3]],['J0913',[0,0]],['J1125',[0.9,2.1]],['J1144',[-0.8,4.55]],['J1218',[-3.2,-6.8]],['J1323',[1.0,1.1]],['J1347',[3.7,0]],['J1446',[0,0]],['J1605',[-3.5,0.1]],['J1606',[-4.8,7.6]],['J1619',[3.8,0]],['J2228',[-2.4,-3.6]]]
        
shifts = dict(shifts)
lz = np.load('/data/ljo31/Lens/LensParams/LensRedshiftsUpdated.npy')[()]


for name in names:
    if name == 'J1248':
        continue
    if name != 'J0837':
        continue
    try:
        result = np.load(dir+name+'_212')
        kresult = np.load(dir+name+'_Kp_212')
    except:
        if name == 'J1347':
            result = np.load(dir+name+'_112')
            kresult = np.load('/data/ljo31/Lens/J1347/twoband_Kp_112_2')
        elif name == 'J1619':
            result = np.load(dir+name+'_212')
            kresult = np.load(dir+name+'_Kp_212_lensandgalon')
            print 'J1619'                                                                                                                                                                                                       
        else:
            result = np.load(dir+name+'_211')
            kresult = np.load(dir+name+'_Kp_211')
    
    model = L.EELs(result, name)
    kmodel = K.EELs(kresult,result,name)
    MakeTab(model,kmodel,name)

