import sys,json,pickle
sys.path.insert(0,'.')
import sim
from sim import *
from fmt import load
def checkpoint(tag,prefix):
    """first label with prefix reached along path; returns (idx of first pick after, label, vars, stack)"""
    p,f=load(tag)
    ks=[x[1] for x in p[1:]]+[f[1]]
    # replay edges recording snapshots
    sim.SNAP=[]
    # initial run
    tr=[];r=run(lab['start']['n'],{},(),trace=tr)
    for i,(s,kk,trx) in enumerate(p):
        sim.SNAP=[]
        tr=[];r=run(s[1],s[2],s[3],ks[i],trace=tr)
        for lab_,vars_,stack in sim.SNAP:
            if lab_.startswith(prefix):
                return dict(after=i+1,label=lab_,vars=vars_,stack=[str(x) for x in stack])
    return None
if __name__=='__main__':
    print(checkpoint(sys.argv[1],sys.argv[2]))
