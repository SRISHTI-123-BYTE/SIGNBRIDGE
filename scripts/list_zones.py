import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'backend')
from indian_sign_languages import INDIAN_SIGN_LANGUAGES

print(f"Total entries in INDIAN_SIGN_LANGUAGES: {len(INDIAN_SIGN_LANGUAGES)}")
for item in INDIAN_SIGN_LANGUAGES:
    print(f"ID: {item.get('id')}")
    print(f"  Name: {item.get('name')}")
    print(f"  Short Name: {item.get('short_name')}")
    print(f"  Native Name: {item.get('native_name')}")
    print(f"  Classification: {item.get('classification')}")
    print(f"  Badge: {item.get('badge')}")
    print(f"  Regions: {item.get('regions')}")
    print(f"  Primary Centers: {item.get('primary_centers')}")
    print(f"  Estimated Signers: {item.get('estimated_signers')}")
    print(f"  Standardizing Body: {item.get('standardizing_body')}")
    print(f"  Description: {item.get('description')}")
    print("-" * 60)
