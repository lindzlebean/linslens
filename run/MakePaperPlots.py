import EELsModels as L
import numpy as np
import pylab as pl

def MakeTab(model):
    model.Initialise()
    model.GetFits(plotsep=True,cmap='bone')
    pl.savefig('/data/ljo31/Lens/TeXstuff/paper/211I'+str(model.name)+'resid.pdf')
    pl.close('all')
    model.GetFits(plotsep=True,cmap='bone_r')
    pl.close()
    pl.savefig('/data/ljo31/Lens/TeXstuff/paper/211I'+str(model.name)+'model.pdf')
    pl.close()
    pl.savefig('/data/ljo31/Lens/TeXstuff/paper/211I'+str(model.name)+'data.pdf')
    pl.close('all')
    # V band
    model.GetFits(plotsep=True,cmap='bone')
    pl.close()
    pl.close()
    pl.close()
    pl.savefig('/data/ljo31/Lens/TeXstuff/paper/211V'+str(model.name)+'resid.pdf')
    pl.close('all')
    model.GetFits(plotsep=True,cmap='bone_r')
    pl.close()
    pl.close()
    pl.close()
    pl.close()
    pl.savefig('/data/ljo31/Lens/TeXstuff/paper/211V'+str(model.name)+'model.pdf')
    pl.close()
    pl.savefig('/data/ljo31/Lens/TeXstuff/paper/211V'+str(model.name)+'data.pdf')
    pl.close('all')
    
'''
result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J0913_211')
model = L.EELs(result,name='J0913')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1125_211')
model = L.EELs(result,name='J1125')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1144_211')
model = L.EELs(result,name='J1144')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1323_211') 
model = L.EELs(result,name='J1323')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1347_211')
model = L.EELs(result,name='J1347')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1446_211')
model = L.EELs(result,name='J1446')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1605_211') 
model = L.EELs(result,name='J1605')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1606_211')
model = L.EELs(result,name='J1606')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J2228_211')
model = L.EELs(result,name='J2228')
MakeTab(model)

'''

print '2 src models'

print r'lens & $z_s$ & $z_l$ & $V$ (mag) & $I$ (mag) & $K$ (mag) & $n_1$ & $R_{e,1}$ (kpc) & & $n_2$ & $R_{e,2}$ (kpc)$ & $R_{e,tot}$ (kpc) & $\mu$ \\'

result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J0913_212_nonconcentric')
model = L.EELs(result,name='J0913')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1125_212')
model = L.EELs(result,name='J1125')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1144_212_allparams')
model = L.EELs(result,name='J1144')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1323_212') 
model = L.EELs(result,name='J1323')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1347_112')
model = L.EELs(result,name='J1347')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1446_212')
model = L.EELs(result,name='J1446')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1605_212_final') 
model = L.EELs(result,name='J1605')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1606_112')
model = L.EELs(result,name='J1606')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J2228_212')
model = L.EELs(result,name='J2228')
MakeTab(model)

