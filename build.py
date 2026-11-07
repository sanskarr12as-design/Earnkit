#!/usr/bin/env python3
"""Sab section files (*.html) + build-order.json se final index.html banata hai.
Run:  python3 build.py   ->  index.html
Section files ke andar '<!--@@EK-BLOCK ...@@-->' wali lines mat hatana."""
import json,os,re,glob,sys
d=os.path.dirname(os.path.abspath(__file__))
blocks={};seen={};per={}
for f in sorted(glob.glob(os.path.join(d,'*.html'))):
    n=os.path.basename(f)
    if n=='index.html': continue
    t=open(f,encoding='utf8',newline='').read().replace('\r\n','\n')
    parts=re.split(r'<!--@@EK-BLOCK (\w+)@@-->\n',t)
    per[n]=(len(t),(len(parts)-1)//2)
    for k in range(1,len(parts),2):
        txt=parts[k+1]
        if parts[k] in blocks:
            sys.exit('ERROR: block '+parts[k]+' do files mein hai ('+seen[parts[k]]+' aur '+n+'). Purani file GitHub se delete karo.')
        seen[parts[k]]=n
        blocks[parts[k]]=txt[:-1] if txt.endswith('\n') else txt
order=json.load(open(os.path.join(d,'build-order.json')))
missing=[b for b in order if b not in blocks]
if missing:
    print('ERROR: ye blocks kisi file mein nahi mile:',missing[:15],'... total',len(missing))
    print('Files ka haal (file: size, blocks mile):')
    for n,(sz,c) in per.items(): print('  ',n,sz,c)
    sys.exit(1)
out=''.join(blocks[b] for b in order)
open(os.path.join(d,'index.html'),'w',encoding='utf8',newline='').write(out)
print('index.html ready',len(out),'chars')
