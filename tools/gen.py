import sys,re,json,os
sys.path.insert(0,'.')
import sim
from sim import *
from fmt import load
ENDS={0:('5H_E00','Хаяма/«5H» (Хикару?), концовка E00'),}
def effects(pyname):
    n=by[pyname]; c=n['nx']; eff={}; k=0
    while c and k<80:
        m=by[c];k+=1
        if m['t']=='If':
            for cond,b in m['entries']:
                mm=re.findall(r'lastB == (-?\d+)',cond)
                if b and mm:
                    e=[];x=b
                    while x and by[x]['t'] in('Python','Label','Translate','EndTranslate','Show','UserStatement','Pass') and len(e)<60:
                        if by[x]['t']=='Python':
                            for v,op,num in re.findall(r'(var00[12]) (\+=|=) (\d+)',by[x]['code']): e.append((v,op,int(num)))
                        x=by[x]['nx']
                    for q in mm: eff[int(q)]=e
        if m['t']=='Return': break
        c=m['nx']
    return eff
def steps(tag):
    p,f=load(tag)
    ks=[x[1] for x in p[1:]]+[f[1]]
    out=[]
    for i,(s,kk,trx) in enumerate(p):
        scene=trx[-1] if trx else '?'
        sim.CL=[]
        tr=[];r=run(s[1],s[2],s[3],ks[i],trace=tr)
        cl=sim.CL; sim.CL=None
        eff=effects(s[5]).get(ks[i],[])
        v=s[2]
        out.append(dict(i=i+1,scene=scene[2:],opts=s[4],k=ks[i],eff=eff,v1=v.get('var001',0),v2=v.get('var002',0),checks=cl))
    return out,f
def fmtstep(x):
    k=x['k']
    if k==-1: pick='ПРОМОЛЧАТЬ: нажми 0 (или дай таймеру выйти)'
    else: pick='вариант %d: %s'%(k+1,x['opts'][k])
    allo=' | '.join('%d) %s'%(j+1,o) for j,o in enumerate(x['opts']) if o and o!='None')
    e=''.join(' %s %s%d'%({'var001':'Сэкаи','var002':'Котоноха'}[v],'+' if op=='+=' else '=',n) for v,op,n in x['eff'])
    s='%2d. [%s] %s\n      (на экране: %s)%s'%(x['i'],x['scene'],pick,allo,('\n      очки: '+e.strip()) if e else '')
    for c in x['checks']:
        s+='\n      проверка очков после: %s -> %s (Сэкаи=%d, Котоноха=%d)'%(c[0],'да' if c[1] else 'нет',c[2],c[3])
    return s
