#!/usr/bin/env python3
"""Sab section files (*.html) + build-order.json se final index.html banata hai.
Run:  python3 build.py   ->  index.html
Section files ke andar '<!--@@EK-BLOCK ...@@-->' wali lines mat hatana."""
import json,os,re,glob
d=os.path.dirname(os.path.abspath(__file__))
blocks={};seen={}
for f in glob.glob(os.path.join(d,'*.html')):
    if os.path.basename(f)=='index.html': continue
    t=open(f,encoding='utf8',newline='').read()
    parts=re.split(r'<!--@@EK-BLOCK (\w+)@@-->\n',t)
    for k in range(1,len(parts),2):
        txt=parts[k+1]
        if parts[k] in blocks:
            raise SystemExit('ERROR: block '+parts[k]+' do files mein hai ('+seen[parts[k]]+' aur '+os.path.basename(f)+'). Purani file GitHub se delete karo.')
        seen[parts[k]]=os.path.basename(f)
        blocks[parts[k]]=txt[:-1] if txt.endswith('\n') else txt
order=json.load(open(os.path.join(d,'build-order.json')))
out=''.join(blocks[b] for b in order)
open(os.path.join(d,'index.html'),'w',encoding='utf8',newline='').write(out)
print('index.html ready',len(out),'chars')
