"""
generate_all_volume_files.py
Generates the remaining 8 volume files with 200 signs each.
"""

import os

def create_volume_file(vol_num, vol_name, filename, base_signs, extra_list, default_cat):
    all_raw = base_signs + extra_list
    seen = set()
    unique = []
    for item in all_raw:
        gloss = item[0]
        if gloss not in seen:
            seen.add(gloss)
            unique.append(item)
    
    assert len(unique) >= 200, f"{vol_name} has only {len(unique)} signs, need 200"
    final_200 = unique[:200]
    
    out_path = os.path.join('scripts', 'volume_data', filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f'"""\nVolume {vol_num}: {vol_name} (200 Signs)\n"""\n\n')
        var_name = f'VOL{vol_num}_{filename.replace(".py", "").split("_")[1].upper()}_200'
        f.write(f'{var_name} = [\n')
        for s in final_200:
            f.write(f'    {repr(s)},\n')
        f.write(']\n')
        f.write(f'assert len({var_name}) == 200\n')
    print(f"Generated {out_path} with 200 signs!")

if __name__ == '__main__':
    print("Helper loaded.")
