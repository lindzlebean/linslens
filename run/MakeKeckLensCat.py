from  linslens import EELsKeckModels as L
import numpy as np

def MakeTab(model):
    model.Initialise()

    mags = model.GetIntrinsicMags()
    Res = model.GetSourceSize(kpc=True)
    restmags, Ls = model.GetPhotometry()
    mus = model.GetSB()
    restmus = model.GetRestSB()
    model.MakePDFDict()
    #model.GetPDFs(kpc=True)
    model.GetPDFs(kpc=True)
    np.save('/data/ljo31/Lens/PDFs/212_Kp'+str(model.name), [np.array(model.muPDF),np.array(model.magPDF),np.array(model.RePDF)])
    med,lo,hi = model.UncertaintiesFromPDF(makecat=True)
    print med,lo,hi
    #np.save('/data/ljo31/Lens/PDFs/211_Kp_new'+str(model.name), [np.array(model.muPDF),np.array(model.magPDF),np.array(model.RePDF)])
    return med,lo,hi

'''
cats_m, cats_l, cats_h = [], [], []
result = np.load('/data/ljo31/Lens/LensModels/J0837_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,hstresult,name='J0837')
print 'J0837'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


hstresult = np.load('/data/ljo31/Lens/LensModels/J0901_211')
result = np.load('/data/ljo31/Lens/LensModels/J0901_Kp_211')
model = L.EELs(result,hstresult,name='J0901')
print 'J0901'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


hstresult = np.load('/data/ljo31/Lens/LensModels/J0913_211')
result = np.load('/data/ljo31/Lens/LensModels/J0913_Kp_211')
model = L.EELs(result,hstresult,name='J0913')
print 'J0913'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/J1125/Kp_211_0')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1125_211')
model = L.EELs(result,hstresult,name='J1125')
print 'J1125'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1144_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1144_211')
model = L.EELs(result,hstresult,name='J1144')
print 'J1144'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J1218_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,hstresult,name='J1218')
print 'J1218'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1323_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1323_211') 
model = L.EELs(result,hstresult,name='J1323')
print 'J1323'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1347_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1347_211')
model = L.EELs(result,hstresult,name='J1347')
print 'J1347'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1446_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1446_211')
model = L.EELs(result,hstresult,name='J1446')
print 'J1446'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1605_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1605_211') 
model = L.EELs(result,hstresult,name='J1605')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1606_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1606_211')
model = L.EELs(result,hstresult,name='J1606')
print 'J1606'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1619_Kp_211_lensandgalon')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1619_211')
model = L.EELs(result,hstresult,name='J1619')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J2228_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J2228_211')
model = L.EELs(result,hstresult,name='J2228')
print 'J2228'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)


from astropy.io.fits import *
names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228'])
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
np.save('/data/ljo31/Lens/LensParams/KeckPhot_1src_new_dict',dic)

'''

## 2 src models
cats_m, cats_l, cats_h = [], [], []


result = np.load('/data/ljo31/Lens/LensModels/J0837_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,hstresult,name='J0837')
print 'J0837'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


hstresult = np.load('/data/ljo31/Lens/LensModels/J0901_211')
result = np.load('/data/ljo31/Lens/LensModels/J0901_Kp_211')
model = L.EELs(result,hstresult,name='J0901')
print 'J0901'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J0913_Kp_212')
hstresult = np.load('/data/ljo31/Lens/LensModels/J0913_212_nonconcentric')
model = L.EELs(result,hstresult,name='J0913')
print 'J0913 nonconcentric'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J1125_Kp_212')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1125_212')
model = L.EELs(result,hstresult,name='J1125')
print 'J1125 nonconcentric'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1144_Kp_212')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1144_212_allparams')
model = L.EELs(result,hstresult,name='J1144')
print 'J1144'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1218_Kp_211')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,hstresult,name='J1218')
print 'J1218'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J1323_Kp_212') # this will need updating
hstresult = np.load('/data/ljo31/Lens/LensModels/J1323_212') 
model = L.EELs(result,hstresult,name='J1323')
print 'J1323'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1347_Kp_112')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1347_112')
model = L.EELs(result,hstresult,name='J1347')
print 'J1347'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1446_Kp_212')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1446_212')
model = L.EELs(result,hstresult,name='J1446')
print 'J1446'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1605_Kp_212')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1605_212_final') 
model = L.EELs(result,hstresult,name='J1605')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1606_Kp_112')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1606_112')
model = L.EELs(result,hstresult,name='J1606')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1619_Kp_212_lensandgalon')
hstresult = np.load('/data/ljo31/Lens/LensModels/J1619_212')
model = L.EELs(result,hstresult,name='J1619')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J2228_Kp_212')
hstresult = np.load('/data/ljo31/Lens/LensModels/J2228_212')
model = L.EELs(result,hstresult,name='J2228')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)

names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228'])
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
np.save('/data/ljo31/Lens/LensParams/KeckPhot_2src_new_dict',dic)



'''
from astropy.io.fits import *
names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J2228'])
c1 = Column(name='name', format='A5',array=names)
c2 = Column(name='mag k', format='D',array=m[:,0])
c4 = Column(name='mu k', format='D',array=m[:,2])
c6 = Column(name='Re k', format='D',array=m[:,4])

### and uncertainties - lower bounds
c2l = Column(name='mag k lo', format='D',array=l[:,0])
c4l = Column(name='mu k lo', format='D',array=l[:,2])
c6l = Column(name='Re k lo', format='D',array=l[:,4])

### and upper bounds
c2h = Column(name='mag k hi', format='D',array=h[:,0])
c4h = Column(name='mu k hi' , format='D',array=h[:,2])
c6h = Column(name='Re k hi', format='D',array=h[:,4])

coldefs = ColDefs([c1,c2,c4,c6,c2l,c4l,c6l,c2h,c4h,c6h])
tbhdu = BinTableHDU.from_columns(coldefs)
tbhdu.writeto('/data/ljo31/Lens/LensParams/KeckPhot_2src_new.fits',clobber=True)

'''
