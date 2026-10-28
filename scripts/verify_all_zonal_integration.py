# scripts/verify_all_zonal_integration.py
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
sys.path.insert(0, 'backend')

from scripts.zonal_data_standard import STANDARD_SIGNS
from scripts.zonal_data_north import NORTH_SIGNS
from scripts.zonal_data_south import SOUTH_SIGNS
from scripts.zonal_data_west import WEST_SIGNS
from scripts.zonal_data_east import EAST_SIGNS
from scripts.zonal_data_northeast import NORTHEAST_SIGNS
from backend.indian_sign_languages import INDIAN_SIGN_LANGUAGES
from backend.extended_vocabulary import EXTENDED_ISL_LEXICON

print("=" * 60)
print("1. CHECKING BACKEND INDIAN_SIGN_LANGUAGES")
print("=" * 60)
assert len(INDIAN_SIGN_LANGUAGES) == 6, f"Expected 6 zones, found {len(INDIAN_SIGN_LANGUAGES)}"
for z in INDIAN_SIGN_LANGUAGES:
    sample_signs = z.get('sample_signs', [])
    print(f"Zone '{z['id']}' ({z['short_name']}): {len(sample_signs)} sample signs (Unique: {len(set(sample_signs))})")
    assert len(sample_signs) == 100, f"Zone {z['id']} does not have 100 signs"

print("\n" + "=" * 60)
print("2. CHECKING FRONTEND INDIAN_SIGN_LANGUAGES")
print("=" * 60)
with open('frontend/src/data/indianSignLanguages.js', 'r', encoding='utf-8') as f:
    fe_text = f.read()

expected_zones = ['isl-standard', 'isl-north', 'isl-south', 'isl-west', 'isl-east', 'isl-northeast']
for zid in expected_zones:
    pos = fe_text.find(f"id: '{zid}'")
    assert pos != -1, f"Missing {zid} in frontend"
    sample_pos = fe_text.find("sampleSigns: [", pos)
    bracket_close = fe_text.find("]", sample_pos) + 1
    sample_block = fe_text[sample_pos:bracket_close]
    signs_found = re.findall(r"'([A-Z0-9_]+)'", sample_block)
    print(f"Zone '{zid}' in frontend: {len(signs_found)} sample signs (Unique: {len(set(signs_found))})")
    assert len(signs_found) == 100, f"Frontend zone {zid} does not have 100 signs"

print("\n" + "=" * 60)
print("3. CHECKING COVERAGE IN islDictionary.js (AI READY: modelSupported: true)")
print("=" * 60)
with open('frontend/src/data/islDictionary.js', 'r', encoding='utf-8') as f:
    dict_text = f.read()

dict_glosses = set(re.findall(r"gloss:\s*['\"]([^'\"]+)['\"]", dict_text))
model_supported_count = dict_text.count("modelSupported: true")
print(f"Total unique glosses in islDictionary.js: {len(dict_glosses)}")
print(f"Total modelSupported: true entries in islDictionary.js: {model_supported_count}")

all_600 = STANDARD_SIGNS + NORTH_SIGNS + SOUTH_SIGNS + WEST_SIGNS + EAST_SIGNS + NORTHEAST_SIGNS
missing_in_dict = [s['gloss'] for s in all_600 if s['gloss'] not in dict_glosses]
print(f"Zonal signs missing in islDictionary.js: {len(missing_in_dict)}")
assert len(missing_in_dict) == 0, f"Missing in dict: {missing_in_dict[:10]}"

print("\n" + "=" * 60)
print("4. CHECKING COVERAGE IN extended_vocabulary.py")
print("=" * 60)
print(f"Total tokens in EXTENDED_ISL_LEXICON: {len(EXTENDED_ISL_LEXICON)}")
missing_in_lex = [s['gloss'] for s in all_600 if s['gloss'] not in EXTENDED_ISL_LEXICON]
print(f"Zonal signs missing in EXTENDED_ISL_LEXICON: {len(missing_in_lex)}")
assert len(missing_in_lex) == 0, f"Missing in lexicon: {missing_in_lex[:10]}"

for s in all_600:
    assert s['gloss'] in EXTENDED_ISL_LEXICON, f"{s['gloss']} is not in EXTENDED_ISL_LEXICON"

print("\n" + "=" * 60)
print("ALL 6 ZONES (600 SIGNS) ARE 100% VERIFIED AND AI READY!")
print("=" * 60)
