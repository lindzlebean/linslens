from linslens import EELsKeckLensModels as L
import numpy as np

def MakeTab(model):
    model.Initialise()
    mags = model.GalaxyObsMag()
    Res = model.GalaxySize(kpc=True)
    mus = model.GetSB()
    model.MakePDFDict()
    model.GetPDFs(kpc=True)
    med,lo,hi = model.UncertaintiesFromPDF(makecat=True)
    np.save('/data/ljo31/Lens/PDFs/212_Kp_lensgals_huge_'+str(model.name), [np.array(model.muPDF),np.array(model.magPDF),np.array(model.RePDF)])
    return med,lo,hi

'''dir = '/data/ljo31/Lens/LensModels/twoband/'

files = [dir+'J0837_Kp_211',dir+'J0901_Kp_211',dir+'J0913_Kp_211',dir+'J1125_Kp_211',dir+'J1144_Kp_211',dir+'J1218_Kp_211',dir+'J1323_Kp_211',dir[:-8]+'J1347_Kp_211',dir+'J1446_Kp_211',dir+'J1605_Kp_211',dir+'J1606_Kp_211',dir[:-8]+'J1619_Kp_211_lensandgalon',dir+'J2228_Kp_211']

hstfiles = [dir+'J0837_211',dir+'J0901_211',dir+'J0913_211',dir+'J1125_211',dir+'J1144_211',dir+'J1218_211',dir+'J1323_211',dir[:-8]+'J1347_211',dir+'J1446_211',dir+'J1605_211',dir+'J1606_211',dir[:-8]+'J1619_211',dir+'J2228_211']

names = ['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']

cats_m, cats_l, cats_h = [], [], []

for ii in range(len(names)):
    result = np.load(files[ii])
    hstresult = np.load(hstfiles[ii])
    model = L.EELs(result,hstresult,names[ii])
    med,lo,hi = MakeTab(model)
    cats_m.append(med)
    cats_l.append(lo)
    cats_h.append(hi)
    print names[ii], 'done'




m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)


from astropy.io.fits import *
names = np.array(names)

dic = dict([])
dic['name'] = names
dic['mag k'] = m[:,0]
dic['mu k'] = m[:,1]
dic['Re k'] = m[:,2]
dic['mag k lo'] = l[:,0]
dic['mu k lo'] = l[:,1]
dic['Re k lo'] = l[:,2]
dic['mag k hi'] = h[:,0]
dic['mu k hi'] = h[:,1]
dic['Re k hi'] = h[:,2]
np.save('/data/ljo31/Lens/LensParams/KeckPhot_lensgals_1src_new_huge_dict',dic)
'''
dir = '/data/ljo31/Lens/LensModels/twoband/'

files = [dir+'J0837_Kp_211',dir+'J0901_Kp_211',dir+'J0913_Kp_212',dir+'J1125_Kp_212',dir+'J1144_Kp_212',dir+'J1218_Kp_211',dir+'J1323_Kp_211',dir[:-8]+'J1347_Kp_112',dir+'J1446_Kp_212',dir+'J1605_Kp_212',dir+'J1606_Kp_212',dir+'J1619_Kp_212_lensandgalon',dir+'J2228_Kp_212']

hstfiles = [dir+'J0837_211',dir+'J0901_211',dir+'J0913_212',dir+'J1125_212',dir+'J1144_212',dir+'J1218_211',dir+'J1323_211',dir[:-8]+'J1347_112',dir+'J1446_212',dir+'J1605_212',dir+'J1606_212',dir+'J1619_212',dir+'J2228_212']

names = ['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228']



cats_m, cats_l, cats_h = [], [], []

for ii in range(len(names)):
    result = np.load(files[ii])
    hstresult = np.load(hstfiles[ii])
    model = L.EELs(result,hstresult,names[ii])
    med,lo,hi = MakeTab(model)
    cats_m.append(med)
    cats_l.append(lo)
    cats_h.append(hi)
    print names[ii], 'done'




m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)


from astropy.io.fits import *
names = np.array(names)

dic = dict([])
dic['name'] = names
dic['mag k'] = m[:,0]
dic['mu k'] = m[:,1]
dic['Re k'] = m[:,2]
dic['mag k lo'] = l[:,0]
dic['mu k lo'] = l[:,1]
dic['Re k lo'] = l[:,2]
dic['mag k hi'] = h[:,0]
dic['mu k hi'] = h[:,1]
dic['Re k hi'] = h[:,2]
np.save('/data/ljo31/Lens/LensParams/KeckPhot_lensgals_2src_new_huge_dict',dic)

