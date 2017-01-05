from linslens import EELsModels as L
import numpy as np

def MakeTab(model):
    model.Initialise()
    mags = model.GetIntrinsicMags()
    Res = model.GetSourceSize(kpc=True)
    Mv,Mi = model.magnification()
    return Mv,Mi

cat = []
result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
name = 'J0837'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))
# also save the PDFs once and for all!!!


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
name = 'J0901'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

result = np.load('/data/ljo31/Lens/LensModels/J0913_211')
model = L.EELs(result,name='J0913')
name = 'J0913'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

result = np.load('/data/ljo31/Lens/LensModels/J1125_211')
model = L.EELs(result,name='J1125')
name = 'J1125'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))



result = np.load('/data/ljo31/Lens/LensModels/J1144_211')
model = L.EELs(result,name='J1144')
name = 'J1144'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))



result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
name = 'J1218'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

result = np.load('/data/ljo31/Lens/LensModels/J1323_211') 
model = L.EELs(result,name='J1323')
name = 'J1323'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1347_211')
model = L.EELs(result,name='J1347')
name = 'J1347'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1446_211')
model = L.EELs(result,name='J1446')
name = 'J1446'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1605_211') 
model = L.EELs(result,name='J1605')
name = 'J1605'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1606_211')
model = L.EELs(result,name='J1606')
name = 'J1606'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

result = np.load('/data/ljo31/Lens/LensModels/J1619_211')
model = L.EELs(result,name='J1619')
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J2228_211')
model = L.EELs(result,name='J2228')
name = 'J2228'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


cat = dict(cat)

np.save('/data/ljo31/Lens/LensParams/magnifications_211',cat)


cat =[]
result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
name = 'J0837'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))
# also save the PDFs once and for all!!!


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
name = 'J0901'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J0913_212_nonconcentric')
model = L.EELs(result,name='J0913')
print 'J0913 nonconcentric'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1125_212')
model = L.EELs(result,name='J1125')
print 'J1125 new!!!'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1144_212_allparams')
model = L.EELs(result,name='J1144')
print 'J1144'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
name = 'J1218'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

print 'here'
result = np.load('/data/ljo31/Lens/LensModels/J1323_212') 
model = L.EELs(result,name='J1323')
print 'J1323'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1347_112')
model = L.EELs(result,name='J1347')
print 'J1347'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


result = np.load('/data/ljo31/Lens/LensModels/J1446_212')
model = L.EELs(result,name='J1446')
print 'J1446'
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))



result = np.load('/data/ljo31/Lens/LensModels/J1605_212_final') 
model = L.EELs(result,name='J1605')
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))




result = np.load('/data/ljo31/Lens/LensModels/J1606_112')
model = L.EELs(result,name='J1606')
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))

result = np.load('/data/ljo31/Lens/LensModels/J1619_212')
model = L.EELs(result,name='J1619')
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))



result = np.load('/data/ljo31/Lens/LensModels/J2228_212')
model = L.EELs(result,name='J2228')
Mv,Mi = MakeTab(model)
cat.append((model.name,[Mv,Mi]))


cat = dict(cat)

np.save('/data/ljo31/Lens/LensParams/magnifications_212',cat)




