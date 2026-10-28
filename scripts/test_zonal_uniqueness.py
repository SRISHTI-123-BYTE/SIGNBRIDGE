import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from scripts.zonal_data_standard import STANDARD_SIGNS
from scripts.zonal_data_north import NORTH_SIGNS
from scripts.zonal_data_south import SOUTH_SIGNS
from scripts.zonal_data_west import WEST_SIGNS
from scripts.zonal_data_east import EAST_SIGNS
from scripts.zonal_data_northeast import NORTHEAST_SIGNS

zones = [
    ("isl-standard", STANDARD_SIGNS),
    ("isl-north", NORTH_SIGNS),
    ("isl-south", SOUTH_SIGNS),
    ("isl-west", WEST_SIGNS),
    ("isl-east", EAST_SIGNS),
    ("isl-northeast", NORTHEAST_SIGNS),
]

all_glosses = set()
for zid, signs in zones:
    gloss_list = [s["gloss"] for s in signs]
    unique_glosses = set(gloss_list)
    print(f"Zone {zid}: Total = {len(gloss_list)}, Unique = {len(unique_glosses)}")
    if len(gloss_list) != len(unique_glosses):
        # find duplicates
        seen = set()
        dups = set()
        for g in gloss_list:
            if g in seen:
                dups.add(g)
            seen.add(g)
        print(f"  WARNING Duplicates in {zid}: {dups}")
    all_glosses.update(unique_glosses)

print(f"\nTotal unique distinct glosses across all 6 zones: {len(all_glosses)}")
