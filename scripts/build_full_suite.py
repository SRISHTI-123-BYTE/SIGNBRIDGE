"""
build_full_suite.py
Constructs Volumes 3 to 9 with 200 signs each.
"""

import os

def save_volume(vol_num, vol_name, signs):
    seen = set()
    unique = []
    for s in signs:
        if s[0] not in seen:
            seen.add(s[0])
            unique.append(s)
    
    assert len(unique) >= 200, f"Vol {vol_num} ({vol_name}) has only {len(unique)} signs, need 200"
    final_200 = unique[:200]
    
    filename = f"vol{vol_num}_{vol_name}.py"
    path = os.path.join("scripts", "volume_data", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'"""\nVolume {vol_num}: {vol_name} (200 Signs)\n"""\n\n')
        var_name = f'VOL{vol_num}_{vol_name.upper()}_200'
        f.write(f'{var_name} = [\n')
        for item in final_200:
            f.write(f'    {repr(item)},\n')
        f.write(']\n\n')
        f.write(f'assert len({var_name}) == 200\n')
    print(f"Generated {path} with 200 signs!")

