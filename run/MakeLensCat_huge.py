from linslens import EELsModels_huge as L
import numpy as np

def MakeTab(model):
    model.Initialise()
    mags = model.GetIntrinsicMags()
    Res = model.GetSourceSize(kpc=True)
    restmags, Ls = model.GetPhotometry()
    mus = model.GetSB()
    restmus = model.GetRestSB()
    model.MakePDFDict()
    model.GetPDFs(kpc=True)
    med,lo,hi = model.UncertaintiesFromPDF(makecat=True)
    np.save('/data/ljo31/Lens/PDFs/211_huge_new_'+str(model.name), [np.array(model.muPDF),np.array(model.magPDF),np.array(model.RePDF)])
    return med,lo,hi


cats_m, cats_l, cats_h = [], [], []
result = np.load('/data/ljo31/Lens/LensModels/twoband/J0837_211')
model = L.EELs(result,name='J0837')
name = 'J0837'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)
print len(hi)
# also save the PDFs once and for all!!!


result = np.load('/data/ljo31/Lens/LensModels/twoband/J0901_211') # still not done
model = L.EELs(result,name='J0901')
name = 'J0901'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/twoband/J0913_211')
model = L.EELs(result,name='J0913')
name = 'J0913'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/twoband/J1125_211') # not really done yet
model = L.EELs(result,name='J1125')
name = 'J1125'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/twoband/J1144_211')
model = L.EELs(result,name='J1144')
name = 'J1144'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/twoband/J1218_211')
model = L.EELs(result,name='J1218')
name = 'J1218'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/twoband/J1323_211') 
model = L.EELs(result,name='J1323')
name = 'J1323'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/J1347/twoband_0')#needs slight iteration
model = L.EELs(result,name='J1347')
name = 'J1347'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/twoband/J1446_211')
model = L.EELs(result,name='J1446')
name = 'J1446'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/twoband/J1605_211') 
model = L.EELs(result,name='J1605')
name = 'J1605'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/twoband/J1606_211')
model = L.EELs(result,name='J1606')
name = 'J1606'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/twoband/J1619_211')
model = L.EELs(result,name='J1619')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/twoband/J2228_211')
model = L.EELs(result,name='J2228')
name = 'J2228'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)


from astropy.io.fits import *
names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228'])

c1 = Column(name='name', format='A5',array=names)
c2 = Column(name='mag v', format='D',array=m[:,0])
c3 = Column(name='mag i', format='D',array=m[:,1])
c4 = Column(name='mu v', format='D',array=m[:,2])
c5 = Column(name='mu i', format='D',array=m[:,3])
c6 = Column(name='Re v', format='D',array=m[:,4])
c7 = Column(name='Re i', format='D',array=m[:,5])
c8 = Column(name='v-i', format='D',array=m[:,6])

### and uncertainties - lower bounds
c2l = Column(name='mag v lo', format='D',array=l[:,0])
c3l = Column(name='mag i lo', format='D',array=l[:,1])
c4l = Column(name='mu v lo', format='D',array=l[:,2])
c5l = Column(name='mu i lo', format='D',array=l[:,3])
c6l = Column(name='Re v lo', format='D',array=l[:,4])
c7l = Column(name='Re i lo', format='D',array=l[:,5])
c8l = Column(name='v-i lo', format='D',array=l[:,6])


### and upper bounds
c2h = Column(name='mag v hi', format='D',array=h[:,0])
c3h = Column(name='mag i hi', format='D',array=h[:,1])
c4h = Column(name='mu v hi' , format='D',array=h[:,2])
c5h = Column(name='mu i hi', format='D',array=h[:,3])
c6h = Column(name='Re v hi', format='D',array=h[:,4])
c7h = Column(name='Re i hi', format='D',array=h[:,5])
c8h = Column(name='v-i hi', format='D',array=h[:,6])



coldefs = ColDefs([c1,c2,c3,c4,c5,c6,c7,c8,c2l,c3l,c4l,c5l,c6l,c7l,c8l,c2h,c3h,c4h,c5h,c6h,c7h,c8h])
tbhdu = BinTableHDU.from_columns(coldefs)
tbhdu.writeto('/data/ljo31/Lens/LensParams/Phot_1src_huge_new.fits',clobber=True)
'''

cats_m, cats_l, cats_h = [], [], []
result = np.load('/data/ljo31/Lens/J0837/twoband_0')
model = L.EELs(result,name='J0837')
name = 'J0837'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)
print len(hi)
# also save the PDFs once and for all!!!


result = np.load('/data/ljo31/Lens/J0901/twoband_2_pte')
model = L.EELs(result,name='J0901')
name = 'J0901'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/J0913/twoband_212')
model = L.EELs(result,name='J0913')
name = 'J0913'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/J1125/twoband_212_pte_ctd_ctd')
model = L.EELs(result,name='J1125')
name = 'J1125'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/J1144/twoband_212')
model = L.EELs(result,name='J1144')
name = 'J1144'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/J1218/twoband_0')
model = L.EELs(result,name='J1218')
name = 'J1218'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/J1323/twoband_212_ctd_ctd') # laeuft
model = L.EELs(result,name='J1323')
name = 'J1323'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/J1347/twoband_212_ctd_ctd') # laeuft
model = L.EELs(result,name='J1347')
name = 'J1347'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

'''
'''result = np.load('/data/ljo31/Lens/J1446/twoband_0')
model = L.EELs(result,name='J1446')
name = 'J1446'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/J1605/twoband_0') # laueft
model = L.EELs(result,name='J1605')
name = 'J1605'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/J1606/twoband_0')
model = L.EELs(result,name='J1606')
name = 'J1606'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/J1619/twoband_0')
model = L.EELs(result,name='J1619')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/J2228/twoband_0')
model = L.EELs(result,name='J2228')
name = 'J2228'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)'''
'''

m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)


from astropy.io.fits import *
names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228'])
names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347'])

c1 = Column(name='name', format='A5',array=names)
c2 = Column(name='mag v', format='D',array=m[:,0])
c3 = Column(name='mag i', format='D',array=m[:,1])
c4 = Column(name='mu v', format='D',array=m[:,2])
c5 = Column(name='mu i', format='D',array=m[:,3])
c6 = Column(name='Re v', format='D',array=m[:,4])
c7 = Column(name='Re i', format='D',array=m[:,5])
c8 = Column(name='v-i', format='D',array=m[:,6])

### and uncertainties - lower bounds
c2l = Column(name='mag v lo', format='D',array=l[:,0])
c3l = Column(name='mag i lo', format='D',array=l[:,1])
c4l = Column(name='mu v lo', format='D',array=l[:,2])
c5l = Column(name='mu i lo', format='D',array=l[:,3])
c6l = Column(name='Re v lo', format='D',array=l[:,4])
c7l = Column(name='Re i lo', format='D',array=l[:,5])
c8l = Column(name='v-i lo', format='D',array=l[:,6])


### and upper bounds
c2h = Column(name='mag v hi', format='D',array=h[:,0])
c3h = Column(name='mag i hi', format='D',array=h[:,1])
c4h = Column(name='mu v hi' , format='D',array=h[:,2])
c5h = Column(name='mu i hi', format='D',array=h[:,3])
c6h = Column(name='Re v hi', format='D',array=h[:,4])
c7h = Column(name='Re i hi', format='D',array=h[:,5])
c8h = Column(name='v-i hi', format='D',array=h[:,6])



coldefs = ColDefs([c1,c2,c3,c4,c5,c6,c7,c8,c2l,c3l,c4l,c5l,c6l,c7l,c8l,c2h,c3h,c4h,c5h,c6h,c7h,c8h])
tbhdu = BinTableHDU.from_columns(coldefs)
tbhdu.writeto('/data/ljo31/Lens/LensParams/Phot_2src_huge_firsthalf.fits',clobber=True)

'''
'''
## 2 src models
cats_m, cats_l, cats_h = [], [], []

result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
name = 'J0837'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)
print len(hi)


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
name = 'J0901'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J0913_212_nonconcentric')
model = L.EELs(result,name='J0913')
print 'J0913 nonconcentric'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1125_212')
model = L.EELs(result,name='J1125')
print 'J1125 new!!!'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J1144_212_allparams')
model = L.EELs(result,name='J1144')
print 'J1144'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
name = 'J1218'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1323_212') 
model = L.EELs(result,name='J1323')
print 'J1323'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J1347_112')
model = L.EELs(result,name='J1347')
print 'J1347'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1446_212')
model = L.EELs(result,name='J1446')
print 'J1446'
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


result = np.load('/data/ljo31/Lens/LensModels/J1605_212_final') 
model = L.EELs(result,name='J1605')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J1606_112')
model = L.EELs(result,name='J1606')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)

result = np.load('/data/ljo31/Lens/LensModels/J1619_212')
model = L.EELs(result,name='J1619')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)



result = np.load('/data/ljo31/Lens/LensModels/J2228_212')
model = L.EELs(result,name='J2228')
med,lo,hi = MakeTab(model)
cats_m.append(med)
cats_l.append(lo)
cats_h.append(hi)


m, l, h = np.array(cats_m), np.array(cats_l), np.array(cats_h)


from astropy.io.fits import *
names = np.array(['J0837','J0901','J0913','J1125','J1144','J1218','J1323','J1347','J1446','J1605','J1606','J1619','J2228'])


c1 = Column(name='name', format='A5',array=names)
c2 = Column(name='mag v', format='D',array=m[:,0])
c3 = Column(name='mag i', format='D',array=m[:,1])
c4 = Column(name='mu v', format='D',array=m[:,2])
c5 = Column(name='mu i', format='D',array=m[:,3])
c6 = Column(name='Re v', format='D',array=m[:,4])
c7 = Column(name='Re i', format='D',array=m[:,5])
c8 = Column(name='v-i', format='D',array=m[:,6])

### and uncertainties - lower bounds
c2l = Column(name='mag v lo', format='D',array=l[:,0])
c3l = Column(name='mag i lo', format='D',array=l[:,1])
c4l = Column(name='mu v lo', format='D',array=l[:,2])
c5l = Column(name='mu i lo', format='D',array=l[:,3])
c6l = Column(name='Re v lo', format='D',array=l[:,4])
c7l = Column(name='Re i lo', format='D',array=l[:,5])
c8l = Column(name='v-i lo', format='D',array=l[:,6])


### and upper bounds
c2h = Column(name='mag v hi', format='D',array=h[:,0])
c3h = Column(name='mag i hi', format='D',array=h[:,1])
c4h = Column(name='mu v hi' , format='D',array=h[:,2])
c5h = Column(name='mu i hi', format='D',array=h[:,3])
c6h = Column(name='Re v hi', format='D',array=h[:,4])
c7h = Column(name='Re i hi', format='D',array=h[:,5])
c8h = Column(name='v-i hi', format='D',array=h[:,6])



coldefs = ColDefs([c1,c2,c3,c4,c5,c6,c7,c8,c2l,c3l,c4l,c5l,c6l,c7l,c8l,c2h,c3h,c4h,c5h,c6h,c7h,c8h])
tbhdu = BinTableHDU.from_columns(coldefs)

tbhdu.writeto('/data/ljo31/Lens/LensParams/Phot_2src_new.fits',clobber=True)
'''



