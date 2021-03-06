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
from linslens.GrabImages_huge import *
import glob

''' lets do these one at a time for now, to avoid errors '''
''' start off with power laws '''
''' pixellated sources '''
''' band by band for now? pixellated sources on many bands? '''


def MakeModel(name,result,oresult,Npnts=1,oldResult=None):
    
    lp,trace,dic,_=result
    a1,a3 = numpy.unravel_index(lp[:,0].argmax(),lp[:,0].shape)

    olp,_,odic,_= oresult
    if len(olp.shape)==3.:
        olp = olp[:,0]
        for key in odic.keys():
            odic[key] = odic[key][:,0]
    oa1,oa2 = np.unravel_index(olp.argmax(),olp.shape)

    # first test: if we put in the old mass model, do we get convergence?
    x_start, y_start = dic['Lens 1 x'][a1,0,a3],dic['Lens 1 y'][a1,0,a3]
    LX = pymc.Uniform('Lens 1 x',x_start-10,x_start+10,value=x_start)
    LY = pymc.Uniform('Lens 1 y',y_start-10,y_start+10,value=y_start)
    LB = pymc.Uniform('Lens 1 b',0.5,100.,value=dic['Lens 1 b'][a1,0,a3]) 
    LETA = pymc.Uniform('Lens 1 eta',0.2,1.5,value=dic['Lens 1 eta'][a1,0,a3])
    LQ = pymc.Uniform('Lens 1 q',0.1,1.,value=dic['Lens 1 q'][a1,0,a3])
    LPA = pymc.Uniform('Lens 1 pa',-180,180,value=dic['Lens 1 pa'][a1,0,a3])
    SH = pymc.Uniform('shear',-0.3,0.3,value=dic['extShear'][a1,0,a3])
    SHPA = pymc.Uniform('shear pa',-180,180,value=dic['extShear PA'][a1,0,a3])
    Mstar = pymc.Uniform('stellar mass',0.01,10.,value=dic['stellar mass'][a1,0,a3])
    print Mstar.value
    lens = MassModels.PowerLaw('lens',{'x':LX,'y':LY,'b':LB,'eta':LETA,'q':LQ,'pa':LPA})
    shear = MassModels.ExtShear('shear',{'x':LX,'y':LY,'b':SH,'pa':SHPA})
    lenses = [lens,shear]

    # define offsets between grid on which stellar deflection angles have been measured and image grid - due to PSF. Ultimately, do this for both V and I bands
    DELTAX = pymc.Uniform('DELTAX',-3,3,0)
    DELTAY = pymc.Uniform('DELTAY',-3,3,0)

    pars = [LX,LY,LB,LETA,LQ,LPA,SH,SHPA,Mstar,DELTAX,DELTAY]
    cov_u = np.array([0., 0., 2., 0.3, 0., 0., 0., 0., 0.2,0.5,0.5])
    cov_n = np.array([0.5,0.5,0., 0.,  0.1,1.,0.05,5.,0,0,0])
    #cov = np.array([0.1,0.1,0.2,0.2,0.1,1,0.05,0.5,0.1])

    # now set up the inference
    imgs = [img1,img2]
    sigs = [sig1,sig2]
    ifltms = [img[pix_mask] for img in imgs]
    sfltms = [sig[pix_mask] for sig in sigs]
    vfltms = [sfltm**2 for sfltm in sfltms]
    cmatms = [diags(1./sfltm,0) for sfltm in sfltms]
    xm,ym = x[pix_mask],y[pix_mask]
    coords = [[xm,ym],[xm+odic['xoffset'][oa1,oa2],ym+odic['yoffset'][oa1,oa2]]]

    # stellar mass deflection angles
    x_stars, y_stars = [V[0].flatten(), I[0].flatten()], [V[1].flatten(), I[1].flatten()]
    x_starms, y_starms = [V[0][pix_mask],I[0][pix_mask]], [V[1][pix_mask], I[1][pix_mask]]

    PSFs = [pT.getPSFMatrix(psf, img1.shape) for psf in [psf1,psf2]]
    PSFms = [pT.maskPSFMatrix(PSF,pix_mask) for PSF in PSFs]
    
    iflts = [img1.flatten(),img2.flatten()]
    sflts = [sig1.flatten(),sig2.flatten()]
    vflts = [sflt**2. for sflt in sflts]
    xflts = [x.flatten(), (x+odic['xoffset'][oa1,oa2]).flatten()]
    yflts = [y.flatten(), (y+odic['yoffset'][oa1,oa2]).flatten()]

    srcs = []
    for ii in range(len(iflts)):
        srcs.append(aT.AdaptiveSource(ifltms[ii]/sfltms[ii],ifltms[ii].size/Npnts))
        xl,yl = pylens.getDeflections(lenses,coords[ii])
        xl,yl = xl - x_starms[ii]*Mstar.value, yl - y_starms[ii]*Mstar.value
        srcs[ii].update(xl,yl)

    import time
    regs=[5.,5.]

    def doFit(p=None):
        global reg
        #regs=[5.,5]
        lp = 0.
        #print '%.2f'%LB.value, '%.2f'%LX.value, '%.2f'%LY.value, '%.2f'%LETA.value, '%.2f'%LQ.value, '%.2f'%LPA.value
        for l in lenses:
            l.setPars()
        for ii in range(1): ### IMPORTANT - JUST DO THE V BAND FOR NOW!!!
            src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
            PSF,coord,iflt,sflt = PSFs[ii],coords[ii],iflts[ii],sflts[ii]
            coord[0]+=DELTAX.value
            coord[1]+=DELTAY.value

            x_star,y_star,x_starm,y_starm =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii]
            xflt,yflt = xflts[ii],yflts[ii]
            xflt+=DELTAX.value
            yflt+=DELTAY.value

            xl,yl = pylens.getDeflections(lenses,coord)
            xl,yl = xl - x_starm*Mstar.value, yl - y_starm*Mstar.value

            srcs[ii].update(xl,yl,doReg=True)
            lmat = PSFm*srcs[ii].lmat
            rmat = srcs[ii].rmat

            # choose regs by letting it find best case, then going slightly higher
            nupdate = 10#0#10
            res,fit,model,_,regg = aT.getModelG(ifltm,vfltm,lmat,cmatm,rmat,reg,nupdate)   
            reg = regg[0]
            #print reg
            xl,yl = pylens.getDeflections(lenses,[xflt,yflt])
            xl,yl = xl - x_star*Mstar.value, yl - y_star*Mstar.value
            oimg,pix = srcs[ii].eval(xl,yl,fit,domask=False)
            oimg = PSF*oimg
            res = (iflt-oimg)/sflt
            lp+= -0.5*(res**2).sum()
        return lp
            

    @pymc.observed
    def likelihood(value=0.,tmp=pars):
        return doFit(None)

    # check initial model
    doFit()
    #reg = 5.
    doFit()
    print 'current regularisation (set by hand): ', '%.1f'%reg
    
    for ii in range(1):#len(imgs)):
        src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
        x_star,y_star,x_starm,y_starm,PSF =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii],PSFs[ii]
        img,sig,coord = imgs[ii],sigs[ii],coords[ii]
        coord[0]+=DELTAX.value
        coord[1]+=DELTAY.value

        xl,yl = pylens.getDeflections(lenses,coord)
        xl,yl = xl - x_starm*Mstar.value, yl - y_starm*Mstar.value
        #print xl.shape
        srcs[ii].update(xl,yl)
        osrc = showRes(xl,yl,srcs[ii],PSFm,img,sig,pix_mask,ifltm,vfltm,cmatm,reg,0,400)
        pl.show()

    if oldResult is not None:
        print 'initialising based on previous chain'
        lp,trace,dic,_ = oldResult
        a1,a3 = np.unravel_index(lp[:,0].argmax(),lp[:,0].shape)
        for i in range(len(pars)):
            pars[i].value = trace[a1,0,a3,i]
    
    # now do some sampling. This will be slow -- make mask tighter?
    S = myEmcee.PTEmcee(pars+[likelihood],cov_u=cov_u,cov_n=cov_n,nthreads=20,nwalkers=100,ntemps=6)
    S.sample(500)

    outFile = '/data/ljo31b/EELs/galsub/emceeruns/'+name+'_pixellated_new_3_reg'
    f = open(outFile,'wb')
    cPickle.dump(S.result(),f,2)
    f.close()

    result = S.result()
    lp,trace,dic,_ = result
    a1,a3 = numpy.unravel_index(lp[:,0].argmax(),lp[:,0].shape)
    a2=0
    for i in range(len(pars)):
        pars[i].value = trace[a1,0,a3,i]
        print "%18s  %8.3f"%(pars[i].__name__,pars[i].value)

    # check inferred model
    doFit()
    doFit()
    print 'current regularisation (set by hand): ', '%.1f'%reg
    

    # re-sample a load of times
    kk=0
    for kk in range(10):
        S.p0 = trace[-1]
        S.sample(500)
        
        f = open(outFile,'wb')
        cPickle.dump(S.result(),f,2)
        f.close()

        result = S.result()
        lp,trace,dic,_=result
        
        a1,a3 = numpy.unravel_index(lp[:,0].argmax(),lp[:,0].shape)
        for i in range(len(pars)):
            pars[i].value = trace[a1,0,a3,i]
        print kk
        kk+=1
        
        
            

# make image smaller
name = 'J0901'
file = py.open('/data/ljo31b/EELs/galsub/images/'+name+'_maxlnL.fits')
img1,img2 = file[1].data, file[2].data

# make images 120 pixels across
XX=60.
#XX=50.
my,mx = img1.shape[0]/2., img1.shape[1]/2.
_,sig1,psf1,_,sig2,psf2,DX,DY,_,_ = EasyAddImages(name)

img1,img2 = img1[my-XX:my+XX,mx-XX:mx+XX], img2[my-XX:my+XX,mx-XX:mx+XX]
sig1,sig2 = sig1[my-XX:my+XX,mx-XX:mx+XX],sig2[my-XX:my+XX,mx-XX:mx+XX]

psf1 = psf1/np.sum(psf1)
psf2 = psf2/np.sum(psf2)

y,x = iT.coords(img1.shape)
x,y = x+DX+(mx-XX), y+DY+(my-XX)

pix_mask = py.open('/data/ljo31b/EELs/galsub/masks/'+name+'.fits')[0].data.copy()[my-XX:my+XX,mx-XX:mx+XX]
#pix_mask -= py.open('/data/ljo31b/EELs/galsub/masks/'+name+'_2.fits')[0].data.copy()[my-XX:my+XX,mx-XX:mx+XX]

from scipy.ndimage.morphology import binary_erosion as erode
pix_mask = pix_mask==1
pix_mask = erode(pix_mask,iterations=3)

# stellar mass deflection angles
V,I,_ = np.load('/data/ljo31b/EELs/galsub/deflections/light_deflections_'+name+'.npy')
# make these the right shapes!
V = [V[ii][my-XX:my+XX,mx-XX:mx+XX] for ii in range(len(V))]
I = [I[ii][my-XX:my+XX,mx-XX:mx+XX] for ii in range(len(I))]

names = ['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']

reg=5.
dir = '/data/ljo31/Lens/LensModels/twoband/'
try:
    oresult = np.load(dir+name+'_212')
except:
    if name == 'J1347':
        oresult = np.load(dir+name+'_112')
    else:
        oresult = np.load(dir+name+'_211')

reg=5.

dir = '/data/ljo31b/EELs/galsub/emceeruns/'
file = glob.glob(dir+name+'_parametric_VI_*')
file.sort()
f = file[-1]
result = np.load(f)

#oldResult = np.load('/data/ljo31b/EELs/galsub/emceeruns/J0901_parametric_1') # pixellated_new_0')
MakeModel(name,result,oresult)#,oldResult=oldResult)
