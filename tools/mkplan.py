import sys,json
sys.path.insert(0,'.')
from fmt import rows
tag=sys.argv[1]
r,f=rows(tag)
json.dump([dict(scene=x['scene'],opts=x['opts'],k=x['k']) for x in r],open('plan_%s.json'%tag,'w'),ensure_ascii=False)
print(len(r))
