from linslens.Profiles import *
from astLib import astCalc
import glob, numpy as np, pylab as pl
import lenslib
from jeans.makemodel import deproject
import GetStellarMass

names = ['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']
lz = np.load('/data/ljo31/Lens/LensParams/LensRedshiftsUpdated.npy')[()]

name = 'J0913'

dir = '/data/ljo31b/EELs/galsub/emceeruns/'
file = glob.glob(dir+name+'_parametric_*')
file.sort()
f = file[-1]
if 'DPL' in f:
    f = file[-2]

result_PL = np.load(f)

file = glob.glob(dir+name+'_parametric_DPL*')
file.sort()
f = file[-1]
result_DPL = np.load(f)

lp_PL,trace_PL,dic_PL,_ = result_PL
lp_DPL,trace_DPL,dic_DPL,_ = result_DPL
a1_PL,a3_PL = np.unravel_index(lp_PL[:,0].argmax(),lp_PL[:,0].shape)
a1_DPL,a3_DPL = np.unravel_index(lp_DPL[:,0].argmax(),lp_DPL[:,0].shape)

## quantities
zl = lz[name][0]
scale = astCalc.da(zl)*np.pi/180./3600 * 1e3
eta = dic_PL['Lens 1 eta'][a1_PL,0,a3_PL]
eta_l = np.percentile(dic_PL['Lens 1 eta'][:,0].ravel(),16)
eta_u = np.percentile(dic_PL['Lens 1 eta'][:,0].ravel(),84)


gamma = dic_DPL['Lens 1 gamma'][a1_DPL,0,a3_DPL]
rs = dic_DPL['Lens 1 rs'][a1_DPL,0,a3_DPL]*0.05*scale
gamma_l = np.percentile(dic_DPL['Lens 1 gamma'][:,0].ravel(),16)
gamma_u = np.percentile(dic_DPL['Lens 1 gamma'][:,0].ravel(),84)
rs_l = np.percentile(dic_DPL['Lens 1 rs'][:,0].ravel(),16)
rs_u = np.percentile(dic_DPL['Lens 1 rs'][:,0].ravel(),84)

r = np.logspace(-7,3,3500)
dpdr_PL = dlogrho_dlogr_PL(r,eta)
dpdr_PL_l = dlogrho_dlogr_PL(r,eta_l)
dpdr_PL_u = dlogrho_dlogr_PL(r,eta_u)


dpdr_DPL = dlogrho_dlogr_gNFW(r,gamma,rs)
dpdr_DPL_l = dlogrho_dlogr_gNFW(r,gamma_l,rs)
dpdr_DPL_u = dlogrho_dlogr_gNFW(r,gamma_u,rs)


pl.figure()
pl.plot(r,dpdr_PL,color='Crimson',label='power law')
pl.plot(r,dpdr_DPL,color='SteelBlue',label='gNFW')
pl.legend(loc='lower right',ncol=2,fontsize=15)
pl.ylabel('DM density slope')
pl.xlabel('radius (kpc)')

pl.fill_between(r,dpdr_PL_l, dpdr_PL_u, color='LightPink',alpha=0.5)
pl.fill_between(r,dpdr_DPL_l, dpdr_DPL_u, color='LightBlue',alpha=0.5)

### also old result -- Einstein radius
cat = np.load('/data/ljo31/Lens/LensParams/Structure_lensgals_2src.npy')[0]
rein = cat[name]['Lens 1 b']*0.05*scale

pl.axvline(rein,color='k',ls='-.',label='Einstein radius',lw=4) # Einstein radius
pl.axvline(rein*cat[name]['Lens 1 q'],color='k',ls='-.',label='Einstein radius',lw=4) # Einstein radius

pl.xlim([0,15])
pl.title(name)
### finally, put some info on the plot
eta_PL, gamma_DPL, rs_DPL = dic_PL['Lens 1 eta'][a1_PL,0,a3_PL], dic_DPL['Lens 1 gamma'][a1_DPL,0,a3_DPL], dic_DPL['Lens 1 rs'][a1_DPL,0,a3_DPL]*0.05*scale
pl.figtext(0.75,0.42,'$\gamma_{PL} = $'+'%.2f'%(1+eta_PL),fontsize=15)
##
pl.figtext(0.73,0.37,'$\gamma_{gNFW} = $'+'%.2f'%gamma_DPL,fontsize=15)
pl.figtext(0.71,0.32,'$r_{s,gNFW} = $'+'%.2f'%rs_DPL+'kpc',fontsize=15)
##
pl.figtext(0.67,0.47,r'$\bar{\gamma}_{gNFW}(<R_{ein}) = 2.37$',fontsize=15)
#pl.figtext(0.69,0.52,r'$\bar{\gamma}_{PL}(<R_{ein}) = 2.32$',fontsize=15)

pl.show()

