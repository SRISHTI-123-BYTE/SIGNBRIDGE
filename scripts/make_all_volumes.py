"""
make_all_volumes.py
Defines 200 signs for each of Volumes 2 through 9 and outputs them into scripts/volume_data/.
"""

import os
import sys

def write_vol(vol_num, vol_key, var_name, signs):
    seen = set()
    unique = []
    for s in signs:
        if s[0] not in seen:
            seen.add(s[0])
            unique.append(s)
    
    assert len(unique) >= 200, f"Vol {vol_num} ({vol_key}) has only {len(unique)} unique signs, need 200"
    final_200 = unique[:200]
    
    filename = f"vol{vol_num}_{vol_key}.py"
    path = os.path.join('scripts', 'volume_data', filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'"""\nVolume {vol_num}: {vol_key} (200 Signs)\n"""\n\n')
        f.write(f'{var_name} = [\n')
        for item in final_200:
            f.write(f'    {repr(item)},\n')
        f.write(']\n\n')
        f.write(f'assert len({var_name}) == 200, f"Expected 200 signs, got {{len({var_name})}}"\n')
    print(f"Generated {path} with 200 signs!")

print("Helper ready.")
