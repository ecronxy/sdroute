import json,os,re,ast,collections,sys,pickle
W=os.environ.get('SDRF_WORK',os.path.join(os.path.dirname(os.path.abspath(__file__)),'work'))
d=json.load(open(W+'/proj/ast_dump.json'))
by={n['n']:n for n in d['nodes']}
lab={n['label']:n for n in d['nodes'] if n['t']=='Label'}
OV=d['overrides']
defaults={}
for n in d['nodes']:
    if n['t']=='Default' and n['f']=='defi.rpyc': defaults[n['var']]=eval(n['code'])
# relevant vars = names used in conditions
rel=set()
for n in d['nodes']:
    if n['t']=='If' and n['f'][0].isdigit():
        for c,_ in n['entries']: rel|=set(re.findall(r'\b(var\w*|flag\d+)\b',c))
rel.discard('lastB')
class RS:
    def free_memory(self):pass
    def notify(self,*a):pass
SNAP=None
CL=None
CE={}
def cc2(c):
    if c not in CE: CE[c]=compile(c,'<c>','eval')
    return CE[c]

CC={}
def cc(code):
    if code not in CC: CC[code]=compile(code,'<n>','exec')
    return CC[code]
def run(node,vars,stack,lastB=-1,trace=None):
    """run deterministically until choice / end. returns ('choice',node_name,vars,stack,opts)|('end',tag)|('ret',)"""
    ns=dict(defaults);ns.update(vars);ns['lastB']=lastB
    ns['renpy']=RS()
    c=node;steps=0
    pend=None
    def sl(a,b=None): 
        nonlocal pend
        pend=(a,b)
    ns['set_lastb']=sl
    while True:
        steps+=1
        if steps>200000: return ('loop',c)
        n=by[c]; t=n['t']
        if t=='Label':
            if trace is not None: trace.append(n['label'])
            if SNAP is not None: SNAP.append((n['label'],{k:ns[k] for k in rel if ns.get(k)!=defaults.get(k)},stack))
        elif t=='Python':
            if n['f'][0].isdigit():
                code=n['code']
                if 'set_lastb' in code:
                    pend=None; exec(cc(code),ns)
                    a,b=pend
                    cur={k:ns[k] for k in rel if ns.get(k)!=defaults.get(k)}
                    return ('choice',n['nx'],cur,stack,b,n['n'])
                if 'renpy.notify' not in code and 'free_memory' not in code:
                    exec(cc(code),ns)
        elif t=='If':
            nxt=n['nx']
            for cond,body in n['entries']:
                r_=eval(cc2(cond),ns)
                if CL is not None and 'var00' in cond: CL.append((cond,bool(r_),ns['var001'],ns['var002']))
                if r_: nxt=body;break
            c=nxt; 
            if c is None: return ('ret',)
            continue
        elif t in('Jump','Call'):
            if n['expr']: return ('bad',n)
            tg=OV.get(n['target'],n['target'])
            m=re.fullmatch(r'sdend(\d+)',n['target'])
            if m: return ('end',int(m.group(1)))
            if t=='Call': stack=stack+(n['nx'],)
            c=lab[tg]['n']; continue
        elif t=='Return':
            if not stack: return ('ret',)
            c=stack[-1]; stack=stack[:-1]; continue
        elif t=='While': return ('bad',n)
        c=n['nx']
        if c is None: return ('ret',)
