import sys
import os

sys.path.append(os.path.dirname(__file__))
from populate_dictionary import SIGN_DEFINITIONS

lines = [
    '"""',
    'SignBridge Extended ISLRTC Lexicon',
    'Contains trilingual dictionary tokens and POS tags for all 230 expanded curricular signs.',
    '"""',
    '',
    'EXTENDED_ISL_LEXICON = {'
]

for gloss, (slug, cat, en, hi, ta, desc, syns) in SIGN_DEFINITIONS.items():
    pos = 'NOUN'
    if cat == 'numbers':
        pos = 'NUMERAL'
    elif cat == 'sentiment':
        pos = 'RESPONSE' if gloss in ['YES', 'NO', 'AGREE', 'DISAGREE'] else 'ADJECTIVE'
    elif cat == 'greeting':
        pos = 'GREETING' if gloss in ['HELLO', 'WELCOME', 'NAMASTE', 'VANAKKAM'] else 'COURTESY'
    elif gloss in ['GO', 'COME', 'SIT', 'WAIT', 'HELP', 'CALL', 'EAT', 'DRINK', 'COOK', 'WASH', 'STUDY', 'WRITE', 'READ', 'SAVE', 'PAY', 'TRANSFER', 'WITHDRAW', 'DEPOSIT', 'PROTECT', 'ARREST']:
        pos = 'VERB'
    elif gloss in ['WHERE', 'HOW', 'WHAT']:
        pos = 'WH_INTERROGATIVE'
    elif gloss in ['SEVERE', 'BAD', 'GOOD', 'NICE', 'HAPPY', 'SAD', 'SAFE', 'CLEAN', 'HUNGRY', 'KIND', 'COLD_WEATHER', 'RAIN_HEAVY']:
        pos = 'ADJECTIVE'

    en_clean = en.split('/')[0].strip().lower()
    hi_clean = hi.split('/')[0].strip()
    ta_clean = ta.split('/')[0].strip()

    lines.append(f'    "{gloss}": {{"en": "{en_clean}", "hi": "{hi_clean}", "ta": "{ta_clean}", "pos": "{pos}"}},')

lines.append('}')
lines.append('')

with open('backend/extended_vocabulary.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Generated backend/extended_vocabulary.py successfully!')
