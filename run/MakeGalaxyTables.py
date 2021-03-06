import EELsLensModels as L
import numpy as np

def MakeTab(model):
    model.MakeDict()
    model.BuildLenses()
    model.BuildGalaxies()
    model.BuildSources()
    model.EasyAddImages()
    model.GetFits(plotresid=False)
    model.GalaxySize()
    model.GalaxyObsMag()
    model.GetSB()
    model.GetPhotometry()
    model.GetRestSB()
    model.MakePDFDict()
    model.GetPDFs(kpc=False)
    l,d,u = model.UncertaintiesFromPDF()
    model.PrintPDFTable()

'''
result = np.load('/data/ljo31/Lens/LensModels/J0837_211')
model = L.EELs(result,name='J0837')
print 'J0837'
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J0901_211')
model = L.EELs(result,name='J0901')
print 'J0901'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J0913_211')
model = L.EELs(result,name='J0913')
print 'J0913'
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1125_211')
model = L.EELs(result,name='J1125')
print 'J1125'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1144_211')
model = L.EELs(result,name='J1144')
print 'J1144'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1218_211')
model = L.EELs(result,name='J1218')
print 'J1218'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1323_211') 
model = L.EELs(result,name='J1323')
print 'J1323'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1347_211')
model = L.EELs(result,name='J1347')
print 'J1347'
MakeTab(model)
'''
result = np.load('/data/ljo31/Lens/LensModels/J1446_212')
model = L.EELs(result,name='J1446')
print 'J1446 212'
MakeTab(model)
'''
result = np.load('/data/ljo31/Lens/LensModels/J1605_211') 
model = L.EELs(result,name='J1605')
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1606_112')
model = L.EELs(result,name='J1606')
print 'J1606 112'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J2228_211')
model = L.EELs(result,name='J2228')
print 'J2228'
MakeTab(model)


print 'mostly 2-source models'


result = np.load('/data/ljo31/Lens/LensModels/J0913_212_concentric')
model = L.EELs(result,name='J0913')
print 'J0913 concentric'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J0913_212_nonconcentric')
model = L.EELs(result,name='J0913')
print 'J0913 nonconcentric'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1125_212_concentric')
model = L.EELs(result,name='J1125')
print 'J1125 concentric'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1125_212_nonconcentric')
model = L.EELs(result,name='J1125')
print 'J1125 nonconcentric'
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1144_212_allparams')
model = L.EELs(result,name='J1144')
print 'J1144'
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1323_212') 
model = L.EELs(result,name='J1323')
print 'J1323'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1347_112')
model = L.EELs(result,name='J1347')
print 'J1347'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1446_211')
model = L.EELs(result,name='J1446')
print 'J1446 211'
MakeTab(model)

result = np.load('/data/ljo31/Lens/LensModels/J1605_212_final') 
model = L.EELs(result,name='J1605')
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J2228_212')
model = L.EELs(result,name='J2228')
print 'J2228'
MakeTab(model)


result = np.load('/data/ljo31/Lens/LensModels/J1606_211')
model = L.EELs(result,name='J1606')
print 'J1606 211'
MakeTab(model)

'''
