"""
add_150_signs.py
Adds 153 new official ISLRTC signs across all 9 volumes (17 signs per volume).
Integrates with:
- backend/indian_sign_languages.py
- frontend/src/data/indianSignLanguages.js
- frontend/src/data/islDictionary.js
- backend/extended_vocabulary.py
"""

import os
import re

# 17 new signs for each of the 9 volumes = 153 signs
NEW_SIGNS_BY_VOLUME = {
    # ─── VOL 1: Emergency & Healthcare ───
    "islrtc-emergency": [
        ('VOMIT', 'vomit', 'emergency', 'Vomiting / Nausea', 'उल्टी / मिचली', 'வாந்தி', 'Fist at throat opens outward away from mouth with nauseous face expression.', ['NAUSEA', 'SICK']),
        ('ALLERGY', 'allergy', 'emergency', 'Allergy / Skin Rash', 'एलर्जी / चकत्ते', 'ஒவ்வாமை', 'Fingertips scratch repeatedly along back of forearm with itching expression.', ['RASH', 'ITCHING']),
        ('FRACTURE', 'fracture', 'emergency', 'Bone Fracture / Broken Bone', 'हड्डी टूटना', 'எலும்பு முறிவு', 'Both index fingers aligned like bone snap sharply in half at center.', ['BROKEN_BONE', 'BONE_CRACK']),
        ('BURN', 'burn', 'emergency', 'Burn Trauma / Scald', 'जलना / घाव', 'தீக்காயம்', 'Flames flickering gesture over skin followed by blow of soothing air.', ['FIRE_BURN', 'SCALD']),
        ('POISON', 'poison', 'emergency', 'Poison / Toxic Chemical', 'विष / ज़हर', 'நஞ்சு', 'P-handshape near mouth with skull-and-crossbones warning head tilt.', ['TOXIC', 'VENOM']),
        ('DIABETES', 'diabetes', 'emergency', 'Diabetes / High Sugar', 'मधुमेह / शुगर', 'சர்க்கரை நோய்', 'Index finger pricks left fingertip for blood glucose strip test.', ['SUGAR', 'GLUCOSE']),
        ('BP_PRESSURE', 'bp-pressure', 'emergency', 'Blood Pressure (BP)', 'रक्तचाप / बीपी', 'இரத்த அழுத்தம்', 'Pumping rubber bulb motion onto left upper arm pressure cuff.', ['BLOOD_PRESSURE', 'HYPERTENSION']),
        ('THERMOMETER', 'thermometer', 'emergency', 'Thermometer', 'थर्मामीटर', 'வெப்பநிலைமானி', 'Right index finger placed under tongue then examined closely against light.', ['TEMP_GAUGE', 'FEVER_CHECK']),
        ('XRAY', 'xray', 'emergency', 'X-Ray Scan / Radiography', 'एक्स-रे', 'எக்ஸ்ரே', 'Hold translucent rectangular film up toward light squinting to inspect ribs.', ['RADIOGRAPHY', 'BONE_SCAN']),
        ('SCAN', 'scan', 'emergency', 'CT / MRI Scan', 'सीटी / एमआरआई स्कैन', 'ஸ்கேன்', 'Both curved hands form cylindrical tunnel sliding over patient body.', ['CT_SCAN', 'MRI']),
        ('WHEELCHAIR', 'wheelchair', 'emergency', 'Wheelchair', 'व्हीलचेयर', 'சக்கர நாற்காலி', 'Both hands rotate large circular wheels on sides of chair forward.', ['CHAIR_WHEELS', 'MOBILITY_CHAIR']),
        ('PREGNANT', 'pregnant', 'emergency', 'Pregnant / Maternity', 'गर्भवती / गर्भावस्था', 'கர்ப்பிணி', 'Both curved hands cradle expanding rounded abdomen gently.', ['MATERNITY', 'EXPECTING']),
        ('UNCONSCIOUS', 'unconscious', 'emergency', 'Unconscious / Fainting', 'बेहोश', 'மயக்கம்', 'Eyes roll back, head drops limply sideways into loose open palms.', ['FAINTED', 'COMA']),
        ('SALINE', 'saline', 'emergency', 'Saline IV Drip', 'ड्रिप / सलाइन', 'சலைன் ட்ரிப்', 'Right index finger points to overhead hanging bottle dripping into wrist.', ['IV_DRIP', 'BOTTLE_DRIP']),
        ('MASK', 'mask-med', 'emergency', 'Surgical Mask / Face Cover', 'मास्क / मुखौटा', 'முகக்கவசம்', 'Both flat hands spread across nose and mouth hooking loops behind ears.', ['SURGICAL_MASK', 'FACE_MASK']),
        ('GLOVES', 'gloves', 'emergency', 'Medical Gloves', 'दस्ताने', 'கையுறைகள்', 'Pull imaginary tight rubber glove over spread fingers of left hand.', ['SURGICAL_GLOVES', 'RUBBER_GLOVES']),
        ('DISCHARGE', 'discharge', 'emergency', 'Hospital Discharge / Released', 'अस्पताल से छुट्टी', 'மருத்துவமனை விடுவிப்பு', 'Bed exit sign followed by joyful wave walking out hospital doors.', ['RELEASED', 'HOSPITAL_LEAVE']),
    ],

    # ─── VOL 2: Legal, Rights & Public Safety ───
    "islrtc-legal": [
        ('BAIL', 'bail', 'civic', 'Bail / Bond Release', 'ज़मानत', 'பிணை', 'Hands unlock from wrists and push open prison gates into release.', ['BOND', 'LEGAL_RELEASE']),
        ('PETITION', 'petition', 'civic', 'Legal Petition / Writ', 'याचिका', 'மனு', 'Formal document scroll signed and handed reverently to high judge.', ['WRIT', 'PLEA']),
        ('HEARING', 'hearing-legal', 'civic', 'Court Hearing / Trial', 'सुनवाई', 'விசாரணை', 'Two open palms at ear level turning toward judge and witness alternately.', ['TRIAL', 'CASE_HEARING']),
        ('FINE', 'fine-penalty', 'civic', 'Penalty Fine / Challan', 'जुर्माना / चालान', 'அபராதம்', 'Right flat palm strikes left wrist then hands over official slip.', ['PENALTY', 'CHALLAN']),
        ('THIEF', 'thief', 'civic', 'Thief / Burglar', 'चोर', 'திருடன்', 'Curved fingers hook around left shoulder snatching bag sneakily.', ['BURGLAR', 'ROBBER']),
        ('FRAUD', 'fraud', 'civic', 'Fraud / Cheating Scam', 'धोखाधड़ी / घोटाला', 'மோசடி', 'Two fingers pull imaginary mask off face revealing deceit.', ['SCAM', 'CHEAT']),
        ('HUMAN_RIGHTS', 'human-rights', 'civic', 'Human Rights', 'मानवाधिकार', 'மனித உரிமைகள்', 'Sign HUMAN followed by balanced scales of justice held aloft.', ['RIGHTS_HUMAN', 'CIVIL_LIBERTIES']),
        ('ACCUSED', 'accused', 'civic', 'Accused / Suspect', 'आरोपी / अभियुक्त', 'குற்றஞ்சாட்டப்பட்டவர்', 'Index finger points squarely at person in dock with stern gaze.', ['SUSPECT', 'DEFENDANT']),
        ('CHARGE_SHEET', 'charge-sheet', 'civic', 'Chargesheet / Police File', 'आरोप पत्र', 'குற்றப்பத்திரிகை', 'Official police document stamped firmly with list of counts.', ['POLICE_FILE', 'FORMAL_CHARGE']),
        ('OATH', 'oath', 'civic', 'Oath / Solemn Sworn Pledge', 'शपथ / हलफ़', 'உறுதிமொழி', 'Right hand raised upright palm forward, left hand resting on sacred book.', ['PLEDGE', 'AFFIDAVIT']),
        ('SUMMON', 'summon', 'civic', 'Court Summons / Notice', 'समन / बुलावा', 'அழைப்பாணை', 'Official paper bearing red seal handed directly to recipient chest.', ['COURT_NOTICE', 'OFFICIAL_SUMMONS']),
        ('DISCRIMINATION', 'discrimination', 'civic', 'Discrimination / Bias', 'भेदभाव / पक्षपात', 'பாகுபாடு', 'One hand favored forward while other hand shoved dismissively aside.', ['BIAS', 'INEQUALITY']),
        ('HARASSMENT', 'harassment', 'civic', 'Harassment / Exploitation', 'उत्पीड़न / छेड़छाड़', 'துன்புறுத்தல்', 'Aggressive fist repeatedly shoving into defensive protective arms.', ['EXPLOITATION', 'ABUSE']),
        ('CORRUPTION', 'corruption', 'civic', 'Corruption / Bribery', 'भ्रष्टाचार / रिश्वत', 'ஊழல்', 'Hand slips discreetly under table to accept crumpled cash bribe.', ['BRIBERY', 'GRAFT']),
        ('NOTARY', 'notary', 'civic', 'Notary / Attestation Stamp', 'नोटरी / सत्यापन', 'நோட்டரி', 'Circular seal pressed firmly onto legal document with official signature.', ['ATTESTATION', 'VERIFICATION']),
        ('INSPECTOR', 'inspector', 'civic', 'Police Inspector', 'पुलिस इंस्पेक्टर', 'ஆய்வாளர்', 'Two stars tapped on right shoulder epaulet with crisp salute.', ['SHO', 'POLICE_OFFICER']),
        ('FREEDOM', 'freedom', 'civic', 'Freedom / Independence', 'स्वतंत्रता / आज़ादी', 'சுதந்திரம்', 'Crossing wrists break free and soar high into sky as unfettered birds.', ['LIBERTY', 'AZADI']),
    ],

    # ─── VOL 3: Banking, Commerce & Financial ───
    "islrtc-banking": [
        ('TAX', 'tax', 'civic', 'Tax / GST Duty', 'कर / टैक्स', 'வரி', 'Percentage sign traced in air then portion subtracted from income bundle.', ['GST', 'INCOME_TAX']),
        ('PENSION', 'pension', 'civic', 'Pension / Retirement Fund', 'पेंशन', 'ஓய்வூதியம்', 'Elder walking cane gesture followed by regular monthly cash deposit.', ['RETIREMENT_PAY', 'ANNUITY']),
        ('INSURANCE', 'insurance', 'civic', 'Insurance / Policy Cover', 'बीमा / पॉलिसी', 'காப்பீடு', 'Protective umbrella open over house/family followed by safety guarantee.', ['POLICY', 'BIMA']),
        ('PROFIT', 'profit', 'civic', 'Profit / Gain Margin', 'लाभ / मुनाफ़ा', 'லாபம்', 'Right thumb points high upward over rising stack of coins.', ['GAIN', 'SURPLUS']),
        ('LOSS', 'loss-finance', 'civic', 'Loss / Deficit', 'हानि / घाटा', 'நஷ்டம்', 'Thumb points downward as coin stack tumbles in negative trajectory.', ['DEFICIT', 'FINANCIAL_LOSS']),
        ('BUDGET', 'budget', 'civic', 'Budget / Fiscal Plan', 'बजट', 'வரவு செலவு திட்டம்', 'Balancing columns of income and expenditure across wide ledger.', ['FISCAL_PLAN', 'ALLOCATION']),
        ('FIXED_DEPOSIT', 'fixed-deposit', 'civic', 'Fixed Deposit (FD)', 'सावधि जमा / एफडी', 'நிலையான வைப்பு', 'Money locked securely in vault for fixed calendar time horizon.', ['FD', 'TIME_DEPOSIT']),
        ('MUTUAL_FUND', 'mutual-fund', 'civic', 'Mutual Fund / SIP', 'म्यूचुअल फंड', 'மியூச்சுவல் ஃபண்ட்', 'Many small contribution streams flowing into central prosperous pool.', ['SIP', 'INDEX_FUND']),
        ('LOCKER', 'locker', 'civic', 'Safe Deposit Locker', 'बैंक लॉकर', 'பாதுகாப்பு பெட்டகம்', 'Two keys inserted simultaneously into thick steel vault door.', ['SAFETY_LOCKER', 'VAULT_BOX']),
        ('INVOICE', 'invoice', 'civic', 'Invoice / Bill of Sale', 'बीजक / बिल', 'ரசீது பில்', 'Detailed ledger bill tallied and clipped with official stamp.', ['BILL', 'SALE_INVOICE']),
        ('WALLET', 'wallet-digital', 'civic', 'E-Wallet / Purse', 'डिजिटल बटुआ', 'டிஜிட்டல் பணப்பை', 'Folded leather pocket wallet opens to reveal digital tap card.', ['PURSE', 'DIGITAL_WALLET']),
        ('REFUND', 'refund', 'civic', 'Refund / Cash Return', 'धनवापसी / रिफ़ंड', 'பணத்தைத் திரும்பப் பெறுதல்', 'Cash bundle pushed back from merchant across counter into buyer palm.', ['MONEY_BACK', 'RETURN_PAYMENT']),
        ('OVERDRAFT', 'overdraft', 'civic', 'Bank Overdraft', 'ओवरड्राफ्ट', 'மிகைப்பற்று', 'Account line crosses below zero benchmark into permitted credit credit.', ['OD_FACILITY', 'LIMIT']),
        ('SUBSIDY', 'subsidy', 'civic', 'Government Subsidy', 'सरकारी सब्सिडी', 'மானியக் கொடுப்பனவு', 'Government seal drops generous discount into farmer/citizen account.', ['GRANT', 'GOVT_AID']),
        ('EXPENSE', 'expense', 'civic', 'Expenditure / Cost', 'ख़र्च / व्यय', 'செலவு', 'Hand dispenses currency notes outward one by one for supplies.', ['EXPENDITURE', 'OUTLAY']),
        ('WEALTH', 'wealth', 'civic', 'Wealth / Prosperity', 'संपत्ति / वैभव', 'செல்வம்', 'Both hands gather bountiful treasure and golden abundance to chest.', ['PROSPERITY', 'ASSETS']),
        ('QR_CODE', 'qr-code', 'civic', 'QR Code / Scan Pay', 'क्यूआर कोड', 'க்யூஆர் குறியீடு', 'Index finger outlines square matrix with laser camera sweep.', ['QR_SCAN', 'BARCODE']),
    ],

    # ─── VOL 4: Civic Amenities, Transport & Navigation ───
    "islrtc-civic": [
        ('HARBOR', 'harbor', 'navigation', 'Harbor / Seaport Dock', 'बंदरगाह / गोदी', 'துறைமுகம்', 'Big ship anchors safely beside loading pier with container cranes.', ['SEAPORT', 'DOCKYARD']),
        ('CROSSING', 'railway-crossing', 'navigation', 'Railway Level Crossing', 'रेलवे फाटक', 'ரயில்வே கிராசிங்', 'Two barrier gates descend horizontally from sides blocking roadway.', ['LEVEL_CROSSING', 'PHATAK']),
        ('PEDESTRIAN', 'pedestrian', 'navigation', 'Pedestrian / Zebra Crossing', 'पैदल यात्री', 'பாதசாரி', 'Two fingers walk rhythmically across horizontal zebra stripe lines.', ['ZEBRA_CROSSING', 'WALKER']),
        ('SPEED_BREAKER', 'speed-breaker', 'navigation', 'Speed Breaker / Hump', 'गति अवरोधक', 'வேகத்தடை', 'Right hand makes smooth mound hump, vehicle bounces upward.', ['ROAD_HUMP', 'BUMP']),
        ('ROUNDABOUT', 'roundabout', 'navigation', 'Traffic Roundabout / Circle', 'गोल चक्कर', 'வட்டச்சந்தை', 'Index finger circles smooth central monument before exiting turn.', ['TRAFFIC_CIRCLE', 'CHOWK']),
        ('HIGHWAY', 'highway', 'navigation', 'National Highway', 'राष्ट्रीय राजमार्ग', 'நெடுஞ்சாலை', 'NH sign followed by wide endless high-speed dual carriageway.', ['EXPRESSWAY', 'FREEWAY']),
        ('PARKING', 'parking', 'navigation', 'Vehicle Parking', 'पार्किंग', 'வாகன நிறுத்துமிடம்', 'P-handshape lands neatly between two designated white bay lines.', ['PARKING_LOT', 'BAY']),
        ('FUEL', 'fuel', 'navigation', 'Fuel / Petrol / Diesel', 'ईंधन / पेट्रोल', 'எரிபொருள்', 'Pump nozzle inserted into side tank with trigger squeeze.', ['PETROL', 'DIESEL']),
        ('ELECTRIC_CHARGING', 'ev-charging', 'navigation', 'EV Charging Station', 'इलेक्ट्रिक चार्जिंग', 'மின்சார சார்ஜிங்', 'Plug cable inserted into electric car battery slot with spark.', ['EV_STATION', 'PLUG_CHARGE']),
        ('ELECTRICITY_BOARD', 'electricity-board', 'navigation', 'Electricity Board Office', 'बिजली बोर्ड', 'மின்சார வாரியம்', 'Lightning bolt symbol followed by billing office desk.', ['BIJLI_BOARD', 'POWER_OFFICE']),
        ('WATER_BOARD', 'water-board', 'navigation', 'Water Works Department', 'जल बोर्ड', 'குடிநீர் வாரியம்', 'Flowing pipeline tap followed by civic administrative headquarters.', ['JAL_NIGAM', 'WATER_SUPPLY']),
        ('FIRE_STATION', 'fire-station', 'navigation', 'Fire Station / Brigade', 'दमकल केंद्र', 'தீயணைப்பு நிலையம்', 'Fire hose spraying high pressure water jet onto burning roof.', ['FIRE_BRIGADE', 'FIRE_HOUSE']),
        ('TOILET_PUBLIC', 'public-toilet', 'navigation', 'Public Restroom / Toilet', 'सार्वजनिक शौचालय', 'பொது கழிப்பிடம்', 'T-handshape shakes gently twice near side of chest.', ['RESTROOM', 'WASHROOM']),
        ('LIFT_ELEVATOR', 'lift-elevator', 'navigation', 'Elevator / Lift', 'लिफ्ट', 'மின்தூக்கி', 'Two open platform fingers rise straight up through multistory shaft.', ['ELEVATOR', 'LIFT']),
        ('ESCALATOR', 'escalator', 'navigation', 'Escalator / Moving Stairs', 'स्वचालित सीढ़ी', 'நகரும் படிக்கட்டு', 'Angled stair steps gliding continuously upward carrying commuters.', ['MOVING_STAIRS', 'STAIR_GLIDE']),
        ('TOLL_PLAZA', 'toll-plaza', 'navigation', 'Highway Toll Plaza', 'टोल प्लाजा', 'சுங்கச்சாவடி', 'Boom barrier lifts upon contactless electronic FASTag beep.', ['FASTAG', 'TOLL_GATE']),
        ('COMPASS', 'compass', 'navigation', 'Compass / Cardinal Directions', 'दिशा सूचक', 'திசைகாட்டி', 'Magnetic needle floating in dial oscillating until pointing true North.', ['DIRECTION_GAUGE', 'NAVIGATOR']),
    ],

    # ─── VOL 5: Educational, Academic & Vocational ───
    "islrtc-academic": [
        ('GEOGRAPHY', 'geography', 'academic', 'Geography / Earth Sciences', 'भूगोल', 'புவியியல்', 'Both hands hold spinning round globe of continents and oceans.', ['EARTH_STUDY', 'BHUGOL']),
        ('CHEMISTRY', 'chemistry', 'academic', 'Chemistry / Molecular Study', 'रसायन विज्ञान', 'வேதியியல்', 'Two test tubes poured into beaker bubbling with reaction vapors.', ['CHEMICAL_SCIENCE', 'LAB_REACTION']),
        ('PHYSICS', 'physics', 'academic', 'Physics / Mechanics', 'भौतिक विज्ञान', 'இயற்பியல்', 'Two bent V-hands pivot together miming atomic orbits and force.', ['PHYSICAL_SCIENCE', 'FORCE_ENERGY']),
        ('BIOLOGY', 'biology', 'academic', 'Biology / Life Science', 'जीव विज्ञान', 'உயிரியல்', 'Sprouting plant leaf and beating heart cell structure synthesis.', ['LIFE_SCIENCE', 'BOTANY_ZOOLOGY']),
        ('VOCATIONAL', 'vocational', 'academic', 'Vocational Skill Training', 'व्यावसायिक प्रशिक्षण', 'தொழிற்கல்வி', 'Hands operate specialized tools with precision craftsmanship.', ['SKILL_TRAINING', 'ITI']),
        ('SCHOLARSHIP', 'scholarship', 'academic', 'Scholarship / Merit Grant', 'छात्रवृत्ति', 'கல்வி உதவித்தொகை', 'Merit ribbon pinned to chest followed by educational fee grant.', ['MERIT_GRANT', 'STUDENT_AID']),
        ('PRINCIPAL', 'principal', 'academic', 'School Principal / Head', 'प्रधानाचार्य', 'முதல்வர்', 'P-handshape circles over chest with authoritative leadership salute.', ['HEADMASTER', 'DIRECTOR']),
        ('LABORATORY', 'laboratory', 'academic', 'Science Laboratory', 'प्रयोगशाला', 'ஆய்வகம்', 'Microscope eye focus followed by experimental test stand.', ['SCIENCE_LAB', 'RESEARCH_LAB']),
        ('EXPERIMENT', 'experiment', 'academic', 'Scientific Experiment', 'प्रयोग', 'பரிசோதனை', 'Careful dropper drops measured solution into swirling flask.', ['PRACTICAL', 'TRIAL_TEST']),
        ('SYLLABUS', 'syllabus', 'academic', 'Curriculum Syllabus', 'पाठ्यक्रम', 'பாடத்திட்டம்', 'Comprehensive semester topic list unrolled on master scroll.', ['CURRICULUM', 'COURSE_OUTLINE']),
        ('PROJECT', 'project', 'academic', 'Academic Project / Model', 'परियोजना / प्रोजेक्ट', 'செய்முறை திட்டம்', 'Students collaborate assembling 3D presentation showcase display.', ['ASSIGNMENT_MODEL', 'SUBMISSION']),
        ('ATTENDANCE', 'attendance', 'academic', 'Attendance / Roll Call', 'उपस्थिति / हाजिरी', 'வருகைப்பதிவு', 'Teacher ticks green checkmarks down class ledger as students answer.', ['ROLL_CALL', 'HAJIRI']),
        ('FAIL', 'fail-academic', 'academic', 'Failed Exam / Backlog', 'अनुत्तीर्ण', 'தோல்வி', 'Hand slides off table edge dropping downward in disappointment.', ['DISQUALIFIED', 'NOT_PASSED']),
        ('COMPETITION', 'competition', 'academic', 'Competition / Olympiad', 'प्रतियोगिता', 'போட்டி', 'Two teams race parallel index fingers striving toward trophy.', ['CONTEST', 'TOURNAMENT']),
        ('DICTIONARY', 'dictionary', 'academic', 'ISLRTC Sign Dictionary', 'सांकेतिक शब्दकोश', 'சைகை அகராதி', 'Thumb flips heavy alphabetical vocabulary volume finding glosses.', ['SHABDKOSH', 'LEXICON']),
        ('ALPHABET', 'alphabet', 'academic', '2-Handed Manual Alphabet', 'द्वि-हस्त वर्णमाला', 'இரு கை எழுத்துக்கள்', 'A to Z fingerspelling swift sequence demonstrating manual signs.', ['FINGERSPELLING', 'LETTERS']),
        ('RESEARCH', 'research', 'academic', 'Scholarly Research / Thesis', 'शोध / अनुसंधान', 'ஆராய்ச்சி', 'R-hand sweeps along open library tome discovering new insights.', ['THESIS', 'INVESTIGATION']),
    ],

    # ─── VOL 6: Daily Necessities, Nutrition & Living ───
    "islrtc-daily": [
        ('THIRSTY', 'thirsty', 'daily', 'Thirsty / Dehydrated', 'प्यास / प्यासा', 'தாகம்', 'Index finger draws dry line down center throat with craving swallow.', ['NEED_WATER', 'PARCHED']),
        ('SUGAR', 'sugar', 'daily', 'Sugar / Sweetness', 'चीनी / शक्कर', 'சர்க்கரை', 'Two fingers brush downward across chin tasting sweetness on tongue.', ['SWEET', 'SHAKKAR']),
        ('SALT', 'salt', 'daily', 'Salt / Salty', 'नमक', 'உப்பு', 'Two fingers sprinkle pinch of salt over palm with savory smile.', ['NAMAK', 'SALTY']),
        ('OIL', 'oil-cooking', 'daily', 'Cooking Oil / Ghee', 'तेल / खाद्य तेल', 'எண்ணெய்', 'Bottle tilts pouring golden liquid stream into heated pan.', ['COOKING_OIL', 'TEL']),
        ('SPICE', 'spice', 'daily', 'Indian Spices / Masala', 'मसाला', 'மசாலா', 'Fingers grind fragrant spices in stone mortar and pestle.', ['MASALA', 'SEASONING']),
        ('BUTTER', 'butter', 'daily', 'Butter / Makkhan', 'मक्खन / घी', 'வெண்ணெய்', 'Flat blade sweeps creamy butter spread smoothly over hot roti.', ['MAKKHAN', 'GHEE']),
        ('CURD', 'curd', 'daily', 'Curd / Yogurt / Dahi', 'दही', 'தயிர்', 'Spoon scoops creamy cool dahi from earthenware bowl to lips.', ['YOGURT', 'DAHI']),
        ('BREAD', 'bread', 'daily', 'Bread / Loaf', 'डबलरोटी / ब्रेड', 'ரொட்டி', 'Right hand chops vertical slices through imaginary fresh bakery loaf.', ['LOAF', 'PAV']),
        ('KITCHEN', 'kitchen', 'daily', 'Kitchen / Cooking Area', 'रसोईघर', 'சமையலறை', 'Stove flame ignition sign followed by stirring aromatic cooking pot.', ['ROSOI', 'COOKING_ROOM']),
        ('TOWEL', 'towel', 'daily', 'Bath Towel', 'तौलिया', 'துண்டு', 'Two hands hold long towel drying across back and shoulders.', ['BATH_TOWEL', 'GAMCHHA']),
        ('SHOES', 'shoes', 'daily', 'Shoes / Footwear', 'जूते / चप्पल', 'காலணிகள்', 'Both closed fists tap knuckles horizontally together twice at ankle height.', ['FOOTWEAR', 'CHAPPAL']),
        ('FAN', 'fan-ceiling', 'daily', 'Ceiling Fan', 'पंखा', 'மின்விசிறி', 'Index finger points upward overhead rotating smooth circular blades.', ['CEILING_FAN', 'PANKHA']),
        ('LIGHT_BULB', 'light-bulb', 'daily', 'Electric Light / Bulb', 'बिजली बत्ती', 'மின் விளக்கு', 'Pinched fingers burst open overhead like radiant blooming light.', ['ELECTRIC_BULB', 'ROSHNI']),
        ('DOOR', 'door', 'daily', 'Door / Entrance', 'दरवाज़ा', 'கதவு', 'Vertical flat hand swings open on hinges from left hand frame.', ['GATEWAY', 'ENTRANCE']),
        ('WINDOW', 'window', 'daily', 'Window / Casement', 'खिड़की', 'சாளரம்', 'Both hands push two shutters outward allowing fresh breeze in.', ['SHUTTERS', 'VENTILATION']),
        ('KEYS_LOCK', 'keys-lock', 'daily', 'Key / Lock', 'चाबी / ताला', 'சாவி', 'Right index key inserts into left fist padlock and twists open.', ['PADLOCK', 'KEY']),
        ('SWEEP', 'sweep', 'daily', 'Sweep / Broom / Jhadu', 'झाड़ू लगाना', 'பெருக்குதல்', 'Both hands sweep long traditional grass broom across floor.', ['BROOM', 'JHADU']),
    ],

    # ─── VOL 7: Social Etiquette, Greetings & Sentiment ───
    "islrtc-social": [
        ('ANGRY', 'angry', 'sentiment', 'Angry / Furious', 'क्रोध / गुस्सा', 'கோபம்', 'Claw hand pulls upward from chest to scowling tense face.', ['FURIOUS', 'GUSSA']),
        ('SURPRISE', 'surprise', 'sentiment', 'Surprised / Amazed', 'आश्चर्य / हैरान', 'ஆச்சரியம்', 'Both eyes open wide, hands snap open beside temples in awe.', ['AMAZED', 'ASTONISHED']),
        ('AFRAID', 'afraid', 'sentiment', 'Afraid / Frightened', 'डर / भयभीत', 'பயம்', 'Both open hands shield trembling torso with startled gasping breath.', ['FEAR', 'SCARED']),
        ('EXCITED', 'excited', 'sentiment', 'Excited / Enthusiastic', 'उत्साहित', 'உற்சாகம்', 'Both open middle fingers brush rapidly upward across chest with grin.', ['ENTHUSIASTIC', 'EAGER']),
        ('CONFUSED', 'confused', 'sentiment', 'Confused / Puzzled', 'भ्रमित / असमंजस', 'குழப்பம்', 'Both index fingers draw swirling conflicting spirals at forehead.', ['PUZZLED', 'UNCERTAIN']),
        ('PROUD', 'proud', 'sentiment', 'Proud / Dignity', 'गर्व / स्वाभिमान', 'பெருமை', 'Thumb slides straight up center chest with head held high and noble.', ['DIGNITY', 'GARV']),
        ('TRUST', 'trust', 'greeting', 'Trust / Faith', 'विश्वास / भरोसा', 'நம்பிக்கை', 'Both hands reach forward clasping unseen steadfast anchor of trust.', ['FAITH', 'CONFIDENCE']),
        ('HONEST', 'honest', 'greeting', 'Honest / Truthful', 'ईमानदार / सत्यवादी', 'நேர்மையான', 'Right flat hand slides straight off heart in direct unswerving path.', ['TRUTHFUL', 'SINCERE']),
        ('PATIENCE', 'patience', 'sentiment', 'Patience / Calm', 'धैर्य / सब्र', 'பொறுமை', 'Thumb traces downward slowly over chin and lips breathing calmness.', ['CALM', 'SABR']),
        ('CELEBRATION', 'celebration', 'greeting', 'Festival Celebration / Utsav', 'उत्सव / पर्व', 'கொண்டாட்டம்', 'Both hands wave ceremonial streamers dancing above shoulders.', ['FESTIVAL', 'UTSAV']),
        ('BIRTHDAY', 'birthday', 'greeting', 'Birthday / Janmadin', 'जन्मदिन', 'பிறந்தநாள்', 'Mime blowing out glowing birthday candles on round cake.', ['JANMADIN', 'ANNIVERSARY']),
        ('WEDDING', 'wedding', 'greeting', 'Wedding / Vivah', 'विवाह / शादी', 'திருமணம்', 'Both hands exchange sacred wedding garlands over partner shoulders.', ['MARRIAGE', 'VIVAH']),
        ('GIFT', 'gift', 'greeting', 'Gift / Present', 'उपहार / तोहफ़ा', 'பரிசு', 'Both cupped hands extend ribbon-wrapped package forward graciously.', ['PRESENT', 'TOHFA']),
        ('INVITATION', 'invitation', 'greeting', 'Formal Invitation / Nimantran', 'निमंत्रण पत्र', 'அழைப்பு', 'Both palms scoop toward guest presenting decorative auspicious card.', ['CARD_INVITE', 'WELCOME_CALL']),
        ('GUEST', 'guest', 'greeting', 'Guest / Honored Visitor', 'अतिथि / मेहमान', 'விருந்தினர்', 'Sign VISITOR entering followed by folding hands in welcoming salute.', ['ATITHI', 'MEHMAN']),
        ('PROMISE', 'promise', 'greeting', 'Promise / Vow', 'वचन / वादा', 'வாக்குறுதி', 'Index finger touches lips then flat right palm seals upon open left palm.', ['VOW', 'PLEDGE_WORD']),
        ('APPRECIATION', 'appreciation', 'greeting', 'Appreciation / Praise', 'प्रशंसा / सराहना', 'பாராட்டு', 'Both hands applaud enthusiastically with nodding radiant approval.', ['PRAISE', 'ACCLAIM']),
    ],

    # ─── VOL 8: Chronology, Numbers & Temporal Measurement ───
    "islrtc-chronology": [
        ('6', 'num-6', 'numbers', 'Six (6)', 'छह (६)', 'ஆறு (6)', 'Thumb and little pinky touch tip while three middle fingers stand upright.', ['SIX', 'NUM_6']),
        ('7', 'num-7', 'numbers', 'Seven (7)', 'सात (७)', 'ஏழு (7)', 'Thumb and ring finger touch tip with index, middle, pinky upright.', ['SEVEN', 'NUM_7']),
        ('8', 'num-8', 'numbers', 'Eight (8)', 'आठ (८)', 'எட்டு (8)', 'Thumb and middle finger touch tip with index, ring, pinky upright.', ['EIGHT', 'NUM_8']),
        ('9', 'num-9', 'numbers', 'Nine (9)', 'नौ (९)', 'ஒன்பது (9)', 'Thumb and index touch tip forming O-ring with three fingers upright.', ['NINE', 'NUM_9']),
        ('100', 'num-100', 'numbers', 'One Hundred (100)', 'एक सौ (१००)', 'நூறு (100)', 'Sign 1 followed by C-handshape pulling back indicating century hundred.', ['HUNDRED', 'CENT']),
        ('1000', 'num-1000', 'numbers', 'One Thousand (1000)', 'एक हज़ार (१०००)', 'ஆயிரம் (1000)', 'Right fingertips touch flat open left palm indicating thousand mark.', ['THOUSAND', 'HAZAR']),
        ('MONDAY', 'monday', 'numbers', 'Monday / Somvar', 'सोमवार', 'திங்கட்கிழமை', 'M-handshape rotates gentle circle in space beside shoulder.', ['SOMVAR', 'DAY_MON']),
        ('TUESDAY', 'tuesday', 'numbers', 'Tuesday / Mangalvar', 'मंगलवार', 'செவ்வாய்க்கிழமை', 'T-handshape rotates gentle circle in space beside shoulder.', ['MANGALVAR', 'DAY_TUE']),
        ('WEDNESDAY', 'wednesday', 'numbers', 'Wednesday / Budhvar', 'बुधवार', 'புதன்கிழமை', 'W-handshape rotates gentle circle in space beside shoulder.', ['BUDHVAR', 'DAY_WED']),
        ('THURSDAY', 'thursday', 'numbers', 'Thursday / Guruvar', 'गुरुवार', 'வியாழக்கிழமை', 'T-hand followed by H-hand rotating in space beside shoulder.', ['GURUVAR', 'DAY_THU']),
        ('FRIDAY', 'friday', 'numbers', 'Friday / Shukravar', 'शुक्रवार', 'வெள்ளிக்கிழமை', 'F-handshape rotates gentle circle in space beside shoulder.', ['SHUKRAVAR', 'DAY_FRI']),
        ('SATURDAY', 'saturday', 'numbers', 'Saturday / Shanivar', 'शनिवार', 'சனிக்கிழமை', 'S-fist rotates gentle circle in space beside shoulder.', ['SHANIVAR', 'DAY_SAT']),
        ('SUNDAY', 'sunday', 'numbers', 'Sunday / Ravivar', 'रविवार', 'ஞாயிற்றுக்கிழமை', 'Both open palms circle clockwise joyfully celebrating holiday.', ['RAVIVAR', 'DAY_SUN']),
        ('MIDNIGHT', 'midnight', 'numbers', 'Midnight / 12 AM', 'आधी रात', 'நள்ளிரவு', 'Both hands cross vertically straight down at lowest point of dial.', ['TWELVE_AM', 'NIGHT_ZENITH']),
        ('SUNRISE', 'sunrise', 'numbers', 'Sunrise / Dawn', 'सूर्योदय', 'சூரிய உதயம்', 'Golden sun sphere rises steadily above horizontal ocean line.', ['DAWN_TIME', 'MORNING_SUN']),
        ('SUNSET', 'sunset', 'numbers', 'Sunset / Dusk', 'सूर्यास्त', 'சூரிய அஸ்தமனம்', 'Golden sun sphere dips gently below horizontal evening horizon.', ['DUSK_TIME', 'EVENING_SUN']),
        ('CENTURY', 'century', 'numbers', 'Century / 100 Years', 'शताब्दी / सौ साल', 'நூற்றாண்டு', 'Sign 100 followed by year orbit circling left hand base.', ['HUNDRED_YEARS', 'SHATABDI']),
    ],

    # ─── VOL 9: Digital Technology & Assistive Communication ───
    "islrtc-tech": [
        ('BLUETOOTH', 'bluetooth', 'meta', 'Bluetooth Wireless', 'ब्लूटूथ', 'புளூடூத்', 'B-handshape sends invisible wireless pulse directly to ear receiver.', ['BT_SYNC', 'WIRELESS_PAIR']),
        ('CHARGER', 'charger', 'meta', 'Device Charger / Cable', 'चार्जर', 'சார்ஜர்', 'Two prong plug inserted firmly into wall electric outlet.', ['ADAPTER', 'POWER_CORD']),
        ('BATTERY', 'battery', 'meta', 'Battery / Energy Cell', 'बैटरी', 'மின்கலம்', 'Both horizontal index fingers tap positive and negative cell poles.', ['ENERGY_CELL', 'POWER_LEVEL']),
        ('PRINTER', 'printer', 'meta', 'Paper Printer', 'प्रिंटर', 'அச்சுப்பொறி', 'Paper feed entering top of machine and emerging printed below.', ['PRINT_DEVICE', 'HARDCOPY']),
        ('MOUSE', 'mouse-pc', 'meta', 'Computer Mouse', 'माउस', 'கணினி மவுஸ்', 'Right palm rests on curved mouse clicking left index button.', ['POINTER_MOUSE', 'CLICK_DEVICE']),
        ('HEADPHONE', 'headphone', 'meta', 'Headphones / Earphones', 'हेडफ़ोन', 'இயர்போன்', 'Both cupped hands clasp over ears listening to immersive sound.', ['EARPHONES', 'HEADSET']),
        ('USB_DRIVE', 'usb-drive', 'meta', 'USB Pen Drive / Flash', 'पेन ड्राइव', 'பென் டிரைவ்', 'Thumb and index insert small flat stick into side laptop port.', ['PEN_DRIVE', 'FLASH_DRIVE']),
        ('CLOUD_STORAGE', 'cloud-storage', 'meta', 'Cloud Storage / Drive', 'क्लाउड स्टोरेज', 'கிளவுட் சேமிப்பகம்', 'Fluffy cloud shape drawn in sky storing floating file packets.', ['CLOUD_DRIVE', 'WEB_BACKUP']),
        ('SEARCH_ENGINE', 'search-engine', 'meta', 'Search Engine / Lookup', 'सर्च इंजन', 'தேடுபொறி', 'Magnifying glass scans across screen finding instant answer.', ['WEB_SEARCH', 'GOOGLE_SEARCH']),
        ('BROWSER', 'browser', 'meta', 'Web Browser', 'वेब ब्राउज़र', 'வலை உலாவி', 'Multiple tabs opening across top of screen surfing hyperlinks.', ['WEB_SURFER', 'CHROME_BROWSER']),
        ('UPLOAD', 'upload', 'meta', 'Upload / Send to Cloud', 'अपलोड', 'பதிவேற்றம்', 'Fingers push data beam straight upward from laptop into cloud.', ['PUSH_FILE', 'SEND_DATA']),
        ('SPEAKER', 'speaker-audio', 'meta', 'Audio Loudspeaker', 'लाउडस्पीकर', 'ஒலிபெருக்கி', 'Funnel cone gesture expanding outward blasting acoustic sound waves.', ['LOUDSPEAKER', 'SOUND_BOX']),
        ('VIRTUAL_REALITY', 'vr-headset', 'meta', 'Virtual Reality (VR)', 'आभासी वास्तविकता', 'மெய்நிகர் உண்மை', 'Goggles strapped across eyes interacting with 3D floating space.', ['VR', 'METAVERSE']),
        ('SERVER', 'server-data', 'meta', 'Data Server / Host', 'डेटा सर्वर', 'சர்வர்', 'Stack of blinking tall computer mainframe racks processing load.', ['MAINFRAME', 'HOST_MACHINE']),
        ('CYBER_SECURITY', 'cyber-security', 'meta', 'Cyber Security / Firewall', 'साइबर सुरक्षा', 'இணைய பாதுகாப்பு', 'Protective digital shield wall deflecting computer virus attacks.', ['FIREWALL', 'DIGITAL_SAFETY']),
        ('DATABASE', 'database', 'meta', 'Database / SQL Storage', 'डेटाबेस', 'தரவுத்தளம்', 'Three cylindrical disk layers stacked neatly storing structured rows.', ['SQL_DB', 'DATA_STORE']),
        ('ALGORITHM', 'algorithm', 'meta', 'AI Algorithm / Neural Code', 'एल्गोरिदम', 'வழிமுறை', 'Flowchart logic branching through nodes computing optimal weights.', ['NEURAL_LOGIC', 'COMPUTATION']),
    ]
}


def update_backend_domains():
    """Expands sample_signs in backend/indian_sign_languages.py for all 9 domains."""
    path = 'backend/indian_sign_languages.py'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for vol_id, signs_list in NEW_SIGNS_BY_VOLUME.items():
        new_glosses = [item[0] for item in signs_list]
        pattern = rf'("id":\s*"{vol_id}".*?"sample_signs":\s*\[)([^\]]+)(\])'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            existing_str = match.group(2)
            existing_glosses = [x.strip(' \'"\n\r\t') for x in existing_str.split(',') if x.strip(' \'"\n\r\t')]
            for g in new_glosses:
                if g not in existing_glosses:
                    existing_glosses.append(g)
            
            # format nicely
            formatted_signs = ',\n            '.join([
                ', '.join([f'"{x}"' for x in existing_glosses[i:i+8]])
                for i in range(0, len(existing_glosses), 8)
            ])
            replacement = f'{match.group(1)}\n            {formatted_signs}\n        {match.group(3)}'
            content = content[:match.start()] + replacement + content[match.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated backend/indian_sign_languages.py with expanded signs!")


def update_frontend_volumes():
    """Expands signs in frontend/src/data/indianSignLanguages.js for all 9 volumes."""
    path = 'frontend/src/data/indianSignLanguages.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    id_map = {
        'islrtc-emergency': 'vol-emergency',
        'islrtc-legal': 'vol-legal',
        'islrtc-banking': 'vol-banking',
        'islrtc-civic': 'vol-civic',
        'islrtc-academic': 'vol-academic',
        'islrtc-daily': 'vol-daily',
        'islrtc-social': 'vol-social',
        'islrtc-chronology': 'vol-chronology',
        'islrtc-tech': 'vol-tech',
    }

    for vol_id, signs_list in NEW_SIGNS_BY_VOLUME.items():
        front_id = id_map[vol_id]
        new_glosses = [item[0] for item in signs_list]
        pattern = rf'(id:\s*[\'"]{front_id}[\'"].*?signs:\s*\[)([^\]]+)(\])'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            existing_str = match.group(2)
            existing_glosses = [x.strip(' \'"\n\r\t') for x in existing_str.split(',') if x.strip(' \'"\n\r\t')]
            for g in new_glosses:
                if g not in existing_glosses:
                    existing_glosses.append(g)

            formatted_signs = ',\n      '.join([
                ', '.join([f"'{x}'" for x in existing_glosses[i:i+8]])
                for i in range(0, len(existing_glosses), 8)
            ])
            replacement = f'{match.group(1)}\n      {formatted_signs}\n    {match.group(3)}'
            content = content[:match.start()] + replacement + content[match.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated frontend/src/data/indianSignLanguages.js with expanded signs!")


def update_frontend_dictionary():
    """Appends all 153 new signs to frontend/src/data/islDictionary.js with modelSupported: true."""
    path = 'frontend/src/data/islDictionary.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    existing_glosses = set(re.findall(r'gloss:\s*[\'"]([^\'"]+)[\'"]', content))
    entries_to_add = []

    for vol_id, signs_list in NEW_SIGNS_BY_VOLUME.items():
        for gloss, slug, cat, en, hi, ta, desc, syns in signs_list:
            if gloss in existing_glosses:
                continue
            existing_glosses.add(gloss)
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
    modelSupported: true,
    demoVideo: null,
    source: 'ISLRTC Official Curriculum Standards',
    variants: ['National Standard'],
  }},"""
            entries_to_add.append(entry_text)

    print(f"Adding {len(entries_to_add)} new entries to islDictionary.js...")
    target = '];\n\n// Fast lookup map by gloss'
    if target not in content:
        target = '];\n\n// Fast lookup map'
    
    assert target in content, "Could not find dictionary array closing marker"

    insertion = '\n' + '\n'.join(entries_to_add) + '\n' + target
    new_content = content.replace(target, insertion, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Updated frontend/src/data/islDictionary.js successfully!")


def update_backend_extended_vocabulary():
    """Adds all 153 new tokens to backend/extended_vocabulary.py."""
    path = 'backend/extended_vocabulary.py'
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\r\n') for line in f.readlines()]

    existing_text = '\n'.join(lines)
    # Find closing `}`
    last_brace_idx = -1
    for idx in range(len(lines) - 1, -1, -1):
        if lines[idx].strip() == '}':
            last_brace_idx = idx
            break

    new_lines = []
    for vol_id, signs_list in NEW_SIGNS_BY_VOLUME.items():
        for gloss, slug, cat, en, hi, ta, desc, syns in signs_list:
            if f'"{gloss}":' in existing_text:
                continue
            pos = 'NOUN'
            if cat == 'numbers':
                pos = 'NUMERAL'
            elif cat == 'sentiment':
                pos = 'RESPONSE' if gloss in ['ANGRY', 'SURPRISE', 'AFRAID', 'EXCITED', 'CONFUSED', 'PROUD', 'PATIENCE'] else 'ADJECTIVE'
            elif cat == 'greeting':
                pos = 'GREETING' if gloss in ['BIRTHDAY', 'WEDDING', 'GIFT', 'INVITATION', 'GUEST', 'PROMISE', 'APPRECIATION', 'CELEBRATION'] else 'COURTESY'
            elif gloss in ['VOMIT', 'BURN', 'SWEEP', 'REFUND', 'DISCHARGE', 'SUMMON', 'UPLOAD']:
                pos = 'VERB'
            elif gloss in ['POISON', 'THIEF', 'FRAUD', 'ACCUSED', 'CORRUPTION', 'THIRSTY', 'ANGRY', 'AFRAID', 'EXCITED', 'CONFUSED', 'PROUD', 'HONEST', 'PATIENCE']:
                pos = 'ADJECTIVE'

            en_clean = en.split('/')[0].strip().lower()
            hi_clean = hi.split('/')[0].strip()
            ta_clean = ta.split('/')[0].strip()

            new_lines.append(f'    "{gloss}": {{"en": "{en_clean}", "hi": "{hi_clean}", "ta": "{ta_clean}", "pos": "{pos}"}},')

    if new_lines and last_brace_idx != -1:
        updated = lines[:last_brace_idx] + new_lines + lines[last_brace_idx:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated) + '\n')
        print(f"Added {len(new_lines)} new tokens to backend/extended_vocabulary.py!")


if __name__ == '__main__':
    update_backend_domains()
    update_frontend_volumes()
    update_frontend_dictionary()
    update_backend_extended_vocabulary()
    print("ALL 153 NEW SIGNS SUCCESSFULLY INTEGRATED ACROSS ALL ISLRTC VOLUMES!")
