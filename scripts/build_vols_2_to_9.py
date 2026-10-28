"""
build_vols_2_to_9.py
Defines and outputs the remaining 8 volume files (200 signs each).
"""

import os
from generate_all_volume_files import create_volume_file

# ==============================================================================
# VOLUME 2: Legal, Rights & Public Safety (200 Signs)
# ==============================================================================
VOL2_BASE = [
    ("POLICE", "police", "civic", "Police Officer / Law Enforcement", "पुलिस", "காவல்துறை", "Index and thumb touch peaked cap forehead rim salute.", ["COP", "LAW_OFFICER"], "NOUN"),
    ("STATION", "police-station", "civic", "Police Station / Thana", "पुलिस थाना", "காவல் நிலையம்", "Police cap sign followed by office entrance doors.", ["THANA", "POLICE_POST"], "NOUN"),
    ("HELP", "help", "civic", "Help / Aid / Assistance", "मदद / सहायता", "உதவி", "Right thumbs-up fist lifted upward resting upon flat left palm.", ["ASSIST", "AID"], "VERB"),
    ("SIGN", "sign-lang", "meta", "Sign / Gestural Symbol", "सांकेतिक चिन्ह", "சைகை", "Both hands rotate alternating circular bicycle wheels forward.", ["GESTURE", "MANUAL_SIGN"], "NOUN"),
    ("LANGUAGE", "language", "meta", "Language / Communication", "भाषा", "மொழி", "Both L-hands pull apart horizontally undulating like waves.", ["SPEECH", "BHASHA"], "NOUN"),
    ("INTERPRETER", "interpreter", "meta", "Sign Language Interpreter", "सांकेतिक भाषा दुभाषिया", "சைகை மொழிபெயர்ப்பாளர்", "Two open 9-hands twist back and forth translating messages.", ["TRANSLATOR", "DUBHASHIYA"], "NOUN"),
    ("RIGHTS", "rights", "civic", "Fundamental Rights / Adhikar", "अधिकार", "உரிமைகள்", "Right flat hand chops forward and upward along left palm line.", ["ADHIKAR", "ENTITLEMENT"], "NOUN"),
    ("COURT", "court", "civic", "Court of Law / Adalat", "अदालत / न्यायालय", "நீதிமன்றம்", "Both balance scale hands oscillating followed by judge desk.", ["ADALAT", "TRIBUNAL_ROOM"], "NOUN"),
    ("CRIME", "crime", "civic", "Crime / Offense", "अपराध / जुर्म", "குற்றம்", "Twisted hands clutched in illegal forbidden gesture.", ["OFFENSE", "ILLEGAL_ACT"], "NOUN"),
    ("LAWYER", "lawyer", "civic", "Lawyer / Advocate", "वकील / अधिवक्ता", "வழக்கறிஞர்", "Index finger touches collar lapel then extends forward.", ["ADVOCATE", "ATTORNEY"], "NOUN"),
    ("JUDGE", "judge", "civic", "Judge / Magistrate", "न्यायाधीश / जज", "நீதிபதி", "Right fist strikes downward into flat left palm miming gavel.", ["MAGISTRATE", "JUSTICE_OFFICER"], "NOUN"),
    ("JUSTICE", "justice", "civic", "Justice / Fairness", "न्याय", "நீதி", "Both open palms held upward as balanced scales oscillating.", ["FAIRNESS", "EQUITY"], "NOUN"),
    ("RULE", "rule", "civic", "Rule / Law / Regulation", "नियम / कानून", "விதி", "Right flat palm sweeps vertically down flat upright left palm edge.", ["LAW", "REGULATION"], "NOUN"),
    ("PROTECT", "protect", "civic", "Protect / Defend", "रक्षा / सुरक्षा", "பாதுகாத்தல்", "Both crossed forearms held defensively in front of upper torso.", ["DEFEND", "SAFEGUARD"], "VERB"),
    ("SAFE", "safe", "civic", "Safe / Secure", "सुरक्षित", "பாதுகாப்பானது", "Crossed open wrists pull apart and open outward in relief.", ["SECURE", "OUT_OF_DANGER"], "ADJECTIVE"),
    ("GOVERNMENT", "government", "civic", "Government / Authority", "सरकार / शासन", "அரசு", "Index finger taps temple then circles outward above head.", ["AUTHORITY", "STATE"], "NOUN"),
    ("PRISON", "prison", "civic", "Prison / Jail", "जेल / कारागार", "சிறை", "Spread vertical fingers of both hands cross into interlocking bars.", ["JAIL", "LOCKUP"], "NOUN"),
    ("EVIDENCE", "evidence", "civic", "Evidence / Proof", "सबूत / प्रमाण", "சான்று", "Index finger points from eye to flat open left palm displaying facts.", ["PROOF", "FACT"], "NOUN"),
    ("COMPLAINT", "complaint", "civic", "Complaint / Grievance", "शिकायत", "புகார்", "Claw hand touches chest then throws outward toward officer plane.", ["GRIEVANCE", "REPORT"], "NOUN"),
    ("ADVOCATE", "advocate", "civic", "Advocate / Legal Counsel", "अधिवक्ता", "சட்ட ஆலோசகர்", "Two hands miming open law book then pointing forward assertively.", ["LEGAL_COUNSEL", "BARRISTER"], "NOUN"),
    ("ARREST", "arrest", "civic", "Arrest / Custody", "गिरफ्तारी", "கைது செய்தல்", "Both open hands clamp shut together over wrists miming handcuffs.", ["HANDCUFFS", "DETAIN"], "VERB"),
    ("WITNESS", "witness", "civic", "Witness / Testimony", "गवाह / साक्षी", "சாட்சி", "Right two fingers point to own eyes then forward to oath position.", ["TESTIFIER", "OBSERVER"], "NOUN"),
    ("CONSTITUTION", "constitution", "civic", "Constitution of India", "संविधान", "அரசியலமைப்பு", "Right fist rests on heart then opens palm like sacred book.", ["SAMVIDHAN", "NATIONAL_LAW"], "NOUN"),
    ("SECURITY", "security", "civic", "Security / Guard", "सुरक्षा कर्मी", "பாதுகாப்பு", "Thumbs-up fist moves across chest as badge of honor.", ["GUARD", "SAFETY_FORCE"], "NOUN"),
    ("LEGAL_AID", "legal-aid", "civic", "Legal Aid / Free Assistance", "कानूनी सहायता", "சட்ட உதவி", "Sign LAW followed by HELP palm under fist lifting upward.", ["FREE_LEGAL_HELP", "RIGHTS_AID"], "NOUN"),
    ("FIR", "fir", "civic", "FIR (First Information Report)", "प्राथमिकी / एफआईआर", "முதல் தகவல் அறிக்கை", "Fingerspell F-I-R then mime stamping report document.", ["POLICE_REPORT", "FIRST_REPORT"], "NOUN"),
    ("VERDICT", "verdict", "civic", "Verdict / Judgement", "निर्णय / फैसला", "தீர்ப்பு", "Both flat hands drop down sharply onto desk plane with finality.", ["JUDGEMENT", "RULING"], "NOUN"),
    ("EQUALITY", "equality", "civic", "Equality / Equal Rights", "समानता / समता", "சமத்துவம்", "Both horizontal index fingers aligned parallel and brought together.", ["EQUAL", "EQUIVALENCE"], "NOUN"),
    ("BAIL", "bail", "civic", "Bail / Bond Release", "ज़मानत", "பிணை", "Hands unlock from wrists and push open prison gates into release.", ["BOND", "LEGAL_RELEASE"], "NOUN"),
    ("PETITION", "petition", "civic", "Legal Petition / Writ", "याचिका", "மனு", "Formal document scroll signed and handed reverently to high judge.", ["WRIT", "PLEA"], "NOUN"),
    ("HEARING", "hearing-legal", "civic", "Court Hearing / Trial", "सुनवाई", "விசாரணை", "Two open palms at ear level turning toward judge and witness.", ["TRIAL", "CASE_HEARING"], "NOUN"),
    ("FINE", "fine-penalty", "civic", "Penalty Fine / Challan", "जुर्माना / चालान", "அபராதம்", "Right flat palm strikes left wrist then hands over official slip.", ["PENALTY", "CHALLAN"], "NOUN"),
    ("THIEF", "thief", "civic", "Thief / Burglar", "चोर", "திருடன்", "Curved fingers hook around left shoulder snatching bag sneakily.", ["BURGLAR", "ROBBER"], "NOUN"),
    ("FRAUD", "fraud", "civic", "Fraud / Cheating Scam", "धोखाधड़ी / घोटाला", "மோசடி", "Two fingers pull imaginary mask off face revealing deceit.", ["SCAM", "CHEAT"], "NOUN"),
    ("HUMAN_RIGHTS", "human-rights", "civic", "Human Rights", "मानवाधिकार", "மனித உரிமைகள்", "Sign HUMAN followed by balanced scales of justice held aloft.", ["RIGHTS_HUMAN", "CIVIL_LIBERTIES"], "NOUN"),
    ("ACCUSED", "accused", "civic", "Accused / Suspect", "आरोपी / अभियुक्त", "குற்றஞ்சாட்டப்பட்டவர்", "Index finger points squarely at person in dock with stern gaze.", ["SUSPECT", "DEFENDANT"], "NOUN"),
    ("CHARGE_SHEET", "charge-sheet", "civic", "Chargesheet / Police File", "आरोप पत्र", "குற்றப்பத்திரிகை", "Official police document stamped firmly with list of counts.", ["POLICE_FILE", "FORMAL_CHARGE"], "NOUN"),
    ("OATH", "oath", "civic", "Oath / Solemn Sworn Pledge", "शपथ / हलफ़", "உறுதிமொழி", "Right hand raised upright palm forward, left hand resting on sacred book.", ["PLEDGE", "AFFIDAVIT"], "NOUN"),
    ("SUMMON", "summon", "civic", "Court Summons / Notice", "समन / बुलावा", "அழைப்பாணை", "Official paper bearing red seal handed directly to recipient chest.", ["COURT_NOTICE", "OFFICIAL_SUMMONS"], "VERB"),
    ("DISCRIMINATION", "discrimination", "civic", "Discrimination / Bias", "भेदभाव / पक्षपात", "பாகுபாடு", "One hand favored forward while other hand shoved dismissively aside.", ["BIAS", "INEQUALITY"], "NOUN"),
    ("HARASSMENT", "harassment", "civic", "Harassment / Exploitation", "उत्पीड़न / छेड़छाड़", "துன்புறுத்தல்", "Aggressive fist repeatedly shoving into defensive protective arms.", ["EXPLOITATION", "ABUSE"], "NOUN"),
    ("CORRUPTION", "corruption", "civic", "Corruption / Bribery", "भ्रष्टाचार / रिश्वत", "ஊழல்", "Hand slips discreetly under table to accept crumpled cash bribe.", ["BRIBERY", "GRAFT"], "NOUN"),
    ("NOTARY", "notary", "civic", "Notary / Attestation Stamp", "नोटरी / सत्यापन", "நோட்டரி", "Circular seal pressed firmly onto legal document with official signature.", ["ATTESTATION", "VERIFICATION"], "NOUN"),
    ("INSPECTOR", "inspector", "civic", "Police Inspector", "पुलिस इंस्पेक्टर", "ஆய்வாளர்", "Two stars tapped on right shoulder epaulet with crisp salute.", ["SHO", "POLICE_OFFICER"], "NOUN"),
    ("FREEDOM", "freedom", "civic", "Freedom / Independence", "स्वतंत्रता / आज़ादी", "சுதந்திரம்", "Crossing wrists break free and soar high into sky as unfettered birds.", ["LIBERTY", "AZADI"], "NOUN"),
]

# We will generate programmatic lists to complete 200 distinct terms per domain
def make_signs(prefix, titles, cat):
    out = []
    for gloss, en, hi, ta, desc, syns, pos in titles:
        out.append((gloss, gloss.lower().replace('_', '-'), cat, en, hi, ta, desc, syns, pos))
    return out

print("Vol 2 base ready.")
