import sys,pickle,time,heapq
sys.path.insert(0,'.')
from graph import *
def key(node,vars,stack): return (node,tuple(sorted(vars.items())),stack)
def dist_to(tgt):
    dist={tgt:0};q=collections.deque([tgt])
    while q:
        x=q.popleft()
        for p in pred[x]:
            if p not in dist: dist[p]=dist[x]+1;q.append(p)
    return dist
SILENT=[True]
def search(end,must=(),tlimit=240,start=None,inits=None,vi0=0):
    """must: ordered list of labels that must be visited (in this order) before ending (None end = just reach last must)"""
    dE=dist_to('END:sdend%d'%end) if end is not None else None
    dM=[dist_to(lab[m]['n']) for m in must]
    t0=time.time()
    def need(vi): return vi
    def dd(node,vi):
        if vi<len(must): return dM[vi].get(node)
        return dE.get(node) if dE else 0
    if inits is None:
        tr=[];r=run(lab['start']['n'],{},(),trace=tr);inits=[(r,tr)]
    seen={};heap=[];cnt=0;final=[None]
    def adv(vi,tr):
        for l in tr:
            if vi<len(must) and l==must[vi]: vi+=1
        return vi
    def push(res,frm,k,tr,vi):
        nonlocal cnt
        vi2=adv(vi,tr)
        if res[0]=='end':
            if res[1]==end and vi2>=len(must): final[0]=(frm,k,tr,vi2); return True
            return False
        if end is None and vi2>=len(must) and must:
            final[0]=(frm,k,tr,vi2); return True
        if res[0]=='choice':
            kk=(key(res[1],res[2],res[3]),vi2)
            if kk in seen: return False
            dv=dd(res[1],vi2)
            if dv is None: return False
            seen[kk]=(res,frm,k,tr)
            cnt+=1;heapq.heappush(heap,(dv+ (len(must)-vi2)*0,cnt,kk))
        return False
    for r,tr in inits:
        if push(r,None,None,tr,vi0): return [],final[0],0
    n=0
    while heap and time.time()-t0<tlimit:
        _,_,kk=heapq.heappop(heap);st=seen[kk][0];n+=1;vi=kk[1]
        for k in [i for i,o in enumerate(st[4]) if o and o!='None']+([-1] if SILENT[0] else []):
            tr=[];res=run(st[1],st[2],st[3],k,trace=tr)
            if push(res,kk,k,tr,vi):
                path=[];cur=kk
                while cur is not None:
                    s,frm,kx,trx=seen[cur]; path.append((s,kx,trx)); cur=frm
                path.reverse()
                return path,final[0],n
    return None,(None if heap else 'EXHAUSTED'),n
if __name__=='__main__':
    tag=sys.argv[1];e=None if sys.argv[2]=='-' else int(sys.argv[2]);must=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3] else []
    t=float(sys.argv[4]) if len(sys.argv)>4 else 300
    SILENT[0]=(len(sys.argv)>5 and sys.argv[5]=='silent')
    res=search(e,must,t)
    pickle.dump(res,open(W+'/p_%s.pkl'%tag,'wb'))
    print(tag,'FOUND' if res[0] is not None else 'NOTFOUND',len(res[0]) if res[0] is not None else '',res[-1])
