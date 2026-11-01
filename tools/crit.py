import sys,pickle,time
sys.path.insert(0,'.')
import search2
from search2 import *
from fmt import load
def crit(tag,end,must=(),silent=True,tl=10):
    search2.SILENT[0]=silent
    path,final=load(tag)
    ks=[p[1] for p in path[1:]]+[final[1]]
    out=[]
    for i,(s,kk_in,tr) in enumerate(path):
        chosen=ks[i]; opts=s[4]
        alts=[j for j,o in enumerate(opts) if o and o!='None' and j!=chosen]+([-1] if silent and chosen!=-1 else [])
        # visited-must index at this state: recompute from all traces up to and including this one
        seen_l=[l for p in path[:i+1] for l in p[2]]
        vi=0
        for l in seen_l:
            if vi<len(must) and l==must[vi]: vi+=1
        res={}
        for a in alts:
            tr2=[];r2=run(s[1],s[2],s[3],a,trace=tr2)
            vi2=vi
            p2,f2,n2=search(end,must,tl,inits=[(r2,tr2)],vi0=vi2)
            res[a]='ok' if p2 is not None else ('no' if f2=='EXHAUSTED' else '?')
        out.append((chosen,res))
        print(tag,i,chosen,res,flush=True)
    pickle.dump(out,open(W+'/crit_%s.pkl'%tag,'wb'))
if __name__=='__main__':
    tag,end=sys.argv[1],int(sys.argv[2]); must=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3] else []
    crit(tag,end,must,silent=(len(sys.argv)>4 and sys.argv[4]=='silent'))
