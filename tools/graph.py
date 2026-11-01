import sys,collections,re
sys.path.insert(0,'.')
from sim import *
succ=collections.defaultdict(set)
callret=[]
for n in d['nodes']:
    if not (n['f'][0].isdigit() or n['f'].startswith('end')):
        continue
    a=n['n']
    if n['t'] in('Jump','Call') and not n['expr']:
        if re.fullmatch(r'sdend\d+',n['target']):
            succ[a].add('END:'+n['target']); continue
        tg=OV.get(n['target'],n['target'])
        if tg in lab: succ[a].add(lab[tg]['n'])
        if n['t']=='Call':
            succ[a].add(n['nx']); callret.append(n['nx'])
        continue
    if n['t']=='If':
        for c,b in n['entries']:
            if b: succ[a].add(b)
        if n['nx']: succ[a].add(n['nx'])
        continue
    if n['t']=='Return':
        for r in callret: succ[a].add(r)
        continue
    if n['nx']: succ[a].add(n['nx'])
pred=collections.defaultdict(set)
for a,bs in succ.items():
    for b in bs: pred[b].add(a)
def back(end):
    tgt='END:sdend%d'%end
    seen={tgt};q=[tgt]
    while q:
        x=q.pop()
        for p in pred[x]:
            if p not in seen: seen.add(p);q.append(p)
    return seen
if __name__=='__main__':
    for e in range(22):
        print(e,len(back(e)))
