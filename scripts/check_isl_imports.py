import os
import re

for root, dirs, files in os.walk('frontend/src'):
    for f in files:
        if f.endswith(('.js', '.jsx')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                txt = fp.read()
                if 'islDictionary' in txt:
                    imports = [line.strip() for line in txt.splitlines() if 'islDictionary' in line]
                    print(p, imports)
