import os
import sys
import pypdf
import re

sys.stdout.reconfigure(encoding='utf-8')

DIR_PATH = r"C:\Users\srish\Downloads\AI_RESEARCHPAPERS"
pdf_files = [f for f in os.listdir(DIR_PATH) if f.endswith('.pdf')]

limitation_findings = []
isolated_vs_continuous = {"isolated": 0, "continuous": 0}
vocab_counts = []
privacy_mentions = 0
hardware_mentions = 0
zonal_mentions = 0

for fname in pdf_files:
    fpath = os.path.join(DIR_PATH, fname)
    try:
        reader = pypdf.PdfReader(fpath)
        all_text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                all_text += t + "\n"

        # Check for isolated vs continuous
        if re.search(r'\bcontinuous\b', all_text, re.IGNORECASE):
            isolated_vs_continuous["continuous"] += 1
        else:
            isolated_vs_continuous["isolated"] += 1

        # Check for privacy / ethics
        if re.search(r'\bprivacy\b|\bconsent\b|\bethic', all_text, re.IGNORECASE):
            privacy_mentions += 1

        # Check for regional dialects / zonal
        if re.search(r'\bdialect|\bzonal|\bregional variation', all_text, re.IGNORECASE):
            zonal_mentions += 1

        # Check for limitations
        limits = re.findall(r'(?i)(?:limitation|drawback|future scope|future work|restricted to|challenges?)(?:[^\.\n]+[\.\n]){1,3}', all_text)
        if limits:
            clean_limits = [l.strip().replace('\n', ' ') for l in limits if len(l.strip()) > 30][:2]
            limitation_findings.append({
                "paper": fname,
                "excerpts": clean_limits
            })
    except Exception as e:
        pass

print(f"Total Papers: {len(pdf_files)}")
print(f"Isolated vs Continuous: {isolated_vs_continuous}")
print(f"Papers addressing Privacy/Consent: {privacy_mentions}/{len(pdf_files)}")
print(f"Papers addressing Regional/Zonal Dialects: {zonal_mentions}/{len(pdf_files)}")
print(f"\nSample Extracted Limitations ({len(limitation_findings)} papers had explicit limitations):")
for item in limitation_findings[:8]:
    print(f"\nPaper: {item['paper'][:40]}")
    for ex in item['excerpts']:
        print(f"  - {ex[:150]}...")
