import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/data/islDictionary.js', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r"gloss:\s*['\"]([^'\"]+)['\"]")
glosses = set(pattern.findall(text))
print(f"Total unique glosses in islDictionary.js: {len(glosses)}")
