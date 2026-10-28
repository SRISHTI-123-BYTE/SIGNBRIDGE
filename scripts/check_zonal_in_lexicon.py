import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
sys.path.insert(0, 'backend')

from extended_vocabulary import EXTENDED_ISL_LEXICON
from scripts.zonal_data_standard import STANDARD_SIGNS
from scripts.zonal_data_north import NORTH_SIGNS
from scripts.zonal_data_south import SOUTH_SIGNS
from scripts.zonal_data_west import WEST_SIGNS
from scripts.zonal_data_east import EAST_SIGNS
from scripts.zonal_data_northeast import NORTHEAST_SIGNS

print(f"Current EXTENDED_ISL_LEXICON size: {len(EXTENDED_ISL_LEXICON)}")
all_zonal = STANDARD_SIGNS + NORTH_SIGNS + SOUTH_SIGNS + WEST_SIGNS + EAST_SIGNS + NORTHEAST_SIGNS
missing_in_lexicon = [s for s in all_zonal if s['gloss'] not in EXTENDED_ISL_LEXICON]
print(f"Missing in EXTENDED_ISL_LEXICON: {len(missing_in_lexicon)}")
