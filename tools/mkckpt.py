import sys,json
sys.path.insert(0,'.')
import ckpt
TAG={0:'e0',1:'e1',2:'n2',3:'e3',4:'n4',5:'n5',6:'n6',7:'n7',8:'e8',9:'n9',10:'e10',11:'e11',12:'e12',13:'n13',14:'n14',15:'n15',16:'n16',17:'n17',18:'e18',19:'e19',20:'e20',21:'c21'}
EXTRA={'kf15':'kf15','kf16':'kf16','kf7':'kf7'}
C={}
for e,t in list(TAG.items()):
    c=ckpt.checkpoint(t,'sd04_04') or ckpt.checkpoint(t,'sd05_05')
    C['end%d'%e]=dict(tag=t,**c)
for k,t in EXTRA.items():
    C[k]=dict(tag=t,**ckpt.checkpoint(t,'sd04_04'))
    c2=ckpt.checkpoint(t,'sd05_05_KF_A00')
    if c2: C[k+'_late']=dict(tag=t,**c2)
json.dump(C,open('ckpts.json','w'),ensure_ascii=False,indent=1)
for k,v in C.items(): print(k,v['label'],v['after'],v['vars'])
