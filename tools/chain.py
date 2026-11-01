import sys,pickle
sys.path.insert(0,'.')
import search2
from search2 import *
from fmt import load
# usage: chain.py newtag basetag end tlimit [silent]
new,base,end,tl=sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4])
search2.SILENT[0]=len(sys.argv)>5
bp,bf=load(base)
s=bp[-1][0]
tr=[];r=run(s[1],s[2],s[3],bf[1],trace=tr)
print('start res',r[0])
p2,f2,n=search(end,(),tl,inits=[(r,tr)])
if p2 is None: print(new,'NOTFOUND',f2,n); sys.exit()
# first entry of p2 has kx=None (init); fix to be (bf[1], tr)
full=list(bp)+[(p2[0][0],bf[1],tr+p2[0][2])]+p2[1:] if p2 else list(bp)
pickle.dump((full,f2,n),open(W+'/p_%s.pkl'%new,'wb'))
print(new,'FOUND',len(full),n)
