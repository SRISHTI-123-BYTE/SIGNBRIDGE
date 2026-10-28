import sys
import re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from scripts.zonal_data_standard import STANDARD_SIGNS
from scripts.zonal_data_north import NORTH_SIGNS
from scripts.zonal_data_south import SOUTH_SIGNS
from scripts.zonal_data_west import WEST_SIGNS
from scripts.zonal_data_east import EAST_SIGNS
from scripts.zonal_data_northeast import NORTHEAST_SIGNS

with open('frontend/src/data/islDictionary.js', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r"gloss:\s*['\"]([^'\"]+)['\"]")
existing_glosses = set(pattern.findall(text))
print(f"Existing glosses in ISL_DICTIONARY: {len(existing_glosses)}")

all_zonal = STANDARD_SIGNS + NORTH_SIGNS + SOUTH_SIGNS + WEST_SIGNS + EAST_SIGNS + NORTHEAST_SIGNS
missing = [s for s in all_zonal if s['gloss'] not in existing_glosses]
already = [s for s in all_zonal if s['gloss'] in existing_glosses]

print(f"Total zonal signs: {len(all_zonal)}")
print(f"Already in ISL_DICTIONARY: {len(already)}")
print(f"Need to be added to ISL_DICTIONARY: {len(missing)}")
