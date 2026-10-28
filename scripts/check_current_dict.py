import re

with open("frontend/src/data/islDictionary.js", "r", encoding="utf-8") as f:
    text = f.read()

glosses = re.findall(r"gloss:\s*['\"]([^'\"]+)['\"]", text)
print("Current count of glosses in islDictionary.js:", len(glosses))
print("Unique glosses:", len(set(glosses)))
