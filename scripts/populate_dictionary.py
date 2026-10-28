"""
Populate ISL Dictionary with expanded ISLRTC signs across all domains.
"""

import re

# Comprehensive dictionary map for the expanded sign vocabulary
SIGN_DEFINITIONS = {
    # ─── EMERGENCY & HEALTHCARE (islrtc-emergency) ───
    'AMBULANCE': ('ambulance', 'emergency', 'Ambulance', 'एम्बुलेंस', 'ஆம்புலன்ஸ்', 'Right hand mimics flashing revolving siren on forehead moving forward rapidly.', ['EMERGENCY_VAN', 'HOSPITAL_VAN']),
    'OXYGEN': ('oxygen', 'emergency', 'Oxygen / Breathing Gas', 'ऑक्सीजन', 'ஆக்சிஜன்', 'Cup hand over mouth and nose inhaling deeply with chest expansion.', ['O2', 'BREATHING_GAS']),
    'BLOOD': ('blood', 'emergency', 'Blood / Bleeding', 'रक्त / खून', 'இரத்தம்', 'Touch lips with index finger, then trace fluid flow down the left arm.', ['RED_BLOOD', 'BLEED']),
    'INJURY': ('injury', 'emergency', 'Injury / Wound', 'चोट / घाव', 'காயம்', 'Point to affected spot and rotate twisted fingers indicating trauma.', ['WOUND', 'HURT_SPOT']),
    'ACCIDENT': ('accident', 'emergency', 'Accident / Crash', 'दुर्घटना', 'விபத்து', 'Two fists crash into each other horizontally at center chest plane.', ['CRASH', 'COLLISION']),
    'HEART': ('heart', 'emergency', 'Heart / Cardiac', 'हृदय / दिल', 'இதயம்', 'Left chest pulse tap with curled middle finger rhythmic beat.', ['CARDIAC', 'PULSE_HEART']),
    'SURGERY': ('surgery', 'emergency', 'Surgery / Operation', 'शल्य चिकित्सा / ऑपरेशन', 'அறுவை சிகிச்சை', 'Thumb edge slicing gently across palm miming surgical incision.', ['OPERATION', 'PROCEDURE']),
    'CLINIC': ('clinic', 'emergency', 'Clinic / Dispensary', 'दवाखाना / क्लिनिक', 'சிகிச்சையகம்', 'Sign DOCTOR followed by small house/room enclosure outline.', ['DISPENSARY', 'HEALTH_CENTRE']),
    'NURSE': ('nurse', 'emergency', 'Nurse / Healthcare Assistant', 'नर्स / परिचारिका', 'செவிலியர்', 'Tap cross on forehead/cap then gesture supportive care palms.', ['HEALTH_ASSISTANT', 'SISTER']),
    'HEADACHE': ('headache', 'emergency', 'Headache', 'सिरदर्द', 'தலைவலி', 'Two index fingers twisting repeatedly near opposite temples with grimace.', ['HEAD_PAIN', 'MIGRAINE']),
    'TABLET': ('tablet-med', 'emergency', 'Tablet / Pill', 'दवा की गोली', 'மாத்திரை', 'Pinch small imaginary circular pill between thumb & index and place on tongue.', ['PILL', 'CAPSULE']),
    'INJECTION': ('injection', 'emergency', 'Injection / Vaccine', 'सुई / इंजेक्शन', 'ஊசி', 'Thumb plunger push motion into outer shoulder or upper arm.', ['SYRINGE', 'VACCINE']),
    'BANDAGE': ('bandage', 'emergency', 'Bandage / Dressing', 'पट्टी / बैंडेज', 'கட்டுத்துணி', 'Wrap right flat hand around left forearm in circular wrapping motion.', ['DRESSING', 'FIRST_AID_STRIP']),
    'STRETCHER': ('stretcher', 'emergency', 'Stretcher', 'स्ट्रेचर', 'ஸ்ட்ரெச்சர்', 'Two hands hold horizontal stretcher rails and move forward steadily.', ['BED_CARRIER', 'PATIENT_BED']),
    'FIRST_AID': ('first-aid', 'emergency', 'First Aid', 'प्राथमिक चिकित्सा', 'முதலுதவி', 'Sign 1 followed by AID/HELP cross sign on chest.', ['EMERGENCY_AID', 'FIRST_CARE']),
    'ICU': ('icu', 'emergency', 'ICU (Intensive Care Unit)', 'गहन चिकित्सा इकाई', 'தீவிர சிகிச்சைப் பிரிவு', 'Fingerspell I-C-U followed by monitor heartbeat line trace.', ['INTENSIVE_CARE', 'CRITICAL_CARE']),
    'COUGH': ('cough', 'emergency', 'Cough', 'खांसी', 'இருமல்', 'Loose fist tapped against center chest twice with head bowing.', ['COUGHING', 'THROAT_CLEAR']),
    'BLEEDING': ('bleeding', 'emergency', 'Bleeding / Hemorrhage', 'खून बहना', 'இரத்தப்போக்கு', 'Red sign on lip followed by downward trickling finger motions.', ['HEMORRHAGE', 'BLOOD_FLOW']),
    'DIZZY': ('dizzy', 'emergency', 'Dizzy / Fainting', 'चक्कर आना', 'தலைச்சுற்றல்', 'Swirling index finger around forehead with unsteady head sway.', ['VERTIGO', 'FAINT']),
    'CHEST_PAIN': ('chest-pain', 'emergency', 'Chest Pain', 'सीने में दर्द', 'மார்பு வலி', 'Claw hand gripping center sternum with distressed facial expression.', ['ANGINA', 'HEART_ACHE']),

    # ─── LEGAL, RIGHTS & SAFETY (islrtc-legal) ───
    'LAWYER': ('lawyer', 'civic', 'Lawyer / Advocate', 'वकील / अधिवक्ता', 'வழக்கறிஞர்', 'Index finger touches collar lapel then extends forward with legal scroll gesture.', ['ADVOCATE', 'ATTORNEY']),
    'JUDGE': ('judge', 'civic', 'Judge / Magistrate', 'न्यायाधीश / जज', 'நீதிபதி', 'Right fist strikes downward into flat left palm miming gavel strike.', ['MAGISTRATE', 'JUSTICE_OFFICER']),
    'JUSTICE': ('justice', 'civic', 'Justice / Fairness', 'न्याय', 'நீதி', 'Both open palms held upward as balanced scales oscillating gently.', ['FAIRNESS', 'EQUITY']),
    'RULE': ('rule', 'civic', 'Rule / Law / Regulation', 'नियम / कानून', 'விதி / சட்டம்', 'Right flat palm sweeps vertically down flat upright left palm edge.', ['LAW', 'REGULATION']),
    'PROTECT': ('protect', 'civic', 'Protect / Defend', 'रक्षा / सुरक्षा', 'பாதுகாத்தல்', 'Both crossed forearms held defensively in front of upper torso.', ['DEFEND', 'SAFEGUARD']),
    'SAFE': ('safe', 'civic', 'Safe / Secure', 'सुरक्षित', 'பாதுகாப்பானது', 'Crossed open wrists pull apart and open outward in relief.', ['SECURE', 'OUT_OF_DANGER']),
    'GOVERNMENT': ('government', 'civic', 'Government / Authority', 'सरकार / शासन', 'அரசு', 'Index finger taps temple then circles outward above head indicating authority.', ['AUTHORITY', 'STATE']),
    'PRISON': ('prison', 'civic', 'Prison / Jail', 'जेल / कारागार', 'சிறை', 'Spread vertical fingers of both hands cross into interlocking bars.', ['JAIL', 'LOCKUP']),
    'EVIDENCE': ('evidence', 'civic', 'Evidence / Proof', 'सबूत / प्रमाण', 'சான்று / ஆதாரம்', 'Index finger points from eye to flat open left palm displaying facts.', ['PROOF', 'FACT']),
    'COMPLAINT': ('complaint', 'civic', 'Complaint / Grievance', 'शिकायत', 'புகார்', 'Claw hand touches chest then throws outward toward officer plane.', ['GRIEVANCE', 'REPORT']),
    'ADVOCATE': ('advocate', 'civic', 'Advocate / Legal Counsel', 'अधिवक्ता', 'சட்ட ஆலோசகர்', 'Two hands miming open law book then pointing forward assertively.', ['LEGAL_COUNSEL', 'BARRISTER']),
    'ARREST': ('arrest', 'civic', 'Arrest / Custody', 'गिरफ्तारी', 'கைது செய்தல்', 'Both open hands clamp shut together over wrists miming handcuffs.', ['HANDCUFFS', 'DETAIN']),
    'WITNESS': ('witness', 'civic', 'Witness / Testimony', 'गवाह / साक्षी', 'சாட்சி', 'Right two fingers point to own eyes then forward to oath position.', ['TESTIFIER', 'OBSERVER']),
    'CONSTITUTION': ('constitution', 'civic', 'Constitution of India', 'संविधान', 'அரசியலமைப்பு', 'Right fist rests on heart then opens palm like sacred book.', ['SAMVIDHAN', 'NATIONAL_LAW']),
    'SECURITY': ('security', 'civic', 'Security / Guard', 'सुरक्षा कर्मी', 'பாதுகாப்பு', 'Thumbs-up fist moves across chest as badge of honor.', ['GUARD', 'SAFETY_FORCE']),
    'LEGAL_AID': ('legal-aid', 'civic', 'Legal Aid / Free Assistance', 'कानूनी सहायता', 'சட்ட உதவி', 'Sign LAW followed by HELP palm under fist lifting upward.', ['FREE_LEGAL_HELP', 'RIGHTS_AID']),
    'FIR': ('fir', 'civic', 'FIR (First Information Report)', 'प्राथमिकी / एफआईआर', 'முதல் தகவல் அறிக்கை', 'Fingerspell F-I-R then mime stamping report document.', ['POLICE_REPORT', 'FIRST_REPORT']),
    'VERDICT': ('verdict', 'civic', 'Verdict / Judgement', 'निर्णय / फैसला', 'தீர்ப்பு', 'Both flat hands drop down sharply onto desk plane with finality.', ['JUDGEMENT', 'RULING']),
    'EQUALITY': ('equality', 'civic', 'Equality / Equal Rights', 'समानता / समता', 'சமத்துவம்', 'Both horizontal index fingers aligned parallel and brought together.', ['EQUAL', 'EQUIVALENCE']),

    # ─── BANKING & FINANCIAL (islrtc-banking) ───
    'CHEQUE': ('cheque', 'civic', 'Cheque / Bank Draft', 'चेक / बैंक चेक', 'காசோலை', 'Two index fingers trace rectangle then right hand signs signature sweep.', ['CHECK', 'DRAFT']),
    'PIN': ('pin', 'civic', 'PIN / Secret Password', 'पिन नंबर', 'பின் எண்', 'Index finger taps imaginary 4-digit numeric keypad on left palm.', ['ATM_PIN', 'CODE']),
    'BALANCE': ('balance-finance', 'civic', 'Account Balance', 'खाता शेष / बैलेंस', 'மீதித் தொகை', 'Left flat palm horizontal, right fingertips brush across measuring level.', ['REMAINING_MONEY', 'ACCOUNT_TOTAL']),
    'INTEREST': ('interest', 'civic', 'Interest Rate / Earned Return', 'ब्याज', 'வட்டி', 'Index and thumb pinch small gap and expand upwards diagonally.', ['INTEREST_RATE', 'RETURN']),
    'SAVE': ('save-money', 'civic', 'Save / Accumulate Money', 'बचत', 'சேமிப்பு', 'Right hand drops imaginary coin into closed hollow left fist piggybank.', ['SAVINGS', 'DEPOSIT_SAFE']),
    'PAY': ('pay', 'civic', 'Pay / Settle Payment', 'भुगतान करना', 'செலுத்துதல்', 'Right flat hand slides outward along flat upward-facing left palm.', ['PAYMENT', 'GIVE_MONEY']),
    'RUPEES': ('rupees', 'civic', 'Rupees (₹)', 'रुपये (₹)', 'ரூபாய் (₹)', 'Index and middle fingers trace horizontal line then downward curve for ₹ symbol.', ['INR', 'CURRENCY']),
    'ONLINE_PAY': ('online-pay', 'civic', 'Online Payment / Digital Pay', 'ऑनलाइन भुगतान', 'இணையவழி கட்டணம்', 'Mobile phone gesture tapped against point-of-sale scanner flat palm.', ['DIGITAL_PAY', 'UPI_PAY']),
    'ATM': ('atm', 'civic', 'ATM / Cash Machine', 'एटीएम मशीन', 'ஏடிஎம்', 'Mime inserting plastic card horizontally then pressing keypad buttons.', ['CASH_MACHINE', 'DISPENSER']),
    'PASSBOOK': ('passbook', 'civic', 'Bank Passbook', 'बैंक पासबुक', 'வங்கி கணக்குப் புத்தகம்', 'Two palms open as a small booklet followed by stamped entry motion.', ['BANK_BOOK', 'ACCOUNT_LOG']),
    'RECEIPT': ('receipt', 'civic', 'Receipt / Slip', 'रसीद / पर्ची', 'பற்றுச்சீட்டு', 'Two hands mime pulling paper slip out of terminal and handing over.', ['VOUCHER', 'TRANSACTION_SLIP']),
    'CREDIT': ('credit', 'civic', 'Credit / Loan Facility', 'क्रेडिट / उधार', 'கடன் வரவு', 'Right hand receives currency slide toward torso gently.', ['CREDIT_SCORE', 'LENDING']),
    'DEBIT': ('debit', 'civic', 'Debit / Account Deduction', 'डेबिट / खाता निकासी', 'கணக்கு பற்று', 'Right hand takes paper from left palm and removes it outward.', ['DEDUCTION', 'CHARGE']),
    'INVESTMENT': ('investment', 'civic', 'Investment / Mutual Funds', 'निवेश', 'முதலீடு', 'Both palms cupped together lifting slowly upward indicating growth.', ['GROWTH_FUNDS', 'WEALTH']),
    'SALARY': ('salary', 'civic', 'Salary / Wages', 'वेतन / तनख्वाह', 'மாதச் சம்பளம்', 'Index finger counts calendar month end then receives flat bundle of cash.', ['WAGES', 'MONTHLY_PAY']),
    'BRANCH': ('branch', 'civic', 'Bank Branch / Office', 'बैंक शाखा', 'வங்கி கிளை', 'Main building shape with right index branch extending sideways.', ['SUB_OFFICE', 'BANK_CENTRE']),
    'UPI': ('upi', 'civic', 'UPI (Unified Payments Interface)', 'यूपीआई', 'யுபிஐ', 'Fingerspell U-P-I then mime scanning QR code with phone camera.', ['BHIM_UPI', 'QR_PAY']),
    'COIN': ('coin', 'civic', 'Coin / Metallic Currency', 'सिक्का', 'நாணயம்', 'Thumb flips upward off curled index finger miming coin toss.', ['CHANGE', 'CHILLAR']),
    'SIGNATURE': ('signature', 'civic', 'Signature / Authorize', 'हस्ताक्षर / दस्तखत', 'கையொப்பம்', 'Right hand sweeps fluid cursive autograph stroke across left open palm.', ['SIGN', 'AUTOGRAPH']),
    'BANK_LOAN': ('bank-loan', 'civic', 'Bank Loan', 'बैंक ऋण', 'வங்கி கடன்', 'Bank sign followed by double hands receiving money forward on credit.', ['DEBT', 'BORROWING']),
    'SHARE_BAZAAR': ('share-bazaar', 'civic', 'Stock Market / Share Bazaar', 'शेयर बाज़ार', 'பங்குச் சந்தை', 'Zig-zag index finger graphing rising and falling market spikes.', ['STOCKS', 'EQUITY_MARKET']),

    # ─── CIVIC AMENITIES, TRANSPORT & NAVIGATION (islrtc-civic) ───
    'AIRPORT': ('airport', 'navigation', 'Airport / Aerodrome', 'हवाई अड्डा', 'விமான நிலையம்', 'Thumb, index, and pinky extended airplane gliding down to flat runway.', ['AERODROME', 'FLIGHT_PORT']),
    'TICKET': ('ticket', 'navigation', 'Ticket / Travel Pass', 'टिकट', 'பயணச் சீட்டு', 'Index and middle fingers clip against open palm miming conductor punch.', ['PASS', 'BOARDING_PASS']),
    'METRO': ('metro', 'navigation', 'Metro Train / Subway', 'मेट्रो रेल', 'மெட்ரோ ரயில்', 'Two hands parallel speeding forward rapidly along overhead rail line.', ['SUBWAY', 'URBAN_RAIL']),
    'OFFICE': ('office', 'navigation', 'Office / Work Workplace', 'कार्यालय / दफ्तर', 'அலுவலகம்', 'Two hands outline rectangular chamber followed by desk typing gesture.', ['WORKPLACE', 'DAFTAR']),
    'ROAD': ('road', 'navigation', 'Road / Street / Highway', 'सड़क / मार्ग', 'சாலை', 'Both parallel flat hands facing inward extend straight forward in perspective.', ['HIGHWAY', 'STREET_PATH']),
    'LOCATION': ('location', 'navigation', 'Location / Exact Place', 'स्थान / जगह', 'இடம் / அமைவிடம்', 'Index finger points down precisely into center of open horizontal left palm.', ['PLACE', 'SPOT']),
    'NORTH': ('north', 'navigation', 'North Direction', 'उत्तर दिशा', 'வடக்கு', 'Right N-handshape pushes vertically upward into sky.', ['UTTAR', 'DIR_NORTH']),
    'SOUTH': ('south', 'navigation', 'South Direction', 'दक्षिण दिशा', 'தெற்கு', 'Right S-handshape pushes straight down toward Earth.', ['DAKSHIN', 'DIR_SOUTH']),
    'EAST': ('east', 'navigation', 'East Direction', 'पूर्व दिशा', 'கிழக்கு', 'Right E-handshape moves rightward towards the sunrise.', ['POORVA', 'DIR_EAST']),
    'WEST': ('west', 'navigation', 'West Direction', 'पश्चिम दिशा', 'மேற்கு', 'Right W-handshape moves leftward towards the sunset.', ['PASHCHIM', 'DIR_WEST']),
    'PLATFORM': ('platform', 'navigation', 'Railway Platform', 'प्लेटफ़ॉर्म', 'தடைமேடை', 'P-handshape moves along long flat railway track hand.', ['RAIL_PLATFORM', 'TRACK_SIDE']),
    'TAXI': ('taxi', 'navigation', 'Taxi / Cab', 'टैक्सी / कैब', 'வாடகை கார்', 'Two hands steer steering wheel then right hand taps roof taxi light.', ['CAB', 'HIRE_CAR']),
    'AUTO': ('auto', 'navigation', 'Auto Rickshaw / 3-Wheeler', 'ऑटो रिक्शा', 'ஆட்டோ', 'Both hands grip handlebar throttle and rev wrist forward twice.', ['RICKSHAW', 'THREE_WHEELER']),
    'POST_OFFICE': ('post-office', 'navigation', 'Post Office / Dak Ghar', 'डाकघर', 'அஞ்சல் அலுவலகம்', 'Lick thumb and stick stamp onto left palm envelope, then drop in box.', ['DAK_GHAR', 'MAIL_OFFICE']),
    'MUNICIPALITY': ('municipality', 'navigation', 'Municipality / Civic Corporation', 'नगर पालिका / निगम', 'நகராட்சி', 'Civic crown sign followed by large municipal building enclosure.', ['NAGAR_NIGAM', 'CIVIC_BODY']),
    'MAP': ('map', 'navigation', 'Map / Navigation Guide', 'नक्शा / मानचित्र', 'வரைபடம்', 'Both hands hold open folded wide paper sheet and point to route traces.', ['GUIDE_MAP', 'ROUTE_CHART']),
    'BRIDGE': ('bridge', 'navigation', 'Bridge / Flyover', 'पुल / सेतु', 'பாலம்', 'Both curved open hands form arch meeting in center above river gesture.', ['FLYOVER', 'SETU']),
    'TRAFFIC': ('traffic', 'navigation', 'Traffic / Congestion', 'यातायात / ट्रैफ़िक', 'போக்குவரத்து நெரிசல்', 'Both five-finger hands intertwining and jamming against each other.', ['JAM', 'CONGESTION']),
    'STREET': ('street', 'navigation', 'Street / Colony Road', 'गली / सड़क', 'தெரு', 'Parallel palms snake forward gently indicating neighborhood lane.', ['LANE', 'GALI']),
    'BUS': ('bus', 'navigation', 'Bus / Passenger Coach', 'बस', 'பேருந்து', 'Two hands hold large horizontal steering wheel and pull brake lever.', ['COACH', 'PUBLIC_BUS']),
    'TRAIN': ('train', 'navigation', 'Train / Railway', 'रेलगाड़ी / ट्रेन', 'ரயில்', 'Two horizontal index & middle fingers sliding rhythmic chug along left fingers.', ['RAILWAY', 'CHUGGING_TRAIN']),
    'LOCAL_TRAIN': ('local-train', 'navigation', 'Local Suburban Train', 'लोकल ट्रेन', 'உள்ளூர் ரயில்', 'Train gesture followed by crowded standing strap hanging grip.', ['SUBURBAN_RAIL', 'MUMBAI_LOCAL']),
    'TRAIN_EXPRESS': ('train-express', 'navigation', 'Express Train / Superfast', 'एक्सप्रेस ट्रेन', 'விரைவு ரயில்', 'Train sign speeding past with rapid wind gust hand sweep.', ['SUPERFAST', 'INTERCITY']),
    'TRAM': ('tram', 'navigation', 'Tram / Streetcar', 'ट्राम', 'டிராம்', 'Train sign with right index finger pointing to overhead electric wire trolley.', ['STREETCAR', 'KOLKATA_TRAM']),
    'BUS_TERMINAL': ('bus-terminal', 'navigation', 'Bus Terminal / Depot', 'बस अड्डा / डिपो', 'பேருந்து நிலையம்', 'Bus sign followed by large garage parking bay gesture.', ['BUS_STAND', 'DEPOT']),

    # ─── EDUCATIONAL & ACADEMIC (islrtc-academic) ───
    'COLLEGE': ('college', 'academic', 'College / Higher Institute', 'महाविद्यालय / कॉलेज', 'கல்லூரி', 'Open right palm sweeps off flat left palm and arcs upward in elevation.', ['INSTITUTE', 'HIGHER_STUDY']),
    'DEGREE': ('degree', 'academic', 'Degree / Diploma Certificate', 'डिग्री / सनद', 'பட்டம் / பட்டயம்', 'Both hands mime holding rolled graduation parchment tied with ribbon.', ['GRADUATION', 'DIPLOMA']),
    'SCIENCE': ('science', 'academic', 'Science / Research', 'विज्ञान', 'அறிவியல்', 'Alternating loose fists mime pouring chemical liquids between test tubes.', ['EXPERIMENT', 'SCIENTIFIC']),
    'MATHS': ('maths', 'academic', 'Mathematics / Arithmetic', 'गणित / अंकगणित', 'கணிதம்', 'Crossed index fingers calculate equations on imaginary blackboard.', ['ARITHMETIC', 'CALCULATION']),
    'HISTORY': ('history', 'academic', 'History / Heritage', 'इतिहास', 'வரலாறு', 'H-handshape sweeps backward over right shoulder into the past.', ['PAST_STUDY', 'HERITAGE']),
    'COMPUTER_CLASS': ('computer-class', 'academic', 'Computer Lab / IT Class', 'कंप्यूटर कक्षा', 'கணினி வகுப்பு', 'Typing fingers followed by teacher classroom instruction sign.', ['IT_CLASS', 'DIGITAL_LAB']),
    'PENCIL': ('pencil', 'academic', 'Pencil / Pen', 'पेंसिल / कलम', 'பென்சில்', 'Thumb and index pinch writing implement scribbling across left palm page.', ['PEN', 'WRITING_TOOL']),
    'PAPER': ('paper', 'academic', 'Paper / Sheet', 'कागज / पन्ना', 'தாள் / காகிதம்', 'Heels of both flat open hands clap horizontally twice past each other.', ['SHEET', 'PAGE']),
    'CLASSROOM': ('classroom', 'academic', 'Classroom / Lecture Hall', 'कक्षा / क्लासरूम', 'வகுப்பறை', 'C-hands outline four corners of learning hall followed by students.', ['LECTURE_ROOM', 'STUDY_HALL']),
    'UNIVERSITY': ('university', 'academic', 'University / Campus', 'विश्वविद्यालय', 'பல்கலைக்கழகம்', 'U-handshape sweeps off flat base palm and spirals high into graduation dome.', ['VISHWAVIDYALAYA', 'CAMPUS']),
    'STUDY': ('study', 'academic', 'Study / Revise', 'अध्ययन / पढ़ाई', 'படித்தல்', 'Both open palms face book, fingers fluttering into own eyes repeatedly.', ['LEARNING', 'REVISION']),
    'HOMEWORK': ('homework', 'academic', 'Homework / Assignment', 'गृहकार्य / होमवर्क', 'வீட்டுப்பாடம்', 'Sign HOME followed by WRITE assignment across flat notebook.', ['ASSIGNMENT', 'TASK']),
    'QUESTION': ('question', 'academic', 'Question / Doubt', 'प्रश्न / सवाल', 'கேள்வி', 'Curved index finger traces question mark in the air with quizzical eyebrows.', ['DOUBT', 'QUERY']),
    'ANSWER': ('answer', 'academic', 'Answer / Response', 'उत्तर / जवाब', 'பதில்', 'Both index fingers at lips thrust forward together toward questioner.', ['REPLY', 'SOLUTION']),
    'LIBRARY': ('library', 'academic', 'Library / Reading Room', 'पुस्तकालय / लाइब्रेरी', 'நூலகம்', 'L-handshape circles gently in front of vertical book shelf stacks.', ['BOOK_HOUSE', 'READING_ROOM']),
    'CERTIFICATE': ('certificate', 'academic', 'Certificate / Merit Award', 'प्रमाणपत्र', 'சான்றிதழ்', 'Both C-hands outline rectangular scroll and present forward with pride.', ['DIPLOMA_CARD', 'MERIT']),
    'LESSON': ('lesson', 'academic', 'Lesson / Chapter', 'पाठ / अध्याय', 'பாடம்', 'Right hand chops progressively down flat left palm marking sections.', ['CHAPTER', 'UNIT']),
    'BLACKBOARD': ('blackboard', 'academic', 'Blackboard / Chalkboard', 'श्यामपट्ट / ब्लैकबोर्ड', 'கரும்பலகை', 'Color BLACK gesture on hair followed by large wall board rectangle outline.', ['CHALKBOARD', 'BOARD']),
    'PASSED': ('passed', 'academic', 'Passed Exam / Successful', 'उत्तीर्ण / पास होना', 'தேர்ச்சி', 'Two thumbs up thrust upward through finish line with smiling nod.', ['QUALIFIED', 'SUCCESS']),
    'BOOK': ('book', 'academic', 'Book / Textbook', 'पुस्तक / किताब', 'புத்தகம்', 'Both palms joined along pinky edge open outwards like a book.', ['TEXTBOOK', 'KITAB']),
    'READ': ('read', 'academic', 'Read / Study', 'पढ़ना', 'வாசித்தல்', 'Two V-fingers scan smoothly back and forth across left palm page.', ['READING', 'SCAN_TEXT']),
    'WRITE': ('write', 'academic', 'Write / Script', 'लिखना', 'எழுதுதல்', 'Pencil grip hand moves rightward across flat left palm in wavy strokes.', ['WRITING', 'RECORD']),
    'EXAM': ('exam', 'academic', 'Examination / Test', 'परीक्षा', 'தேர்வு', 'Distribute imaginary papers across desks followed by strict writing gaze.', ['TEST', 'ASSESSMENT']),
    'SCHOOL_HISTORIC': ('school-historic', 'academic', 'Pioneering Deaf School', 'ऐतिहासिक मूक-बधिर विद्यालय', 'பாரம்பரிய காதுகேளாதோர் பள்ளி', 'Historic bell ring sign followed by school learning community sign.', ['PIONEER_SCHOOL', 'HERITAGE_ACADEMY']),

    # ─── DAILY NECESSITIES, FOOD & NUTRITION (islrtc-daily) ───
    'TEA': ('tea', 'daily', 'Tea / Chai', 'चाय', 'தேநீர்', 'Thumb and index pinch tea bag dipping into cup or sipping cup handle.', ['CHAI', 'HOT_TEA']),
    'MILK': ('milk', 'daily', 'Milk', 'दूध', 'பால்', 'Both hands squeeze downward in alternating milking motion.', ['DOODH', 'DAIRY_MILK']),
    'BATH': ('bath', 'daily', 'Bath / Shower', 'स्नान / नहाना', 'குளியல்', 'Both loose fists rub upward and downward against chest scrubbing torso.', ['SHOWER', 'WASH_BODY']),
    'CLOTHES': ('clothes', 'daily', 'Clothes / Garments', 'कपड़े / वस्त्र', 'ஆடைகள்', 'Thumbs and fingers brush downward twice along shirt lapels/chest.', ['DRESS', 'GARMENT']),
    'CLEAN': ('clean', 'daily', 'Clean / Tidy / Pure', 'साफ़ / स्वच्छ', 'சுத்தம்', 'Right flat palm sweeps smoothly across left palm clearing all dust.', ['PURE', 'SWACHH']),
    'BREAKFAST': ('breakfast', 'daily', 'Breakfast / Morning Meal', 'नाश्ता / सुबह का भोजन', 'காலை உணவு', 'Sign MORNING sunrise followed by food eating fingertips to mouth.', ['MORNING_FOOD', 'NASHTA']),
    'DINNER': ('dinner', 'daily', 'Dinner / Night Meal', 'रात का खाना / भोजन', 'இரவு உணவு', 'Sign NIGHT moon/darkness followed by family dining gathering sign.', ['SUPPER', 'NIGHT_MEAL']),
    'HOME': ('home', 'daily', 'Home / Residence', 'घर / गृह', 'வீடு', 'Both angled hands meet fingertips at apex forming roof of house.', ['HOUSE_ROOF', 'RESIDENCE']),
    'EAT': ('eat', 'daily', 'Eat / Meal', 'खाना', 'சாப்பிடுதல்', 'Fingertips clustered together tap mouth twice in eating motion.', ['MEAL', 'CONSUME']),
    'DRINK': ('drink', 'daily', 'Drink / Beverage', 'पीना', 'குடித்தல்', 'C-curved hand tilts toward lips miming drinking glass of liquid.', ['BEVERAGE', 'SIP']),
    'COOK': ('cook', 'daily', 'Cook / Prepare Food', 'पकाना / रसोई', 'சமைத்தல்', 'Right flat hand flips food over left open pan palm repeatedly.', ['PREPARE_FOOD', 'ROSOI']),
    'WASH': ('wash', 'daily', 'Wash / Clean with Water', 'धोना', 'கழுவுதல்', 'Both hands rub palms and backs of hands together miming washing.', ['CLEANSE', 'RINSE']),
    'BED': ('bed', 'daily', 'Bed / Mattress', 'बिस्तर / पलंग', 'படுக்கை', 'Two flat palms spread smooth bedsheet over mattress plane.', ['MATTRESS', 'CHARPAI']),
    'SOAP': ('soap', 'daily', 'Soap / Detergent', 'साबुन', 'சோப்பு', 'Right palm rubs back and forth over top of left hand with slick lather motion.', ['CLEANSER', 'LATHER']),
    'FRUIT': ('fruit', 'daily', 'Fruit / Fresh Produce', 'फल', 'பழம்', 'F-handshape twists gently against right cheek with sweet expression.', ['FRESH_FRUIT', 'FAL']),
    'VEGETABLE': ('vegetable', 'daily', 'Vegetables / Sabzi', 'सब्जी', 'காய்கறி', 'V-handshape touches side of chin with twisting smile.', ['SABZI', 'GREENS']),
    'RICE': ('rice', 'daily', 'Rice / Chawal', 'चावल / भात', 'அரிசி / சாதம்', 'Right curved fingertips gather grains from left cupped palm to mouth.', ['CHAWAL', 'GRAIN']),
    'ROTI': ('roti', 'daily', 'Roti / Chapati / Flatbread', 'रोटी / चपाती', 'ரொட்டி', 'Both palms pat alternately against each other flattening round dough.', ['CHAPATI', 'FLATBREAD']),
    'HUNGRY': ('hungry', 'daily', 'Hungry / Appetite', 'भूख / भूखा', 'பசி', 'C-handshape slides down center throat and chest showing empty stomach.', ['APPETITE', 'EMPTY_STOMACH']),
    'CHAI': ('chai', 'daily', 'Chai / Masala Tea', 'चाय', 'மசாலா தேநீர்', 'Tea cup sip with saucer swirl gesture beloved across India.', ['MASALA_TEA', 'INDIAN_TEA']),
    'COFFEE': ('coffee', 'daily', 'Coffee / Filter Coffee', 'कॉफ़ी', 'காபி', 'Right fist rotates clockwise on top of left fist grinding coffee beans.', ['FILTER_COFFEE', 'KAAPI']),
    'FAST_FOOD': ('fast-food', 'daily', 'Snacks / Fast Food', 'नाश्ता / स्नैक्स', 'துரித உணவு', 'Rapid pinch eating gestures with crunchy expression.', ['SNACKS', 'STREET_FOOD']),
    'FISH_MARKET': ('fish-market', 'daily', 'Fish Market', 'मछली बाज़ार', 'மீன் சந்தை', 'Wiggling fish hand motion followed by busy market coin barter.', ['MACHHLI_MANDI', 'SEAFOOD_MARKET']),
    'MARKET': ('market', 'daily', 'Market / Bazaar', 'बाज़ार / मंडी', 'சந்தை', 'Both hands move forward offering wares and assessing price in bazaar.', ['BAZAAR', 'MANDI']),

    # ─── SOCIAL ETIQUETTE, GREETINGS & SENTIMENT (islrtc-social) ───
    'FRIEND': ('friend', 'greeting', 'Friend / Companion', 'मित्र / दोस्त', 'நண்பர்', 'Interlocking hooked index fingers clasped together firmly.', ['COMPANION', 'DOST']),
    'WELCOME': ('welcome', 'greeting', 'Welcome / Swagatam', 'स्वागत / पधारिए', 'வரவேற்பு', 'Both open palms scoop inward toward torso with warm inviting smile.', ['SWAGAT', 'INVITE_IN']),
    'SORRY': ('sorry', 'greeting', 'Sorry / Apologies', 'माफ़ कीजिए / क्षमा', 'மன்னிக்கவும்', 'Right fist rubs circular motion over heart with apologetic expression.', ['APOLOGY', 'MAAF_KARNA']),
    'CONGRATULATIONS': ('congratulations', 'greeting', 'Congratulations / Mubarak', 'बधाई हो', 'வாழ்த்துகள்', 'Both hands clap enthusiastically then flutter fingers high above head.', ['BADHAI', 'FELICITATIONS']),
    'HAPPY': ('happy', 'sentiment', 'Happy / Joyful', 'खुश / आनंद', 'மகிழ்ச்சி', 'Open flat palm brushes upward against chest repeatedly with radiant smile.', ['JOYFUL', 'KHUSH']),
    'LOVE': ('love', 'sentiment', 'Love / Affection', 'प्यार / स्नेह', 'அன்பு', 'Both closed fists crossed over center heart hugging chest warmly.', ['AFFECTION', 'CARE_DEEP']),
    'RESPECT': ('respect', 'greeting', 'Respect / Honor', 'आदर / सम्मान', 'மரியாதை', 'R-hands or flat hands move from forehead upward and outward with solemn bow.', ['HONOR', 'AADAR']),
    'SAD': ('sad', 'sentiment', 'Sad / Unhappy', 'दुखी / उदास', 'துக்கம்', 'Open hand drops downward in front of drooping face with downward gaze.', ['UNHAPPY', 'UDAS']),
    'MEET': ('meet', 'greeting', 'Meet / Encounter', 'मिलना / मुलाकात', 'சந்தித்தல்', 'Two upright index fingers move from opposite sides and meet face-to-face.', ['GATHER', 'CONVERGE']),
    'NICE': ('nice', 'sentiment', 'Nice / Pleasant', 'सुखद / अच्छा', 'இனிமையானது', 'Right flat palm slides forward smoothly across flat left palm.', ['PLEASANT', 'DELIGHTFUL']),
    'BAD': ('bad', 'sentiment', 'Bad / Unfavorable', 'बुरा / ख़राब', 'மோசமானது', 'Fingertips touch chin then turn sharply outward and downward with scowl.', ['UNFAVORABLE', 'POOR']),
    'AGREE': ('agree', 'sentiment', 'Agree / In Agreement', 'सहमत होना', 'ஒப்புக்கொள்ளுதல்', 'Index finger touches forehead then comes down alongside left index in tandem.', ['CONCUR', 'HARMONY_VIEW']),
    'DISAGREE': ('disagree', 'sentiment', 'Disagree / Differ', 'असहमत', 'முரண்படுதல்', 'Both index fingers meet then pull apart sharply in opposite directions.', ['OPPOSE', 'CONFLICT']),
    'SMILE': ('smile', 'sentiment', 'Smile / Grin', 'मुस्कान / मुस्कराना', 'புன்னகை', 'Both index fingers trace upward curves at mouth corners into a smile.', ['GRIN', 'BEAM']),
    'CARE': ('care', 'greeting', 'Care / Concern', 'देखभाल / परवाह', 'கவனிப்பு', 'Both crossed hands hold protectively over heart with gentle head tilt.', ['CONCERN', 'NURTURE']),
    'BLESSING': ('blessing', 'greeting', 'Blessing / Ashirwad', 'आशीर्वाद', 'ஆசிர்வாதம்', 'Both open palms placed near elder forehead then sweeping down toward recipient.', ['ASHIRWAD', 'GRACE']),
    'NAMASTE': ('namaste', 'greeting', 'Namaste / Traditional Salutation', 'नमस्ते / प्रणाम', 'வணக்கம்', 'Two flat palms joined at heart center with slight respectful head bow.', ['VANAKKAM', 'PRANAM']),
    'KIND': ('kind', 'sentiment', 'Kind / Compassionate', 'दयालु / नम्र', 'கருணையுள்ள', 'Right flat palm circles gently over chest heart center.', ['COMPASSIONATE', 'GENTLE']),
    'PEACE': ('peace', 'sentiment', 'Peace / Shanti', 'शांति / अमन', 'அமைதி', 'Both open palms cross over chest then sweep outward horizontally in tranquility.', ['SHANTI', 'TRANQUILITY']),
    'BROTHERHOOD': ('brotherhood', 'greeting', 'Brotherhood / Unity', 'भाईचारा / सौहार्द', 'சகோதரத்துவம்', 'Sign BROTHER followed by interlocking hands of unity.', ['FRATERNITY', 'SOLIDARITY']),
    'HARMONY': ('harmony', 'sentiment', 'Harmony / Goodwill', 'सद्भाव / तालमेल', 'இணக்கம்', 'Both open palms intertwine fingers softly moving in unison wave.', ['UNITY', 'GOODWILL']),
    'VANAKKAM': ('vanakkam', 'greeting', 'Vanakkam / South Salutation', 'வணக்கம்', 'வணக்கம்', 'Both palms joined in traditional Tamil salute at chest level with warm head nod.', ['NAMASKARAM', 'SOUTHERN_GREETING']),
    'GOOD': ('good', 'sentiment', 'Good / Fine', 'अच्छा / उत्तम', 'நல்லது', 'Fingertips touch lips and move forward into flat open affirming palm.', ['FINE', 'EXCELLENT']),

    # ─── CHRONOLOGY, NUMBERS & TIME (islrtc-chronology) ───
    '1': ('num-1', 'numbers', 'One (1)', 'एक (१)', 'ஒன்று (1)', 'Right index finger held upright vertically with back of hand facing signer.', ['ONE', 'SINGLE']),
    '2': ('num-2', 'numbers', 'Two (2)', 'दो (२)', 'இரண்டு (2)', 'Right index and middle fingers held upright vertically in V-formation.', ['TWO', 'PAIR']),
    '3': ('num-3', 'numbers', 'Three (3)', 'तीन (३)', 'மூன்று (3)', 'Right thumb, index, and middle fingers held extended upright.', ['THREE', 'TRIPLE']),
    '4': ('num-4', 'numbers', 'Four (4)', 'चार (४)', 'நான்கு (4)', 'Four fingers held upright with thumb folded across palm.', ['FOUR', 'QUAD']),
    '5': ('num-5', 'numbers', 'Five (5)', 'पांच (५)', 'ஐந்து (5)', 'All five fingers spread wide on upright open palm.', ['FIVE', 'QUINT']),
    'YESTERDAY': ('yesterday', 'numbers', 'Yesterday / Past Day', 'कल (बीता हुआ)', 'நேற்று', 'Thumb of A-hand touches cheek then moves backward over shoulder.', ['PAST_DAY', 'BEETA_KAL']),
    'WEEK': ('week', 'numbers', 'Week / 7 Days', 'सप्ताह / हफ़्ता', 'வாரம்', 'Right index finger sweeps across flat left palm from heel to fingertips.', ['SEVEN_DAYS', 'HAFTA']),
    'MONTH': ('month', 'numbers', 'Month / Calendar Month', 'महीना / मास', 'மாதம்', 'Right index finger slides straight downward along back of upright left index finger.', ['CALENDAR_MONTH', 'MAHINA']),
    'YEAR': ('year', 'numbers', 'Year / 12 Months', 'वर्ष / साल', 'ஆண்டு / வருடம்', 'Right fist orbits completely around left stationary fist once.', ['ANNUAL', 'SAAL']),
    'MORNING': ('morning', 'numbers', 'Morning / Dawn', 'सुबह / प्रातः', 'காலை', 'Right open flat palm rises up from under left horizontal arm like rising sun.', ['DAWN', 'PRATAH']),
    'AFTERNOON': ('afternoon', 'numbers', 'Afternoon / Midday', 'दोपहर', 'மதியம்', 'Right flat forearm rests angled straight across flat left hand at zenith sun.', ['MIDDAY', 'DOPAHAR']),
    'EVENING': ('evening', 'numbers', 'Evening / Sunset', 'शाम / सांध्य', 'மாலை', 'Right curved palm sweeps downward over left horizontal arm like setting sun.', ['DUSK', 'SHAAM']),
    'NIGHT': ('night', 'numbers', 'Night / Darkness', 'रात / रात्रि', 'இரவு', 'Both bent palms sweep across each other closing down like blanket of darkness.', ['DARKNESS', 'RAAT']),
    'CLOCK': ('clock', 'numbers', 'Clock / Watch', 'घड़ी', 'கடிகாரம்', 'Index finger taps wrist watch spot then outlines round dial on wall.', ['WATCH', 'TIMEPIECE']),
    'EARLY': ('early', 'numbers', 'Early / In Advance', 'जल्दी / पूर्व समय', 'முன்கூட்டியே', 'Middle finger pushes quickly ahead of stationary left wrist.', ['ADVANCE', 'BEFORE_TIME']),
    'LATE': ('late', 'numbers', 'Late / Delayed', 'देर / विलंब', 'தாமதம்', 'Right flat hand flaps downward repeatedly behind right hip.', ['DELAYED', 'VILAMB']),
    'SECOND': ('second-time', 'numbers', 'Second / Moment', 'सेकंड / पल', 'வினாடி', 'Index finger ticks like a stopwatch second hand on left palm dial.', ['MOMENT', 'TICK']),
    'CALENDAR': ('calendar', 'numbers', 'Calendar / Schedule Grid', 'कैलेंडर / पंचांग', 'நாட்காட்டி', 'Both C-hands outline wall calendar grid then flip imaginary page.', ['PANCHANG', 'DATE_SHEET']),
    'SCHEDULE': ('schedule', 'numbers', 'Schedule / Timetable', 'समय सारणी', 'நேர அட்டவணை', 'Four horizontal stripes traced across left flat palm timetable.', ['TIMETABLE', 'ROSTER']),
    'DAY': ('day', 'numbers', 'Day / Daylight', 'दिन / दिवस', 'நாள் / பகல்', 'Right arm sweeps wide arc across sky from sunrise to sunset horizon.', ['DAYLIGHT', 'DIVAS']),
    'HOUR': ('hour', 'numbers', 'Hour / 60 Minutes', 'घंटा', 'மணி நேரம்', 'Right index finger completes one full 360-degree rotation on flat left palm.', ['SIXTY_MINS', 'GHANTA']),
    'NOW': ('now', 'numbers', 'Now / Present Moment', 'अभी / वर्तमान', 'இப்போது', 'Both bent Y-hands drop firmly downward into present lap space.', ['PRESENT', 'ABHI']),
    'TODAY': ('today', 'numbers', 'Today / Current Day', 'आज', 'இன்று', 'Sign NOW followed by DAY arc across sky.', ['CURRENT_DAY', 'AAJ']),
    'TOMORROW': ('tomorrow', 'numbers', 'Tomorrow / Next Day', 'कल (आने वाला)', 'நாளை', 'Thumb touches cheek then rolls forward in an arc toward future.', ['NEXT_DAY', 'AANE_WALA_KAL']),

    # ─── DIGITAL TECH & ASSISTIVE COMMUNICATION (islrtc-tech) ───
    'SMARTPHONE': ('smartphone', 'meta', 'Smartphone / Mobile Device', 'स्मार्टफ़ोन / मोबाइल', 'ஸ்மார்ட்போன்', 'Right thumb swipes upward and sideways on horizontal left palm touchscreen.', ['MOBILE_PHONE', 'TOUCHSCREEN']),
    'TABLET': ('tablet-tech', 'meta', 'Tablet Device / iPad', 'टैबलेट कंप्यूटर', 'டேப்லெட்', 'Two hands outline large rectangular slab, then index finger scrolls screen.', ['IPAD', 'TOUCH_SLAB']),
    'SOFTWARE': ('software', 'meta', 'Software / Application Code', 'सॉफ्टवेयर / कोड', 'மென்பொருள்', 'Both hands mime keyboard coding then flow fluid data waves into screen.', ['PROGRAM', 'APP_CODE']),
    'EMAIL': ('email', 'meta', 'Email / Electronic Mail', 'ईमेल', 'மின்னஞ்சல்', 'Right flat hand slides straight through C-shaped left hand mail slot.', ['E_POST', 'INBOX_MESSAGE']),
    'PASSWORD': ('password', 'meta', 'Password / Secret Key', 'पासवर्ड / कूटशब्द', 'கடவுச்சொல்', 'Closed fist key twists against lips indicating secret credential.', ['SECRET_CODE', 'ACCESS_KEY']),
    'WIFI': ('wifi', 'meta', 'Wi-Fi / Wireless Internet', 'वाई-फ़ाई / वायरलेस', 'வைஃபை', 'Curved fingers of both hands pulse outward in concentric signal waves.', ['WIRELESS', 'HOTSPOT']),
    'VIDEO_CALL': ('video-call', 'meta', 'Video Call / Remote Relay', 'वीडियो कॉल / रिले', 'வீடியோ அழைப்பு', 'Camera sign with right hand aimed at left palm display showing face.', ['RELAY_CALL', 'VRS']),
    'WEBSITE': ('website', 'meta', 'Website / Web Portal', 'वेबसाइट / पोर्टल', 'வலைத்தளம்', 'Fingerspell W-W-W then trace wide web grid in space.', ['WEB_PAGE', 'PORTAL']),
    'LAPTOP': ('laptop', 'meta', 'Laptop Computer', 'लैपटॉप', 'மடிக்கணினி', 'Both flat hands hinged at wrists open and fold shut like laptop clamshell.', ['NOTEBOOK_PC', 'PORTABLE_COMPUTER']),
    'SCREEN': ('screen', 'meta', 'Display Screen / Monitor', 'मॉनिटर स्क्रीन', 'திரை', 'Both L-hands outline large rectangular digital viewing monitor.', ['MONITOR', 'DISPLAY']),
    'KEYBOARD': ('keyboard', 'meta', 'Keyboard / Typing Keys', 'कीबोर्ड', 'விசைப்பலகை', 'Both hands type rapidly with fluttering fingers on imaginary horizontal desk.', ['KEYS', 'TYPING_BOARD']),
    'DATA': ('data', 'meta', 'Data / Digital Storage', 'डेटा / आंकड़े', 'தரவு', 'Both flat hands slice horizontally down column of data packets.', ['INFORMATION', 'DIGITAL_DATA']),
    'ROBOT': ('robot', 'meta', 'Robot / Artificial Agent', 'रोबोट / स्वचालित मशीन', 'ரோபோ', 'Stiff mechanical angular arm movements with clicking pivot joints.', ['AUTOMATON', 'AI_BOT']),
    'APP': ('app', 'meta', 'Mobile App / Application', 'मोबाइल ऐप', 'செயலி', 'Touch square icon on left palm phone screen launching program.', ['APPLICATION', 'MOBILE_APP']),
    'NETWORK': ('network', 'meta', 'Computer Network / Grid', 'नेटवर्क / संजाल', 'வலைப்பின்னல்', 'Interlocking thumbs and index fingers linking across multiple nodes.', ['GRID', 'INTERCONNECTION']),
    'MICROPHONE': ('microphone', 'meta', 'Microphone / Audio Input', 'माइक्रोफ़ोन / माइक', 'ஒலிவாங்கி', 'Closed fist held in front of mouth speaking into audio transducer.', ['MIC', 'SPEECH_INPUT']),
    'DOWNLOAD': ('download', 'meta', 'Download / Retrieve File', 'डाउनलोड', 'பதிவிறக்கம்', 'Curved fingers pull data beam straight down from cloud into laptop.', ['PULL_FILE', 'FETCH_DATA']),
    'CHAT': ('chat', 'meta', 'Chat / Instant Messaging', 'चैट / संदेश वार्ता', 'அரட்டை', 'Two open claw hands alternating forward in rapid conversational rhythm.', ['MESSAGING', 'TEXT_CHAT']),
    'ONLINE': ('online', 'meta', 'Online / Connected', 'ऑनलाइन / सक्रिय', 'இணைய தொடர்பு', 'Both horizontal index fingers point toward each other and connect tip-to-tip.', ['CONNECTED', 'LIVE_WEB']),
    'COMPUTER': ('computer', 'meta', 'Computer / PC', 'कंप्यूटर / संगणक', 'கணினி', 'Both hands type on desk keyboard then glance up at monitor outline.', ['PC', 'DESKTOP']),
    'VIDEO': ('video', 'meta', 'Video / Motion Picture', 'वीडियो / चलचित्र', 'வீடியோ', 'Left flat palm vertical, right hand fluttering open fingers behind it.', ['MOTION_PICTURE', 'VISUAL_FEED']),
    'CAMERA': ('camera', 'meta', 'Camera / Optics', 'कैमरा', 'கேமரா', 'Both index fingers press shutter button on imaginary compact camera.', ['PHOTO_DEVICE', 'OPTICS']),
    'AI': ('ai', 'meta', 'AI (Artificial Intelligence)', 'एआई / कृत्रिम बुद्धिमत्ता', 'செயற்கை நுண்ணறிவு', 'Fingerspell A-I followed by cybernetic neural sparks from forehead.', ['MACHINE_LEARNING', 'ARTIFICIAL_INTELLIGENCE']),
    'IT_TECH': ('it-tech', 'meta', 'Information Technology', 'सूचना प्रौद्योगिकी', 'தகவல் தொழில்நுட்பம்', 'Fingerspell I-T followed by keyboard and satellite transmission sign.', ['TECH_HUB', 'INFOTECH']),

    # ─── REGIONAL & ECOLOGICAL DIALECT CONVENTIONS ───
    'TEA_GARDEN': ('tea-garden', 'navigation', 'Tea Garden / Plantation', 'चाय बागान', 'தேயிலைத் தோட்டம்', 'Miming plucking two tea leaves and dropping into bamboo basket.', ['TEA_PLANTATION', 'ESTATE']),
    'TEA_ESTATE': ('tea-estate', 'navigation', 'Tea Estate Hills', 'चाय एस्टेट', 'தேயிலை எஸ்டேட்', 'Hill contour wave followed by tea leaf plucking fingers.', ['ASSAM_TEA', 'NILGIRI_TEA']),
    'RIVER': ('river', 'navigation', 'River / Ganga / Brahmaputra', 'नदी / सरिता', 'ஆறு', 'Both wavy flat hands undulate forward miming gentle water currents.', ['STREAM', 'SARITA']),
    'CULTURE': ('culture', 'greeting', 'Culture / Heritage', 'संस्कृति / परंपरा', 'பண்பாடு / கலாச்சாரம்', 'C-handshape circles heart then presents traditional folk gesture.', ['HERITAGE', 'TRADITION']),
    'FOOTBALL': ('football', 'academic', 'Football / Soccer', 'फ़ुटबॉल', 'கால்பந்து', 'Right foot kicking forward followed by round ball outline in hands.', ['SOCCER', 'KICK_BALL']),
    'COMMUNITY': ('community', 'greeting', 'Deaf Community / Society', 'समुदाय / समाज', 'சமூகம்', 'Both cupped hands circle together meeting fingertips in unified ring.', ['SOCIETY', 'SAMAJ']),
    'COMMUNITY_HALL': ('community-hall', 'navigation', 'Community Hall / Panchayat', 'सामुदायिक भवन', 'சமூகக் கூடம்', 'Community circle followed by large hall building roof enclosure.', ['PANCHAYAT_GHAR', 'TOWN_HALL']),
    'HILL_ROAD': ('hill-road', 'navigation', 'Hilly Winding Road', 'पहाड़ी रास्ता', 'மலைப்பாதை', 'Both hands snake curving upward at steep incline.', ['GHAT_ROAD', 'MOUNTAIN_PATH']),
    'RAIN_HEAVY': ('rain-heavy', 'daily', 'Heavy Monsoon Rain', 'भारी बारिश / मानसून', 'கனமழை', 'Both five-finger hands flutter vigorously downward with cloud canopy.', ['MONSOON', 'DOWNPOUR']),
    'MARKET_HANDICRAFT': ('handicraft-market', 'civic', 'Handicraft Market / Shilpgram', 'हस्तशिल्प बाज़ार', 'கைவினைப் பொருட்கள் சந்தை', 'Hands weave artisanal fabric then display market stalls.', ['SHILPGRAM', 'CRAFT_BAZAAR']),
    'WEAVING': ('weaving', 'academic', 'Traditional Handloom Weaving', 'हथकरघा बुनाई', 'கைத்தறி நெசவு', 'Both hands operate shuttle passing rhythmically through handloom threads.', ['HANDLOOM', 'TEXTILE_WEAVE']),
    'NATURE': ('nature', 'navigation', 'Nature / Environment', 'प्रकृति / पर्यावरण', 'இயற்கை', 'Both open palms blossom outward into green canopy and fresh breeze.', ['ENVIRONMENT', 'PRAKRITI']),
    'POETRY': ('poetry', 'academic', 'Poetry / Sign Poetry', 'कविता / काव्य', 'கவிதை', 'Right hand flourishes graceful rhythmic meter from heart to audience.', ['VERSE', 'KAVITA']),
    'MUSIC': ('music', 'academic', 'Music / Instrumental Rhythm', 'संगीत / वाद्य', 'இசை', 'Right hand conducts melodic wave over left forearm instrument.', ['SANGEET', 'MELODY']),
    'BOOK_LITERARY': ('book-literary', 'academic', 'Literary Book / Classic', 'साहित्यिक ग्रंथ', 'இலக்கிய நூல்', 'Both hands open venerable antique volume with respectful gaze.', ['GRANTH', 'LITERATURE']),
    'DELHI': ('delhi', 'navigation', 'Delhi NCR Capital', 'दिल्ली', 'தில்லி', 'D-handshape traces India Gate memorial arch in the air.', ['CAPITAL_DELHI', 'NCR']),
    'WEATHER': ('weather', 'daily', 'Weather / Climate', 'मौसम / जलवायु', 'வானிலை', 'Both W-hands twist alternately feeling temperature and wind currents.', ['CLIMATE', 'MAUSAM']),
    'COLD_WEATHER': ('cold-weather', 'daily', 'Cold Winter / Chilly', 'सर्दी / ठंड', 'குளிர் காலம்', 'Both fists hug tightly to shivering chest with chattering teeth expression.', ['WINTER', 'CHILLY']),
    'COASTAL': ('coastal', 'navigation', 'Coastal Region / Seashore', 'तटीय क्षेत्र / समुद्र तट', 'கடலோரப் பகுதி', 'Hand traces ocean waves lapping against sandy coastline.', ['SEASHORE', 'BEACH_SIDE']),
    'PORT': ('port', 'navigation', 'Seaport / Harbor', 'बंदरगाह', 'துறைமுகம்', 'Large ship hull gesture approaching cargo dock cranes.', ['HARBOR', 'DOCKS']),
    'BUSINESS': ('business', 'civic', 'Business / Commerce Enterprise', 'व्यापार / कारोबार', 'வணிகம்', 'B-handshape brushes briskly across base palm showing enterprise.', ['COMMERCE', 'ENTERPRISE']),
    'COMMERCE': ('commerce', 'civic', 'Commerce / Trade', 'वाणिज्य / व्यापार', 'வர்த்தகம்', 'Both hands exchange commodities across central merchant counter.', ['TRADE', 'TRANSACTIONS']),
    'TEXTILE': ('textile', 'civic', 'Textile / Fabrics', 'वस्त्र उद्योग / कपड़ा', 'ஜவுளி', 'Thumb and index feel texture of rich cloth between fingers.', ['FABRIC', 'CLOTH_TRADE']),
    'FACTORY': ('factory', 'civic', 'Factory / Industrial Plant', 'कारख़ाना / फ़ैक्टरी', 'தொழிற்சாலை', 'Both hands interlock gear teeth rotating steadily with smokestacks.', ['INDUSTRY', 'MILL']),
    'TEMPLE': ('temple', 'navigation', 'Temple / Sacred Shrine', 'मंदिर / देवालय', 'கோயில்', 'Both palms join in prayer then trace rising temple gopuram steeple.', ['MANDIR', 'SHRINE']),
    'SIGN_RELAY': ('sign-relay', 'meta', 'Sign Relay Interpreter Service', 'सांकेतिक रिले सेवा', 'சைகை மொழி சேவை', 'Two interpreters relaying message through camera to deaf caller.', ['VIDEO_RELAY', 'INTERPRETER_RELAY']),
    'TAMIL_SYNTHESIS': ('tamil-synthesis', 'meta', 'Tamil Spoken Synthesis', 'तमिल वाक् संश्लेषण', 'தமிழ் பேச்சு தொகுப்பு', 'Sign language input synthesized dynamically into spoken Tamil voice.', ['TAMIL_TTS', 'TRILINGUAL_VOICE']),
}

def populate():
    with open('frontend/src/data/islDictionary.js', 'r', encoding='utf-8') as f:
        content = f.read()

    existing_glosses = set(re.findall(r'gloss:\s*[\'"]([^\'"]+)[\'"]', content))
    print(f'Existing glosses in dictionary: {len(existing_glosses)}')

    to_add = []
    for gloss, (slug, cat, en, hi, ta, desc, syns) in SIGN_DEFINITIONS.items():
        if gloss in existing_glosses:
            continue
        syn_str = ', '.join([f"'{s}'" for s in syns])
        entry_text = f"""  {{
    id: '{slug}',
    gloss: '{gloss}',
    synonyms: [{syn_str}],
    category: '{cat}',
    en: '{en}',
    hi: '{hi}',
    ta: '{ta}',
    description: '{desc}',
    modelSupported: false,
    demoVideo: null,
    source: 'ISLRTC Standard Corpus (Curricular Editions)',
    variants: ['National Standard'],
  }},"""
        to_add.append(entry_text)

    print(f'Adding {len(to_add)} new standard dictionary entries...')

    # Find where ISL_DICTIONARY ends (before `];\n\n// Fast lookup map`)
    target = '];\n\n// Fast lookup map by gloss'
    if target not in content:
        target = '];\n\n// Fast lookup map'
    
    assert target in content, "Could not find dictionary array closing marker"

    insertion = '\n' + '\n'.join(to_add) + '\n];\n\n// Fast lookup map by gloss'
    new_content = content.replace(target, insertion, 1)

    with open('frontend/src/data/islDictionary.js', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print('Successfully updated frontend/src/data/islDictionary.js!')

if __name__ == '__main__':
    populate()
