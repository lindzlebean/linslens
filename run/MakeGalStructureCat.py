import EELsLensModels as L
import numpy as np

def MakeTab(model):
    model.Initialise()
    lo,med,hi = model.Ldic, model.Ddic, model.Udic
    return lo,med,hi
    

cats_m, cats_l, cats_h = [], [], []





cats_m, cats_l, cats_h = [], [], []
result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
print 'J0837'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
print 'J0901'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/new/J0913_211')
model = L.EELs(result,name='J0913')
print 'J0913'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1125_211')
model = L.EELs(result,name='J1125')
print 'J1125'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1144_211')
model = L.EELs(result,name='J1144')
print 'J1144'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
print 'J1218'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1323_211') 
model = L.EELs(result,name='J1323')
print 'J1323'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1347_211')
model = L.EELs(result,name='J1347')
print 'J1347'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/new/J1446_211')
model = L.EELs(result,name='J1446')
print 'J1446'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1605_211') 
model = L.EELs(result,name='J1605')
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1606_211')
model = L.EELs(result,name='J1606')
print 'J1606'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J2228_211')
model = L.EELs(result,name='J2228')
print 'J2228'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])

m, l, h = dict(cats_m), dict(cats_l), dict(cats_h)

np.save('/data/ljo31/Lens/LensParams/Structure_lensgals_1src',[m,l,h])



## 2 src models
cats_m, cats_l, cats_h = [], [], []

cats_m, cats_l, cats_h = [], [], []
result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
print 'J0837'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
print 'J0901'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J0913_212_nonconcentric')
model = L.EELs(result,name='J0913')
print 'J0913 nonconcentric'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1125_212')
model = L.EELs(result,name='J1125')
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1144_212_allparams')
model = L.EELs(result,name='J1144')
print 'J1144'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])

result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
print 'J1218'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])




result = np.load('/data/ljo31/Lens/LensModels/J1323_212') 
model = L.EELs(result,name='J1323')
print 'J1323'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1347_112')
model = L.EELs(result,name='J1347')
print 'J1347'
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1446_212')
model = L.EELs(result,name='J1446')
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1605_212_final') 
model = L.EELs(result,name='J1605')
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J1606_112')
model = L.EELs(result,name='J1606')
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


result = np.load('/data/ljo31/Lens/LensModels/J2228_212')
model = L.EELs(result,name='J2228')
lo,med,hi = MakeTab(model)
cats_m.append([model.name,med])
cats_l.append([model.name,lo])
cats_h.append([model.name,hi])


m, l, h = dict(cats_m), dict(cats_l), dict(cats_h)

np.save('/data/ljo31/Lens/LensParams/Structure_lensgals_2src',[m,l,h])

