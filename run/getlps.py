from linslens import EELsModels_huge as L
import numpy as np, pylab as pl, pyfits as py

for name in ['J0837','J0913','J1144']:#,'J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']:
    print name
    result0 = np.load('/data/ljo31/Lens/LensModels/'+name+'_211')
    if name in ['J0913','J1144']:
        result1 = np.load('/data/ljo31/Lens/'+name+'/twoband_1')
    else:
        result1 = np.load('/data/ljo31/Lens/'+name+'/twoband_0')
    # old model
    model0 = L.EELs(result0,name=name)
    model0.Initialise()
    lp0 = model0.lp
    ### new model
    model1 = L.EELs(result1,name=name)
    model1.Initialise()
    lp1 = model1.lp
    print name, lp0[0]/lp1[0], lp0[1]/lp1[1], (lp0[0]+lp0[1])/(lp1[0]+lp1[1])
    model1.GetFits(plotresid=True)
    model0.GetFits(plotresid=True)
    pl.show()
