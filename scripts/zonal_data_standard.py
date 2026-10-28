# scripts/zonal_data_standard.py
"""
ISLRTC National Apex Standard (isl-standard) - 100 Domain Specific Signs
Focus: National civic, constitutional, parliamentary governance, central ministries,
NCERT academics, AIIMS healthcare, supreme judiciary, national identity, federal infrastructure.
"""

STANDARD_SIGNS = [
    {
        "gloss": "DOCTOR",
        "en": "Doctor / Medical Practitioner",
        "hi": "चिकित्सक / डॉक्टर",
        "ta": "மருத்துவர்",
        "category": "emergency",
        "description": "Tap index and middle fingers on the radial pulse of the non-dominant wrist twice."
    },
    {
        "gloss": "WATER",
        "en": "Water / Drinking Water",
        "hi": "जल / पानी",
        "ta": "தண்ணீர்",
        "category": "daily",
        "description": "Form a cup with the right hand and bring it toward the mouth with a slight chin tilt."
    },
    {
        "gloss": "HELP",
        "en": "Help / Assistance",
        "hi": "सहायता / मदद",
        "ta": "உதவி",
        "category": "emergency",
        "description": "Place closed right fist thumb-up on the flat palm of the left hand and lift both together."
    },
    {
        "gloss": "THANK_YOU",
        "en": "Thank You / Gratitude",
        "hi": "धन्यवाद / शुक्रिया",
        "ta": "நன்றி",
        "category": "greeting",
        "description": "Touch fingers of flat right hand to chin or chest and move forward with an acknowledging nod."
    },
    {
        "gloss": "HOSPITAL",
        "en": "Hospital / Medical Center",
        "hi": "अस्पताल / चिकित्सालय",
        "ta": "மருத்துவமனை",
        "category": "emergency",
        "description": "Trace a cross on the left upper arm with the right index finger, followed by the roof sign."
    },
    {
        "gloss": "MEDICINE",
        "en": "Medicine / Pharmaceuticals",
        "hi": "दवा / औषधि",
        "ta": "மருந்து",
        "category": "emergency",
        "description": "Place right middle finger into center of left palm and rotate as if grinding medication."
    },
    {
        "gloss": "POLICE",
        "en": "Police Officer / Law Enforcement",
        "hi": "पुलिस / कानून व्यवस्था",
        "ta": "காவல்துறை",
        "category": "emergency",
        "description": "Right thumb and index finger touch the forehead rim indicating a peaked uniform cap."
    },
    {
        "gloss": "SCHOOL",
        "en": "School / Educational Institution",
        "hi": "विद्यालय / स्कूल",
        "ta": "பள்ளி",
        "category": "academic",
        "description": "Clap palms together horizontally twice, then indicate an enclosed building structure."
    },
    {
        "gloss": "BANK",
        "en": "Bank / Financial Institution",
        "hi": "बैंक / वित्तीय संस्था",
        "ta": "வங்கி",
        "category": "civic",
        "description": "Fingerspell B-A-N-K, followed by thumb flicking index finger miming counting banknotes."
    },
    {
        "gloss": "TIME",
        "en": "Time / Clock Hours",
        "hi": "समय / वक्त",
        "ta": "நேரம்",
        "category": "numbers",
        "description": "Tap the index finger of the right hand twice onto the wrist where a watch is worn."
    },
    {
        "gloss": "BOOK",
        "en": "Book / Textbook",
        "hi": "पुस्तक / किताब",
        "ta": "புத்தகம்",
        "category": "academic",
        "description": "Place both flat palms together, then open them outwards like opening the pages of a book."
    },
    {
        "gloss": "HELLO",
        "en": "Hello / Greetings",
        "hi": "नमस्ते / हैलो",
        "ta": "வணக்கம்",
        "category": "greeting",
        "description": "Open dominant hand moves outward from temple in an open-palm formal greeting."
    },
    {
        "gloss": "PLEASE",
        "en": "Please / Polite Request",
        "hi": "कृपया / निवेदन",
        "ta": "தயவுசெய்து",
        "category": "greeting",
        "description": "Circular motion of flat right hand on the chest with an earnest facial expression."
    },
    {
        "gloss": "FOOD",
        "en": "Food / Meal",
        "hi": "भोजन / खाना",
        "ta": "உணவு",
        "category": "daily",
        "description": "Touch bunched fingertips of dominant hand to the mouth repeatedly."
    },
    {
        "gloss": "TRAIN",
        "en": "Train / Railway Transit",
        "hi": "रेलगाड़ी / ट्रेन",
        "ta": "ரயில்",
        "category": "navigation",
        "description": "Two fingers of right hand move back and forth along the top of two fingers of left hand miming tracks."
    },
    {
        "gloss": "WHERE",
        "en": "Where / Location Query",
        "hi": "कहाँ / किस स्थान पर",
        "ta": "எங்கே",
        "category": "navigation",
        "description": "Both palms open facing upward moving side to side with furrowed inquisitive brows."
    },
    {
        "gloss": "FAMILY",
        "en": "Family / Household",
        "hi": "परिवार / कुटुम्ब",
        "ta": "குடும்பம்",
        "category": "daily",
        "description": "Both hands form F-shapes with thumbs and index fingers meeting, tracing a circle outward until pinkies meet."
    },
    {
        "gloss": "TODAY",
        "en": "Today / Present Day",
        "hi": "आज / वर्तमान दिन",
        "ta": "இன்று",
        "category": "numbers",
        "description": "Both open hands with palms up drop down decisively in front of chest."
    },
    {
        "gloss": "SIGN",
        "en": "Sign / Sign Language",
        "hi": "संकेत / सांकेतिक भाषा",
        "ta": "சைகை",
        "category": "meta",
        "description": "Both open hands with index fingers circling each other in an alternating rolling movement."
    },
    {
        "gloss": "COMPUTER",
        "en": "Computer / Workstation",
        "hi": "संगणक / कंप्यूटर",
        "ta": "கணினி",
        "category": "academic",
        "description": "Wiggle fingers of both hands over a horizontal plane miming fast typing on a keyboard."
    },
    {
        "gloss": "EMERGENCY",
        "en": "Emergency / Urgent Situation",
        "hi": "आपातकाल / संकट",
        "ta": "அவசரம்",
        "category": "emergency",
        "description": "Right hand E-shape wave rapidly side to side with wide alarmed non-manual eye expression."
    },
    {
        "gloss": "NEED",
        "en": "Need / Necessity",
        "hi": "आवश्यकता / जरूरत",
        "ta": "தேவை",
        "category": "daily",
        "description": "Right bent index finger drops downwards firmly with affirmative head nod."
    },
    {
        "gloss": "LAWYER",
        "en": "Lawyer / Advocate",
        "hi": "वकील / अधिवक्ता",
        "ta": "வழக்கறிஞர்",
        "category": "civic",
        "description": "Right hand in L-shape taps palm of upright flat left hand twice at top and bottom."
    },
    {
        "gloss": "STUDENT",
        "en": "Student / Learner",
        "hi": "विद्यार्थी / छात्र",
        "ta": "மாணவர்",
        "category": "academic",
        "description": "Right hand mimes gathering knowledge from left palm to forehead, followed by agentive suffix."
    },
    {
        "gloss": "CONSTITUTION",
        "en": "Constitution of India / Samvidhan",
        "hi": "भारत का संविधान",
        "ta": "இந்திய அரசியலமைப்பு",
        "category": "civic",
        "description": "Fingerspell C, tap it on heart, then open flat hands solemnly like the grand national parchment."
    },
    {
        "gloss": "PARLIAMENT",
        "en": "Parliament of India / Sansad Bhavan",
        "hi": "संसद / संसद भवन",
        "ta": "நாடாளுமன்றம்",
        "category": "civic",
        "description": "Both curved hands trace circular architecture of Sansad Bhavan, followed by gathering debate gesture."
    },
    {
        "gloss": "SUPREME_COURT",
        "en": "Supreme Court of India / Apex Court",
        "hi": "सर्वोच्च न्यायालय / सुप्रीम कोर्ट",
        "ta": "உச்ச நீதிமன்றம்",
        "category": "civic",
        "description": "Balance scale gesture with both palms dipping alternately, then raise right index to highest apex."
    },
    {
        "gloss": "PRESIDENT",
        "en": "President of India / Rashtrapati",
        "hi": "राष्ट्रपति / राष्ट्राध्यक्ष",
        "ta": "குடியரசுத் தலைவர்",
        "category": "civic",
        "description": "Both hands at sides of forehead pull outwards miming broad presidential crown of state."
    },
    {
        "gloss": "PRIME_MINISTER",
        "en": "Prime Minister / Pradhan Mantri",
        "hi": "प्रधानमंत्री",
        "ta": "பிரதமர்",
        "category": "civic",
        "description": "Number one index finger thrust forward firmly from center chest, followed by ministerial seal tap."
    },
    {
        "gloss": "GOVERNMENT",
        "en": "Government / Sarkar",
        "hi": "सरकार / शासन",
        "ta": "அரசாங்கம்",
        "category": "civic",
        "description": "Right index finger points to temple, twists outwards, and forms authoritative horizontal boundary."
    },
    {
        "gloss": "CITIZEN",
        "en": "Citizen / National of India",
        "hi": "नागरिक / देशवासी",
        "ta": "குடிமகன்",
        "category": "civic",
        "description": "Both hands trace boundary of national map then point thumb firmly to center chest."
    },
    {
        "gloss": "DEMOCRACY",
        "en": "Democracy / Republic Rule",
        "hi": "लोकतंत्र / प्रजातंत्र",
        "ta": "மக்களாட்சி",
        "category": "civic",
        "description": "All people gesture with open hands circling in, then all pointing fingers casting ballots together."
    },
    {
        "gloss": "VOTE_ELECTION",
        "en": "Vote / Cast Ballot",
        "hi": "मतदान / वोट डालना",
        "ta": "வாக்களிப்பு",
        "category": "civic",
        "description": "Right hand pinches imaginary slip and deposits it into ballot slot with ink mark on index finger."
    },
    {
        "gloss": "ELECTION_COMMISSION",
        "en": "Election Commission of India",
        "hi": "भारतीय निर्वाचन आयोग",
        "ta": "தேர்தல் ஆணையம்",
        "category": "civic",
        "description": "Fingerspell E-C-I, followed by ballot drop gesture and official certification stamp."
    },
    {
        "gloss": "NATIONAL_ANTHEM",
        "en": "National Anthem / Jana Gana Mana",
        "hi": "राष्ट्रगान / जन गण मन",
        "ta": "தேசிய கீதம்",
        "category": "civic",
        "description": "Attention posture, right flat palm over left chest, head elevated with reverent expression."
    },
    {
        "gloss": "NATIONAL_FLAG",
        "en": "National Tricolor Flag / Tiranga",
        "hi": "राष्ट्रीय ध्वज / तिरंगा",
        "ta": "தேசியக் கொடி",
        "category": "civic",
        "description": "Right hand holds flagpole while left and right trace three horizontal stripes and center wheel."
    },
    {
        "gloss": "EMBLEM_ASHOKA",
        "en": "State Emblem of India / Lion Capital of Ashoka",
        "hi": "राजचिह्न / अशोक स्तम्भ",
        "ta": "அரசு சின்னம்",
        "category": "civic",
        "description": "Both curved claw hands meet facing forward, miming the three noble lions guarding four directions."
    },
    {
        "gloss": "CENTRAL_MINISTRY",
        "en": "Central Government Ministry",
        "hi": "केंद्रीय मंत्रालय",
        "ta": "மத்திய அமைச்சகம்",
        "category": "civic",
        "description": "Right hand M-shape taps right shoulder then moves across horizontal executive desk."
    },
    {
        "gloss": "SECRETARIAT",
        "en": "Secretariat / Central Administrative Complex",
        "hi": "सचिवालय",
        "ta": "தலைமைச் செயலகம்",
        "category": "civic",
        "description": "Fingers mime rapid administrative typing, then arms trace sprawling grand administrative edifice."
    },
    {
        "gloss": "CIVIL_SERVICES",
        "en": "Civil Services / IAS / IPS Cadre",
        "hi": "सिविल सेवा / लोक सेवा",
        "ta": "குடிமைப் பணிகள்",
        "category": "civic",
        "description": "Fingertips trace shoulder epaulets and executive lapel with authoritative posture."
    },
    {
        "gloss": "UPSC",
        "en": "Union Public Service Commission",
        "hi": "संघ लोक सेवा आयोग",
        "ta": "மத்திய அரசுப் பணியாளர் தேர்வாணையம்",
        "category": "civic",
        "description": "Fingerspell U-P-S-C, followed by examination paper review and grand apex seal stamp."
    },
    {
        "gloss": "NCERT",
        "en": "NCERT National Curriculum Council",
        "hi": "राष्ट्रीय शैक्षिक अनुसंधान और प्रशिक्षण परिषद",
        "ta": "தேசிய கல்வியியல் ஆராய்ச்சி மற்றும் பயிற்சி நிறுவனம்",
        "category": "academic",
        "description": "Fingerspell N-C-E-R-T, then open book icon with standard apex certificate gesture."
    },
    {
        "gloss": "AIIMS_HOSPITAL",
        "en": "AIIMS Central Institute of Medical Sciences",
        "hi": "अखिल भारतीय आयुर्विज्ञान संस्थान (एम्स)",
        "ta": "எய்ம்ஸ் மருத்துவக் கழகம்",
        "category": "emergency",
        "description": "Fingerspell A-I-I-M-S, followed by stethoscope neck tap and apex hospital roof sign."
    },
    {
        "gloss": "ISRO_SPACE",
        "en": "ISRO Indian Space Research Organisation",
        "hi": "भारतीय अंतरिक्ष अनुसंधान संगठन (इसरो)",
        "ta": "இஸ்ரோ விண்வெளி ஆய்வு நிறுவனம்",
        "category": "academic",
        "description": "Rocket shape hand blasts upwards from flat base palm ascending toward stars."
    },
    {
        "gloss": "DEFENCE_FORCE",
        "en": "Armed Forces / Defence Ministry",
        "hi": "रक्षा बल / भारतीय सेना",
        "ta": "பாதுகாப்புப் படை",
        "category": "civic",
        "description": "Both hands form shield across chest, then salute firmly at forehead."
    },
    {
        "gloss": "ARMY",
        "en": "Indian Army / Land Warfare",
        "hi": "थल सेना / भारतीय थलसेना",
        "ta": "தரைப்படை",
        "category": "civic",
        "description": "Marching salute with dominant hand touching temple with firm jawline."
    },
    {
        "gloss": "NAVY",
        "en": "Indian Navy / Maritime Defence",
        "hi": "नौसेना / जल सेना",
        "ta": "கடற்படை",
        "category": "civic",
        "description": "Both hands mime ocean waves, followed by anchor shape and naval salute."
    },
    {
        "gloss": "AIR_FORCE",
        "en": "Indian Air Force / Aviation Wing",
        "hi": "वायु सेना / एयर फोर्स",
        "ta": "விமானப்படை",
        "category": "civic",
        "description": "Fighter jet hand shape soars across upper signing space with aerial roar mouthing."
    },
    {
        "gloss": "RAILWAY_BOARD",
        "en": "Railway Board / Indian Railways Central",
        "hi": "रेलवे बोर्ड / भारतीय रेल",
        "ta": "ரயில்வே வாரியம்",
        "category": "civic",
        "description": "Parallel train tracks motion leading into executive boardroom conference circle."
    },
    {
        "gloss": "RESERVE_BANK",
        "en": "Reserve Bank of India / RBI Apex Bank",
        "hi": "भारतीय रिज़र्व बैंक (आरबीआई)",
        "ta": "இந்திய ரிசர்வ் வங்கி",
        "category": "civic",
        "description": "Fingerspell R-B-I, mime currency note printing, and raise both palms as central vault guardian."
    },
    {
        "gloss": "PASSPORT_SEVA",
        "en": "Passport / International Travel Document",
        "hi": "पासपोर्ट सेवा / पारपत्र",
        "ta": "கடவுச்சீட்டு சேவை",
        "category": "civic",
        "description": "Small booklet held in left hand stamped firmly with round visa seal by right fist."
    },
    {
        "gloss": "AADHAAR_CARD",
        "en": "Aadhaar Card / UIDAI Biometric Identity",
        "hi": "आधार कार्ड / पहचान पत्र",
        "ta": "ஆதார் அட்டை",
        "category": "civic",
        "description": "Thumb pressed onto imaginary biometric glass reader, followed by 12-digit card tap."
    },
    {
        "gloss": "PAN_CARD",
        "en": "PAN Card / Permanent Account Number",
        "hi": "पैन कार्ड / स्थायी खाता संख्या",
        "ta": "பான் அட்டை",
        "category": "civic",
        "description": "Fingerspell P-A-N, tap wallet card gesture with tax seal."
    },
    {
        "gloss": "INCOME_TAX",
        "en": "Income Tax / Direct Taxes",
        "hi": "आयकर / इनकम टैक्स",
        "ta": "வருமான வரி",
        "category": "civic",
        "description": "Right hand scoops portion from left palm stack and deposits into government revenue ledger."
    },
    {
        "gloss": "GST_COUNCIL",
        "en": "Goods and Services Tax / GST Council",
        "hi": "वस्तु एवं सेवा कर (जीएसटी)",
        "ta": "சரக்கு மற்றும் சேவை வரி",
        "category": "civic",
        "description": "Fingerspell G-S-T, circle hands horizontally to show unified nationwide tax."
    },
    {
        "gloss": "GAZETTE_OF_INDIA",
        "en": "The Gazette of India / Official Notification",
        "hi": "भारत का राजपत्र / गजट",
        "ta": "இந்திய அரசிதழ்",
        "category": "civic",
        "description": "Open broad ceremonial scroll and imprint official state seal of public record."
    },
    {
        "gloss": "CENSUS_INDIA",
        "en": "Census of India / Population Count",
        "hi": "भारतीय जनगणना",
        "ta": "இந்திய மக்கள் தொகை கணக்கெடுப்பு",
        "category": "civic",
        "description": "Clipboard checkmark gesture repeated house to house counting every family member."
    },
    {
        "gloss": "POST_OFFICE",
        "en": "India Post / Postal Department",
        "hi": "डाकघर / भारतीय डाक",
        "ta": "அஞ்சல் அலுவலகம்",
        "category": "civic",
        "description": "Lick imaginary postage stamp, affix to envelope corner, and drop in red postbox."
    },
    {
        "gloss": "METEOROLOGICAL_DEPT",
        "en": "India Meteorological Department / IMD Mausam",
        "hi": "भारतीय मौसम विज्ञान विभाग",
        "ta": "இந்திய வானிலை ஆய்வு மையம்",
        "category": "academic",
        "description": "Look upwards at sky, mime rain gauge, thermometer, and radar satellite scan."
    },
    {
        "gloss": "CENTRAL_UNIVERSITY",
        "en": "Central University of India",
        "hi": "केंद्रीय विश्वविद्यालय",
        "ta": "மத்தியப் பல்கலைக்கழகம்",
        "category": "academic",
        "description": "Mortarboard hat gesture above head, followed by national standard pillar gesture."
    },
    {
        "gloss": "UNIVERSITY_GRANTS",
        "en": "University Grants Commission / UGC",
        "hi": "विश्वविद्यालय अनुदान आयोग (यूजीसी)",
        "ta": "பல்கலைக்கழக மானியக் குழு",
        "category": "academic",
        "description": "Fingerspell U-G-C, distribute financial research grants with open forward palms."
    },
    {
        "gloss": "IIT_INSTITUTE",
        "en": "Indian Institute of Technology / IIT",
        "hi": "भारतीय प्रौद्योगिकी संस्थान (आईआईटी)",
        "ta": "இந்திய தொழில்நுட்ப நிறுவனம்",
        "category": "academic",
        "description": "Fingerspell I-I-T, connect engineering cogwheels and high-tech microprocessor circuits."
    },
    {
        "gloss": "IIM_INSTITUTE",
        "en": "Indian Institute of Management / IIM",
        "hi": "भारतीय प्रबंधन संस्थान (आईआईएम)",
        "ta": "இந்திய மேலாண்மை நிறுவனம்",
        "category": "academic",
        "description": "Fingerspell I-I-M, trace corporate business growth chart ascending diagonally."
    },
    {
        "gloss": "NATIONAL_HIGHWAY",
        "en": "National Highway / NHAI Expressway",
        "hi": "राष्ट्रीय राजमार्ग / एक्सप्रेसवे",
        "ta": "தேசிய நெடுஞ்சாலை",
        "category": "navigation",
        "description": "Both arms extend straight forward parallel, tracing a long four-lane arterial thoroughfare."
    },
    {
        "gloss": "SPEED_POST",
        "en": "Speed Post / Express Postal Courier",
        "hi": "स्पीड पोस्ट / द्रुत डाक",
        "ta": "ஸ்பீட் போஸ்ட்",
        "category": "civic",
        "description": "Letter held in right hand shoots forward with aerodynamic speed motion."
    },
    {
        "gloss": "CURRENCY_NOTE",
        "en": "Currency Note / Rupee Cash",
        "hi": "करेंसी नोट / भारतीय रुपया",
        "ta": "ரூபாய் நோட்டு",
        "category": "civic",
        "description": "Both hands outline rectangular banknote, flick watermark with thumb and index."
    },
    {
        "gloss": "COMMISSIONER",
        "en": "Commissioner / Senior Executive Authority",
        "hi": "आयुक्त / कमिश्नर",
        "ta": "ஆணையர்",
        "category": "civic",
        "description": "Salute touching peak of cap, followed by ceremonial sash across shoulder."
    },
    {
        "gloss": "CHIEF_JUSTICE",
        "en": "Chief Justice of India / CJI",
        "hi": "भारत के मुख्य न्यायाधीश",
        "ta": "இந்திய தலைமை நீதிபதி",
        "category": "civic",
        "description": "Right hand raps gavel firmly three times, then touches heart and apex constitutional crest."
    },
    {
        "gloss": "ATTORNEY_GENERAL",
        "en": "Attorney General for India",
        "hi": "भारत के महान्यायवादी",
        "ta": "இந்திய அரசு தலைமை வழக்கறிஞர்",
        "category": "civic",
        "description": "Apex legal counsel gesture advising the Council of Ministers in parliament."
    },
    {
        "gloss": "COMPTROLLER_AUDITOR",
        "en": "Comptroller and Auditor General / CAG",
        "hi": "नियंत्रक एवं महालेखापरीक्षक (कैग)",
        "ta": "தலைமைக் கணக்குத் தணிக்கையாளர்",
        "category": "civic",
        "description": "Scrutinize public accounts ledger with magnifying lens, stamp audit clearance seal."
    },
    {
        "gloss": "LOK_SABHA",
        "en": "Lok Sabha / House of the People",
        "hi": "लोकसभा / संसद का निचला सदन",
        "ta": "மக்களவை",
        "category": "civic",
        "description": "People gesture seated in green carpet semicircular rows debating national statutes."
    },
    {
        "gloss": "RAJYA_SABHA",
        "en": "Rajya Sabha / Council of States",
        "hi": "राज्यसभा / संसद का उच्च सदन",
        "ta": "மாநிலங்களவை",
        "category": "civic",
        "description": "States representation gesture seated in red carpet upper chamber of elders."
    },
    {
        "gloss": "SPEAKER_HOUSE",
        "en": "Speaker of the Lok Sabha",
        "hi": "लोकसभा अध्यक्ष / स्पीकर",
        "ta": "மக்களவைத் தலைவர்",
        "category": "civic",
        "description": "Elevated central chair gesture, rap gavel asking members to maintain decorum."
    },
    {
        "gloss": "BILL_LEGISLATION",
        "en": "Legislative Bill / Draft Statute",
        "hi": "विधेयक / मसौदा कानून",
        "ta": "சட்ட மசோதா",
        "category": "civic",
        "description": "Draft document placed on podium, read aloud, and put to vote for legislative assent."
    },
    {
        "gloss": "ACT_LAW",
        "en": "Enacted Act / Statutory Law",
        "hi": "अधिनियम / पारित कानून",
        "ta": "சட்டம்",
        "category": "civic",
        "description": "Presidential signature motion over legislation followed by firm gavel strike."
    },
    {
        "gloss": "ORDINANCE",
        "en": "Presidential Ordinance / Promulgation",
        "hi": "अध्यादेश / आपात आदेश",
        "ta": "அவசரச் சட்டம்",
        "category": "civic",
        "description": "Urgent presidential decree stamp enacted during parliamentary recess."
    },
    {
        "gloss": "FUNDAMENTAL_RIGHTS",
        "en": "Fundamental Rights / Part III of Constitution",
        "hi": "मौलिक अधिकार",
        "ta": "அடிப்படை உரிமைகள்",
        "category": "civic",
        "description": "Five open fingers raised proudly representing constitutional liberty, equality, and dignity."
    },
    {
        "gloss": "FUNDAMENTAL_DUTIES",
        "en": "Fundamental Duties / Article 51A",
        "hi": "मौलिक कर्तव्य",
        "ta": "அடிப்படை கடமைகள்",
        "category": "civic",
        "description": "Fist over chest and respectful bow toward the national flag affirming civic duties."
    },
    {
        "gloss": "DIRECTIVE_PRINCIPLES",
        "en": "Directive Principles of State Policy",
        "hi": "राज्य के नीति निर्देशक तत्व",
        "ta": "அரசு வழிகாட்டு நெறிமுறைகள்",
        "category": "civic",
        "description": "Index finger points guiding pathway forward for welfare of all citizens."
    },
    {
        "gloss": "JUDICIAL_REVIEW",
        "en": "Judicial Review / Constitutional Bench",
        "hi": "न्यायिक पुनरावलोकन",
        "ta": "நீதித்துறை மறுஆய்வு",
        "category": "civic",
        "description": "Gavel in hand examining statute book against constitutional parchment."
    },
    {
        "gloss": "AFFIDAVIT",
        "en": "Sworn Affidavit / Legal Oath",
        "hi": "शपथ पत्र / हलफनामा",
        "ta": "உறுதிமொழிப் பத்திரம்",
        "category": "civic",
        "description": "Raise right hand in solemn oath, press thumb signature on legal stamp paper."
    },
    {
        "gloss": "NOTARY_PUBLIC",
        "en": "Notary Public / Attestation Seal",
        "hi": "नोटरी पब्लिक / सत्यापन अधिकारी",
        "ta": "நோட்டரி பப்ளிக்",
        "category": "civic",
        "description": "Emboss red circular notary seal and sign signature with gold stamp."
    },
    {
        "gloss": "GAZETTED_OFFICER",
        "en": "Gazetted Officer / Class-I Civil Authority",
        "hi": "राजपत्रित अधिकारी",
        "ta": "அரசிதழ் பதிவு பெற்ற அதிகாரி",
        "category": "civic",
        "description": "Class one shoulder pin gesture followed by signature verification stamp."
    },
    {
        "gloss": "HUMAN_RIGHTS_COMMISSION",
        "en": "National Human Rights Commission / NHRC",
        "hi": "राष्ट्रीय मानवाधिकार आयोग",
        "ta": "தேசிய மனித உரிமைகள் ஆணையம்",
        "category": "civic",
        "description": "Open hand protecting human figure silhouette under equal justice balance."
    },
    {
        "gloss": "DISABILITY_COMMISSION",
        "en": "Chief Commissioner for Persons with Disabilities",
        "hi": "दिव्यांगजन मुख्य आयुक्त",
        "ta": "மாற்றுத்திறனாளிகளுக்கான தலைமை ஆணையர்",
        "category": "civic",
        "description": "Accessibility wheel icon combined with commissioner crest of protection."
    },
    {
        "gloss": "RPWD_ACT_2016",
        "en": "Rights of Persons with Disabilities Act 2016",
        "hi": "दिव्यांगजन अधिकार अधिनियम 2016",
        "ta": "மாற்றுத்திறனாளிகள் உரிமைச் சட்டம் 2016",
        "category": "civic",
        "description": "Sign 2-1 disability categories shield, followed by binding statutory act law sign."
    },
    {
        "gloss": "NEP_2020",
        "en": "National Education Policy 2020 / ISL Inclusion",
        "hi": "राष्ट्रीय शिक्षा नीति 2020",
        "ta": "தேசிய கல்விக் கொள்கை 2020",
        "category": "academic",
        "description": "Fingerspell N-E-P, sign ISL language medium inclusion in NCERT school curriculum."
    },
    {
        "gloss": "ACCESSIBILITY_INDIA",
        "en": "Accessible India Campaign / Sugamya Bharat",
        "hi": "सुगम्य भारत अभियान",
        "ta": "அணுகக்கூடிய இந்தியா இயக்கம்",
        "category": "civic",
        "description": "Barrier removed by two parting hands creating open ramp and tactile path for all."
    },
    {
        "gloss": "SIGN_INTERPRETER",
        "en": "Certified Sign Language Interpreter / ISLRTC",
        "hi": "प्रमाणित सांकेतिक दुभाषिया",
        "ta": "சைகை மொழி மொழிபெயர்ப்பாளர்",
        "category": "meta",
        "description": "Both hands relaying message smoothly back and forth between speaker and deaf viewer."
    },
    {
        "gloss": "HEARING_IMPAIRMENT",
        "en": "Deaf / Hearing Impairment / Divyang",
        "hi": "बधिर / मूक-बधिर / दिव्यांगजन",
        "ta": "செவித்திறன் குறைபாடு / செவி மாற்றுத்திறனாளி",
        "category": "meta",
        "description": "Right index touches ear then mouth gently indicating deaf cultural identity."
    },
    {
        "gloss": "INCLUSION_POLICY",
        "en": "Inclusive Education & Universal Access",
        "hi": "समावेशी नीति / सबका साथ",
        "ta": "உள்ளடக்கிய கொள்கை",
        "category": "academic",
        "description": "Both open hands gather everyone into unified central circle of equal opportunity."
    },
    {
        "gloss": "REPUBLIC_DAY",
        "en": "Republic Day / 26th January Parade",
        "hi": "गणतंत्र दिवस / 26 जनवरी",
        "ta": "குடியரசு தினம்",
        "category": "civic",
        "description": "Sign 2-6 January, salute at Rajpath parade with flypast tricolor smoke trail."
    },
    {
        "gloss": "INDEPENDENCE_DAY",
        "en": "Independence Day / 15th August Red Fort",
        "hi": "स्वतंत्रता दिवस / 15 अगस्त लाल किला",
        "ta": "சுதந்திர தினம்",
        "category": "civic",
        "description": "Sign 1-5 August, mime Prime Minister hoisting Tricolor atop Red Fort ramparts."
    },
    {
        "gloss": "GANDHI_JAYANTI",
        "en": "Gandhi Jayanti / 2nd October",
        "hi": "गांधी जयंती / 2 अक्टूबर",
        "ta": "காந்தி ஜெயந்தி",
        "category": "civic",
        "description": "Sign round spectacles with thumbs and index fingers, followed by spin charkha wheel."
    },
    {
        "gloss": "MARTYRS_DAY",
        "en": "Martyrs' Day / Shaheed Diwas",
        "hi": "शहीद दिवस",
        "ta": "தியாகிகள் தினம்",
        "category": "civic",
        "description": "Two minutes solemn silence salute, right fist over heart honoring national sacrifice."
    },
    {
        "gloss": "NATIONAL_ARCHIVES",
        "en": "National Archives of India / Historical Records",
        "hi": "भारतीय राष्ट्रीय अभिलेखागार",
        "ta": "இந்திய தேசிய ஆவணக் காப்பகம்",
        "category": "civic",
        "description": "Preserve ancient manuscripts in climate controlled vault with careful white glove gesture."
    },
    {
        "gloss": "NATIONAL_MUSEUM",
        "en": "National Museum / Archaeological Heritage",
        "hi": "राष्ट्रीय संग्रहालय",
        "ta": "தேசிய அருங்காட்சியகம்",
        "category": "civic",
        "description": "Glass showcase display gesture honoring Indus Valley dancing girl and historical artifacts."
    },
    {
        "gloss": "RASHTRAPATI_BHAVAN",
        "en": "Rashtrapati Bhavan / President's Estate",
        "hi": "राष्ट्रपति भवन",
        "ta": "ராஷ்டிரபதி பவன்",
        "category": "civic",
        "description": "Grand central dome trace with Mughal gardens and ceremonial forecourt."
    },
    {
        "gloss": "INDIA_GATE",
        "en": "India Gate / All India War Memorial",
        "hi": "इंडिया गेट",
        "ta": "இந்தியா கேட்",
        "category": "civic",
        "description": "Both hands trace massive triumphal memorial arch with Amar Jawan Jyoti eternal flame."
    },
    {
        "gloss": "AMRIT_MAHOTSAV",
        "en": "Azadi Ka Amrit Mahotsav / 75 Years Milestone",
        "hi": "आज़ादी का अमृत महोत्सव",
        "ta": "சுதந்திரத்தின் அமிர்தப் பெருவிழா",
        "category": "civic",
        "description": "Sign 7-5 celebration burst with national tricolor streamers flying across the sky."
    }
]
