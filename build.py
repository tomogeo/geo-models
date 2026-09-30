import json
reg=json.load(open('registry.json'))
payload={m['id']:open(f"models/{m['id']}.html",encoding='utf-8').read() for m in reg['models']}
def safe(o): return json.dumps(o,ensure_ascii=False).replace('</','<\\/')
t=open('template.html',encoding='utf-8').read()
t=t.replace('__REGISTRY__',safe(reg)).replace('__PAYLOAD__',safe(payload))
open('geo-models.html','w',encoding='utf-8').write(t)
print(len(t.encode()))
