"""
scripts/generate_vol3_banking.py
Generates exactly 200 signs for Volume 3: Banking, Commerce & Financial Standards.
"""

import os
import sys

from build_vols_3_to_9 import VOL3_BASE, bank_extras

# Add 35 more signs to guarantee >= 200
vol3_more = [
    ("MONEY_ORDER", "money-order", "civic", "Postal Money Order", "मनी ऑर्डर", "பண அஞ்சல்", "Postal counter issuing cash remittance to remote village.", ["POSTAL_ORDER", "MO"], "NOUN"),
    ("GOLD_BULLION", "gold-bullion", "civic", "Gold Bullion / Sovereign", "सोने का सिक्का", "தங்கக் கட்டி", "Pure hallmark 24-carat gold bar with certified seal.", ["GOLD_BAR", "SOVEREIGN_GOLD"], "NOUN"),
    ("SILVER_COIN", "silver-coin", "civic", "Silver Coin", "चाँदी का सिक्का", "வெள்ளி நாணயம்", "Sterling silver coin stamped with national emblem.", ["SILVER_CURRENCY", "CHANDI_SIKKA"], "NOUN"),
    ("BOND", "govt-bond", "civic", "Sovereign Gold / Govt Bond", "सरकारी बॉन्ड", "அரசுப் பத்திரம்", "Government sovereign security paying guaranteed coupon yield.", ["SOVEREIGN_BOND", "G_SEC"], "NOUN"),
    ("DEBENTURE", "debenture", "civic", "Corporate Debenture", "ऋणपत्र / डिबेंचर", "கடனீட்டுப் பத்திரம்", "Company debt instrument yielding fixed contractual return.", ["CORP_BOND", "DEBT_SECURITY"], "NOUN"),
    ("VENTURE_CAPITAL", "venture-capital", "civic", "Venture Capital / VC", "उद्यम पूंजी / वीसी", "துணிகர மூலதனம்", "Institutional fund investing risk capital in tech startup.", ["VC_FUND", "STARTUP_INVESTOR"], "NOUN"),
    ("ANGEL_INVESTOR", "angel-investor", "civic", "Angel Investor", "एंजेल निवेशक", "ஏஞ்சல் முதலீட்டாளர்", "Affluent early-stage investor backing innovative seed idea.", ["SEED_FUNDER", "ANGEL_FUND"], "NOUN"),
    ("EQUITY_DIVIDEND", "equity-dividend", "civic", "Interim Equity Dividend", "अंतरिम लाभांश", "இடைக்கால ஈவுத்தொகை", "Half-yearly dividend warrant credited directly to bank account.", ["INTERIM_PAYOUT", "SHARE_PROFIT"], "NOUN"),
    ("TREASURY_BILL", "treasury-bill", "civic", "RBI Treasury Bill (T-Bill)", "ट्रेजरी बिल", "கருவூல பத்திரம்", "Short-term sovereign paper issued at discount by RBI.", ["T_BILL", "MONEY_MARKET_BILL"], "NOUN"),
    ("COMMERCIAL_PAPER", "comm-paper", "civic", "Commercial Paper (CP)", "वाणिज्यिक पत्र", "வணிகத் தாள்", "Short-term unsecured debt paper issued by leading corporates.", ["CP", "SHORT_TERM_NOTE"], "NOUN"),
    ("CERTIFICATE_OF_DEPOSIT", "cd-deposit", "civic", "Certificate of Deposit (CD)", "जमा प्रमाणपत्र", "வைப்புச் சான்றிதழ்", "Negotiable term money market receipt issued by bank.", ["CD", "INTERBANK_DEPOSIT"], "NOUN"),
    ("CALL_MONEY", "call-money", "civic", "Interbank Call Money", "कॉल मनी मार्केट", "அழைப்புப் பணம்", "Overnight lending market between scheduled commercial banks.", ["OVERNIGHT_BORROW", "INTERBANK_LEND"], "NOUN"),
    ("CREDIT_RATING", "credit-rating", "civic", "Credit Rating (CRISIL/ICRA)", "क्रेडिट रेटिंग", "கடன் மதிப்பீடு", "Triple-A rating measuring creditworthiness and risk.", ["CRISIL_RATING", "AAA_RATING"], "NOUN"),
    ("CIBIL_SCORE", "cibil-score", "civic", "CIBIL Credit Score (300-900)", "सिबिल स्कोर", "சிபில் மதிப்பெண்", "Credit bureau score determining loan eligibility and rate.", ["CREDIT_SCORE", "BUREAU_RATING"], "NOUN"),
    ("FINANCIAL_INCLUSION", "fin-inclusion", "civic", "Financial Inclusion / Jan Dhan", "वित्तीय समावेशन / जन-धन", "அனைவருக்குமான நிதிச் சேவை", "Opening universal bank accounts for all unbanked citizens.", ["JAN_DHAN", "BANKING_FOR_ALL"], "NOUN"),
    ("BANK_MITRA", "bank-mitra", "civic", "Bank Mitra / CSP Agent", "बैंक मित्र / बीसी", "வங்கி மித்ரா", "Customer Service Point agent serving remote rural hamlet.", ["BC_AGENT", "CSP_OUTLET"], "NOUN"),
    ("SELF_HELP_GROUP", "shg-group", "civic", "Self Help Group (SHG)", "स्वयं सहायता समूह (एसएचजी)", "சுய உதவிக் குழு", "Village women micro-savings and micro-credit community collective.", ["SHG", "MICRO_CREDIT"], "NOUN"),
    ("NABARD", "nabard-bank", "civic", "NABARD Rural Apex Bank", "नाबार्ड", "நபார்டு வங்கி", "Apex development bank financing agriculture and rural craft.", ["RURAL_DEVELOP_BANK", "AGRI_FINANCE"], "NOUN"),
    ("SIDBI", "sidbi-bank", "civic", "SIDBI Small Industry Bank", "सिडबी", "சிட்பி வங்கி", "Principal financial institution promoting MSME small industry.", ["SMALL_INDUSTRY_BANK", "MSME_FINANCE"], "NOUN"),
    ("EXIM_BANK", "exim-bank", "civic", "Export-Import Bank of India", "एक्ज़िम बैंक", "ஏற்றுமதி இறக்குமதி வங்கி", "Financing cross-border international bilateral merchandise trade.", ["FOREIGN_TRADE_BANK", "EXIM"], "NOUN"),
    ("FOREIGN_REMITTANCE", "forex-remit", "civic", "Inward NRI Remittance", "विदेशी आवक धन", "அந்நிய பண வரவு", "Family abroad wiring foreign currency home to Indian account.", ["INWARD_MONEY", "HAWALA_PREVENT"], "NOUN"),
    ("HAWALA_PREVENTION", "pmla-hawala", "civic", "Anti-Hawala Prevention", "हवाला निषेध", "ஹவாலா தடுப்பு", "Strict prohibition on illicit underground cash couriers.", ["ILLEGAL_REMIT", "CASH_COURIER_BAN"], "NOUN"),
    ("DEVALUATION", "devaluation", "civic", "Currency Devaluation", "मुद्रा अवमूल्यन", "நாணய மதிப்பு குறைப்பு", "Downward adjustment of official domestic exchange rate peg.", ["RUPEE_DROP", "CURRENCY_SLIDE"], "NOUN"),
    ("APPRECIATION_FX", "appreciation-fx", "civic", "Rupee Currency Appreciation", "मुद्रा अधिमूल्यन", "நாணய மதிப்பு உயர்வு", "Rising purchasing strength of Indian Rupee in global forex.", ["RUPEE_RISE", "FX_STRENGTH"], "NOUN"),
    ("DEMONETIZATION", "demonetization", "civic", "Demonetization of Currency", "नोटबंदी / विमुद्रीकरण", "பணமதிப்பிழப்பு", "Stripping specified old banknote denominations of legal tender.", ["NOTEBANDI", "CURRENCY_REPLACEMENT"], "NOUN"),
    ("CURRENCY_CHEST", "currency-chest", "civic", "RBI Authorized Currency Chest", "करेंसी चेस्ट", "நாணயக் களஞ்சியம்", "Fortified bank vault holding fresh banknotes across regions.", ["CASH_DEPOT", "RESERVE_CHEST"], "NOUN"),
    ("MINT", "security-mint", "civic", "Government Currency Mint (SPMCIL)", "टकसाल", "நாணய ஆலை", "Official government security press printing banknotes and coins.", ["TAKSAAL", "SECURITY_PRESS"], "NOUN"),
    ("FORGERY", "fake-currency", "civic", "Counterfeit Fake Currency (FICN)", "नकली नोट", "போலி ரூபாய் நோட்டு", "Ultrasonic ultraviolet detection seizing fake counterfeit notes.", ["FAKE_NOTE", "FICN"], "NOUN"),
    ("WATERMARK", "watermark-note", "civic", "Banknote Security Watermark", "नोट का वॉटरमार्क", "நீர்க்குறி", "Mahatma Gandhi portrait watermark visible against clear light.", ["SECURITY_THREAD", "GANDHI_PORTRAIT"], "NOUN"),
    ("SECURITY_THREAD", "security-thread", "civic", "Windowed Security Thread", "सुरक्षा धागा", "பாதுகாப்பு நூல்", "Metallic micro-lettered color-shifting strip woven in note.", ["RBI_THREAD", "COLOR_SHIFT_STRIP"], "NOUN"),
    ("LATENT_IMAGE", "latent-image", "civic", "Latent Denomination Image", "प्रच्छन्न चित्र", "மறைந்திருக்கும் படம்", "Tilted currency note revealing denominational numeral optical.", ["OPTICAL_IMAGE", "TILT_FEATURE"], "NOUN"),
    ("BLEED_LINES", "bleed-lines", "civic", "Tactile Bleed Lines for Blind", "ब्लीड लाइन (दृष्टिबाधित)", "தொட்டுணரும் கோடுகள்", "Raised tactile intaglio edge marks aiding visually impaired.", ["INTAGLIO_MARKS", "TACTILE_DENOMINATION"], "NOUN"),
    ("MANI_APP", "mani-app", "civic", "RBI MANI App (Note Identifier)", "आरबीआई मानी ऐप", "மானி மொபைல் செயலி", "Mobile camera scanning and announcing currency value in audio.", ["NOTE_AUDIO_APP", "MANI_IDENTIFIER"], "NOUN"),
    ("SOVEREIGNTY_RUPEE", "sovereign-rupee", "civic", "Sovereign Legal Tender", "वैध मुद्रा", "சட்டப்பூர்வ நாணயம்", "Promissory note backed by sovereign credit guarantee of RBI.", ["LEGAL_TENDER", "PROMISOR"], "NOUN"),
    ("DISBURSEMENT", "disbursement", "civic", "Loan Disbursal to Account", "ऋण संवितरण", "கடன் தொகை விடுவிப்பு", "Sanctioned loan capital transferred directly into bank balance.", ["LOAN_RELEASE", "FUNDS_SANCTION"], "NOUN"),
]

raw_signs = VOL3_BASE + bank_extras + vol3_more
seen = set()
unique_signs = []
for s in raw_signs:
    if s[0] not in seen:
        seen.add(s[0])
        unique_signs.append(s)

final_200 = unique_signs[:200]
assert len(final_200) == 200, f"Expected 200 signs, got {len(final_200)}"

out_path = os.path.join("scripts", "volume_data", "vol3_banking.py")
with open(out_path, "w", encoding="utf-8") as f:
    f.write('"""\nVolume 3: Banking, Commerce & Financial Standards (200 Signs)\n"""\n\n')
    f.write("VOL3_BANKING_200 = [\n")
    for item in final_200:
        f.write(f"    {repr(item)},\n")
    f.write("]\n\n")
    f.write('assert len(VOL3_BANKING_200) == 200, f"Expected 200 signs, got {len(VOL3_BANKING_200)}"\n')

print(f"Successfully generated {out_path} with {len(final_200)} unique signs!")
