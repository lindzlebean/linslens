from linslens import EELsModels_huge as L
import numpy as np
import pylab as pl
from linslens import EELsKeckModels as K
from linslens.Plotter import *



def clip(arr,nsig=3.5):
    a = arr.flatten()
    m,s,l = a.mean(),a.std(),a.size
    while 1:
        a = a[abs(a-m)<s*nsig]
        if a.size==l:
            return m,s
        m,s,l = a.mean(),a.std(),a.size


def Subtract(model,name):
    model.Initialise()
    img_v, img_i = model.imgs
    comps_v, comps_i = model.comps
    if model.galno == 1:
        galaxy_v, galaxy_i= comps_v[0], comps_i[0]
    else:
        galaxy_v, galaxy_i = comps_v[0:2].sum(0), comps_i[0:2].sum(0)
        print 'check it is both components!', comps_v[0:2].shape
    sub_v, sub_i = img_v-galaxy_v, img_i-galaxy_i
    '''y,x = sub_v.shape
    my,mx = int(y/2.), int(x/2.)
    sub_v, sub_i = sub_v[my-75:my+75,mx-75:mx+75],sub_i[my-75:my+75,mx-75:mx+75]
    pl.figure(figsize=(30,7))
    pl.subplot(131)
    pl.imshow(sub_v,interpolation='nearest',origin='lower',vmin = np.median(sub_v)-3.*np.std(sub_v),vmax=np.median(sub_v)+3.*np.std(sub_v))
    pl.subplot(132)
    pl.imshow(sub_i,interpolation='nearest',origin='lower',vmin = np.median(sub_i)-3.*np.std(sub_i),vmax=np.median(sub_i)+3.*np.std(sub_i))
    pl.subplot(133)
    pl.imshow(sub_k,interpolation='nearest',origin='lower',vmin = np.median(sub_k)-3.*np.std(sub_k),vmax=np.median(sub_k)+3.*np.std(sub_k))
    pl.show()'''
    outname = '/data/ljo31b/EELs/galsub/images/'+name+'newmodel_maxlnL.fits'
    hdu = py.HDUList()
    phdu = py.PrimaryHDU()
    hdr = phdu.header
    hdr['object'] = name
    vband   = py.ImageHDU(sub_v,name=bands[name])
    iband = py.ImageHDU(sub_i,name='F814W')
    hdu.append(phdu)
    hdu.append(vband)
    hdu.append(iband)
    hdu.writeto(outname,clobber=True)
    
    

dir = '/data/ljo31/Lens/LensModels/twoband/'
sz = np.load('/data/ljo31/Lens/LensParams/SourceRedshiftsUpdated.npy')[()]
bands = np.load('/data/ljo31/Lens/LensParams/HSTBands.npy')[()]

names = sz.keys()
names.sort()
     
name='J1144'
result = np.load('/data/ljo31/Lens/J1144/twoband_darkandlightprep')
model = L.EELs(result, name)
Subtract(model,name)

