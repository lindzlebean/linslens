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

def showRes(x,y,src,psf,img,sig,mask,iflt,vflt,cmat,reg,niter,npix):
    oy,ox = iT.coords((npix,npix))
    oy -= oy.mean()
    ox -= ox.mean()
    span = max(x.max()-x.min(),y.max()-y.min())
    oy *= span/npix
    ox *= span/npix
    ox += x.mean()
    oy += y.mean()
    lmat = psf*src.lmat
    rmat = src.rmat
    res,fit,model,rhs,regg = aT.getModelG(iflt,vflt,lmat,cmat,rmat,reg,niter=niter)
    osrc = src.eval(ox.ravel(),oy.ravel(),fit).reshape(ox.shape)

    oimg = img*numpy.nan
    oimg[mask] = (lmat*fit)

    ext = [0,img.shape[1],0,img.shape[0]]
    ext2 = [x.mean()-span/2.,x.mean()+span/2.,y.mean()-span/2.,y.mean()+span/2.]
    pylab.figure()
    pylab.subplot(221)
    img[~mask] = numpy.nan
    pylab.imshow(img,origin='lower',interpolation='nearest',extent=ext,vmin=0,vmax=1,cmap='jet',aspect='auto')
    pylab.colorbar()
    pylab.subplot(222)
    pylab.imshow(oimg,origin='lower',interpolation='nearest',extent=ext,vmin=0,vmax=1,cmap='jet',aspect='auto')
    pylab.colorbar()
    pylab.subplot(223)
    pylab.imshow((img-oimg)/sig,origin='lower',interpolation='nearest',extent=ext,vmin=-3,vmax=3,cmap='jet',aspect='auto')
    pylab.colorbar()
    pylab.subplot(224)
    pylab.imshow(osrc,origin='lower',interpolation='nearest',extent=ext2,vmin=0,vmax=1,cmap='jet',aspect='auto')
    pylab.colorbar()
    return osrc


def MakeModel(name,result,kresult,Npnts=1):
    # construct model and work out q, pa of DM. Do this, for the eels, using EELsModels
    model = K.EELs(kresult,result,name)
    model.Initialise()
    vmodel = L.EELs(result,name)
    vmodel.Initialise()
    b_start, sh_start, sh_pa_start = model.lenses[0].b, model.lenses[1].b, model.lenses[1].pa
    if model.galno == 1.:
        # simple case
        gal = model.gals[0]
        q_start, pa_start, x_start, y_start = gal.q, gal.pa, gal.x, gal.y
    else:
        # choose the brightest component
        gal1,gal2 = model.gals
        ii = np.where(model.fits[0:2]!=0.)
        if len(ii[0])<len(model.gals):
            print 'one of the components has no flux!'
            print 'component ', '%.2f'%np.where(kmodel.fits[0:2]==0), 'has no flux so we are removing it'
            model.galno = 1.
            model.gals = [model.gals[ii[0]]]
            gal = model.gals[0]
            q_start, pa_start, x_start, y_start = gal.q, gal.pa, gal.x, gal.y, model.lenses[0].b
        else:
            m1,m2 = gal1.getMag(model.fits[0],0), gal2.getMag(model.fits[1],0)
            F1,F2 = 10**(-0.4*m1), 10**(-0.4*m2)
            f1,f2 = F1/(F1+F2), F2/(F1+F2)
            ii = np.argmax((f1,f2))
            gal = model.gals[ii]
            q_start, pa_start, x_start, y_start = gal.q, gal.pa, gal.x, gal.y

    log_Mstar = logM[names==name]
    Mstar_start = (10**log_Mstar) * 1e-12 * 0.75
    print 'Mstar start', Mstar_start

    lp,trace,dic,_=result
    a1,a3 = numpy.unravel_index(lp[:,0].argmax(),lp[:,0].shape)

    # now set up priors
    '''LX = pymc.Uniform('Lens x',x_start-10,x_start+10,x_start)
    LY = pymc.Uniform('Lens y',y_start-10,y_start+10,y_start)
    LB = pymc.Uniform('Lens b',0.,100.,3.313)# from optimising bright pixels
    LETA = pymc.Uniform('Lens eta',0.5,1.5,1.)
    LQ = pymc.Uniform('Lens q',0.1,1.,q_start)
    LPA = pymc.Uniform('Lens pa',-180,180,pa_start)
    SH = pymc.Uniform('shear',-0.3,0.3,sh_start)
    SHPA = pymc.Uniform('shear pa',-180,180,sh_pa_start)'''
    #Mstar = pymc.Uniform('stellar mass',0.01,10.,0.191) # from optimising bright pixels. Units of 1e12 except for J2228!

    # first test: if we put in the old mass model, do we get convergence?
    x_start, y_start = dic['Lens 1 x'][a1,0,a3],dic['Lens 1 y'][a1,0,a3]
    LX = pymc.Uniform('Lens x',x_start-10,x_start+10,value=x_start)
    LY = pymc.Uniform('Lens y',y_start-10,y_start+10,value=y_start)
    LB = pymc.Uniform('Lens b',0.5,100.,value=dic['Lens 1 b'][a1,0,a3]) 
    LETA = pymc.Uniform('Lens eta',0.5,1.5,value=dic['Lens 1 eta'][a1,0,a3])
    LQ = pymc.Uniform('Lens q',0.1,1.,value=dic['Lens 1 q'][a1,0,a3])
    LPA = pymc.Uniform('Lens pa',-180,180,value=dic['Lens 1 pa'][a1,0,a3])
    SH = pymc.Uniform('shear',-0.3,0.3,value=dic['extShear'][a1,0,a3])
    SHPA = pymc.Uniform('shear pa',-180,180,value=dic['extShear PA'][a1,0,a3])

    lens = MassModels.PowerLaw('lens',{'x':LX,'y':LY,'b':LB,'eta':LETA,'q':LQ,'pa':LPA})
    shear = MassModels.ExtShear('shear',{'x':LX,'y':LY,'b':SH,'pa':SHPA})
    lenses = [lens,shear]

    pars = [LX,LY,LB,LETA,LQ,LPA,SH,SHPA]#,Mstar]
    cov = np.array([0.05,0.05,0.2,0.2,0.05,0.1,0.05,0.5]) # not realistic though!
    #cov = np.array([0.5,0.5,1.,0.2,0.1,5.,0.01,10.])#,2.])

    # now set up the inference
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
    xflts = [x.flatten(), (x+vmodel.Ddic['xoffset']).flatten()]
    yflts = [y.flatten(), (y+vmodel.Ddic['yoffset']).flatten()]

    srcs = []
    for ii in range(len(iflts)-1):
        srcs.append(aT.AdaptiveSource(ifltms[ii]/sfltms[ii],ifltms[ii].size/Npnts))
        xl,yl = pylens.getDeflections(lenses,coords[ii])
        #xl,yl = xl - x_starms[ii]*Mstar.value, yl - y_starms[ii]*Mstar.value
        srcs[ii].update(xl,yl)

    import time
    reg=5.

    def doFit(p=None):
        global reg
        reg=5.
        lp = 0.
        #print '%.2f'%LB.value, '%.2f'%LX.value, '%.2f'%LY.value, '%.2f'%LETA.value, '%.2f'%LQ.value, '%.2f'%LPA.value
        for l in lenses:
            l.setPars()
        for ii in range(len(ifltms)-1): ### IMPORTANT - JUST DO THE V BAND FOR NOW!!!
            src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
            PSF,coord,iflt,sflt = PSFs[ii],coords[ii],iflts[ii],sflts[ii]
            x_star,y_star,x_starm,y_starm =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii]
            xflt,yflt = xflts[ii],yflts[ii]

            xl,yl = pylens.getDeflections(lenses,coord)
            #xl,yl = xl - x_starm*Mstar.value, yl - y_starm*Mstar.value

            srcs[ii].update(xl,yl,doReg=True)
            lmat = PSFm*srcs[ii].lmat
            rmat = srcs[ii].rmat

            nupdate = 0
            res,fit,model,_,regg = aT.getModelG(ifltm,vfltm,lmat,cmatm,rmat,reg,nupdate)   
            reg = regg[0]
            xl,yl = pylens.getDeflections(lenses,[xflt,yflt])
            #xl,yl = xl - x_star*Mstar.value, yl - y_star*Mstar.value
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
    
    for ii in range(len(imgs)-1):
        src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
        x_star,y_star,x_starm,y_starm,PSF =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii],PSFs[ii]
        img,sig,coord = imgs[ii],sigs[ii],coords[ii]
            
        xl,yl = pylens.getDeflections(lenses,coord)
        #xl,yl = xl - x_starm*Mstar.value, yl - y_starm*Mstar.value
        print xl.shape
        srcs[ii].update(xl,yl)
        osrc = showRes(xl,yl,srcs[ii],PSFm,img,sig,pix_mask,ifltm,vfltm,cmatm,reg,0,400)
        pl.show()

        # just checkj deflections all look sensible
        '''pl.figure(figsize=(15,5))
        pl.subplot(131)
        pl.imshow(lenses[0].deflections(x,y)[0],origin='lower',interpolation='nearest')
        pl.title('power law')
        pl.colorbar()
        pl.subplot(132)
        pl.imshow(V[0]*0.1,origin='lower',interpolation='nearest')
        pl.title('sersic')
        pl.colorbar()
        pl.subplot(133)
        pl.imshow(lenses[1].deflections(x,y)[0],origin='lower',interpolation='nearest')
        pl.colorbar()
        pl.title('shear')
        pl.suptitle('x deflections')
        ####
        pl.figure(figsize=(15,5))
        pl.subplot(131)
        pl.imshow(lenses[0].deflections(x,y)[1],origin='lower',interpolation='nearest')
        pl.title('power law')
        pl.colorbar()
        pl.subplot(132)
        pl.imshow(V[1]*0.1,origin='lower',interpolation='nearest')
        pl.title('sersic')
        pl.colorbar()
        pl.subplot(133)
        pl.imshow(lenses[1].deflections(x,y)[1],origin='lower',interpolation='nearest')
        pl.colorbar()
        pl.title('shear')
        pl.suptitle('y deflections')'''
        
        pl.show()
        
        
    # old results
    '''result = np.load('/data/ljo31b/EELs/galsub/emceeruns/'+name+'_'+str(X))
    lp,trace,dic,_ = result
    a1,a3 = numpy.unravel_index(lp[:,0].argmax(),lp[:,0].shape)
    a2=0
    for i in range(len(pars)):
        pars[i].value = trace[a1,0,a3,i]
        print "%18s  %8.3f"%(pars[i].__name__,pars[i].value)'''
    
    # now do some sampling. This will be slow -- make mask tighter?
    S = myEmcee.PTEmcee(pars+[likelihood],cov=cov,nthreads=24,nwalkers=100,ntemps=3)
    S.sample(500)

    outFile = '/data/ljo31b/EELs/galsub/emceeruns/'+name+'_'+str(X)
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
    
    '''for ii in range(len(imgs)-1):
        src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
        x_star,y_star,x_starm,y_starm,PSF =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii],PSFs[ii]
        img,sig,coord = imgs[ii],sigs[ii],coords[ii]
            
        xl,yl = pylens.getDeflections(lenses,coord)
        #xl,yl = xl - x_starm*Mstar.value, yl - y_starm*Mstar.value
        srcs[ii].update(xl,yl)
        osrc = showRes(xl,yl,srcs[ii],PSFm,img,sig,pix_mask,ifltm,vfltm,cmatm,reg,0,400)
        pl.show()'''

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
        
        # check inferred model each time!
        '''doFit()
        doFit()
        print 'current regularisation (set by hand): ', '%.1f'%reg
    
        for ii in range(len(imgs)-1):
            src,ifltm,sfltm,vfltm,PSFm,cmatm = srcs[ii],ifltms[ii],sfltms[ii],vfltms[ii],PSFms[ii],cmatms[ii]
            x_star,y_star,x_starm,y_starm,PSF =x_stars[ii],y_stars[ii],x_starms[ii],y_starms[ii],PSFs[ii]
            img,sig,coord = imgs[ii],sigs[ii],coords[ii]
            
            xl,yl = pylens.getDeflections(lenses,coord)
            #xl,yl = xl - x_starm*Mstar.value, yl - y_starm*Mstar.value
            srcs[ii].update(xl,yl)
            osrc = showRes(xl,yl,srcs[ii],PSFm,img,sig,pix_mask,ifltm,vfltm,cmatm,reg,0,400)
            pl.show()'''
            

# make image smaller
name = 'J0837'
X = 3
file = py.open('/data/ljo31b/EELs/galsub/images/'+name+'.fits')
img1,img2 = file[1].data, file[2].data

# make images 120 pixels across
my,mx = img1.shape[0]/2., img1.shape[1]/2.
img1,img2 = img1[my-25:my+25,mx-25:mx+25], img2[my-25:my+25,mx-25:mx+25]
pix_mask = py.open('/data/ljo31b/EELs/galsub/masks/'+name+'.fits')[0].data.copy()[my-25:my+25,mx-25:mx+25]
pix_mask = pix_mask==1
_,sig1,psf1,_,sig2,psf2,DX,DY,OVRS,_ = Image.J0837()  
sig1,sig2 = sig1[my-25:my+25,mx-25:mx+25], sig2[my-25:my+25,mx-25:mx+25]
y,x = iT.coords(img1.shape)
x,y = x+DX+(mx-25.), y+DY+(my-25.) 


# Start off DM with same q and pa as light. Try to make it as automated as possible
# stellar mass deflection angles
V,I,_ = np.load('/data/ljo31b/EELs/galsub/deflections/light_deflections_'+name+'.npy')
# make these the right shapes!
V = [V[ii][my-25:my+25,mx-25:mx+25] for ii in range(len(V))]
I = [I[ii][my-25:my+25,mx-25:mx+25] for ii in range(len(I))]

masses = np.load('/data/ljo31b/EELs/inference/new/huge/masses_212.npy')
names = ['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']
logM = masses[0]

# load results for making model
dir = '/data/ljo31/Lens/LensModels/twoband/'
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
    else:
        result = np.load(dir+name+'_211')
        kresult = np.load(dir+name+'_Kp_211')
reg=5.
MakeModel(name,result,kresult)
