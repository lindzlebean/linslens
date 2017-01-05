import numpy as np, pylab as pl
from linslens.Plotter import *
import indexTricks as iT
from pylens import MassModels,pylens
from imageSim import SBObjects,convolve
from scipy.sparse import diags
import pymc,cPickle
import myEmcee_blobs as myEmcee
from linslens.GrabImages_huge import *
import glob
from scipy.special import gamma
import lenslib
from astLib import astCalc
from jeans.makemodel import deproject

''' lets do these one at a time for now, to avoid errors '''
''' start off with power laws '''
''' pixellated sources '''
''' band by band for now? pixellated sources on many bands? '''

def MakeModel(name,result,oresult,plotresid=False,plotmass=True,plot=True):
    
    olp,otrace,odic,_ = oresult
    lp,trace,dic,_=result
    if len(olp.shape)==3:
        olp = olp[:,0]
        for key in odic.keys():
            odic[key] = odic[key][:,0]
    oa1,oa2 = np.unravel_index(olp.argmax(),olp.shape)
    a1,a3 = np.unravel_index(lp[:,0].argmax(),lp[:,0].shape)
    a2=0.
    
    # set up data
    imgs = [img1]#,img2]
    sigs = [sig1]#,sig2]
    psfs = [psf1]#,psf2]
    PSFs = []
    for i in range(len(psfs)):
        psf = psfs[i]
        image = imgs[i]
        psf /= psf.sum()
        psf = convolve.convolve(image,psf)[1]
        PSFs.append(psf)

    # set up parameters
    dxs = [0.,odic['xoffset'][oa1,oa2]]
    dys = [0.,odic['yoffset'][oa1,oa2]]

    # lens
    X = dic['Lens 1 x'][a1,0,a3]
    Y = dic['Lens 1 y'][a1,0,a3]
    B =dic['Lens 1 b'][a1,0,a3]
    Q = dic['Lens 1 q'][a1,0,a3]
    ETA = dic['Lens 1 eta'][a1,0,a3]
    PA = dic['Lens 1 pa'][a1,0,a3]

    SH = dic['extShear'][a1,0,a3]
    SHPA = dic['extShear PA'][a1,0,a3]

    lens1 = MassModels.PowerLaw('Lens 1',{'x':X,'y':Y,'b':B,'eta':ETA,'q':Q,'pa':PA})
    shear = MassModels.ExtShear('shear',{'x':X,'y':Y,'b':SH,'pa':SHPA})
    lenses = [lens1,shear]
    
    # source 1
    if 'Source 1 x' in dic.keys():
        SX = dic['Source 1 x'][a1,0,a3]
        SY = dic['Source 1 y'][a1,0,a3]
    elif name in ['J1347','J1323']:
        SX = dic['Source 2 x'][a1,0,a3]
        SY = dic['Source 2 y'][a1,0,a3]
    else:
        SX = dic['Source 2 x'][a1,0,a3]+X
        SY = dic['Source 2 y'][a1,0,a3]+Y
    try:
        SPA = dic['Source 1 pa'][a1,0,a3]
    except:
        SPA = dic['Source 2 pa'][a1,0,a3]
    SR = dic['Source 1 re'][a1,0,a3]
    SN = dic['Source 1 n'][a1,0,a3]
    SQ = dic['Source 1 q'][a1,0,a3]
    src = SBObjects.Sersic('Source 1',{'x':SX,'y':SY,'pa':SPA,'q':SQ,'re':SR,'n':SN})
    srcs = [src]

    # source 2
    if 'Source 2 re' in dic.keys():
        SX2 = dic['Source 2 x'][a1,0,a3]
        SY2 = dic['Source 2 y'][a1,0,a3]
        SR2 = dic['Source 2 re'][a1,0,a3]
        SN2 = dic['Source 2 n'][a1,0,a3]
        SPA2 = dic['Source 2 pa'][a1,0,a3]
        SQ2 = dic['Source 2 q'][a1,0,a3]
        src2 = SBObjects.Sersic('Source 2',{'x':SX2,'y':SY2,'pa':SPA2,'q':SQ2,'re':SR2,'n':SN2})
        srcs.append(src2)

    Mstar = dic['stellar mass'][a1,0,a3]
    if name == 'J1606':
        box = dic['boxiness'][a1,0,a3]
    
    LP = 0.
    colours = ['V', 'I']
    models = []
    fits = []
    for i in range(len(imgs)):
        dx,dy = dxs[i],dys[i]
        xp,yp = xc+dx,yc+dy
        image,sigma,psf = imgs[i],sigs[i],PSFs[i]
        imin,sigin,xin,yin = image.flatten(), sigma.flatten(),xp.flatten(),yp.flatten()
        model = np.empty((len(srcs)+1,imin.size))
        for lens in lenses:
            lens.setPars()
        x0,y0 = pylens.getDeflections(lenses,[xin,yin])
        x0 -= Mstar*xstars[i]
        y0 -= Mstar*ystars[i] 
        
        n = 0
        for src in srcs:
            src.setPars()
            tmp = xc*0.
            if name == 'J1606' and src.name == 'Source 2':
                tmp = src.boxypixeval(x0,y0,1./OVRS,csub=31,c=box).reshape(xc.shape)
            else:
                tmp = src.pixeval(x0,y0,1./OVRS,csub=31).reshape(xc.shape)
            tmp = iT.resamp(tmp,OVRS,True)
            tmp = convolve.convolve(tmp,psf,False)[0]
            model[n] = tmp.ravel()
            if name == 'J0837' and src.name == 'Source 2':
                model[n] *= -1.
                print 'it is J0837'
            n+=1
        model[n] = np.ones(model[n].shape)
        n+=1
        rhs = image[mask]/sigma[mask]
        mmodel = model.reshape((n,image.shape[0],image.shape[1]))
        mmmodel = np.empty((n,image[mask].size))
        for m in range(mmodel.shape[0]):
            mmmodel[m] = mmodel[m][mask]
        op = (mmmodel/sigma[mask]).T
        rhs = image[mask]/sigma[mask]
        fit, chi = optimize.nnls(op,rhs)
        components = (model.T*fit).T.reshape((n,image.shape[0],image.shape[1]))
        model = components.sum(0)
        models.append(model)
        resid = (model-image)/sigma
        LP += -0.5*(resid**2.).sum()
        print 'likelihood: ', LP

        if plotresid==True:
            NotPlicely(image,model,sigma,colours[i])
            pl.show()
        for ii in range(3):
            pl.figure()
            pl.imshow(components[ii],interpolation='nearest',origin='lower')
            pl.colorbar()
        pl.show()
                  
    if plotmass==True:
        # write this up as a function!
        # this is using circularised radii -- make a 2D plot next!
        # dark mass
        zl,zs = lz[name][0], sz[name][0]
        sig_crit = lenslib.sig_crit(zl,zs) # solar masses per Mpc^2
        sig_crit /= (1e3)**2. # solar masses per kpc^2
        scale = astCalc.da(zl)*np.pi/180./3600 * 1e3
        rein = B*0.05*scale # rein in kpc
        g1 = gamma(0.5*(1.+ETA))
        g2 = gamma(0.5*ETA)
        rho_0 = (2.-ETA)/(2.*np.pi**0.5) * sig_crit * rein**ETA * g1 / g2
        r = np.logspace(-7,3,3500)
        lr = r[:-100]
        DM_rho = rho_0 * lr**-ETA
        DMmodel = splrep(lr,DM_rho*4.*np.pi*lr**2.)
        DM = np.array([splint(0,lr[ii],DMmodel) for ii in range(lr.size)])
        
        # stellar mass -- deproject the sersic, converting everything to kpc as we go
        if 'Galaxy 1 x' in odic.keys():
            gx1,gy1 = odic['Galaxy 1 x'][oa1,oa2]*0.05*scale, odic['Galaxy 1 y'][oa1,oa2]*0.05*scale
        else:
            gx1,gy1 = odic['Galaxy 2 x'][oa1,oa2]*0.05*scale, odic['Galaxy 2 y'][oa1,oa2]*0.05*scale
        gr1,gn1 = odic['Galaxy 1 re'][oa1,oa2]*0.05*scale, odic['Galaxy 1 n'][oa1,oa2]
        gpa1,gq1 = odic['Galaxy 1 pa'][oa1,oa2], odic['Galaxy 1 q'][oa1,oa2]
        frac = [1.,0.]
        gal1 = SBModels.Sersic('galaxy 1',{'x':0,'y':0,'re':gr1,'n':gn1,'pa':gpa1,'q':gq1})
        gals = [gal1]
        if 'Galaxy 2 re' in odic.keys():
            if 'Galaxy 2 x' not in odic.keys():
                gx2,gy2 = gx1, gy1
            else:
                gx2,gy2 = odic['Galaxy 2 x'][oa1,oa2]*0.05*scale, odic['Galaxy 2 y'][oa1,oa2]*0.05*scale
            gr2,gn2 = odic['Galaxy 2 re'][oa1,oa2]*0.05*scale, odic['Galaxy 2 n'][oa1,oa2]
            try:
                gpa2,gq2 = odic['Galaxy 2 pa'][oa1,oa2], odic['Galaxy 2 q'][oa1,oa2]
            except:
                gpa2,gq2 = odic['Galaxy 1 pa'][oa1,oa2], odic['Galaxy 2 q'][oa1,oa2]
            frac = fracs[name]
            gal2 = SBModels.Sersic('galaxy 2',{'x':gx2-gx1,'y':gy2-gy1,'re':gr2,'n':gn2,'pa':gpa2,'q':gq2})
            gals.append(gal2) 

        if frac[1]>frac[0]:
            # centroid on the brightest component
            gals[0].x += (gx1-gx2)
            gals[0].y += (gy1-gy2)
            gals[1].x,gals[1].y = 0.,0.
        sb = np.zeros(r.size)
        for ii in range(len(gals)):
            sb += frac[ii]*gals[ii].eval(r)

        #deproject
        lr,light = deproject(r,sb)
        # cumulatively sum
        lightmod = splrep(lr,light*4.*np.pi*lr**2.)
        cumlight = np.array([splint(0,lr[ii],lightmod) for ii in range(lr.size)])
        cumlight /= cumlight[-1]
        LM = cumlight*Mstar*1e12
        if name == 'J2228':
            LM *= 5. # different deflection angle normalisation!
        LM[0] = LM[1]
        #pl.figure()
        #pl.loglog(lr,DM_rho,label='DM')
        #pl.loglog(lr,light,label='LM')
        #pl.ylabel(r'$\rho (M_{\odot}$kpc$^{-3}$)')
        #pl.xlabel('r (kpc)')
        if plot:
            pl.figure()
            pl.plot(lr,DM,color='k',ls=':',label='DM')
            pl.plot(lr,LM,color='k',ls='--',label='LM')
            pl.plot(lr,LM+DM,color='k',label='total')
            pl.yscale('log')
            pl.legend(loc='lower right')
            pl.ylabel(r'M (M$_{\odot}$)')
            pl.xlabel('r (kpc)')
            pl.axvline(rein,color='k',ls='-.') # Einstein radius
            pl.axvline(r_eff[names==name],color='k',ls='-.') # effective radius
            pl.errorbar(r_eff[names==name], Mvir[names==name],xerr = dr_eff[names==name],yerr=dMvir[names==name],color='k',marker='o')
            pl.axis([0,20,1e7,6e11])
            pl.title(name)
            pl.figure()
            pl.plot(lr,DM,color='k',ls=':',label='DM')
            pl.plot(lr,LM,color='k',ls='--',label='LM')
            pl.plot(lr,LM+DM,color='k',label='total')
            pl.legend(loc='upper left')
            pl.ylabel(r'M (M$_{\odot}$)')
            pl.xlabel('r (kpc)')
            pl.axis([0,20,1e7,5e11])
            pl.title(name)
            pl.show()

    if plot:
        pl.figure()
        pl.plot(lp[:,0])
        pl.show()

        pl.figure()
        pl.hist(dic['stellar mass'][:,0].ravel()*10.,30,histtype='stepfilled',alpha=0.6)
        pl.xlabel('M$_{\star}$ ($10^{11}$M$_{\odot})$')
        pl.show()

    # make table
    l,u,d = [], [], []
    for key in dic.keys():
        f = dic[key][:,0].reshape((trace[:,0].shape[0]*trace[:,0].shape[1]))
        lo,med,up = np.percentile(f,50)-np.percentile(f,16), np.percentile(f,50), np.percentile(f,84)-np.percentile(f,50) 
        d.append((key,med))
        l.append((key,lo))
        u.append((key,up))
    Ddic = dict(d)                    
    Ldic = dict(l)
    Udic = dict(u)
    Ddic['Source 1 x'] -= Ddic['Lens 1 x']
    Ddic['Source 1 y'] -= Ddic['Lens 1 y']
    if 'Source 2 x' in Ddic.keys():
        Ddic['Source 2 x'] -= Ddic['Lens 1 x']
        Ddic['Source 2 y'] -= Ddic['Lens 1 y']
    for key in ['Source 1 x','Source 1 y','Lens 1 x','Lens 1 y','Lens 1 b','Source 1 re','Source 2 re','Source 2 x','Source 2 y']:
        if key in Ddic.keys():
            Ddic[key] *= 0.02
            Ldic[key] *= 0.02
            Udic[key] *= 0.02

    '''print r'\begin{table}[H]'
    print r'\centering'
    print r'\begin{tabular}{|c|ccccccc|}\hline'
    print r' mass & $R_{Ein}$ & $\eta$ & $\theta_{L}$ & $q$ & $\log(M_{\star}/10^{11}M_{\odot})$ & $\gamma_{SH}$ & $\theta_{SH}$ \\\hline'
    for key in ['b','eta','pa','q']:
        print '&', '%.2f'%Ddic['Lens 1 '+key], '$_{-', '%.2f'%Ldic['Lens 1 '+key], '}^{+', '%.2f'%Udic['Lens 1 '+key], '}$',
    print '& ','%.2f'%(10.*Ddic['stellar mass']), '$_{-', '%.2f'%Ldic['stellar mass'], '}^{+', '%.2f'%Udic['stellar mass'], '}$ &',
    print '%.2f'%Ddic['extShear'], '$_{-', '%.2f'%Ldic['extShear'], '}^{+', '%.2f'%Udic['extShear'], '}$ &',
    print '%.2f'%Ddic['extShear PA'], '$_{-', '%.2f'%Ldic['extShear PA'], '}^{+', '%.2f'%Udic['extShear PA'], '}$', r'\\\hline'
    
    print r'source & $R_e$ & $n$ & $\theta_S$ & $q$ & $\Delta x$ & $\Delta y$ & -- \\\hline'
    for key in ['re','n','pa','q','x','y']:
        print '&', '%.2f'%Ddic['Source 1 '+key], '$_{-', '%.2f'%Ldic['Source 1 '+key], '}^{+', '%.2f'%Udic['Source 1 '+key], '}$',
    print r' & -- \\\hline'
    if 'Source 2 re' in Ddic.keys():
        for key in ['re','n','pa','q','x','y']:
            print '%.2f'%Ddic['Source 2 '+key], '$_{-', '%.2f'%Ldic['Source 2 '+key], '}^{+', '%.2f'%Udic['Source 2 '+key], '}$',
        print r' & -- \\\hline'
    print '\end{tabular}'
    print '\end{table}'
    '''

    print r'\begin{table}[H]'
    print r'\centering'
    print r'\begin{tabular}{|c|c|}\hline'
    print '$R_{Ein}$ & ' 
    print '$\eta$ & '
    print r'$\theta_{L}$ &'
    print '$q$ & '
    print '$\log(M_{\star}/10^{11}M_{\odot})$ & '
    print '$\gamma_{SH}$ & '
    print '$\theta_{SH}$ &'
    print '$R_e$ & '
    print '$n$ & '
    print r'$\theta_S$ & '
    print '$q$ & '
    print '$\Delta x$ & '
    print '$\Delta y$ & '

    for key in ['b','eta','pa','q']:
        print  '%.2f'%Ddic['Lens 1 '+key], '$_{-', '%.2f'%Ldic['Lens 1 '+key], '}^{+', '%.2f'%Udic['Lens 1 '+key], r'}$ \\'
    print '%.2f'%(10.*Ddic['stellar mass']), '$_{-', '%.2f'%Ldic['stellar mass'], '}^{+', '%.2f'%Udic['stellar mass'], r'}$ \\'
    print '%.2f'%Ddic['extShear'], '$_{-', '%.2f'%Ldic['extShear'], '}^{+', '%.2f'%Udic['extShear'], r'}$ \\',
    print '%.2f'%Ddic['extShear PA'], '$_{-', '%.2f'%Ldic['extShear PA'], '}^{+', '%.2f'%Udic['extShear PA'], '}$', r'\\\hline'
    for key in ['re','n','pa','q','x','y']:
        print '%.2f'%Ddic['Source 1 '+key], '$_{-', '%.2f'%Ldic['Source 1 '+key], '}^{+', '%.2f'%Udic['Source 1 '+key], r'}$ \\'
    if 'Source 2 re' in Ddic.keys():
        for key in ['re','n','pa','q','x','y']:
            print '%.2f'%Ddic['Source 2 '+key], '$_{-', '%.2f'%Ldic['Source 2 '+key], '}^{+', '%.2f'%Udic['Source 2 '+key], r'}$ \\'
    ## also print kinematic comparison!
    print '\n\n KINEMATICS DATA -- MODEL'
    ml,b,eta = Mstar, B*0.05*scale, ETA
    vd1, vd2 = ml * sigma_star**2., b**eta * sigma_dm.eval(np.array([eta]))
    s2 = ml * sigma_star**2. + b**eta * sigma_dm.eval(np.array([eta]))
    print '%.2f,%.2f,%.2f'%(vd1**0.5,vd2**0.5,s2**0.5)


# make image smaller
import sys
name = sys.argv[1] #'J0901'
print name
X = 0
file = py.open('/data/ljo31b/EELs/galsub/images/'+name+'_maxlnL.fits')
img1,img2 = file[1].data, file[2].data

# make images 120 pixels across
XX=60.
my,mx = img1.shape[0]/2., img1.shape[1]/2.
_,sig1,psf1,_,sig2,psf2,DX,DY,_,mask = EasyAddImages(name)

img1,img2 = img1[my-XX:my+XX,mx-XX:mx+XX], img2[my-XX:my+XX,mx-XX:mx+XX]
sig1,sig2,mask = sig1[my-XX:my+XX,mx-XX:mx+XX],sig2[my-XX:my+XX,mx-XX:mx+XX],mask[my-XX:my+XX,mx-XX:mx+XX]

psf1 = psf1/np.sum(psf1)
psf2 = psf2/np.sum(psf2)

OVRS=1
if name in ['J1125','J1347']:
    OVRS=2
yc,xc = iT.overSample(img1.shape,OVRS)
yo,xo = iT.coords(img1.shape)
xc,yc = xc+DX+(mx-XX), yc+DY+(my-XX) 
xo,yo = xo+DX+(mx-XX), yo+DY+(my-XX) 
if OVRS >1:
    tck = RectBivariateSpline(yo[:,0],xo[0],mask)
    mask2 = tck.ev(xc,yc)
    mask2[mask2<0.5] = 0
    mask2[mask2>0.5] = 1
    mask2 = mask2==0
mask = mask==0
if OVRS == 1:
    mask2 = mask

# stellar mass deflection angles
V,I,_ = np.load('/data/ljo31b/EELs/galsub/deflections/light_deflections_'+name+'.npy')
if name == 'J1144':
    V,I = np.load('/data/ljo31b/EELs/galsub/deflections/light_deflections_'+name+'_newmodel.npy')
# make these the right shapes!
V = [V[ii][my-XX:my+XX,mx-XX:mx+XX] for ii in range(len(V))]
I = [I[ii][my-XX:my+XX,mx-XX:mx+XX] for ii in range(len(I))]
if OVRS>1:
    for i in range(len(V)):
        tck = RectBivariateSpline(yo[:,0],xo[0],V[i])
        V[i] = tck.ev(yc,xc)
        tck = RectBivariateSpline(yo[:,0],xo[0],I[i])
        I[i] = tck.ev(yc,xc)
xstars, ystars = [V[0].flatten(), I[0].flatten()], [V[1].flatten(), I[1].flatten()]
xstarms, ystarms = [V[0][mask2],I[0][mask2]], [V[1][mask2], I[1][mask2]]


# load results for making model
dir = '/data/ljo31b/EELs/galsub/emceeruns/'
file = glob.glob(dir+name+'_parametric_*')
file.sort()
f = file[-1]
while 1:
    if 'DPL' in f:
        file = file[:-1]
        f = file[-1]
    else:
        break

print 'reading file ', f[35:]
#f = dir+'J1144_parametric_1'
result = np.load(f)

dir = '/data/ljo31/Lens/LensModels/twoband/'
try:
    oresult = np.load(dir+name+'_212')
except:
    if name == 'J1347':
        oresult = np.load(dir+name+'_112')
    else:
        oresult = np.load(dir+name+'_211')
if name == 'J1144':
    oresult = np.load('/data/ljo31/Lens/J1144/twoband_darkandlightprep')

# also add kinematics
sigma_star = np.loadtxt('/data/ljo31b/EELs/phys_models/models/sigma_star_'+name+'.dat')[()]
sigma_dm = np.load('/data/ljo31b/EELs/phys_models/models/interpolators/PL_aperture_mass_measure_'+name+'.npy')[()]
S2N=40. # signal-to-noise of ESI spectra to weight kinematic term

## load ESI kinematics
dir3 = '/data/ljo31b/EELs/esi/kinematics/inference/vdfit/NEW/'
result_K = np.load(dir3+name+'_1.00_lens_esi_indous_vdfit_LENS')
lp_K, trace_K, dic_K, _ = result_K
SIGMA = np.median(dic_K['lens dispersion'])
DSIGMA = SIGMA*0.05

sz = np.load('/data/ljo31/Lens/LensParams/SourceRedshiftsUpdated.npy')[()]
lz = np.load('/data/ljo31/Lens/LensParams/LensRedshiftsUpdated.npy')[()]
fracs = np.load('/data/ljo31b/EELs/galsub/fracs.npy')[()]

L,M,U = np.load('/data/ljo31b/EELs/esi/kinematics/inference/results_1.00_lens_vdfit.npy')
vl,vs,sl,ss = M.T
vl_lo,vs_lo,sl_lo,ss_lo = L.T
phot = py.open('/data/ljo31/Lens/LensParams/Phot_2src_lensgals_huge_new.fits')[1].data
r_eff, dr_eff = phot['Re v'], np.median((phot['Re v lo'],phot['Re v hi']),axis=0)
G = 4.3e-6
Mvir = 5. * sl**2. * r_eff / G
dMvir = Mvir * (2.*sl_lo / sl + dr_eff/r_eff)
np.save('/data/ljo31/Lens/LensParams/Mvir.npy',[Mvir,dMvir,r_eff,dr_eff])
names = ['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']

# also read in kinematics...

MakeModel(name,result,oresult,True,True,True)#True,True,True)

