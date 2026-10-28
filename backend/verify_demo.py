import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

from synthetic_data import generate_sign_trajectory

test_signs = ['YES', 'NO', 'HELP', 'DOCTOR', 'CHEST', 'POLICE', 'WATER', 'HELLO', 'PAIN', 'HOSPITAL', '10']

print("=" * 65)
print(" SIGNBRIDGE ALL-SIGNS END-TO-END INFERENCE & TRANSLATION VERIFICATION")
print("=" * 65)

for sign in test_signs:
    traj = generate_sign_trajectory(sign, 30)
    data = json.dumps({'sequence': traj.tolist()}).encode()
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/recognize',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    res = urllib.request.urlopen(req)
    res_data = json.loads(res.read().decode())
    tokens = [f"{t['gloss']} ({int(t['confidence']*100)}%)" for t in res_data['recognized_tokens']]
    en = res_data['translations']['en']
    hi = res_data['translations']['hi']
    ta = res_data['translations']['ta']
    print(f"[{sign:8s}] -> Tokens: {tokens}")
    print(f"            EN: {en}")
    print(f"            HI: {hi}")
    print(f"            TA: {ta}")
    print("-" * 65)
