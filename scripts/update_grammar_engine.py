with open('backend/grammar_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Import
import_find = 'import re\nfrom typing import Dict, List, Any, Optional, Tuple'
import_find_crlf = 'import re\r\nfrom typing import Dict, List, Any, Optional, Tuple'
import_replacement = '''import re
from typing import Dict, List, Any, Optional, Tuple

try:
    from extended_vocabulary import EXTENDED_ISL_LEXICON
except ImportError:
    try:
        from backend.extended_vocabulary import EXTENDED_ISL_LEXICON
    except ImportError:
        EXTENDED_ISL_LEXICON = {}'''

if import_find in text:
    text = text.replace(import_find, import_replacement, 1)
elif import_find_crlf in text:
    text = text.replace(import_find_crlf, import_replacement.replace('\n', '\r\n'), 1)

# 2. Update gloss_dict
dict_find = '            "THANK_YOU": {"en": "Thank you", "hi": "धन्यवाद", "ta": "நன்றி", "pos": "COURTESY"}\n        }'
dict_find_crlf = '            "THANK_YOU": {"en": "Thank you", "hi": "धन्यवाद", "ta": "நன்றி", "pos": "COURTESY"}\r\n        }'
dict_replacement = '''            "THANK_YOU": {"en": "Thank you", "hi": "धन्यवाद", "ta": "நன்றி", "pos": "COURTESY"}
        }

        # Update with full 281 AI-Ready standard lexicon
        if EXTENDED_ISL_LEXICON:
            self.gloss_dict.update(EXTENDED_ISL_LEXICON)'''

if dict_find in text:
    text = text.replace(dict_find, dict_replacement, 1)
elif dict_find_crlf in text:
    text = text.replace(dict_find_crlf, dict_replacement.replace('\n', '\r\n'), 1)

# 3. Dynamic keywords
kw_find = '            "மொழிபெயர்ப்பாளர்": "INTERPRETER"\n        }'
kw_find_crlf = '            "மொழிபெயர்ப்பாளர்": "INTERPRETER"\r\n        }'
kw_replacement = '''            "மொழிபெயர்ப்பாளர்": "INTERPRETER"
        }

        # Dynamically extend keywords from gloss_dict
        for gloss, entry in self.gloss_dict.items():
            en_w = entry.get("en", "").lower().strip()
            if en_w and en_w not in self.multilingual_keywords:
                self.multilingual_keywords[en_w] = gloss
            hi_w = entry.get("hi", "").strip()
            if hi_w and hi_w not in self.multilingual_keywords:
                self.multilingual_keywords[hi_w] = gloss
            ta_w = entry.get("ta", "").strip()
            if ta_w and ta_w not in self.multilingual_keywords:
                self.multilingual_keywords[ta_w] = gloss'''

if kw_find in text:
    text = text.replace(kw_find, kw_replacement, 1)
elif kw_find_crlf in text:
    text = text.replace(kw_find_crlf, kw_replacement.replace('\n', '\r\n'), 1)

with open('backend/grammar_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated backend/grammar_engine.py!')
