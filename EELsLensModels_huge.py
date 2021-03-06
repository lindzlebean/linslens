import pyfits as py, numpy as np
from imageSim import SBModels,convolve
from pylens import *
import indexTricks as iT
from scipy import optimize
from scipy.interpolate import splrep, splev, splint,RectBivariateSpline
from astLib import astCalc
import EELsImages_huge as EELsImages, Plotter
from GetPhotometry import *
import SBBModels, SBBProfiles
import itertools
from Plotter import *

bands = dict([('J0837','F606W'),('J0901','F606W'),('J0913','F555W'),('J1125','F606W'),('J1144','F606W'),('J1218','F606W'),('J1248','F555W'),('J1323','F555W'),('J1347','F606W'),('J1446','F606W'),('J1605','F555W'),('J1606','F606W'),('J1619','F606W'),('J2228','F555W')])

source_redshifts = dict([('J0837',0.6411),('J0901',0.586),('J0913',0.539),('J1125',0.689),('J1144',0.706),('J1218',0.6009),('J1248',0.528),('J1323',0.4641),('J1347',0.63),('J1446',0.585),('J1605',0.542),('J1606',0.6549),('J1619',0.6137),('J2228',0.4370)])

lens_redshifts = dict([('J0837',0.4256),('J0901',0.311),('J0913',0.395),('J1125',0.442),('J1144',0.372),('J1218',0.3182),('J1248',0.304),('J1323',0.3194),('J1347',0.39),('J1446',0.317),('J1605',0.306),('J1606',0.3816),('J1619',0.3638),('J2228',0.2391)])


class EELs:
    def __init__(self,result,name,fits=None):
        self.result = result
        if self.result is not None:
            self.lp, self.trace, self.dic,_ = self.result
        self.name = name
        self.fits = fits
        if self.trace.shape[1] < 10:
            self.lp, self.trace =self.lp[:,0], self.trace[:,0]
            d = []
            for key in self.dic.keys():
                d.append((key,self.dic[key][:,0]))
            self.dic = dict(d)
        if name == 'J0837':
            print "repositioning J0837's source"
            self.dic['Source 2 x'] -= self.dic['Lens 1 x']
            self.dic['Source 2 y'] -= self.dic['Lens 1 y']
                       
                          
    def MakeDict(self):
        if 'Source 2 re' not in self.dic.keys():
            self.srcno = 1
        else:
            self.srcno = 2
        if 'Galaxy 2 re' not in self.dic.keys() and 'Galaxy 3 re' not in self.dic.keys():
            self.galno = 1
        elif 'Galaxy 2 re' in self.dic.keys() and 'Galaxy 3 re' not in self.dic.keys():
            self.galno = 2
        else:
            self.galno = 3
        if self.srcno==2 and (self.name == 'J1323' or self.name == 'J1347') :
            print "repositioning J1323's/J1347's source"
            self.dic['Source 2 x'] -= self.dic['Lens 1 x']
            self.dic['Source 2 y'] -= self.dic['Lens 1 y']
        if 'Source 1 pa' not in self.dic.keys():
            self.dic['Source 1 pa'] = self.dic['Source 2 pa']
        if self.galno == 2 and 'Galaxy 2 pa' not in self.dic.keys():
            self.dic['Galaxy 2 pa'] = self.dic['Galaxy 1 pa'] 

        #ftrace = self.trace.reshape((self.trace.shape[0]*self.trace.shape[1],self.trace.shape[2]))
        #upperlower = map(lambda v: (v[0],v[1],v[2]),zip(*np.percentile(ftrace,[16,50,84],axis=0)))

        l,u,d = [], [], []
        for key in self.dic.keys():
            f = self.dic[key].reshape((self.trace.shape[0]*self.trace.shape[1]))
            lo,med,up = np.percentile(f,50)-np.percentile(f,16), np.percentile(f,50), np.percentile(f,84)-np.percentile(f,50) 
            d.append((key,med))
            l.append((key,lo))
            u.append((key,up))
        
        if 'Source 1 x' not in self.dic.keys():
            for key in 'x', 'y':
                f = self.dic['Source 2 '+key].reshape((self.trace.shape[0]*self.trace.shape[1]))
                lo,med,up = np.percentile(f,50)-np.percentile(f,16), np.percentile(f,50), np.percentile(f,84)-np.percentile(f,50) 
                d.append(('Source 1 '+key,med))
                l.append(('Source 1 '+key,lo))
                u.append(('Source 1 '+key,up))
                self.dic['Source 1 '+key] = self.dic['Source 2 '+key]
        if 'Galaxy 2 x' not in self.dic.keys():
            for key in 'x', 'y':
                f = self.dic['Galaxy 1 '+key].reshape((self.trace.shape[0]*self.trace.shape[1]))
                lo,med,up = np.percentile(f,50)-np.percentile(f,16), np.percentile(f,50), np.percentile(f,84)-np.percentile(f,50) 
                d.append(('Galaxy 2 '+key,med))
                l.append(('Galaxy 2 '+key,lo))
                u.append(('Galaxy 2 '+key,up))
                self.dic['Galaxy 2 '+key] = self.dic['Galaxy 1 '+key]
        

        self.Ddic = dict(d)                    
        self.Ldic = dict(l)
        self.Udic = dict(u)
        #return self.Ddic,self.Ldic,self.Udic

    def PrintTable(self):
        print r'\begin{table}[H]'
        print r'\centering'
        print r'\begin{tabular}{|c|cccccc|}\hline'
        print r' object & x & y & re & n & pa & q \\\hline'
        print 'source 1 & $', '%.2f'%(self.Ddic['Source 1 x']+self.Ddic['Lens 1 x']), '_{-', '%.2f'%self.Ldic['Source 1 x'],'}^{+','%.2f'%self.Udic['Source 1 x'], '}$ & $', '%.2f'%(self.Ddic['Source 1 y']+self.Ddic['Lens 1 y']),'_{-', '%.2f'%self.Ldic['Source 1 y'],'}^{+', '%.2f'%self.Udic['Source 1 y'], '}$ & $', '%.2f'%self.Ddic['Source 1 re'],'_{-', '%.2f'%self.Ldic['Source 1 re'],'}^{+', '%.2f'%self.Udic['Source 1 re'], '}$ & $', '%.2f'%self.Ddic['Source 1 n'],'_{-', '%.2f'%self.Ldic['Source 1 n'],'}^{+', '%.2f'%self.Udic['Source 1 n'], '}$ & $','%.2f'%self.Ddic['Source 1 pa'],'_{-', '%.2f'%self.Ldic['Source 1 pa'],'}^{+', '%.2f'%self.Udic['Source 1 pa'], '}$ & $','%.2f'%self.Ddic['Source 1 q'],'_{-', '%.2f'%self.Ldic['Source 1 q'],'}^{+', '%.2f'%self.Udic['Source 1 q'], '}$',r'\\'
        ###
        if self.srcno ==2:
            print 'source 2 & $', '%.2f'%(self.Ddic['Source 2 x']+self.Ddic['Lens 1 x']), '_{-', '%.2f'%self.Ldic['Source 2 x'],'}^{+','%.2f'%self.Udic['Source 2 x'], '}$ & $', '%.2f'%(self.Ddic['Source 2 y']+self.Ddic['Lens 1 x']),'_{-', '%.2f'%self.Ldic['Source 2 y'],'}^{+', '%.2f'%self.Udic['Source 2 y'], '}$ & $', '%.2f'%self.Ddic['Source 2 re'],'_{-', '%.2f'%self.Ldic['Source 2 re'],'}^{+', '%.2f'%self.Udic['Source 2 re'], '}$ & $', '%.2f'%self.Ddic['Source 2 n'],'_{-', '%.2f'%self.Ldic['Source 2 n'],'}^{+', '%.2f'%self.Udic['Source 2 n'], '}$ & $','%.2f'%self.Ddic['Source 2 pa'],'_{-', '%.2f'%self.Ldic['Source 2 pa'],'}^{+', '%.2f'%self.Udic['Source 2 pa'], '}$ & $','%.2f'%self.Ddic['Source 2 q'],'_{-', '%.2f'%self.Ldic['Source 2 q'],'}^{+', '%.2f'%self.Udic['Source 2 q'], '}$',r'\\'
###
        print 'galaxy 1 & $', '%.2f'%self.Ddic['Galaxy 1 x'], '_{-', '%.2f'%self.Ldic['Galaxy 1 x'],'}^{+','%.2f'%self.Udic['Galaxy 1 x'], '}$ & $', '%.2f'%self.Ddic['Galaxy 1 y'],'_{-', '%.2f'%self.Ldic['Galaxy 1 y'],'}^{+', '%.2f'%self.Udic['Galaxy 1 y'], '}$ & $', '%.2f'%self.Ddic['Galaxy 1 re'],'_{-', '%.2f'%self.Ldic['Galaxy 1 re'],'}^{+', '%.2f'%self.Udic['Galaxy 1 re'], '}$ & $', '%.2f'%self.Ddic['Galaxy 1 n'],'_{-', '%.2f'%self.Ldic['Galaxy 1 n'],'}^{+', '%.2f'%self.Udic['Galaxy 1 n'], '}$ & $','%.2f'%self.Ddic['Galaxy 1 pa'],'_{-', '%.2f'%self.Ldic['Galaxy 1 pa'],'}^{+', '%.2f'%self.Udic['Galaxy 1 pa'], '}$ & $','%.2f'%self.Ddic['Galaxy 1 q'],'_{-', '%.2f'%self.Ldic['Galaxy 1 q'],'}^{+', '%.2f'%self.Udic['Galaxy 1 q'], '}$',r'\\'
        ###
        print 'galaxy 2 & $', '%.2f'%self.Ddic['Galaxy 2 x'], '_{-', '%.2f'%self.Ldic['Galaxy 2 x'],'}^{+','%.2f'%self.Udic['Galaxy 2 x'], '}$ & $', '%.2f'%self.Ddic['Galaxy 2 y'],'_{-', '%.2f'%self.Ldic['Galaxy 2 y'],'}^{+', '%.2f'%self.Udic['Galaxy 2 y'], '}$ & $', '%.2f'%self.Ddic['Galaxy 2 re'],'_{-', '%.2f'%self.Ldic['Galaxy 2 re'],'}^{+', '%.2f'%self.Udic['Galaxy 2 re'], '}$ & $', '%.2f'%self.Ddic['Galaxy 2 n'],'_{-', '%.2f'%self.Ldic['Galaxy 2 n'],'}^{+', '%.2f'%self.Udic['Galaxy 2 n'], '}$ & $','%.2f'%self.Ddic['Galaxy 2 pa'],'_{-', '%.2f'%self.Ldic['Galaxy 2 pa'],'}^{+', '%.2f'%self.Udic['Galaxy 2 pa'], '}$ & $','%.2f'%self.Ddic['Galaxy 2 q'],'_{-', '%.2f'%self.Ldic['Galaxy 2 q'],'}^{+', '%.2f'%self.Udic['Galaxy 2 q'], '}$',r'\\'
        ###
        if 'Galaxy 3 x' in self.dic.keys():
            print 'galaxy 3 & $', '%.2f'%self.Ddic['Galaxy 3 x'], '_{-', '%.2f'%self.Ldic['Galaxy 3 x'],'}^{+','%.2f'%self.Udic['Galaxy 3 x'], '}$ & $', '%.2f'%self.Ddic['Galaxy 3 y'],'_{-', '%.2f'%self.Ldic['Galaxy 3 y'],'}^{+', '%.2f'%self.Udic['Galaxy 3 y'], '}$ & $', '%.2f'%self.Ddic['Galaxy 3 re'],'_{-', '%.2f'%self.Ldic['Galaxy 3 re'],'}^{+', '%.2f'%self.Udic['Galaxy 3 re'], '}$ & $', '%.2f'%self.Ddic['Galaxy 3 n'],'_{-', '%.2f'%self.Ldic['Galaxy 3 n'],'}^{+', '%.2f'%self.Udic['Galaxy 3 n'], '}$ & $','%.2f'%self.Ddic['Galaxy 3 pa'],'_{-', '%.2f'%self.Ldic['Galaxy 3 pa'],'}^{+', '%.2f'%self.Udic['Galaxy 3 pa'], '}$ & $','%.2f'%self.Ddic['Galaxy 3 q'],'_{-', '%.2f'%self.Ldic['Galaxy 3 q'],'}^{+', '%.2f'%self.Udic['Galaxy 3 q'], '}$',r'\\'
        ###
        print 'lens 1 & $', '%.2f'%self.Ddic['Lens 1 x'], '_{-', '%.2f'%self.Ldic['Lens 1 x'],'}^{+','%.2f'%self.Udic['Lens 1 x'], '}$ & $', '%.2f'%self.Ddic['Lens 1 y'],'_{-', '%.2f'%self.Ldic['Lens 1 y'],'}^{+', '%.2f'%self.Udic['Lens 1 y'], '}$ & $', '%.2f'%self.Ddic['Lens 1 b'],'_{-', '%.2f'%self.Ldic['Lens 1 b'],'}^{+', '%.2f'%self.Udic['Lens 1 b'], '}$ & $', '%.2f'%self.Ddic['Lens 1 eta'],'_{-', '%.2f'%self.Ldic['Lens 1 eta'],'}^{+', '%.2f'%self.Udic['Lens 1 eta'], '}$ & $','%.2f'%self.Ddic['Lens 1 pa'],'_{-', '%.2f'%self.Ldic['Lens 1 pa'],'}^{+', '%.2f'%self.Udic['Lens 1 pa'], '}$ & $','%.2f'%self.Ddic['Lens 1 q'],'_{-', '%.2f'%self.Ldic['Lens 1 q'],'}^{+', '%.2f'%self.Udic['Lens 1 q'], '}$',r'\\\hline'
        ###
        print r'\end{tabular}'
        print r'\caption{', 'shear = $', '%.2f'%self.Ddic['extShear'], '_{-', '%.2f'%self.Ldic['extShear'],'}^{+','%.2f'%self.Udic['extShear'], '}$ , shear pa = $',  '%.2f'%self.Ddic['extShear PA'], '_{-', '%.2f'%self.Ldic['extShear PA'],'}^{+','%.2f'%self.Udic['extShear PA'], '}$}'
        print r'\end{table}'

    def BuildSources(self):
        self.srcs = []
        for number in range(1,1+self.srcno):
            name = 'Source '+str(number)
            p = {}
            for key in 'q','re','n','pa':
                p[key] = self.Ddic[name+' '+key]
            for key in 'x','y': # subtract lens potition - to be added back on later in each likelihood iteration!
                p[key] = self.Ddic[name+' '+key]+self.Ddic['Lens 1 '+key]
            self.srcs.append(SBBModels.Sersic(name,p))

    def BuildGalaxies(self):
        self.gals = []
        for number in range(1,1+self.galno):
            name = 'Galaxy '+str(number)
            p = {}
            for key in 'x','y','q','re','n','pa':
                p[key] = self.Ddic[name+' '+key]
            self.gals.append(SBBModels.Sersic(name,p))

    def BuildLenses(self):
        self.lenses = []
        p = {}
        for key in 'x','y','q','pa','b','eta':
            p[key] = self.Ddic['Lens 1 '+key]
        self.lenses.append(MassModels.PowerLaw('Lens 1',p))
        p = {}
        p['x'] = self.lenses[0].pars['x']
        p['y'] = self.lenses[0].pars['y']
        p['b'] = self.Ddic['extShear']
        p['pa'] = self.Ddic['extShear PA']
        self.lenses.append(MassModels.ExtShear('shear',p))

    def AddImages(self,img1,sig1,psf1,img2,sig2,psf2,Dx=None,Dy=None):
        self.img1=img1
        self.sig1=sig1
        self.psf1=psf1
        self.img2=img2
        self.sig2=sig2
        self.psf2=psf2
        self.Dx=Dx
        self.Dy=Dy
        self.imgs = [self.img1,self.img2]
        self.sigs = [self.sig1,self.sig2]
        self.psfs = [self.psf1,self.psf2]
        self.PSFs = []
        for i in range(len(self.imgs)):
            psf = self.psfs[i]
            image = self.imgs[i]
            psf /= psf.sum()
            psf = convolve.convolve(image,psf)[1]
            self.PSFs.append(psf)


    def EasyAddImages(self):
        if self.name == 'J0837':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J0837()
        elif self.name == 'J0901':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask  = EELsImages.J0901()
        elif self.name == 'J0913':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask  = EELsImages.J0913(self.srcno)
        elif self.name == 'J1125':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask  = EELsImages.J1125()
        elif self.name == 'J1144':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask   = EELsImages.J1144()
        elif self.name == 'J1218':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask  = EELsImages.J1218()
        elif self.name == 'J1248':
            self.img1,self.sig1,self.psf1,self.Dx,self.Dy,self.OVRS,self.mask  = EELsImages.J1248()
        elif self.name == 'J1323':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask  = EELsImages.J1323(self.srcno)
        elif self.name == 'J1347':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J1347()
        elif self.name == 'J1446':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J1446()
        elif self.name == 'J1605':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J1605(self.srcno)
        elif self.name == 'J1606':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J1606()
        elif self.name == 'J1619':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J1619()
        elif self.name == 'J2228':
            self.img1,self.sig1,self.psf1,self.img2,self.sig2,self.psf2,self.Dx,self.Dy,self.OVRS,self.mask = EELsImages.J2228()
        else:
            print 'are you sure this is an EEL?'
            return
        if self.name == 'J1248':
            self.imgs = [self.img1]
            self.sigs = [self.sig1]
            self.psfs = [self.psf1]
        else:
            self.imgs = [self.img1,self.img2]
            self.sigs = [self.sig1,self.sig2]
            self.psfs = [self.psf1,self.psf2]
        self.PSFs = []
        for i in range(len(self.imgs)):
            psf = self.psfs[i]
            image = self.imgs[i]
            psf /= psf.sum()
            psf = convolve.convolve(image,psf)[1]
            self.PSFs.append(psf)
        yc,xc = iT.overSample(self.img1.shape,self.OVRS)
        yo,xo = iT.overSample(self.img1.shape,1)
        tck = RectBivariateSpline(yo[:,0],xo[0],self.mask)
        mask2 = tck.ev(xc,yc)
        mask2[mask2<0.5] = 0
        mask2[mask2>0.5] = 1
        self.mask2 = mask2==0
        self.mask = self.mask==0


    def GetFits(self,plotsep=False,plotresid=False,plotcomps=False):
        print "why didn't you save these before?!?"
        OVRS=self.OVRS
        mask,mask2 = self.mask, self.mask2
        yo,xo = iT.coords(self.img1.shape)
        yc,xc=iT.overSample(self.img1.shape,OVRS)
        colours = [bands[self.name], 'F814W']
        models = []
        fits = []
        for i in range(len(self.imgs)):
            if i == 0:
                dx,dy = 0,0
            else:
                dx = self.Ddic['xoffset']
                dy = self.Ddic['yoffset']
            xp,yp = xc+dx+self.Dx,yc+dy+self.Dy
            xop,yop = xo+dy+self.Dx,yo+dy+self.Dy
            image = self.imgs[i]
            sigma = self.sigs[i]
            psf = self.PSFs[i]
            imin,sigin,xin,yin = image.flatten(), sigma.flatten(),xp.flatten(),yp.flatten()
            n = 0
            model = np.empty(((len(self.gals) + len(self.srcs)+1),imin.size))
            for gal in self.gals:
                gal.setPars()
                tmp = xc*0.
                tmp = gal.pixeval(xp,yp,1./OVRS,csub=11) # evaulate on the oversampled grid. OVRS = number of new pixels per old pixel.
                tmp = iT.resamp(tmp,OVRS,True) # convert it back to original size
                tmp = convolve.convolve(tmp,psf,False)[0]
                model[n] = tmp.ravel()
                n +=1
            for lens in self.lenses:
                lens.setPars()
            x0,y0 = pylens.lens_images(self.lenses,self.srcs,[xp,yp],1./OVRS,getPix=True)
            for src in self.srcs:
                src.setPars()
                tmp = xc*0.
                if 'boxiness' in self.dic.keys():
                    if src.pars['q']<0.2:
                        print 'this source has a boxy/disky component with c = ', '%.2f'%self.Ddic['boxiness'], '. I hope this is J1606!'
                        tmp = src.boxypixeval(x0,y0,1./OVRS,csub=11,c=self.Ddic['boxiness'])
                    else:
                        tmp = src.pixeval(x0,y0,1./OVRS,csub=11)
                else:
                    tmp = src.pixeval(x0,y0,1./OVRS,csub=11)
                tmp = iT.resamp(tmp,OVRS,True)
                tmp = convolve.convolve(tmp,psf,False)[0]
                model[n] = tmp.ravel()
                if self.name == 'J0837':
                    if src.name == 'Source 2':
                        print "just making J0837's second source component into a dust lane..."
                        model[n] *= -1
                n +=1
            model[n] = np.ones(model[n].shape)
            n +=1
            # mask to get amplitudes
            mmodel = model.reshape((n,image.shape[0],image.shape[1]))
            mmmodel = np.empty(((len(self.gals) + len(self.srcs)+1),image[mask].size))
            for m in range(mmodel.shape[0]):
                mmmodel[m] = mmodel[m][mask]
            op = (mmmodel/sigma[mask]).T
            rhs = image[mask]/sigma[mask]
            fit, chi = optimize.nnls(op,rhs)
            
            components = (model.T*fit).T.reshape((n,image.shape[0],image.shape[1]))
            model = components.sum(0)
            models.append(model)
            if plotsep:
                SotPleparately(image,model,sigma,colours[i])
            if plotresid:
                NotPlicely(image,model,sigma,colours[i])
            if plotcomps:
                CotSomponents(components,colours[i])
            fits.append(fit)
        self.fits = fits
            
    def Initialise(self):
        self.MakeDict()
        self.BuildSources()
        self.BuildGalaxies()
        self.BuildLenses()
        self.EasyAddImages()
        self.GetFits(plotresid=False)

    def GalaxySize(self,kpc=False):
        self.z = lens_redshifts[self.name]
        self.Da = astCalc.da(self.z)
        self.scale = self.Da*1e3*np.pi/180./3600.
        if self.galno == 1:
            self.Re_v = self.Ddic['Galaxy 1 re']*0.05
            self.Re_i = self.Re_v.copy()
            self.Re_lower = self.Ldic['Galaxy 1 re']*0.05
            self.Re_upper = self.Udic['Galaxy 1 re']*0.05
        elif self.galno == 2:
            Xgrid = np.logspace(-4,5,1501)
            Res = []
            for i in range(len(self.imgs)):
                galaxy = self.fits[i][0]*self.gals[0].eval(Xgrid) + self.fits[i][1]*self.gals[1].eval(Xgrid)
                R = Xgrid.copy()
                light = galaxy*2.*np.pi*R
                mod = splrep(R,light,t=np.logspace(-3.8,4.8,1301))
                intlight = np.zeros(len(R))
                for i in range(len(R)):
                    intlight[i] = splint(0,R[i],mod)
                model = splrep(intlight[:-300],R[:-300])
                if len(model[1][np.where(np.isnan(model[1])==True)]>0):
                    print "arrays need to be increasing monotonically! But don't worry about it"
                    model = splrep(intlight[:-450],R[:-450])
                if len(model[1][np.where(np.isnan(model[1])==True)]>0):
                    print "take two: arrays need to be increasing monotonically! But don't worry about it"
                    model = splrep(intlight[:-600],R[:-600])
                if len(model[1][np.where(np.isnan(model[1])==True)]>0):
                    print "take three: arrays need to be increasing monotonically! But don't worry about it"
                    model = splrep(intlight[:-700],R[:-700])
                reff = splev(0.5*intlight[-1],model)
                Res.append(reff*0.05)
            self.Re_v,self.Re_i = Res
        else:
            print 'do you have more than two galaxy components? and do you NEED them really?'
        if kpc:
            return [self.Re_v*self.scale, self.Re_i*self.scale]
        return [self.Re_v, self.Re_i]

    def GalaxyObsMag(self):
        ZPdic = dict([('F555W',25.711),('F606W',26.493),('F814W',25.947)])
        self.ZPs = [ZPdic[bands[self.name]],ZPdic['F814W']]
        if self.galno == 1:
            self.mag_v = self.gals[0].getMag(self.fits[0][0],self.ZPs[0])
            self.mag_i = self.gals[0].getMag(self.fits[1][0],self.ZPs[1])
        elif self.galno == 2:
            mv1,mv2 = self.gals[0].getMag(self.fits[0][0],self.ZPs[0]), self.gals[1].getMag(self.fits[0][1],self.ZPs[0])
            mi1,mi2 = self.gals[0].getMag(self.fits[1][0],self.ZPs[1]),self.gals[1].getMag(self.fits[1][1],self.ZPs[1]) 
            Fv = 10**(0.4*(self.ZPs[0]-mv1)) + 10**(0.4*(self.ZPs[0]-mv2))
            Fi = 10**(0.4*(self.ZPs[1]-mi1)) + 10**(0.4*(self.ZPs[1]-mi2))
            self.mag_v, self.mag_i = -2.5*np.log10(Fv) + self.ZPs[0], -2.5*np.log10(Fi) + self.ZPs[1]
        else:
            print 'you have more than two galaxy components?!'
        return [self.mag_v, self.mag_i]

    def GetSB(self):
        self.mu_v = self.mag_v + 2.5*np.log10(2.*np.pi*self.Re_v**2.)
        self.mu_i = self.mag_i + 2.5*np.log10(2.*np.pi*self.Re_i**2.)
        return [self.mu_v, self.mu_i]
    
    def GetPhotometry(self,K=False):
        if bands[self.name] == 'F555W':
            vband, bband = MassV2, MassV2toB
        elif bands[self.name] == 'F606W':
            vband, bband = MassV1, MassV1toB
        iband, kband = MassI, MassK
        self.Lv,self.mag_v_rest = vband(self.mag_v, self.z)
        self.Li,self.mag_i_rest = iband(self.mag_i, self.z)
        self.Lb, self.mag_b_rest = bband(self.mag_v, self.z)
        if K:
            self.Lk,self.mag_k_rest = kband(self.mag_k, self.z)
        return [self.mag_v_rest, self.mag_i_rest, self.mag_b_rest], [self.Lv, self.Li, self.Lb]

    def GetPhotometryAtAge(self,K=False,age=4.):
        if bands[self.name] == 'F555W':
            vband, bband = MassV2, MassV2toB
        elif bands[self.name] == 'F606W':
            vband, bband = MassV1, MassV1toB
        iband, kband = MassI, MassK
        Lv,mag_v_rest = vband(self.mag_v, self.z,age=age)
        Li,mag_i_rest = iband(self.mag_i, self.z,age=age)
        Lb, mag_b_rest = bband(self.mag_v, self.z,age=age)
        if K:
            self.Lk,self.mag_k_rest = kband(self.mag_k, self.z,age=age)
        return Lv, Li, Lb

    def GetRestSB(self):
        self.mu_v_rest = self.mag_v_rest + 2.5*np.log10(2.*np.pi*self.Re_v**2.)
        self.mu_i_rest = self.mag_i_rest + 2.5*np.log10(2.*np.pi*self.Re_i**2.)
        return [self.mu_v_rest, self.mu_i_rest]

    def Arcsec2Kpc(self,z=None):
        self.z=z
        self.Da = astCalc.da(self.z)
        self.scale = self.Da*1e3*np.pi/180./3600.
        self.Re_v_kpc = self.Re_v*scale
        self.Re_i_kpc = self.Re_i*scale
        return [self.Re_v_kpc,self.Re_i_kpc]

    def MakePDFDict(self):
        self.dictionaries = []
        for b1,b2 in itertools.product(range(self.trace.shape[0]), range(self.trace.shape[1])):
            go = []
            for key in self.dic.keys():
                go.append((key,self.dic[key][b1,b2]))
            go = dict(go)
            self.dictionaries.append(go)
        print len(self.dictionaries)

    def GetPDFs(self,kpc=False):
        self.muPDF = []
        self.murestPDF = []
        self.RePDF = []
        self.magrestPDF = []
        self.LumPDF = []
        self.magPDF = []
        self.fitPDF = []
        self.viPDF = []
        OVRS,mask,mask2=self.OVRS,self.mask,self.mask2
        yo,xo = iT.coords(self.img1.shape)
        yc,xc=iT.overSample(self.img1.shape,OVRS)
        colours = [bands[self.name], 'F814W']
        for b1 in range(0,len(self.dictionaries),400):
            srcs,gals,lenses = [],[],[]
            for number in range(1,1+self.srcno):
                name = 'Source '+str(number)
                p = {}
                for key in 'q','re','n','pa':
                    p[key] = self.dictionaries[b1][name+' '+key]
                for key in 'x','y': # subtract lens potition - to be added back on later in each likelihood iteration!
                    p[key] = self.dictionaries[b1][name+' '+key]+self.dictionaries[b1]['Lens 1 '+key]
                srcs.append(SBBModels.Sersic(name,p))
            for number in range(1,1+self.galno):
                name = 'Galaxy '+str(number)
                p = {}
                for key in 'x','y','q','re','n','pa':
                    p[key] = self.dictionaries[b1][name+' '+key]
                gals.append(SBBModels.Sersic(name,p))
            p = {}
            for key in 'x','y','q','pa','b','eta':
                p[key] = self.dictionaries[b1]['Lens 1 '+key]
            lenses.append(MassModels.PowerLaw('Lens 1',p))
            p = {}
            p['x'] = lenses[0].pars['x']
            p['y'] = lenses[0].pars['y']
            p['b'] = self.dictionaries[b1]['extShear']
            p['pa'] = self.dictionaries[b1]['extShear PA']
            lenses.append(MassModels.ExtShear('shear',p))
            # fits
            fits = []
            for i in range(len(self.imgs)):
                if i == 0:
                    dx,dy = 0,0
                else:
                    dx = self.dictionaries[b1]['xoffset']
                    dy = self.dictionaries[b1]['yoffset']
                xp,yp = xc+dx+self.Dx,yc+dy+self.Dy
                xop,yop = xo+dy+self.Dx,yo+dy+self.Dy
                image = self.imgs[i]
                sigma = self.sigs[i]
                psf = self.PSFs[i]
                imin,sigin,xin,yin = image.flatten(), sigma.flatten(),xp.flatten(),yp.flatten()
                n = 0
                model = np.empty(((len(gals) + len(srcs)+1),imin.size))
                for gal in gals:
                    gal.setPars()
                    tmp = xc*0.
                    tmp = gal.pixeval(xp,yp,1./OVRS,csub=11) 
                    tmp = iT.resamp(tmp,OVRS,True) 
                    tmp = convolve.convolve(tmp,psf,False)[0]
                    model[n] = tmp.ravel()
                    n +=1
                for lens in lenses:
                    lens.setPars()
                    x0,y0 = pylens.lens_images(lenses,srcs,[xp,yp],1./OVRS,getPix=True)
                for src in srcs:
                    src.setPars()
                    tmp = xc*0.
                    if 'boxiness' in self.dic.keys() and src.name == 'Source 2':
                        tmp = src.boxypixeval(x0,y0,1./OVRS,csub=11,c=self.dictionaries[b1]['boxiness'])
                    else:
                        tmp = src.pixeval(x0,y0,1./OVRS,csub=11)
                    tmp = iT.resamp(tmp,OVRS,True)
                    tmp = convolve.convolve(tmp,psf,False)[0]
                    model[n] = tmp.ravel()
                    if self.name == 'J0837':
                        if src.name == 'Source 2':
                            model[n] *= -1
                    n +=1
                model[n] = np.ones(model[n].shape)
                n +=1
                
                mmodel = model.reshape((n,image.shape[0],image.shape[1]))
                mmmodel = np.empty(((len(gals) + len(srcs)+1),image[mask].size))
                for m in range(mmodel.shape[0]):
                    mmmodel[m] = mmodel[m][mask]
                
                op = (mmmodel/sigma[mask]).T
                rhs = image[mask]/sigma[mask]
                fit, chi = optimize.nnls(op,rhs)
                fits.append(fit)
            # source plane (observed) magnitudes
            if self.galno == 1:
                mag_v = gals[0].getMag(fits[0][0],self.ZPs[0])
                mag_i = gals[0].getMag(fits[1][0],self.ZPs[1])
            elif self.galno == 2:
                if np.any(fits[0][0:2]==0):
                    print 'hh'
                    ii = np.where(fits[0][0:2] !=0)[0]
                    mag_v = gals[ii].getMag(fits[0][ii],self.ZPs[0])
                else:
                    mv1,mv2 = gals[0].getMag(fits[0][0],self.ZPs[0]), gals[1].getMag(fits[0][1],self.ZPs[0])
                    Fv = 10**(0.4*(self.ZPs[0]-mv1)) + 10**(0.4*(self.ZPs[0]-mv2))
                    mag_v = -2.5*np.log10(Fv) + self.ZPs[0]
                if np.any(fits[1][0:2]==0):
                    print 'gg'
                    ii = np.where(fits[1][0:2] !=0)[0]
                    mag_i = gals[ii].getMag(fits[1][ii],self.ZPs[1])
                else:
                    mi1,mi2 = gals[0].getMag(fits[1][0],self.ZPs[1]),gals[1].getMag(fits[1][1],self.ZPs[1]) 
                    Fi = 10**(0.4*(self.ZPs[1]-mi1)) + 10**(0.4*(self.ZPs[1]-mi2))
                    mag_i = -2.5*np.log10(Fi) + self.ZPs[1]
            else:
                print 'how many galaxies do you want from me? 5 quid per object'
            # intrinsic magnitudes
            if bands[self.name] == 'F555W':
                vband = MassV2
                bband = MassV2toB
            elif bands[self.name] == 'F606W':
                vband = MassV1
                bband = MassV1toB
            iband, kband = MassI, MassK
            Lv,mag_v_rest = vband(mag_v, self.z)
            Li,mag_i_rest = iband(mag_i, self.z)
            Lb,mag_b_rest = bband(mag_v,self.z)
            # sizes
            if self.galno == 1:
                Re_v, Re_i = gals[0].pars['re']*0.05, gals[0].pars['re']*0.05
            elif self.galno == 2:
                Xgrid = np.logspace(-4,5,1501)
                Ygrid = np.logspace(-4,5,1501)
                bandRes = []
                for i in range(len(self.imgs)):
                    galaxy = fits[i][0]*gals[0].eval(Xgrid) + fits[i][1]*gals[1].eval(Xgrid)
                    R = Xgrid.copy()
                    light = galaxy*2.*np.pi*R
                    mod = splrep(R,light,t=np.logspace(-3.8,4.8,1301))
                    intlight = np.zeros(len(R))
                    for i in range(len(R)):
                        intlight[i] = splint(0,R[i],mod)
                    model = splrep(intlight[:-300],R[:-300])
                    if len(model[1][np.where(np.isnan(model[1])==True)]>0):
                        model = splrep(intlight[:-600],R[:-600])
                    if len(model[1][np.where(np.isnan(model[1])==True)]>0):
                        model = splrep(intlight[:-700],R[:-700])
                    reff = splev(0.5*intlight[-1],model)
                    bandRes.append(reff*0.05)
                Re_v,Re_i = bandRes
            # surface brightnesses
            mu_v_rest = mag_v_rest +  2.5*np.log10(2.*np.pi*Re_v**2.)
            mu_i_rest = mag_i_rest + 2.5*np.log10(2.*np.pi*Re_i**2.)
            mu_b_rest = mag_b_rest + 2.5*np.log10(2.*np.pi*Re_v**2.)
            mu_v = mag_v +  2.5*np.log10(2.*np.pi*Re_v**2.)
            mu_i = mag_i + 2.5*np.log10(2.*np.pi*Re_i**2.)
            self.muPDF.append([mu_v,mu_i])
            self.murestPDF.append([mu_v_rest,mu_i_rest,mu_b_rest])
	    if kpc:
		self.RePDF.append([Re_v*self.scale,Re_i*self.scale])
	    else:
		self.RePDF.append([Re_v,Re_i])
            self.magrestPDF.append([mag_v_rest,mag_i_rest,mag_b_rest])
            self.LumPDF.append([Lv,Li,Lb])
            self.magPDF.append([mag_v,mag_i])
            self.fitPDF.append(fits)
            self.viPDF.append(mag_v-mag_i)

    #def EasyAddPDFs(self):
    #    self.muPDF, self.magPDF, self.fitPDF, self.viPDF,self.RePDF = np.load('/data/ljo31/Lens/PDFs/211_lensgals_'+str(self.name+'.npy'))
    #    self.muPDF,self.magPDF,self.fitPDF,self.RePDF = self.muPDF[0],self.magPDF[0],self.fitPDF[0],self.RePDF[0]



    def PrintPDFTable(self):
        magPDF,magrestPDF,muPDF,RePDF,LumPDF = np.array(self.magPDF),np.array(self.magrestPDF),np.array(self.muPDF),np.array(self.RePDF),np.array(self.LumPDF)
        print r'\begin{table}[H]'
        print r'\centering'
        print r'\begin{tabular}{|c|cccccc|}\hline'
        print r' band & $m_{int}$ & $m_{rest}$ & $\mu_{e}$ & $R_e$ / ', r"$''$ & $R_e$ / kpc & $\log(L)$ ",r'\\\hline'
        print bands[self.name], '& $', '%.2f'%(np.percentile(magPDF[:,0],50)), '_{-','%.2f'%(np.percentile(magPDF[:,0],50)-np.percentile(magPDF[:,0],16)), '}^{+', '%.2f'%(np.percentile(magPDF[:,0],84)-np.percentile(magPDF[:,0],50)), '}$ & $', '%.2f'%(np.percentile(magrestPDF[:,0],50)), '_{-','%.2f'%(np.percentile(magrestPDF[:,0],50)-np.percentile(magrestPDF[:,0],16)), '}^{+', '%.2f'%(np.percentile(magrestPDF[:,0],84)-np.percentile(magrestPDF[:,0],50)), '}$ & $', '%.2f'%(np.percentile(muPDF[:,0],50)), '_{-','%.2f'%(np.percentile(muPDF[:,0],50)-np.percentile(muPDF[:,0],16)), '}^{+', '%.2f'%(np.percentile(muPDF[:,0],84)-np.percentile(muPDF[:,0],50)), '}$ & $', '%.2f'%(np.percentile(RePDF[:,0],50)), '_{-','%.2f'%(np.percentile(RePDF[:,0],50)-np.percentile(RePDF[:,0],16)), '}^{+', '%.2f'%(np.percentile(RePDF[:,0],84)-np.percentile(RePDF[:,0],50)), '}$ & $', '%.2f'%(np.percentile(RePDF[:,0],50)*self.scale), '_{-','%.2f'%(self.scale*(np.percentile(RePDF[:,0],50)-np.percentile(RePDF[:,0],16))), '}^{+', '%.2f'%(self.scale*(np.percentile(RePDF[:,0],84)-np.percentile(RePDF[:,0],50))), '}$ & $', '%.2f'%(np.percentile(LumPDF[:,0],50)), '_{-','%.2f'%(np.percentile(LumPDF[:,0],50)-np.percentile(LumPDF[:,0],16)), '}^{+', '%.2f'%(np.percentile(LumPDF[:,0],84)-np.percentile(LumPDF[:,0],50)), r'}$ \\'
        print 'F814W', '& $', '%.2f'%(np.percentile(magPDF[:,1],50)), '_{-','%.2f'%(np.percentile(magPDF[:,1],50)-np.percentile(magPDF[:,1],16)), '}^{+', '%.2f'%(np.percentile(magPDF[:,1],84)-np.percentile(magPDF[:,1],50)), '}$ & $', '%.2f'%(np.percentile(magrestPDF[:,1],50)), '_{-','%.2f'%(np.percentile(magrestPDF[:,1],50)-np.percentile(magrestPDF[:,1],16)), '}^{+', '%.2f'%(np.percentile(magrestPDF[:,1],84)-np.percentile(magrestPDF[:,1],50)), '}$ & $', '%.2f'%(np.percentile(muPDF[:,1],50)), '_{-','%.2f'%(np.percentile(muPDF[:,1],50)-np.percentile(muPDF[:,1],16)), '}^{+', '%.2f'%(np.percentile(muPDF[:,1],84)-np.percentile(muPDF[:,1],50)), '}$ & $', '%.2f'%(np.percentile(RePDF[:,1],50)), '_{-','%.2f'%(np.percentile(RePDF[:,1],50)-np.percentile(RePDF[:,1],16)), '}^{+', '%.2f'%(np.percentile(RePDF[:,1],84)-np.percentile(RePDF[:,1],50)), '}$ & $', '%.2f'%(np.percentile(RePDF[:,1],50)*self.scale), '_{-','%.2f'%(self.scale*(np.percentile(RePDF[:,1],50)-np.percentile(RePDF[:,1],16))), '}^{+', '%.2f'%(self.scale*(np.percentile(RePDF[:,1],84)-np.percentile(RePDF[:,1],50))), '}$ & $', '%.2f'%(np.percentile(LumPDF[:,1],50)), '_{-','%.2f'%(np.percentile(LumPDF[:,1],50)-np.percentile(LumPDF[:,1],16)), '}^{+', '%.2f'%(np.percentile(LumPDF[:,1],84)-np.percentile(LumPDF[:,1],50)), r'}$ \\\hline'
        print r'\end{tabular}'
        print r'\caption{Galaxy photometry}'
        print r'\end{table}'

   
    def UncertaintiesFromPDF(self,makecat=False):
        magPDF,muPDF,RePDF,viPDF = np.array(self.magPDF),np.array(self.muPDF),np.array(self.RePDF),np.array(self.viPDF)
        keys = ['magPDF','muPDF','RePDF','viPDF']
        vals = [magPDF,muPDF,RePDF,viPDF]
        l,d,u=[],[],[]
        f1,f2,f3 = np.zeros((len(keys),2)),np.zeros((len(keys),2)),np.zeros((len(keys),2))
        for i in range(len(vals)):
            key = keys[i]
            print key
            f = vals[i]
            if key == 'viPDF':
                L,M,U = np.percentile(f,16), np.percentile(f,50),np.percentile(f,84)
                V = [M-L, M, U-M]
                d.append((key,V[1]))
                l.append((key,V[0]))
                u.append((key,V[2]))
                f1[i],f2[i],f3[i] = [V[1],0],[V[0],0], [V[2],0]
            else:
                V,I =  map(lambda v: (v[1]-v[0],v[1],v[2]-v[1]),zip(*np.percentile(f,[16,50,84],axis=0)))
                d.append((key,[V[1],I[1]]))
                l.append((key,[V[0],I[0]]))
                u.append((key,[V[2],I[2]]))
                f1[i],f2[i],f3[i] = [V[1],I[1]],[V[0],I[0]], [V[2],I[2]]
        self.photometry = [l,d,u]
        if makecat:
            return f1.flatten().tolist(),f2.flatten().tolist(), f3.flatten().tolist()
        return d,l,u
