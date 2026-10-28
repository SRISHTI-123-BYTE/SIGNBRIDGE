import os
import sys
import pypdf
import re

sys.stdout.reconfigure(encoding='utf-8')

DIR_PATH = r"C:\Users\srish\Downloads\AI_RESEARCHPAPERS"

pdf_files = [f for f in os.listdir(DIR_PATH) if f.endswith('.pdf')]
print(f"Total PDF papers found: {len(pdf_files)}")

results = []

for idx, fname in enumerate(pdf_files):
    fpath = os.path.join(DIR_PATH, fname)
    try:
        reader = pypdf.PdfReader(fpath)
        num_pages = len(reader.pages)
        # Extract text from first 2 pages
        text = ""
        for p in range(min(2, num_pages)):
            t = reader.pages[p].extract_text()
            if t:
                text += t + "\n"
        
        # Also extract last page for conclusion/future work/limitations
        last_text = ""
        if num_pages > 2:
            t = reader.pages[-1].extract_text()
            if t:
                last_text += t + "\n"

        # Search for Abstract
        abstract_match = re.search(r'(?i)abstract[:\s—\-]+(.*?)(?=(?:1\.?\s+|I\.?\s+|introduction|keywords|key\s+words))', text, re.DOTALL)
        abstract = abstract_match.group(1).strip()[:500] if abstract_match else text[:400].replace('\n', ' ')

        # Look for keywords
        models = []
        for m in ['CNN', 'LSTM', 'GRU', 'ST-GCN', 'GCN', 'Transformer', 'SVM', 'Random Forest', 'YOLO', 'ResNet', 'MediaPipe', 'OpenPose', 'Kinect', 'CTC', '3D-CNN']:
            if re.search(r'\b' + re.escape(m) + r'\b', text + last_text, re.IGNORECASE):
                models.append(m)

        # Look for vocabulary size / dataset
        vocab_match = re.search(r'(\d+)\s*(?:signs|classes|words|gestures|glosses|samples)', text + last_text, re.IGNORECASE)
        vocab_mention = vocab_match.group(0) if vocab_match else "Not specified"

        # Look for bidirectional, avatar, Indian languages
        is_bidirectional = bool(re.search(r'bidirectional|two-way|both ways', text + last_text, re.IGNORECASE))
        has_avatar = bool(re.search(r'avatar|3d model|animation|blender|three\.js|unity', text + last_text, re.IGNORECASE))
        regional_langs = re.findall(r'(?i)\b(Hindi|Tamil|Telugu|Bengali|Marathi|Gujarati|Malayalam|Kannada)\b', text + last_text)

        results.append({
            "filename": fname,
            "pages": num_pages,
            "abstract": abstract[:300] + "...",
            "models": list(set(models)),
            "vocab": vocab_mention,
            "bidirectional": is_bidirectional,
            "avatar": has_avatar,
            "languages": list(set(regional_langs)),
        })
        print(f"[{idx+1}/{len(pdf_files)}] Analyzed: {fname[:45]} | Models: {models[:4]} | Vocab: {vocab_mention}")
    except Exception as e:
        print(f"[{idx+1}/{len(pdf_files)}] Error reading {fname}: {e}")

print("\n--- ANALYSIS COMPLETED ---")
