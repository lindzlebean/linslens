from linslens import EELsModels_huge as L
import numpy as np
import pylab as pl
from linslens import EELsKeckModels as K
from linslens.Plotter import *
import colorImage
from scipy import ndimage

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
    pl.figure(figsize=(30,8))
    pl.figtext(0.05,0.8,name,fontsize=40,color='White')
    # scale bar?
    xx,yy = np.arange(5,26,1), np.ones(21)*5.
    pl.subplot(142)
    ###
    pl.figtext(0.28,0.8,'V',fontsize=40)
    ###
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])
    resid = (imgs[0]-mods[0])/sigs[0]
    m,s = clip(resid)
    resid-=m
    pl.imshow(resid,interpolation='nearest',origin='lower',cmap='gray_r',vmin=-1*s,vmax=7.5*s)
    pl.subplot(143)
    ###
    pl.figtext(0.53,0.8,'I',fontsize=40)
    ###
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])
    resid = (imgs[1]-mods[1])/sigs[1]
    m,s = clip(resid)
    resid-=m
    pl.imshow(resid,interpolation='nearest',origin='lower',cmap='gray_r',vmin=-1*s,vmax=7.5*s)
    kmodel.Initialise()

    img,sig,mod = kmodel.img,kmodel.sig,kmodel.model
    if name in ['J1218','J1347','J1606','J2228']:
        scale = 5./3
    elif name in ['J0837','J0901','J0913','J1125','J1144','J1323','J1446','J1605','J1619']:
        scale = 5.
    xm,ym = int(img.shape[1]/2.), int(img.shape[0]/2.)
    if name == 'J1606':
        ym -= 10*scale
    '''if scale*30>xm: 
        scale2 = int(xm/30.)
    else:
        scale2 = scale
    if scale*30.>ym:
        scale1 = int(ym/30.)
    else:
        scale1=scale
    scale3 = np.min((scale1,scale2))'''
    img = img[ym-30*scale:ym+30*scale,xm-30*scale:xm+30*scale]
    sig = sig[ym-30*scale:ym+30*scale,xm-30*scale:xm+30*scale]
    mod = mod[ym-30*scale:ym+30*scale,xm-30*scale:xm+30*scale]
    pl.subplot(144)
    ###
    pl.figtext(0.78,0.8,'K',fontsize=40)
    ###
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])
    resid = (img-mod)/sig
    m,s = clip(resid)
    resid-=m
    pl.imshow((img-mod)/sig,interpolation='nearest',origin='lower',cmap='gray_r',vmin=-1*s,vmax=7.5*s)
    #if name == 'J1619':
    #    pl.imshow((img-mod)/sig,interpolation='nearest',origin='lower',cmap='Greys_r',vmin=-3,vmax=3)
    #else:
    #    pl.imshow((img-mod)/sig,interpolation='nearest',origin='lower',cmap='Greys_r',vmin=-2,vmax=2)
    pl.subplot(141)
    CI = colorImage.ColorImage()
    CI.nonlin = 40.
    V,I,K = imgs[0],imgs[1],img
    dxi,dyi = model.Ddic['xoffset'],model.Ddic['yoffset']
    dxk,dyk = kmodel.Ddic['xoffset']+kmodel.Dx,kmodel.Ddic['yoffset']+kmodel.Dy
    I = ndimage.shift(I,[dyi,dxi])
    
    K = ndimage.zoom(K,1./scale)

    K = ndimage.shift(K,[-shifts[name][1],-shifts[name][0]])

    '''pl.figure()
    pl.imshow(K)
    pl.figure()
    pl.imshow(V)
    pl.figure()
    pl.imshow(I)
    pl.show()'''
    vki = CI.createModel(V,I,K)
    pl.imshow(vki,interpolation='nearest',origin='lower')
    pl.plot(xx,yy,color='White',lw=4)
    pl.imshow(vki,interpolation='nearest',origin='lower')  
    pl.figtext(0.07,0.16,"$1''$",color='White',fontsize=45,weight=1000,family='sans-serif',stretch='ultra-expanded')  
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])
    #pl.close()
    #pl.savefig('/data/ljo31/Lens/TeXstuff/paper/phot_paper/'+str(model.name)+'residTHREE.pdf')
    #pl.show()
    '''pl.figure()
    pl.imshow(vki,interpolation='nearest',origin='lower')
    pl.plot(xx,yy,color='White')
    pl.imshow(vki,interpolation='nearest',origin='lower')  
    pl.figtext(0.325,0.16,"$1''$",color='White',fontsize=45,weight=1000,family='sans-serif',stretch='ultra-expanded') 
    pl.gca().xaxis.set_ticks([])
    pl.gca().yaxis.set_ticks([])'''
    pl.show()
    
    #if name in ['J1347','J1125','J1446']:
    #    py.writeto('/data/ljo31/public_html/Lens/DM/'+name+'_vki.fits',vki,clobber=True)
    #    pl.savefig('/data/ljo31/public_html/Lens/DM/'+name+'_vki.png')
    

dir = '/data/ljo31/Lens/LensModels/twoband/'
sz = np.load('/data/ljo31/Lens/LensParams/SourceRedshiftsUpdated.npy')[()]
names = sz.keys()
names.sort()
shifts = [['J0837',[1.3,2.9]],['J0901',[0,3]],['J0913',[0,0]],['J1125',[0.9,2.1]],['J1144',[-0.8,4.55]],['J1218',[-3.2,-6.8]],['J1323',[1.0,1.1]],['J1347',[3.7,0]],['J1446',[0,0]],['J1605',[-3.5,0.1]],['J1606',[-4.8,7.6]],['J1619',[3.8,0]],['J2228',[-2.4,-3.6]]]
        
shifts = dict(shifts)


for name in names:
    if name == 'J1248':
        continue
    if name != 'J1347':
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

