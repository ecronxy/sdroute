import sys,os,re,pickle,json,glob
sys.path.insert(0,'.')
from gen import *
OUT=os.environ.get('SDRF_OUT',os.path.join(W,'out'))
CODES=['5H_E00','5H_E01','5O_A09','5O_B04','5O_D10','A2_Z00','A2_F00','B0_F00','G0_L03','KB_L03','KC_F00','KC_H00','KI_L03','SA_G05','SA_T00','SB_E01','SB_I02','SC_L03','SD_A01','SD_E01','SE_S00','9H_A01']
TAG={0:'e0',1:'e1',2:'n2',3:'e3',4:'n4',5:'n5',6:'n6',7:'n7',8:'e8',9:'n9',10:'e10',11:'e11',12:'e12',13:'n13',14:'n14',15:'n15',16:'n16',17:'n17',18:'e18',19:'e19',20:'e20',21:'c21'}
def speakers(label):
    f=by[lab[label]['n']]['f']; sp={}
    for n in d['nodes']:
        if n['f']==f and n['t']=='Python' and 'renpy.notify([' in n['code']:
            m=re.match(r'renpy.notify\(\["([^":]{1,25}):',n['code'])
            if m: sp[m.group(1)]=sp.get(m.group(1),0)+1
    return [k for k,v in sorted(sp.items(),key=lambda x:-x[1])][:5]
def verified(tag,nplan_end):
    lg=os.path.join(W,'run_%s.log'%tag)
    if not os.path.exists(lg): return 'нет прогона'
    t=open(lg).read()
    if 'MISMATCH' in t: return 'ПРОВАЛ: расхождение с движком'
    m=re.search(r'ENDING (\d+)',t)
    if not m: return 'не подтверждён (прогон не дошёл до финала)'
    n=int(m.group(1)); cs=len(re.findall(r'^C ',t,re.M))
    if n!=nplan_end: return 'ПРОВАЛ: движок пришёл в концовку %d'%n
    return 'ПОДТВЕРЖДЕНО прогоном движка (%d выборов, финал sdend%d)'%(cs,n)
def critmap(tag):
    p=os.path.join(W,'crit_%s.pkl'%tag)
    return pickle.load(open(p,'rb')) if os.path.exists(p) else None
def write(e,tag,extra_title='',fname=None):
    st,f=steps(tag)
    cr=critmap(tag)
    ver=verified(tag,e)
    lines=[]
    code=CODES[e]
    lines.append('Концовка %d: %s%s'%(e,code,extra_title))
    lines.append('Статус: '+ver)
    final_trace=[l for l in f[2] if l.startswith('sd0')]
    fin=[l for l in f[2] if l.startswith('sd05_05_')]
    try: sp=speakers(fin[-1] if fin else final_trace[-1])
    except Exception: sp=[]
    lines.append('Последняя сцена: %s; говорят: %s'%(final_trace[-1][2:] if final_trace else '?', ', '.join(sp)))
    silent=sum(1 for x in st if x['k']==-1)
    lines.append('Выборов на маршруте: %d (из них «промолчать»: %d). Начинай НОВУЮ игру.'%(len(st),silent))
    lines.append('')
    lines.append('Как читать: [код сцены] что выбрать. «(на экране)» — все варианты, чтобы узнать момент. «Промолчать» = нажать 0 на клавиатуре (в порте это клавиша 0) — это тоже выбор. Очки: Сэкаи = var001, Котоноха = var002, показаны очки ДО выбора.')
    lines.append('')
    for i,x in enumerate(st):
        s=fmtstep(x)
        s+='\n      очки до выбора: Сэкаи %d, Котоноха %d'%(x['v1'],x['v2'])
        if cr:
            ch,res=cr[i]
            if res:
                if all(v=='no' for v in res.values()): s+='\n      ВАЖНО: только этот вариант (любой другой уводит от концовки, перебор доказал)'
                elif any(v=='ok' for v in res.values()): s+='\n      (другой вариант тоже не закрывает концовку, но дальше держись списка: очки изменятся)'
                else: s+='\n      (влияние не доказано, делай как в списке)'
        lines.append(s)
    lines.append('')
    lines.append('Итог очков в конце: см. последний шаг; финальная концовка %s.'%code)
    name=fname or '%02d_%s.txt'%(e,code)
    open(os.path.join(OUT,name),'w').write('\n'.join(lines)+'\n')
    return dict(e=e,code=code,tag=tag,ver=ver,n=len(st),silent=silent,speakers=sp,last=final_trace[-1][2:] if final_trace else '?')
if __name__=='__main__':
    res=[]
    for e,t in TAG.items(): res.append(write(e,t))
    json.dump(res,open(os.path.join(W,'summary.json'),'w'),ensure_ascii=False)
    for r in res: print(r['e'],r['code'],r['ver'][:30],r['n'],r['silent'],r['speakers'])
