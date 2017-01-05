import numpy as np, pylab as pl

def clip(result,lpclip):
    lp,trace,dic,_ = result
    if trace.shape[1]<10:
        lp = lp[:,0]
        trace = trace[:,0]
        for key in dic.keys():
            dic[key] = dic[key][:,0]
    row = lp[-1,:]
    lp2 = lp[:,row>lpclip]
    trace2 = trace[:,row>lpclip,:]
    for key in dic.keys():
        dic[key] = dic[key][:,row>lpclip]
    a1,a3 = np.unravel_index(lp.argmax(),lp.shape)
    res = [lp2,trace2,dic,trace[a1,a3]]
    return res

def clip2(result,lpclip):
    lp,trace,dic,_ = result
    row = lp[0,0,:]
    lp2 = lp[:,:,row>lpclip]
    trace2 = trace[:,:,row>lpclip,:]
    for key in dic.keys():
        dic[key] = dic[key][:,:,row>lpclip]
    a1,a3 = np.unravel_index(lp[:,0].argmax(),lp[:,0].shape)
    res = [lp2,trace2,dic,trace[a1,0,a3]]
    return res

def clipburnin(chain,burnin):
    if chain.shape[1]<10:
        chain = chain[:,0]
    return chain[burnin:]
