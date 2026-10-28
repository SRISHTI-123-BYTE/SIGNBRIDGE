import re
import json

# Check how many signs in original islDictionary vs new
with open("backend/extended_vocabulary.py", "r", encoding="utf-8") as f:
    text = f.read()

tokens = re.findall(r'"([A-Z0-9_]+)":\s*\{', text)
print(f"Tokens in extended_vocabulary.py: {len(tokens)}")

with open("frontend/src/data/islDictionary.js", "r", encoding="utf-8") as f:
    text = f.read()

glosses = re.findall(r"gloss:\s*['\"]([^'\"]+)['\"]", text)
print(f"Glosses in islDictionary.js: {len(glosses)}, unique: {len(set(glosses))}")

with open("frontend/src/data/indianSignLanguages.js", "r", encoding="utf-8") as f:
    text = f.read()

vol_matches = re.findall(r"volume:\s*['\"]([^'\"]+)['\"],[\s\S]*?signs:\s*\[([\s\S]*?)\]", text)
for vol_name, signs_block in vol_matches:
    signs = re.findall(r"['\"]([^'\"]+)['\"]", signs_block)
    print(f"{vol_name}: {len(signs)} signs (unique: {len(set(signs))})")

with open("backend/indian_sign_languages.py", "r", encoding="utf-8") as f:
    text = f.read()

b_vol_matches = re.findall(r'"badge":\s*"([^"]+)",[\s\S]*?"sample_signs":\s*\[([\s\S]*?)\]', text)
for badge, signs_block in b_vol_matches:
    signs = re.findall(r'"([^"]+)"', signs_block)
    print(f"Backend {badge}: {len(signs)} signs (unique: {len(set(signs))})")
