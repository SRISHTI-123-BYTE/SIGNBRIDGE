"""
SignBridge Multilingual Grammar Synthesis & ISL Gloss Translation Engine
Translates continuous ISL gloss sequences into syntactically fluid English, Hindi, and Tamil,
and converts spoken/typed hearing input into canonical ISL gloss sequences with full word-boundary matching,
negation awareness, and multilingual support.
"""

import re
from typing import Dict, List, Any, Optional, Tuple

try:
    from extended_vocabulary import EXTENDED_ISL_LEXICON
except ImportError:
    try:
        from backend.extended_vocabulary import EXTENDED_ISL_LEXICON
    except ImportError:
        EXTENDED_ISL_LEXICON = {}


class GrammarEngine:
    """
    Multilingual bidirectional translation engine between Indian Sign Language (ISL) glosses
    and natural spoken languages (English, Hindi, Tamil) with topic-comment reordering.
    """

    def __init__(self):
        # 1. Canonical Emergency, Civic & Healthcare Scenarios
        self.exact_phrases = {
            ("DOCTOR", "CHEST", "PAIN", "SEVERE"): {
                "en": "Doctor, I am experiencing severe chest pain.",
                "hi": "डॉक्टर, मुझे सीने में बहुत तेज़ दर्द हो रहा है।",
                "ta": "மருத்துவரே, எனக்கு கடுமையான மார்பு வலி உள்ளது."
            },
            ("CHEST", "PAIN", "SEVERE"): {
                "en": "I have severe chest pain.",
                "hi": "मुझे सीने में गंभीर दर्द है।",
                "ta": "எனக்கு கடுமையான மார்பு வலி உள்ளது."
            },
            ("POLICE", "STATION", "WHERE"): {
                "en": "Where is the nearest police station?",
                "hi": "निकटतम पुलिस स्टेशन कहाँ है?",
                "ta": "அருகிலுள்ள காவல் நிலையம் எங்கே இருக்கிறது?"
            },
            ("POLICE", "WHERE"): {
                "en": "Where is the police officer?",
                "hi": "पुलिस कहाँ है?",
                "ta": "காவல் எங்கே இருக்கிறது?"
            },
            ("HOSPITAL", "GO", "HOW"): {
                "en": "How do I get to the hospital?",
                "hi": "अस्पताल कैसे जाना है?",
                "ta": "மருத்துவமனைக்கு எப்படி செல்வது?"
            },
            ("HOSPITAL", "WHERE"): {
                "en": "Where is the hospital located?",
                "hi": "अस्पताल कहाँ है?",
                "ta": "மருத்துவமனை எங்கே உள்ளது?"
            },
            ("SIT", "WAIT", "10", "MINUTES"): {
                "en": "Please sit down and wait for 10 minutes.",
                "hi": "कृपया बैठ जाएं और 10 मिनट प्रतीक्षा करें।",
                "ta": "தயவுசெய்து அமர்ந்து 10 நிமிடங்கள் காத்திருங்கள்."
            },
            ("SIT", "WAIT"): {
                "en": "Please sit down and wait.",
                "hi": "कृपया बैठें और प्रतीक्षा करें।",
                "ta": "தயவுசெய்து அமர்ந்து காத்திருங்கள்."
            },
            ("HELP", "ME", "PLEASE"): {
                "en": "Please help me.",
                "hi": "कृपया मेरी मदद करें।",
                "ta": "தயவுசெய்து எனக்கு உதவுங்கள்."
            },
            ("HELP", "ME"): {
                "en": "Help me, please.",
                "hi": "मेरी मदद कीजिए।",
                "ta": "எனக்கு உதவுங்கள்."
            },
            ("MEDICINE", "TIME", "WHAT"): {
                "en": "What is the time for medicine?",
                "hi": "दवा लेने का क्या समय है?",
                "ta": "மருந்து சாப்பிடும் நேரம் என்ன?"
            },
            ("NAME", "YOUR", "WHAT"): {
                "en": "What is your name?",
                "hi": "आपका नाम क्या है?",
                "ta": "உங்கள் பெயர் என்ன?"
            },
            ("FEVER", "BREATHING", "PROBLEM"): {
                "en": "I have fever and breathing difficulty.",
                "hi": "मुझे बुखार और सांस लेने में तकलीफ है।",
                "ta": "எனக்கு காய்ச்சல் மற்றும் மூச்சுத் திணறல் உள்ளது."
            },
            ("CALL", "FAMILY", "EMERGENCY"): {
                "en": "Please call my family, this is an emergency!",
                "hi": "कृपया मेरे परिवार को फोन करें, यह आपातकाल है!",
                "ta": "தயவுசெய்து எனது குடும்பத்தினரை அழையுங்கள், இது அவசர நிலை!"
            },
            ("MONEY", "ACCOUNT", "BANK", "DEPOSIT"): {
                "en": "I want to deposit money into my bank account.",
                "hi": "मैं अपने बैंक खाते में पैसे जमा करना चाहता हूँ।",
                "ta": "நான் எனது வங்கிக் கணக்கில் பணம் டெபாசிட் செய்ய விரும்புகிறேன்."
            },
            ("MONEY", "BANK", "WITHDRAW"): {
                "en": "I want to withdraw money from the bank.",
                "hi": "मैं बैंक से पैसे निकालना चाहता हूँ।",
                "ta": "நான் வங்கியில் இருந்து பணம் எடுக்க விரும்புகிறேன்."
            },
            ("SIGN", "LANGUAGE", "INTERPRETER"): {
                "en": "Do you have a sign language interpreter?",
                "hi": "क्या आपके पास सांकेतिक भाषा दुभाषिया है?",
                "ta": "உங்களிடம் சைகை மொழி மொழிபெயர்ப்பாளர் இருக்கிறாரா?"
            },
            ("WATER", "NEED"): {
                "en": "I need drinking water.",
                "hi": "मुझे पीने का पानी चाहिए।",
                "ta": "எனக்கு குடிநீர் வேண்டும்."
            },
            ("THANK_YOU",): {
                "en": "Thank you very much.",
                "hi": "आपका बहुत-बहुत धन्यवाद।",
                "ta": "மிக்க நன்றி."
            },
            ("HELLO",): {
                "en": "Hello, greetings.",
                "hi": "नमस्ते, नमस्कार।",
                "ta": "வணக்கம்."
            },
            ("YES",): {
                "en": "Yes, understood.",
                "hi": "हाँ, समझ गया।",
                "ta": "ஆம், புரிந்தது."
            },
            ("NO",): {
                "en": "No, I do not agree.",
                "hi": "नहीं, मैं सहमत नहीं हूँ।",
                "ta": "இல்லை, நான் ஏற்கவில்லை."
            },
            ("HELP",): {
                "en": "Please help me!",
                "hi": "कृपया मेरी मदद करें!",
                "ta": "தயவுசெய்து எனக்கு உதவுங்கள்!"
            },
            ("PAIN",): {
                "en": "I am experiencing pain.",
                "hi": "मुझे दर्द हो रहा है।",
                "ta": "எனக்கு வலி இருக்கிறது."
            },
            ("HOSPITAL",): {
                "en": "Hospital.",
                "hi": "अस्पताल।",
                "ta": "மருத்துவமனை."
            },
            ("10",): {
                "en": "Ten minutes.",
                "hi": "10 मिनट।",
                "ta": "10 நிமிடங்கள்."
            },
            ("WATER",): {
                "en": "I need water.",
                "hi": "मुझे पानी चाहिए।",
                "ta": "எனக்கு தண்ணீர் வேண்டும்."
            },
            ("POLICE",): {
                "en": "Police.",
                "hi": "पुलिस।",
                "ta": "காவல்."
            },
            ("DOCTOR",): {
                "en": "Doctor.",
                "hi": "डॉक्टर।",
                "ta": "மருத்துவர்."
            },
            ("EMERGENCY",): {
                "en": "This is an emergency!",
                "hi": "यह आपातकाल है!",
                "ta": "இது ஒரு அவசர நிலை!"
            },
            ("BANK", "CARD"): {
                "en": "Please provide your bank card.",
                "hi": "कृपया अपना बैंक कार्ड दें।",
                "ta": "தயவுசெய்து உங்கள் வங்கிக் கார்டை வழங்கவும்."
            },
            ("FOOD", "NEED"): {
                "en": "I need food to eat.",
                "hi": "मुझे खाने के लिए भोजन चाहिए।",
                "ta": "எனக்கு உணவு வேண்டும்."
            },
            ("FOOD",): {
                "en": "Food and meal.",
                "hi": "भोजन और खाना।",
                "ta": "உணவு."
            },
            ("STOP",): {
                "en": "Please stop here.",
                "hi": "कृपया यहाँ रुकिए।",
                "ta": "தயவுசெய்து இங்கே நிறுத்துங்கள்."
            },
            ("COME",): {
                "en": "Please come here.",
                "hi": "कृपया यहाँ आइए।",
                "ta": "தயவுசெய்து இங்கே வாருங்கள்."
            },
            ("SCHOOL", "GO"): {
                "en": "I am going to school.",
                "hi": "मैं स्कूल जा रहा हूँ।",
                "ta": "நான் பள்ளிக்குச் செல்கிறேன்."
            },
            ("TEACHER", "WHERE"): {
                "en": "Where is the teacher?",
                "hi": "शिक्षक कहाँ हैं?",
                "ta": "ஆசிரியர் எங்கே இருக்கிறார்?"
            },
            ("STUDENT", "LEARN"): {
                "en": "The student is learning.",
                "hi": "छात्र सीख रहा है।",
                "ta": "மாணவர் கற்றுக்கொள்கிறார்."
            },
            ("LEARN", "SIGN", "LANGUAGE"): {
                "en": "I want to learn Indian Sign Language.",
                "hi": "मैं भारतीय सांकेतिक भाषा सीखना चाहता हूँ।",
                "ta": "நான் இந்திய சைகை மொழியைக் கற்க விரும்புகிறேன்."
            },
            ("SLEEP", "NEED"): {
                "en": "I am tired and need to sleep.",
                "hi": "मैं थक गया हूँ और मुझे सोना है।",
                "ta": "நான் சோர்வாக இருக்கிறேன், எனக்கு தூக்கம் தேவை."
            },
            ("SLEEP",): {
                "en": "Sleep and rest.",
                "hi": "सोना और आराम।",
                "ta": "தூக்கம் மற்றும் ஓய்வு."
            }
        }

        # 2. ISL Vocabulary Dictionary with Syntactic Parts of Speech
        self.gloss_dict = {
            "DOCTOR": {"en": "doctor", "hi": "डॉक्टर", "ta": "மருத்துவர்", "pos": "NOUN"},
            "CHEST": {"en": "chest", "hi": "सीने में", "ta": "மார்பில்", "pos": "NOUN"},
            "PAIN": {"en": "pain", "hi": "दर्द", "ta": "வலி", "pos": "NOUN"},
            "SEVERE": {"en": "severe", "hi": "गंभीर", "ta": "கடுமையான", "pos": "ADJECTIVE"},
            "POLICE": {"en": "police", "hi": "पुलिस", "ta": "காவல்", "pos": "NOUN"},
            "STATION": {"en": "station", "hi": "स्टेशन", "ta": "நிலையம்", "pos": "NOUN"},
            "WHERE": {"en": "where is", "hi": "कहाँ है", "ta": "எங்கே", "pos": "WH_INTERROGATIVE"},
            "HOSPITAL": {"en": "hospital", "hi": "अस्पताल", "ta": "மருத்துவமனை", "pos": "NOUN"},
            "GO": {"en": "go to", "hi": "जाना", "ta": "செல்வது", "pos": "VERB"},
            "HOW": {"en": "how to", "hi": "कैसे", "ta": "எப்படி", "pos": "WH_INTERROGATIVE"},
            "SIT": {"en": "sit down", "hi": "बैठें", "ta": "அமருங்கள்", "pos": "VERB"},
            "WAIT": {"en": "wait", "hi": "प्रतीक्षा करें", "ta": "காத்திருங்கள்", "pos": "VERB"},
            "10": {"en": "10", "hi": "10", "ta": "10", "pos": "NUMERAL"},
            "MINUTES": {"en": "minutes", "hi": "मिनट", "ta": "நிமிடங்கள்", "pos": "NOUN"},
            "HELP": {"en": "help", "hi": "मदद", "ta": "உதவி", "pos": "VERB"},
            "ME": {"en": "I", "hi": "मुझे", "ta": "எனக்கு", "pos": "PRONOUN"},
            "PLEASE": {"en": "please", "hi": "कृपया", "ta": "தயவுசெய்து", "pos": "POLITE_MARKER"},
            "MEDICINE": {"en": "medicine", "hi": "दवाई", "ta": "மருந்து", "pos": "NOUN"},
            "TIME": {"en": "time", "hi": "समय", "ta": "நேரம்", "pos": "NOUN"},
            "WHAT": {"en": "what is", "hi": "क्या है", "ta": "என்ன", "pos": "WH_INTERROGATIVE"},
            "NAME": {"en": "name", "hi": "नाम", "ta": "பெயர்", "pos": "NOUN"},
            "YOUR": {"en": "your", "hi": "आपका", "ta": "உங்கள்", "pos": "POSSESSIVE"},
            "WATER": {"en": "water", "hi": "पानी", "ta": "தண்ணீர்", "pos": "NOUN"},
            "NEED": {"en": "need", "hi": "चाहिए", "ta": "வேண்டும்", "pos": "VERB"},
            "EMERGENCY": {"en": "emergency", "hi": "आपातकाल", "ta": "அவசர நிலை", "pos": "NOUN"},
            "FEVER": {"en": "fever", "hi": "बुखार", "ta": "காய்ச்சல்", "pos": "NOUN"},
            "BREATHING": {"en": "breathing", "hi": "सांस", "ta": "சுவாசம்", "pos": "NOUN"},
            "PROBLEM": {"en": "problem", "hi": "समस्या", "ta": "பிரச்சினை", "pos": "NOUN"},
            "CALL": {"en": "call", "hi": "फोन करें", "ta": "அழையுங்கள்", "pos": "VERB"},
            "FAMILY": {"en": "family", "hi": "परिवार", "ta": "குடும்பம்", "pos": "NOUN"},
            "MONEY": {"en": "money", "hi": "पैसे", "ta": "பணம்", "pos": "NOUN"},
            "ACCOUNT": {"en": "account", "hi": "खाता", "ta": "கணக்கு", "pos": "NOUN"},
            "BANK": {"en": "bank", "hi": "बैंक", "ta": "வங்கி", "pos": "NOUN"},
            "DEPOSIT": {"en": "deposit", "hi": "जमा करें", "ta": "டெபாசிட் செய்யுங்கள்", "pos": "VERB"},
            "WITHDRAW": {"en": "withdraw", "hi": "निकासी करें", "ta": "பணம் எடுங்கள்", "pos": "VERB"},
            "SIGN": {"en": "sign", "hi": "सांकेतिक", "ta": "சைகை", "pos": "NOUN"},
            "LANGUAGE": {"en": "language", "hi": "भाषा", "ta": "மொழி", "pos": "NOUN"},
            "INTERPRETER": {"en": "interpreter", "hi": "दुभाषिया", "ta": "மொழிபெயர்ப்பாளர்", "pos": "NOUN"},
            "CARD": {"en": "card", "hi": "कार्ड", "ta": "கார்டு", "pos": "NOUN"},
            "COME": {"en": "come", "hi": "आइए", "ta": "வாருங்கள்", "pos": "VERB"},
            "STOP": {"en": "stop", "hi": "रुकिए", "ta": "நிறுத்துங்கள்", "pos": "VERB"},
            "LEARN": {"en": "learn", "hi": "सीखना", "ta": "கற்பது", "pos": "VERB"},
            "TEACHER": {"en": "teacher", "hi": "शिक्षक", "ta": "ஆசிரியர்", "pos": "NOUN"},
            "STUDENT": {"en": "student", "hi": "छात्र", "ta": "மாணவர்", "pos": "NOUN"},
            "SCHOOL": {"en": "school", "hi": "स्कूल", "ta": "பள்ளி", "pos": "NOUN"},
            "FOOD": {"en": "food", "hi": "भोजन", "ta": "உணவு", "pos": "NOUN"},
            "SLEEP": {"en": "sleep", "hi": "सोना", "ta": "தூக்கம்", "pos": "VERB"},
            "YES": {"en": "Yes", "hi": "हाँ", "ta": "ஆம்", "pos": "RESPONSE"},
            "NO": {"en": "No", "hi": "नहीं", "ta": "இல்லை", "pos": "RESPONSE"},
            "HELLO": {"en": "Hello", "hi": "नमस्ते", "ta": "வணக்கம்", "pos": "GREETING"},
            "THANK_YOU": {"en": "Thank you", "hi": "धन्यवाद", "ta": "நன்றி", "pos": "COURTESY"}
        }

        # Update with full 281 AI-Ready standard lexicon
        if EXTENDED_ISL_LEXICON:
            self.gloss_dict.update(EXTENDED_ISL_LEXICON)

        # Multilingual keyword lookup maps for speech-to-sign parsing
        self._build_multilingual_lexicon()

    def _build_multilingual_lexicon(self):
        """Constructs exact word-boundary keyword mapping across English, Hindi, and Tamil."""
        self.multilingual_keywords = {
            # English mappings
            "doctor": "DOCTOR", "dr": "DOCTOR", "doc": "DOCTOR", "physician": "DOCTOR",
            "chest": "CHEST",
            "pain": "PAIN", "ache": "PAIN", "hurting": "PAIN", "hurt": "PAIN",
            "severe": "SEVERE", "intense": "SEVERE", "sharp": "SEVERE",
            "police": "POLICE", "cop": "POLICE",
            "station": "STATION",
            "where": "WHERE", "location": "WHERE",
            "hospital": "HOSPITAL", "clinic": "HOSPITAL",
            "go": "GO", "reach": "GO",
            "how": "HOW",
            "sit": "SIT", "seated": "SIT",
            "wait": "WAIT", "waiting": "WAIT",
            "10": "10", "ten": "10",
            "minutes": "MINUTES", "minute": "MINUTES", "mins": "MINUTES",
            "help": "HELP", "assist": "HELP", "assistance": "HELP",
            "me": "ME", "my": "ME", "i": "ME",
            "please": "PLEASE", "kindly": "PLEASE",
            "medicine": "MEDICINE", "medication": "MEDICINE", "pills": "MEDICINE", "tablets": "MEDICINE",
            "time": "TIME", "clock": "TIME",
            "what": "WHAT",
            "name": "NAME",
            "your": "YOUR", "you": "YOUR",
            "yes": "YES", "yeah": "YES", "yep": "YES",
            "no": "NO", "nope": "NO",
            "thank": "THANK_YOU", "thanks": "THANK_YOU",
            "hello": "HELLO", "hi": "HELLO", "hey": "HELLO",
            "water": "WATER", "drink": "WATER",
            "need": "NEED", "want": "NEED", "require": "NEED",
            "emergency": "EMERGENCY", "urgent": "EMERGENCY",
            "fever": "FEVER", "temperature": "FEVER",
            "breathing": "BREATHING", "breath": "BREATHING",
            "problem": "PROBLEM", "trouble": "PROBLEM", "issue": "PROBLEM",
            "call": "CALL", "phone": "CALL", "ring": "CALL",
            "family": "FAMILY", "relatives": "FAMILY",
            "money": "MONEY", "cash": "MONEY", "rupees": "MONEY",
            "account": "ACCOUNT",
            "bank": "BANK",
            "deposit": "DEPOSIT",
            "withdraw": "WITHDRAW",
            "sign": "SIGN",
            "language": "LANGUAGE",
            "interpreter": "INTERPRETER", "translator": "INTERPRETER",
            "card": "CARD", "atm": "CARD", "debit": "CARD", "credit": "CARD",
            "come": "COME", "approach": "COME",
            "stop": "STOP", "halt": "STOP",
            "learn": "LEARN", "study": "LEARN", "studying": "LEARN",
            "teacher": "TEACHER", "instructor": "TEACHER", "professor": "TEACHER",
            "student": "STUDENT", "pupil": "STUDENT",
            "school": "SCHOOL", "college": "SCHOOL", "classroom": "SCHOOL",
            "food": "FOOD", "eat": "FOOD", "meal": "FOOD", "eating": "FOOD",
            "sleep": "SLEEP", "rest": "SLEEP", "sleeping": "SLEEP",

            # Hindi mappings
            "डॉक्टर": "DOCTOR", "चिकित्सक": "DOCTOR",
            "सीना": "CHEST", "सीने": "CHEST",
            "दर्द": "PAIN", "तकलीफ": "PAIN",
            "गंभीर": "SEVERE", "तेज": "SEVERE",
            "पुलिस": "POLICE",
            "स्टेशन": "STATION", "थाना": "STATION",
            "कहाँ": "WHERE", "किधर": "WHERE",
            "अस्पताल": "HOSPITAL",
            "जाना": "GO", "जाएं": "GO",
            "कैसे": "HOW",
            "बैठें": "SIT", "बैठिए": "SIT", "बैठ": "SIT",
            "रुकिए": "WAIT", "प्रतीक्षा": "WAIT", "इंतजार": "WAIT",
            "दस": "10",
            "मिनट": "MINUTES",
            "मदद": "HELP", "सहायता": "HELP",
            "मुझे": "ME", "मेरी": "ME", "मैं": "ME",
            "कृपया": "PLEASE",
            "दवा": "MEDICINE", "दवाई": "MEDICINE",
            "समय": "TIME", "वक्त": "TIME",
            "क्या": "WHAT",
            "नाम": "NAME",
            "आपका": "YOUR", "तुम्हारा": "YOUR", "आप": "YOUR",
            "हाँ": "YES",
            "नहीं": "NO",
            "धन्यवाद": "THANK_YOU", "शुक्रिया": "THANK_YOU",
            "नमस्ते": "HELLO", "नमस्कार": "HELLO", "हैलो": "HELLO",
            "पानी": "WATER",
            "चाहिए": "NEED", "जरूरत": "NEED",
            "आपातकाल": "EMERGENCY",
            "बुखार": "FEVER",
            "सांस": "BREATHING",
            "कार्ड": "CARD", "एटीएम": "CARD",
            "आइए": "COME", "आओ": "COME", "आना": "COME",
            "रुकिए": "STOP", "रुको": "STOP", "रोकिए": "STOP",
            "सीखना": "LEARN", "पढ़ना": "LEARN", "सीखिए": "LEARN",
            "शिक्षक": "TEACHER", "अध्यापक": "TEACHER", "गुरु": "TEACHER",
            "छात्र": "STUDENT", "विद्यार्थी": "STUDENT",
            "स्कूल": "SCHOOL", "विद्यालय": "SCHOOL",
            "भोजन": "FOOD", "खाना": "FOOD", "आहार": "FOOD",
            "सोना": "SLEEP", "नींद": "SLEEP", "आराम": "SLEEP",
            "समस्या": "PROBLEM", "दिक्कत": "PROBLEM",
            "फोन": "CALL", "कॉल": "CALL",
            "परिवार": "FAMILY",
            "पैसे": "MONEY", "रुपये": "MONEY",
            "खाता": "ACCOUNT",
            "बैंक": "BANK",
            "जमा": "DEPOSIT",
            "निकासी": "WITHDRAW", "निकालना": "WITHDRAW",
            "सांकेतिक": "SIGN",
            "भाषा": "LANGUAGE",
            "दुभाषिया": "INTERPRETER",

            # Tamil mappings
            "மருத்துவர்": "DOCTOR",
            "மார்பு": "CHEST",
            "வலி": "PAIN",
            "கடுமையான": "SEVERE",
            "காவல்": "POLICE",
            "நிலையம்": "STATION",
            "எங்கே": "WHERE",
            "மருத்துவமனை": "HOSPITAL",
            "செல்வது": "GO", "போ": "GO",
            "எப்படி": "HOW",
            "அமருங்கள்": "SIT", "உட்காருங்கள்": "SIT",
            "காத்திருங்கள்": "WAIT",
            "பத்து": "10",
            "நிமிடம்": "MINUTES", "நிமிடங்கள்": "MINUTES",
            "உதவி": "HELP",
            "எனக்கு": "ME", "நான்": "ME",
            "தயவுசெய்து": "PLEASE",
            "மருந்து": "MEDICINE",
            "நேரம்": "TIME",
            "என்ன": "WHAT",
            "பெயர்": "NAME",
            "உங்கள்": "YOUR", "நீ": "YOUR",
            "ஆம்": "YES",
            "இல்லை": "NO",
            "நன்றி": "THANK_YOU",
            "வணக்கம்": "HELLO",
            "தண்ணீர்": "WATER",
            "வேண்டும்": "NEED",
            "அவசர": "EMERGENCY",
            "காய்ச்சல்": "FEVER",
            "சுவாசம்": "BREATHING",
            "பிரச்சினை": "PROBLEM",
            "அழையுங்கள்": "CALL",
            "குடும்பம்": "FAMILY",
            "பணம்": "MONEY",
            "கணக்கு": "ACCOUNT",
            "வங்கி": "BANK",
            "டெபாசிட்": "DEPOSIT",
            "எடுங்கள்": "WITHDRAW",
            "சைகை": "SIGN",
            "மொழி": "LANGUAGE",
            "மொழிபெயர்ப்பாளர்": "INTERPRETER"
        }

        # Dynamically extend keywords from gloss_dict
        for gloss, entry in self.gloss_dict.items():
            en_w = entry.get("en", "").lower().strip()
            if en_w and en_w not in self.multilingual_keywords:
                self.multilingual_keywords[en_w] = gloss
            hi_w = entry.get("hi", "").strip()
            if hi_w and hi_w not in self.multilingual_keywords:
                self.multilingual_keywords[hi_w] = gloss
            ta_w = entry.get("ta", "").strip()
            if ta_w and ta_w not in self.multilingual_keywords:
                self.multilingual_keywords[ta_w] = gloss

        # Negation tokens across languages
        self.negation_tokens = {
            "no", "not", "dont", "don't", "never", "without", "none", "neither",
            "नहीं", "ना", "मत", "बिना", "बगैर",
            "இல்லை", "வேண்டாம்", "கூடாது"
        }

    def speech_to_isl_glosses(self, spoken_text: str, source_language: str = "en") -> List[Dict[str, Any]]:
        """
        Tokenizes hearing speech/text using exact word-boundary regex matching,
        negation detection, and multilingual vocabulary mapping.
        """
        if not spoken_text or not spoken_text.strip():
            return []

        # Extract words using Unicode-aware word boundaries
        raw_words = re.findall(r'[\w\u0900-\u097F\u0B80-\u0BFF]+', spoken_text.lower())
        if not raw_words:
            return []

        # Check for negation in the sentence
        has_negation = any(w in self.negation_tokens for w in raw_words)

        # Identify ordered glosses matching recognized vocabulary words
        matched_glosses: List[str] = []
        i = 0
        while i < len(raw_words):
            w = raw_words[i]

            # Compound checks (e.g. "thank you", "chest pain", "police station")
            if i + 1 < len(raw_words):
                two_word = f"{w} {raw_words[i+1]}"
                if two_word in ["thank you", "thanks you"]:
                    matched_glosses.append("THANK_YOU")
                    i += 2
                    continue
                if two_word in ["chest pain", "सीने में दर्द", "மார்பு வலி"]:
                    if not has_negation:
                        matched_glosses.extend(["CHEST", "PAIN"])
                    i += 2
                    continue
                if two_word in ["police station", "थाना"]:
                    matched_glosses.extend(["POLICE", "STATION"])
                    i += 2
                    continue

            # Skip negation tokens from emitting as positive signs
            if w in self.negation_tokens:
                # If isolated standalone "no" / "नहीं"
                if len(raw_words) <= 2:
                    matched_glosses.append("NO")
                i += 1
                continue

            # Look up single word in multilingual lexicon
            gloss = self.multilingual_keywords.get(w)
            if gloss:
                # If sentence has negation and word is a symptom like pain or fever, do not hallucinate severe pain
                if has_negation and gloss in ["PAIN", "FEVER", "SEVERE", "PROBLEM"]:
                    pass
                else:
                    if not matched_glosses or matched_glosses[-1] != gloss:
                        matched_glosses.append(gloss)
            i += 1

        # Format output tokens for animation rig
        result = []
        for g in matched_glosses:
            dur = 1200 if g in ["DOCTOR", "POLICE", "HOSPITAL", "EMERGENCY"] else 1000
            result.append({"gloss": g, "duration_ms": dur})

        return result

    def translate_gloss_sequence(self, glosses: List[str], nmm_affect: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Translates a list of continuous ISL Gloss tokens into grammatically fluid English, Hindi, and Tamil.
        Supports exact phrase matching, sub-phrase composition with surrounding token preservation,
        and dynamic SOV syntax trees.
        """
        if not glosses:
            return {
                "gloss_sequence": [],
                "translations": {"en": "", "hi": "", "ta": ""},
                "sentence_type": "EMPTY",
                "grammar_alignment": []
            }

        # Normalize and remove consecutive duplicate glosses
        filtered = [g.strip().upper() for g in glosses if g.strip() and g.strip() != "<BLANK>"]
        dedup = []
        for g in filtered:
            if not dedup or dedup[-1] != g:
                dedup.append(g)
        clean_glosses = tuple(dedup)

        if not clean_glosses:
            return {
                "gloss_sequence": [],
                "translations": {"en": "", "hi": "", "ta": ""},
                "sentence_type": "EMPTY",
                "grammar_alignment": []
            }

        # 1. Exact canonical phrase lookup
        if clean_glosses in self.exact_phrases:
            res = self.exact_phrases[clean_glosses]
            return {
                "gloss_sequence": list(clean_glosses),
                "translations": {
                    "en": res["en"],
                    "hi": res["hi"],
                    "ta": res["ta"]
                },
                "sentence_type": "CANONICAL_PHRASE",
                "grammar_alignment": self._build_alignment(list(clean_glosses), res["en"])
            }

        # 2. Sub-phrase composition: Find largest matching sub-phrase and preserve surrounding prefix/suffix
        for key_len in range(len(clean_glosses) - 1, 1, -1):
            for start in range(len(clean_glosses) - key_len + 1):
                sub_key = clean_glosses[start:start + key_len]
                if sub_key in self.exact_phrases:
                    matched_res = self.exact_phrases[sub_key]
                    prefix_glosses = list(clean_glosses[:start])
                    suffix_glosses = list(clean_glosses[start + key_len:])

                    # Compose translations
                    en_parts = []
                    hi_parts = []
                    ta_parts = []

                    if prefix_glosses:
                        pre_trans = self._synthesize_dynamic_grammar(prefix_glosses, nmm_affect)
                        en_parts.append(pre_trans["translations"]["en"].rstrip(".!?"))
                        hi_parts.append(pre_trans["translations"]["hi"].rstrip("।!?"))
                        ta_parts.append(pre_trans["translations"]["ta"].rstrip(".!?"))

                    en_parts.append(matched_res["en"])
                    hi_parts.append(matched_res["hi"])
                    ta_parts.append(matched_res["ta"])

                    if suffix_glosses:
                        suf_trans = self._synthesize_dynamic_grammar(suffix_glosses, nmm_affect)
                        en_parts.append(suf_trans["translations"]["en"])
                        hi_parts.append(suf_trans["translations"]["hi"])
                        ta_parts.append(suf_trans["translations"]["ta"])

                    en_text = " ".join(en_parts)
                    hi_text = " ".join(hi_parts)
                    ta_text = " ".join(ta_parts)

                    return {
                        "gloss_sequence": list(clean_glosses),
                        "translations": {
                            "en": en_text,
                            "hi": hi_text,
                            "ta": ta_text
                        },
                        "sentence_type": "COMPOSED_SUB_PHRASE",
                        "grammar_alignment": self._build_alignment(list(clean_glosses), en_text)
                    }

        # 3. Dynamic Rule-Based Syntax Reordering Engine (ISL Topic-Comment to SVO / SOV)
        return self._synthesize_dynamic_grammar(list(clean_glosses), nmm_affect)

    def _synthesize_dynamic_grammar(self, gloss_list: List[str], nmm_affect: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Reorders ISL Topic-Comment sequences into grammatical SVO (English) and SOV (Hindi, Tamil).
        Corrects subject pronouns ("ME NEED WATER" -> "I need water.").
        """
        is_question = bool(nmm_affect and nmm_affect.get("is_interrogative", False))
        is_urgent = bool(nmm_affect and nmm_affect.get("is_urgent", False))

        # Check for interrogatives in glosses
        if any(g in ["WHERE", "HOW", "WHAT"] for g in gloss_list):
            is_question = True

        # Special handling for single-word queries / requests
        if len(gloss_list) == 1:
            g = gloss_list[0]
            if g == "TIME":
                if is_question:
                    return {
                        "gloss_sequence": gloss_list,
                        "translations": {
                            "en": "What time is it?",
                            "hi": "समय क्या हुआ है?",
                            "ta": "நேரம் என்ன?"
                        },
                        "sentence_type": "INTERROGATIVE",
                        "grammar_alignment": self._build_alignment(gloss_list, "What time is it?")
                    }
                else:
                    return {
                        "gloss_sequence": gloss_list,
                        "translations": {
                            "en": "Time.",
                            "hi": "समय।",
                            "ta": "நேரம்."
                        },
                        "sentence_type": "SINGLE_TOKEN",
                        "grammar_alignment": self._build_alignment(gloss_list, "Time.")
                    }

        # Subject pronoun grammatical normalization for English
        # (ME at start of clause acts as subject "I")
        en_tokens = []
        for idx, g in enumerate(gloss_list):
            item = self.gloss_dict.get(g, {"en": g.lower(), "hi": g, "ta": g, "pos": "NOUN"})
            en_val = item["en"]
            if g == "ME":
                en_val = "I" if idx == 0 or (idx > 0 and gloss_list[idx - 1] in ["HELLO", "PLEASE"]) else "me"
            en_tokens.append(en_val)

        # English sentence construction
        en_raw = " ".join(en_tokens)
        if "where is" in en_raw.lower():
            topic = [w for w in en_tokens if "where is" not in w.lower()]
            en_text = f"Where is {' '.join(topic)}?"
        elif "how to" in en_raw.lower():
            topic = [w for w in en_tokens if "how to" not in w.lower()]
            en_text = f"How do I {' '.join(topic)}?"
        elif "what is" in en_raw.lower():
            topic = [w for w in en_tokens if "what is" not in w.lower()]
            en_text = f"What is {' '.join(topic)}?"
        else:
            en_text = en_raw.capitalize()
            if is_question:
                en_text += "?"
            elif is_urgent:
                en_text += "!"
            else:
                en_text += "."

        # Hindi SOV Syntax Construction (Subject + Object + Verb)
        hi_tokens = []
        verbs_hi = []
        for g in gloss_list:
            item = self.gloss_dict.get(g, {"hi": g, "pos": "NOUN"})
            if item.get("pos") == "VERB":
                verbs_hi.append(item["hi"])
            else:
                hi_tokens.append(item["hi"])
        # Place verbs at end for Hindi SOV order
        hi_ordered = hi_tokens + verbs_hi
        hi_text = " ".join(hi_ordered)
        if is_question and not hi_text.endswith("?"):
            hi_text += "?"
        elif not hi_text.endswith("।") and not hi_text.endswith("?"):
            hi_text += "।"

        # Tamil SOV Syntax Construction
        ta_tokens = []
        verbs_ta = []
        for g in gloss_list:
            item = self.gloss_dict.get(g, {"ta": g, "pos": "NOUN"})
            if item.get("pos") == "VERB":
                verbs_ta.append(item["ta"])
            else:
                ta_tokens.append(item["ta"])
        ta_ordered = ta_tokens + verbs_ta
        ta_text = " ".join(ta_ordered)
        if is_question and not ta_text.endswith("?"):
            ta_text += "?"
        elif not ta_text.endswith("."):
            ta_text += "."

        return {
            "gloss_sequence": gloss_list,
            "translations": {
                "en": en_text,
                "hi": hi_text,
                "ta": ta_text
            },
            "sentence_type": "DYNAMIC_REORDERED",
            "grammar_alignment": self._build_alignment(gloss_list, en_text)
        }

    def _build_alignment(self, glosses: List[str], translation: str) -> List[Dict[str, str]]:
        """
        Creates a side-by-side syntactic mapping showing how ISL gloss tokens
        correspond to words in the natural target sentence.
        """
        alignment = []
        for g in glosses:
            meaning = self.gloss_dict.get(g, {}).get("en", g.lower())
            alignment.append({
                "isl_gloss": g,
                "syntactic_role": self.gloss_dict.get(g, {}).get("pos", "TOKEN"),
                "spoken_word": meaning
            })
        return alignment
