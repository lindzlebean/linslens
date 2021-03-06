import numpy as np, pylab as pl
from linslens import EELsKeckLensModels as K, EELsImages_huge as Image, EELsModels_huge as L
from linslens.Plotter import *
from linslens.pixplot import *
import indexTricks as iT
from pylens import MassModels,pylens,adaptTools as aT,pixellatedTools as pT
from imageSim import SBModels,convolve
from scipy.sparse import diags
import pymc,cPickle
import myEmcee_blobs as myEmcee

''' lets do these one at a time for now, to avoid errors '''
''' start off with power laws '''
''' pixellated sources '''
''' band by band for now? pixellated sources on many bands? '''

def MakeModel(name,result,Npnts=2):
    
    # read model
    lp,trace,dic,_ = result
    a2=0
    a1,a3 = np.unravel_index(lp[:,0].argmax(),lp[:,0].shape)

    # now set up lenses
    LX = dic['Lens x'][a1,a2,a3]
    LY = dic['Lens y'][a1,a2,a3]
    LB = dic['Lens b'][a1,a2,a3]
    LETA = dic['Lens eta'][a1,a2,a3]
    LQ = dic['Lens q'][a1,a2,a3]
    LPA = dic['Lens pa'][a1,a2,a3]
    SH = dic['shear'][a1,a2,a3]
    SHPA = dic['shear pa'][a1,a2,a3]
    Mstar = dic['stellar mass'][a1,a2,a3]

    lens = MassModels.PowerLaw('lens',{'x':LX,'y':LY,'b':LB,'eta':LETA,'q':LQ,'pa':LPA})
    shear = MassModels.ExtShear('shear',{'x':LX,'y':LY,'b':SH,'pa':SHPA})
    lenses = [lens,shear]
    for l in lenses:
        l.setPars()

    # now set up the images etc
    imgs = [img1,img2]
    sigs = [sig1,sig2]
    ifltms = [img[pix_mask] for img in imgs]
    sfltms = [sig[pix_mask] for sig in sigs]
    vfltms = [sfltm**2 for sfltm in sfltms]
    cmatms = [diags(1./sfltm,0) for sfltm in sfltms]
    xm,ym = x[pix_mask],y[pix_mask]
    coords = [[xm,ym],[xm+vmodel.Ddic['xoffset'],ym+vmodel.Ddic['yoffset']]]

    # stellar mass deflection angles
    x_stars, y_stars = [V[0].flatten(), I[0].flatten()], [V[1].flatten(), I[1].flatten()]
    x_starms, y_starms = [V[0][pix_mask],I[0][pix_mask]], [V[1][pix_mask], I[1][pix_mask]]

    PSFs = [pT.getPSFMatrix(psf, img1.shape) for psf in [psf1,psf2]]
    PSFms = [pT.maskPSFMatrix(PSF,pix_mask) for PSF in PSFs]
    
    iflts = [img1.flatten(),img2.flatten()]
    sflts = [sig1.flatten(),sig2.flatten()]
    vflts = [sflt**2. for sflt in sflts]
    xflt,yflt = x.flatten(), y.flatten()

    srcs = []
    for ii in range(len(iflts)):
        srcs.append(aT.AdaptiveSource(ifltms[ii]/sfltms[ii],ifltms[ii].size/Npnts))
        xl,yl = pylens.getDeflections(lenses,coords[ii])
        xl,yl = xl - x_starms[ii]*Mstar, yl - y_starms[ii]*Mstar
        srcs[ii].update(xl,yl)

    import time
    reg=5.

    def doFit(p=None,updateReg=False,checkImgs=False,doReg=True):
        global reg
        reg=5.
        lp = 0.
        
        for l in lenses:
            l.setPars()
        for ii in range(len(ifltms)):
            src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
            PSF,coord,iflt,sflt = PSFs[ii],coords[ii],iflts[ii],sflts[ii]
            x_star,y_star,x_starm,y_starm =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii]
            
            xl,yl = pylens.getDeflections(lenses,coord)
            xl,yl = xl - x_starm*Mstar, yl - y_starm*Mstar

            src.update(xl,yl,doReg=doReg)

            lmat = PSFm*src.lmat
            rmat = src.rmat

            nupdate = 0
            if updateReg==True:
                nupdate = 10

            res,fit,model,_,regg = aT.getModelG(ifltm,vfltm,lmat,cmatm,rmat,reg,nupdate)   
            reg = regg[0]
            if checkImgs is False:
                lp += -0.5*res

            else:
                xl,yl = pylens.getDeflections(lenses,[xflt,yflt])
                xl,yl = xl - x_star*Mstar, yl - y_star*Mstar
                oimg,pix = src.eval(xl,yl,fit,domask=False)
                oimg = PSF*oimg
                res = (iflt-oimg)/sflt
                lp+= -0.5*(res**2).sum()
            return lp
            
    # check initial model
    doFit(False,True)
    doFit(False,True)
    print 'current regularisation (set by hand): ', '%.1f'%reg
    
    vms = [1.,6.]
    for ii in range(len(imgs)):
        src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
        x_star,y_star,x_starm,y_starm,PSF =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii],PSFs[ii]
        img,sig,coord = imgs[ii],sigs[ii],coords[ii]
            
        xl,yl = pylens.getDeflections(lenses,coord)
        xl,yl = xl - x_starm*Mstar, yl - y_starm*Mstar
        print xl.shape
        osrc = showRes(xl,yl,src,PSFm,img,sig,pix_mask,ifltm,vfltm,cmatm,reg,0,400,vmax_src=vms[ii])
        pl.show()

       

# make image smaller
name = 'J0837'
file = py.open('/data/ljo31b/EELs/galsub/images/'+name+'.fits')
img1,img2 = file[1].data, file[2].data

# make images 160 pixels across
my,mx = img1.shape[0]/2., img1.shape[1]/2.
img1,img2 = img1[my-80:my+80,mx-80:mx+80], img2[my-80:my+80,mx-80:mx+80] 
pix_mask = py.open('/data/ljo31b/EELs/galsub/masks/'+name+'.fits')[0].data.copy()[my-80:my+80,mx-80:mx+80]
pix_mask = pix_mask==1
_,sig1,psf1,_,sig2,psf2,DX,DY,OVRS,_ = Image.J0901()  
sig1,sig2 = sig1[my-80:my+80,mx-80:mx+80], sig2[my-80:my+80,mx-80:mx+80]
y,x = iT.coords(img1.shape)
x,y = x+DX+(mx-80.), y+DY+(my-80.) 


# Start off DM with same q and pa as light. Try to make it as automated as possible
# stellar mass deflection angles
V,I,_ = np.load('/data/ljo31b/EELs/galsub/deflections/light_deflections_'+name+'.npy')
# make these the right shapes!
V = [V[ii][my-80:my+80,mx-80:mx+80] for ii in range(len(V))]
I = [I[ii][my-80:my+80,mx-80:mx+80] for ii in range(len(I))]

# just need to grab a couple of things
dir = '/data/ljo31/Lens/LensModels/twoband/'
try:
    result = np.load(dir+name+'_212')
except:
    if name == 'J1347':
        result = np.load(dir+name+'_112')
    elif name == 'J1619':
        result = np.load(dir+name+'_212')
    else:
        result = np.load(dir+name+'_211')

vmodel = L.EELs(result,name)
vmodel.Initialise()

# load results for making model
result = np.load('/data/ljo31b/EELs/galsub/emceeruns/'+name+'_2')
lp,trace,dic,_ = result

MakeModel(name,result)

pl.figure()
pl.plot(lp[:,0])
for key in dic.keys():
    pl.figure()
    pl.hist(dic[key][:,0].ravel(),30)
    pl.title(key)

pl.show()
