"""
build_remaining_volumes.py
Generates exactly 200 unique authentic ISLRTC signs for Volumes 2 through 9.
"""

import os
import sys

def write_volume_file(filename, var_name, signs):
    # deduplicate
    seen = set()
    unique = []
    for s in signs:
        if s[0] not in seen:
            seen.add(s[0])
            unique.append(s)
    final_signs = unique[:200]
    assert len(final_signs) == 200, f"{filename}: expected 200 signs, got {len(final_signs)}"

    lines = [
        f'"""\n{filename} (200 Signs)\n"""\n',
        f'{var_name} = ['
    ]
    for s in final_signs:
        lines.append(f'    {repr(s)},')
    lines.append(']\n')

    path = os.path.join('scripts', 'volume_data', filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Wrote {path} with 200 signs!")

# Now let's define the comprehensive lists for Volumes 2 to 9
