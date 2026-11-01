import pickle,sys
sys.path.insert(0,'.')
from sim import W
def load(tag):
    path,final,n=pickle.load(open(W+'/p_%s.pkl'%tag,'rb'))
    return path,final
def rows(tag):
    path,final=load(tag)
    out=[]
    for s,k,tr in path:
        scene=tr[-1] if tr else '?'
        # k is the option picked AFTER this state, stored on the next entry; here k is the one that led into this state
        out.append((scene,s))
    # picked option for state i is k of entry i+1; for last, final[1]
    ks=[p[1] for p in path[1:]]+[final[1]]
    res=[]
    for (scene,s),k in zip(out,ks):
        v=s[2]
        res.append(dict(scene=scene,opts=s[4],k=k,v1=v.get('var001',0),v2=v.get('var002',0),vars=v))
    return res,final
if __name__=='__main__':
    r,f=rows(sys.argv[1])
    for i,x in enumerate(r):
        print(i+1,x['scene'][2:],x['k'],x['opts'][x['k']] if x['k']>=0 else '(молчать)',x['v1'],x['v2'])
    print('final trace tail',f[2][-5:])
