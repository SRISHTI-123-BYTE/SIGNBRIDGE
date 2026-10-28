import sys
import re
sys.path.append('backend')

with open('frontend/src/data/islDictionary.js', 'r', encoding='utf-8') as f:
    text = f.read()

glosses = re.findall(r'gloss:\s*[\'"]([^\'"]+)[\'"]', text)
model_true = text.count('modelSupported: true')
model_false = text.count('modelSupported: false')
print(f'Frontend Dictionary total signs: {len(glosses)}')
print(f'AI Ready (modelSupported: true): {model_true}')
print(f'Pending Data (modelSupported: false): {model_false}')

from grammar_engine import GrammarEngine
ge = GrammarEngine()
print(f'Backend GrammarEngine total recognized glosses: {len(ge.gloss_dict)}')

from indian_sign_languages import get_islrtc_standard_domains
domains = get_islrtc_standard_domains()
print('ISLRTC Volumes count:', len(domains))
for d in domains:
    print(f'  {d["id"]}: {len(d["sample_signs"])} signs')
