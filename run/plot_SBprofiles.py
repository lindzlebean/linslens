import numpy as np, pyfits as py, pylab as pl
from astLib import astCalc
from linslens import EELsModels_huge as L
from imageSim import SBModels,convolve,SBObjects


dir = '/data/ljo31/Lens/LensModels/twoband/'
sz = np.load('/data/ljo31/Lens/LensParams/SourceRedshiftsUpdated.npy')[()]
lz = np.load('/data/ljo31/Lens/LensParams/LensRedshiftsUpdated.npy')[()]

bands = np.load('/data/ljo31/Lens/LensParams/HSTBands.npy')[()]

names = sz.keys()
names.sort()
     
def Deflect(model,name):
    pl.figure()
    model.Initialise()
    _ = model.GetSourceSize()
    Xgrid = np.logspace(-2,np.log10(60),1101)


    src1 = model.fits[0][-3]*model.srcs[0].eval(Xgrid)
    src2 = model.fits[0][-2]*model.srcs[1].eval(Xgrid)
    jj = np.argmin(np.abs(src1-src2))
    #print name, jj, Xgrid[jj]
    if src1[0]>src2[0]:
        A,B = src1,src2
    else:
        A,B = src2,src1

    

    pl.plot(Xgrid[:jj]*0.25,A[:jj],color='k',ls='-')
    pl.plot(Xgrid[jj:]*0.25,A[jj:],color='k',ls='--')
    pl.plot(Xgrid[:jj]*0.25,B[:jj],color='k',ls='--')
    pl.plot(Xgrid[jj:]*0.25,B[jj:],color='k',ls='-')

    pl.fill_between(Xgrid*0.25,A*0.85,A*1.15,color='LightGray')#,alpha=0.5)
    pl.fill_between(Xgrid*0.25,B*0.85,B*1.15,color='LightGray')#,alpha=0.5)


    pl.xlim(0,15)
    pl.yscale('log')
    pl.xlabel('R$_e$ / kpc')
    pl.ylabel('log I$_{\mathrm{V band}}$')
    pl.ylim(1e-4,10)
    pl.title(name)
    
    print name, model.srcs[0].pars['n']#, model.srcs[1].pars['n']
    try:
        print  model.srcs[1].pars['n']
    except:
        return


#ZPs = np.load('/data/ljo31/Lens/LensParams/Keck_zeropoints.npy')[()]
names = ['J2228','J1619','J1347','J1144']

FRACS = []
for ii in range(len(names)):
    name = names[ii]
    if name == 'J1248':
        continue
    try:
        result = np.load(dir+name+'_212')
    except:
        result = np.load(dir+name+'_112')                                                       
        
    model = L.EELs(result, name)
    print name
    Deflect(model,name)

pl.show()
