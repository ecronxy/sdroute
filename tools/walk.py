import json,os
W=os.environ.get('SDRF_WORK',os.path.join(os.path.dirname(os.path.abspath(__file__)),'work'))
d=json.load(open(W+'/proj/ast_dump.json'))
by={n['n']:n for n in d['nodes']}
lab={n['label']:n for n in d['nodes'] if n['t']=='Label'}
SKIP=('Translate','EndTranslate','Show','Scene','With','Image')
def boring(n):
    return n['t'] in SKIP or (n['t']=='UserStatement' and not n['line'].startswith('call screen')) or (n['t']=='Python' and ('renpy.notify' in n['code'] or 'free_memory' in n['code']))
def show(label,maxn=400):
    c=lab[label]['n'];out=[];k=0
    while c and k<maxn:
        n=by[c];k+=1
        if not boring(n):
            s={kk:v for kk,v in n.items() if kk not in('f','n','nx')}
            if n['t']=='If': s['entries']=[[e[0],e[1] and by[e[1]]['l']] for e in n['entries']]
            out.append((n['l'],s))
        c=n['nx']
    return out
if __name__=='__main__':
    import sys
    for x in show(sys.argv[1]): print(x)
