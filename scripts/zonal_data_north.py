# scripts/zonal_data_north.py
"""
Standard ISL — Northern Zone Chapter (isl-north) - 100 Domain Specific Signs
Focus: Delhi NCR, Punjab, UP, Haryana, Himachal, J&K, Uttarakhand, Chandigarh.
Northern administrative centers, agrarian heartland (wheat, mandis, MSP, irrigation),
seasonal weather extremes (fog, loo, snow), Delhi Metro, Northern festivals and staples.
"""

NORTH_SIGNS = [
    {
        "gloss": "DELHI",
        "en": "Delhi / National Capital Territory",
        "hi": "दिल्ली / राष्ट्रीय राजधानी क्षेत्र",
        "ta": "தில்லி",
        "category": "navigation",
        "description": "Fingerspell D-L, followed by pointing toward India Gate monument gesture."
    },
    {
        "gloss": "CHANDIGARH",
        "en": "Chandigarh / City Beautiful",
        "hi": "चंडीगढ़",
        "ta": "சண்டிகர்",
        "category": "navigation",
        "description": "Open hand palm forward pivoting in grid layout mimicking Le Corbusier sector plan."
    },
    {
        "gloss": "LUCKNOW",
        "en": "Lucknow / City of Nawabs",
        "hi": "लखनऊ",
        "ta": "லக்னோ",
        "category": "navigation",
        "description": "Polite tehzeeb hand over heart bowing gently, followed by Rumi Darwaza arch outline."
    },
    {
        "gloss": "AMRITSAR",
        "en": "Amritsar / Holy City",
        "hi": "अमृतसर",
        "ta": "அமிர்தசரஸ்",
        "category": "navigation",
        "description": "Dip fingertips into holy nectar pool, then bring hands to heart in reverence."
    },
    {
        "gloss": "JAIPUR",
        "en": "Jaipur / Pink City",
        "hi": "जयपुर / गुलाबी नगर",
        "ta": "ஜெய்ப்பூர்",
        "category": "navigation",
        "description": "Pink color sign touching cheek, followed by Hawa Mahal multi-window latticework gesture."
    },
    {
        "gloss": "SRINAGAR",
        "en": "Srinagar / Dal Lake Valley",
        "hi": "श्रीनगर / डल झील",
        "ta": "ஸ்ரீநகர்",
        "category": "navigation",
        "description": "Both hands paddle a wooden shikara boat gently over tranquil mountain waters."
    },
    {
        "gloss": "DEHRADUN",
        "en": "Dehradun / Doon Valley",
        "hi": "देहरादून",
        "ta": "டேராடூன்",
        "category": "navigation",
        "description": "Both hands trace valley between Shivalik hills and high Himalayan ridges."
    },
    {
        "gloss": "SHIMLA",
        "en": "Shimla / Summer Capital Hill Station",
        "hi": "शिमला / देवभूमि",
        "ta": "சிம்லா",
        "category": "navigation",
        "description": "Shiver from alpine pine chill, followed by toy train winding up misty ridges."
    },
    {
        "gloss": "YAMUNA_RIVER",
        "en": "Yamuna River",
        "hi": "यमुना नदी",
        "ta": "யமுனை ஆறு",
        "category": "navigation",
        "description": "Wavy river gesture flowing along Delhi ghats past Red Fort."
    },
    {
        "gloss": "GANGA_RIVER",
        "en": "Ganga River / Holy Ganges",
        "hi": "गंगा नदी / भागीरथी",
        "ta": "கங்கை ஆறு",
        "category": "navigation",
        "description": "Holy water poured gently from copper vessel into cupped palms at Haridwar ghats."
    },
    {
        "gloss": "SUTLEJ_RIVER",
        "en": "Sutlej River / Punjab Waters",
        "hi": "सतलुज नदी",
        "ta": "சத்லஜ் ஆறு",
        "category": "navigation",
        "description": "Fast rushing alpine river waters descending into Punjab canal network."
    },
    {
        "gloss": "HIMALAYAS",
        "en": "Himalayas / Snow Mountains",
        "hi": "हिमालय पर्वतमाला",
        "ta": "இமயமலை",
        "category": "navigation",
        "description": "Both arms elevate forming towering majestic snow-capped jagged peaks."
    },
    {
        "gloss": "COLD_WEATHER",
        "en": "Cold Weather / Winter Season",
        "hi": "ठंड का मौसम / शीतकाल",
        "ta": "குளிர்காலம்",
        "category": "daily",
        "description": "Cross arms over chest, shiver shoulders with clattering teeth non-manual expression."
    },
    {
        "gloss": "FOG_SMOG",
        "en": "Dense Fog / Northern Winter Smog / Kohra",
        "hi": "घना कोहरा / धुंध",
        "ta": "பனிமூட்டம்",
        "category": "daily",
        "description": "Both spread hands move in front of eyes blurring vision, squinting forward."
    },
    {
        "gloss": "LOO_HEATWAVE",
        "en": "Loo / Scorching Northern Summer Heatwave",
        "hi": "लू / ग्रीष्म लहर",
        "ta": "அனல் காற்று",
        "category": "daily",
        "description": "Wave hands rapidly fanning face with panting breath and wiping brow."
    },
    {
        "gloss": "SNOWFALL",
        "en": "Snowfall / Snow Flakes",
        "hi": "बर्फबारी / हिमपात",
        "ta": "பனிப்பொழிவு",
        "category": "daily",
        "description": "Fingers flutter softly drifting down from upper space settling on shoulders."
    },
    {
        "gloss": "METRO",
        "en": "Delhi Metro / Rapid Rail Transit",
        "hi": "दिल्ली मेट्रो",
        "ta": "மெட்ரோ ரயில்",
        "category": "navigation",
        "description": "Both hands form train sliding along overhead elevated track, then underground tunnel tap."
    },
    {
        "gloss": "BUS_TERMINAL",
        "en": "ISBT Bus Terminal / Inter-State Bus Terminus",
        "hi": "बस टर्मिनल / आईएसबीटी",
        "ta": "பேருந்து நிலையம்",
        "category": "navigation",
        "description": "Steering wheel motion followed by row of buses parked in angled bays."
    },
    {
        "gloss": "INTERSTATE_BUS",
        "en": "Interstate Roadways Bus / Haryana & Punjab Roadways",
        "hi": "रोडवेज बस / अंतरराज्यीय बस",
        "ta": "மாநிலங்களிடை பேருந்து",
        "category": "navigation",
        "description": "Heavy bus steering with pneumatic horn double honk gesture."
    },
    {
        "gloss": "RING_ROAD",
        "en": "Ring Road / Arterial Orbital Highway",
        "hi": "रिंग रोड / परिक्रमा मार्ग",
        "ta": "வட்டச் சாலை",
        "category": "navigation",
        "description": "Both index fingers trace broad continuous loop circling the capital city."
    },
    {
        "gloss": "FLYOVER",
        "en": "Flyover / Elevated Bypass Viaduct",
        "hi": "फ्लाईओवर / उपरिगामी पुल",
        "ta": "மேம்பாலம்",
        "category": "navigation",
        "description": "One hand drives over an arched bridge while traffic flows underneath on flat palm."
    },
    {
        "gloss": "TOLL_PLAZA",
        "en": "Toll Plaza / FASTag Highway Barrier",
        "hi": "टोल प्लाजा / चुंगी नाका",
        "ta": "சுங்கச்சாவடி",
        "category": "navigation",
        "description": "Barrier arm lifts up automatically as digital windshield RFID tag beeps."
    },
    {
        "gloss": "HIGHWAY_NH44",
        "en": "National Highway NH44 / Grand Trunk Route",
        "hi": "राष्ट्रीय राजमार्ग 44 / जीटी रोड",
        "ta": "தேசிய நெடுஞ்சாலை 44",
        "category": "navigation",
        "description": "Straight forward speed cruise along infinite North-South grand trunk corridor."
    },
    {
        "gloss": "DISTRICT_MAGISTRATE",
        "en": "District Magistrate / DM / Collector",
        "hi": "जिलाधिकारी / डीएम",
        "ta": "மாவட்ட ஆட்சியர்",
        "category": "civic",
        "description": "Fingerspell D-M, executive pen sign authorizing district administrative orders."
    },
    {
        "gloss": "TEHSILDAR",
        "en": "Tehsildar / Sub-Divisional Revenue Officer",
        "hi": "तहसीलदार / राजस्व अधिकारी",
        "ta": "தாசில்தார்",
        "category": "civic",
        "description": "Review revenue land records ledger and stamp official sub-division seal."
    },
    {
        "gloss": "PATWARI",
        "en": "Patwari / Village Land Records Keeper",
        "hi": "पटवारी / लेखपाल",
        "ta": "கிராம நிர்வாக அலுவலர்",
        "category": "civic",
        "description": "Unroll cloth land map (shajra) and measure agricultural boundaries with brass chain."
    },
    {
        "gloss": "COLLECTORATE",
        "en": "Collectorate / District Administrative HQ",
        "hi": "कलेक्ट्रेट / जिला मुख्यालय",
        "ta": "மாவட்ட ஆட்சியர் அலுவலகம்",
        "category": "civic",
        "description": "Flagpole outside grand administrative building housing all district services."
    },
    {
        "gloss": "SECRETARIAT_CIVIL",
        "en": "Civil Secretariat / Sachivalaya",
        "hi": "नागरिक सचिवालय",
        "ta": "சிவில் செயலகம்",
        "category": "civic",
        "description": "Multi-story government administrative corridors with files moving between departments."
    },
    {
        "gloss": "HIGH_COURT_BENCH",
        "en": "High Court Bench / Allahabad & Delhi High Court",
        "hi": "उच्च न्यायालय खंडपीठ",
        "ta": "உயர் நீதிமன்ற அமர்வு",
        "category": "civic",
        "description": "Gavel rapped on podium, two advocates arguing before elevated bench of judges."
    },
    {
        "gloss": "SESSION_COURT",
        "en": "District & Sessions Court",
        "hi": "जिला एवं सत्र न्यायालय",
        "ta": "மாவட்ட மற்றும் அமர்வு நீதிமன்றம்",
        "category": "civic",
        "description": "Witness box gesture with right hand raised on oath stand."
    },
    {
        "gloss": "POLICE_CHOWKI",
        "en": "Police Chowki / Police Outpost",
        "hi": "पुलिस चौकी",
        "ta": "காவல் புறக்காவல் நிலையம்",
        "category": "emergency",
        "description": "Barricade check-post gesture with khaki cap salute."
    },
    {
        "gloss": "THANA",
        "en": "Police Station / Kotwali / Thana",
        "hi": "थाना / कोतवाली",
        "ta": "காவல் நிலையம்",
        "category": "emergency",
        "description": "FIR register entry motion followed by detention cell door locking gesture."
    },
    {
        "gloss": "WHEAT",
        "en": "Wheat Crop / Gehun",
        "hi": "गेहूं की फसल",
        "ta": "கோதுமை",
        "category": "daily",
        "description": "Mime golden wheat spikelets swaying in the breeze and grain rub between palms."
    },
    {
        "gloss": "BASMATI_RICE",
        "en": "Basmati Rice / Aromatic Grain",
        "hi": "बासमती चावल",
        "ta": "பாசுமதி அரிசி",
        "category": "daily",
        "description": "Elongated slender grain gesture, sniff rich aromatic fragrance with delighted smile."
    },
    {
        "gloss": "SUGARCANE",
        "en": "Sugarcane / Ganna",
        "hi": "गन्ना",
        "ta": "கரும்பு",
        "category": "daily",
        "description": "Hold tall thick stalk, snap nodes with hands, and bite into sweet juicy fiber."
    },
    {
        "gloss": "MUSTARD_FIELD",
        "en": "Yellow Mustard Fields / Sarson Ke Khet",
        "hi": "सरसों के खेत",
        "ta": "கடுகு வயல்",
        "category": "daily",
        "description": "Both palms sway across expansive sea of bright yellow blossoming flowers."
    },
    {
        "gloss": "GRAIN_MANDI",
        "en": "Grain Mandi / Agricultural Wholesale Market",
        "hi": "अनाज मंडी / आढ़त",
        "ta": "தானிய சந்தை",
        "category": "civic",
        "description": "Weigh jute bags on industrial scales, grain commission agent auction call."
    },
    {
        "gloss": "MSP_PRICE",
        "en": "Minimum Support Price / MSP",
        "hi": "न्यूनतम समर्थन मूल्य (एमएसपी)",
        "ta": "குறைந்தபட்ச ஆதரவு விலை",
        "category": "civic",
        "description": "Government statutory price floor guaranteed under grain sacks."
    },
    {
        "gloss": "FARMER_KISAN",
        "en": "Farmer / Annadata Kisan",
        "hi": "किसान / अन्नदाता",
        "ta": "விவசாயி",
        "category": "daily",
        "description": "Carry wooden plough over shoulder with gamcha tied around forehead."
    },
    {
        "gloss": "TRACTOR",
        "en": "Tractor / Agricultural Vehicle",
        "hi": "ट्रैक्टर",
        "ta": "டிராக்டர்",
        "category": "daily",
        "description": "Hold large steering wheel bouncing gently over furrowed farmland soil."
    },
    {
        "gloss": "COMBINE_HARVESTER",
        "en": "Combine Harvester Machine",
        "hi": "कंबाइन हार्वेस्टर",
        "ta": "அறுவடை இயந்திரம்",
        "category": "daily",
        "description": "Rotating front cutting reel cutting wheat stalks and pouring grain into tractor trolley."
    },
    {
        "gloss": "TUBEWELL_PUMP",
        "en": "Tubewell / Electric Irrigation Borewell",
        "hi": "ट्यूबवेल / सबमर्सिबल पंप",
        "ta": "குழாய் கிணறு",
        "category": "daily",
        "description": "Switch on starter box, gushing thick stream of crystal cold groundwater into field channel."
    },
    {
        "gloss": "CANAL_IRRIGATION",
        "en": "Canal Irrigation / Nahar Waterway",
        "hi": "नहर सिंचाई / सिंचाई नाली",
        "ta": "கால்வாய் பாசனம்",
        "category": "daily",
        "description": "Open iron sluice gate allowing canal water to flow across green furrows."
    },
    {
        "gloss": "FERTILIZER_UREA",
        "en": "Fertilizer / Urea Sacks",
        "hi": "उर्वरक / यूरिया खाद",
        "ta": "உரம் / யூரியா",
        "category": "daily",
        "description": "White granular powder broadcast by hand sweeping across sprouted seedlings."
    },
    {
        "gloss": "ROTI",
        "en": "Roti / Phulka / Flatbread",
        "hi": "रोटी / फुल्का",
        "ta": "ரொட்டி",
        "category": "daily",
        "description": "Pat dough between palms in round motion, then puff up puffed bread on tawa."
    },
    {
        "gloss": "PARATHA",
        "en": "Stuffed Paratha / Aloo & Gobhi Paratha",
        "hi": "भरवां पराठा",
        "ta": "பராத்தா",
        "category": "daily",
        "description": "Roll out thick bread with rolling pin, smear golden butter on top."
    },
    {
        "gloss": "MAKKI_ROTI",
        "en": "Makki Di Roti / Cornmeal Bread",
        "hi": "मक्के की रोटी",
        "ta": "சோள ரொட்டி",
        "category": "daily",
        "description": "Pat golden coarse yellow dough carefully between hands on iron griddle."
    },
    {
        "gloss": "SARSON_SAAG",
        "en": "Sarson Da Saag / Mustard Greens",
        "hi": "सरसों का साग",
        "ta": "கடுகு கீரை குழம்பு",
        "category": "daily",
        "description": "Stir rich green leafy saag in earthenware pot, dollop fresh homemade butter."
    },
    {
        "gloss": "CHOLE_BHATURE",
        "en": "Chole Bhature / Spiced Chickpeas & Fried Bread",
        "hi": "छोले भटूरे",
        "ta": "சோலே பட்டூரே",
        "category": "daily",
        "description": "Drop flat dough into hot kadhai watching giant balloon bread swell, serve with tangy chickpeas."
    },
    {
        "gloss": "RAJMA_CHAWAL",
        "en": "Rajma Chawal / Red Kidney Beans with Basmati",
        "hi": "राजमा चावल",
        "ta": "ராஜ்மா சாதம்",
        "category": "daily",
        "description": "Ladle thick spiced kidney bean curry over steaming heap of white rice."
    },
    {
        "gloss": "KADHI_PAKORA",
        "en": "Kadhi Pakora / Gram Flour Yogurt Curry",
        "hi": "कढ़ी पकोड़ा",
        "ta": "கடி பக்கோடா",
        "category": "daily",
        "description": "Whisk yellow yogurt curry, drop crispy fried dumplings with mustard seed tempering."
    },
    {
        "gloss": "DAL_MAKHANI",
        "en": "Dal Makhani / Slow Cooked Black Lentils",
        "hi": "दाल मखनी",
        "ta": "தால் மக்கானி",
        "category": "daily",
        "description": "Slow simmer black lentils overnight, swirl in fresh dairy cream and butter."
    },
    {
        "gloss": "PANEER",
        "en": "Paneer / Fresh Indian Cottage Cheese",
        "hi": "पनीर",
        "ta": "பனீர்",
        "category": "daily",
        "description": "Cut firm white cheese into soft cubes, pop one into mouth."
    },
    {
        "gloss": "LASSI",
        "en": "Lassi / Sweet Churned Buttermilk",
        "hi": "मीठी लस्सी",
        "ta": "லஸ்ஸி",
        "category": "daily",
        "description": "Churn yogurt vigorously in wooden madhani, serve in tall brass glass with malai."
    },
    {
        "gloss": "CHAI",
        "en": "Chai / Masala Milk Tea",
        "hi": "मसाला चाय",
        "ta": "தேநீர்",
        "category": "daily",
        "description": "Pour hot tea from high kettle into small clay kulhad cup, sip with satisfaction."
    },
    {
        "gloss": "JALEBI",
        "en": "Jalebi / Crispy Sweet Pretzel",
        "hi": "कुरकुरी जलेबी",
        "ta": "ஜிலேபி",
        "category": "daily",
        "description": "Squeeze cloth nozzle in concentric hot oil spirals, soak in saffron sugar syrup."
    },
    {
        "gloss": "SAMOSA",
        "en": "Samosa / Spiced Potato Pastry",
        "hi": "समोसा",
        "ta": "சமோசா",
        "category": "daily",
        "description": "Three-cornered pyramid shape formed with fingers, crack crispy crust."
    },
    {
        "gloss": "GHEE",
        "en": "Desi Ghee / Clarified Butter",
        "hi": "शुद्ध देसी घी",
        "ta": "நெய்",
        "category": "daily",
        "description": "Ladle golden fragrant clarified butter pouring over hot roti."
    },
    {
        "gloss": "BUTTERMILK",
        "en": "Chhachh / Spiced Buttermilk",
        "hi": "छाछ / मट्ठा",
        "ta": "மோர்",
        "category": "daily",
        "description": "Drink cold churned salted buttermilk with roasted cumin seeds."
    },
    {
        "gloss": "GUR_JAGGERY",
        "en": "Gur / Raw Cane Jaggery",
        "hi": "गुड़ / देसी गुड़",
        "ta": "வெல்லம்",
        "category": "daily",
        "description": "Break solid block of dark golden sugarcane jaggery, chew warm sweet piece."
    },
    {
        "gloss": "BAISAKHI",
        "en": "Baisakhi / Harvest Festival",
        "hi": "बैसाखी उत्सव",
        "ta": "பைசாகி திருவிழா",
        "category": "greeting",
        "description": "Bhangra celebratory shoulder bounce and drum beat rhythm honoring ripe crops."
    },
    {
        "gloss": "LOHRI",
        "en": "Lohri / Winter Bonfire Festival",
        "hi": "लोहड़ी पर्व",
        "ta": "லோஹ்ரி பண்டிகை",
        "category": "greeting",
        "description": "Circle around glowing bonfire tossing sesame seeds and rewri into flames."
    },
    {
        "gloss": "GURPURAB",
        "en": "Gurpurab / Sikh Guru Prakash Utsav",
        "hi": "गुरपर्व / प्रकाश पर्व",
        "ta": "குர்புரப்",
        "category": "greeting",
        "description": "Cover head with respectful rumal scarf, fold hands before holy scripture."
    },
    {
        "gloss": "GOLDEN_TEMPLE",
        "en": "Harmandir Sahib / Golden Temple Amritsar",
        "hi": "स्वर्ण मंदिर / हरमंदिर साहिब",
        "ta": "பொற்கோவில்",
        "category": "navigation",
        "description": "Four doors open to all humanity surrounded by serene nectar pool."
    },
    {
        "gloss": "LANGAR_SERVICE",
        "en": "Langar / Free Community Kitchen",
        "hi": "लंगर सेवा",
        "ta": "சமூக உணவு சேவை",
        "category": "daily",
        "description": "Sit on long floor mats in equality, serve hot rotis and dal with humility."
    },
    {
        "gloss": "KUMBH_MELA",
        "en": "Kumbh Mela / Sacred Confluence Pilgrimage",
        "hi": "कुंभ मेला / महाकुंभ",
        "ta": "கும்பமேளா",
        "category": "greeting",
        "description": "Millions gathering at Sangam waters taking holy dip at auspicious hour."
    },
    {
        "gloss": "GANGA_AARTI",
        "en": "Ganga Aarti / River Worship with Brass Lamps",
        "hi": "गंगा आरती / दीपदान",
        "ta": "கங்கா ஆரத்தி",
        "category": "greeting",
        "description": "Lift heavy multi-tiered brass oil lamp in circular reverent arcs over river."
    },
    {
        "gloss": "CHHATH_PUJA",
        "en": "Chhath Puja / Sun Deity Worship in Water",
        "hi": "छठ पूजा / सूर्य उपासना",
        "ta": "சத் பூஜை",
        "category": "greeting",
        "description": "Stand chest-deep in water at sunset holding bamboo soop laden with fruits to Sun."
    },
    {
        "gloss": "RAMLILA",
        "en": "Ramlila / Traditional Dramatic Folk Play",
        "hi": "रामलीला नाटक",
        "ta": "ராம்லீலா",
        "category": "greeting",
        "description": "Draw bowstring taut in heroic theatrical stance reenacting epic virtue."
    },
    {
        "gloss": "DUSSEHRA_MELA",
        "en": "Dussehra Mela / Effigy Burning of Ravana",
        "hi": "दशहरा मेला / रावण दहन",
        "ta": "தசரா திருவிழா",
        "category": "greeting",
        "description": "Giant effigy bursts into fireworks as fire arrow hits, crowd cheers victory of truth."
    },
    {
        "gloss": "KARWA_CHAUTH",
        "en": "Karwa Chauth / Fasting & Moon Sieve",
        "hi": "करवा चौथ",
        "ta": "கர்வா சௌத்",
        "category": "greeting",
        "description": "Look at shining full moon through round brass sieve, then view spouse's face."
    },
    {
        "gloss": "TEEYAN",
        "en": "Teeyan / Monsoon Women's Festival of Punjab",
        "hi": "तीयां पर्व",
        "ta": "தீயன் பண்டிகை",
        "category": "greeting",
        "description": "Swing high on banyan tree swings singing folk songs with colourful phulkari dupattas."
    },
    {
        "gloss": "HOLI_VRINDAVAN",
        "en": "Braj Holi / Vrindavan & Mathura Color Festival",
        "hi": "ब्रज की होली / लट्ठमार होली",
        "ta": "பிரிஜ் ஹோலி",
        "category": "greeting",
        "description": "Toss gulal pink powders in the air, joyous dancing with brass water pichkari."
    },
    {
        "gloss": "DIWALI",
        "en": "Diwali / Deepawali Festival of Lights",
        "hi": "दीपावली / रोशनी का पर्व",
        "ta": "தீபாவளி",
        "category": "greeting",
        "description": "Place clay oil diyas along home verandas, fireworks sparkle in twilight."
    },
    {
        "gloss": "KURTA_PAJAMA",
        "en": "Kurta Pajama / Traditional Men's Attire",
        "hi": "कुर्ता पाजामा",
        "ta": "குர்தா பைஜாமா",
        "category": "daily",
        "description": "Trace knee-length cotton tunic neckline and pull straight drawstrings."
    },
    {
        "gloss": "PAGRI_TURBAN",
        "en": "Pagri / Turban / Dastar",
        "hi": "पगड़ी / साफा / दस्तार",
        "ta": "தலைப்பாகை",
        "category": "daily",
        "description": "Wind long cloth carefully around head in angled graceful folds, tucking tail."
    },
    {
        "gloss": "SHAWL_PASHMINA",
        "en": "Pashmina Shawl / Fine Cashmere Wool",
        "hi": "पश्मीना शॉल",
        "ta": "பஷ்மினா சால்வை",
        "category": "daily",
        "description": "Drape gossamer soft wool shawl over shoulders with delicate touch."
    },
    {
        "gloss": "NEHRU_JACKET",
        "en": "Nehru Jacket / Bandhgala Waistcoat",
        "hi": "नेहरू जैकेट / बंडी",
        "ta": "நேரு ஜாக்கெட்",
        "category": "daily",
        "description": "Fasten mandarin high collar buttons down sleeveless tailored vest."
    },
    {
        "gloss": "WOOLEN_SWEATER",
        "en": "Handknit Woolen Sweater / Pullover",
        "hi": "ऊनी स्वेटर",
        "ta": "கம்பளி சட்டை",
        "category": "daily",
        "description": "Pull warm thick woolen pullover over head settling wrists."
    },
    {
        "gloss": "BLANKET_KAMBAL",
        "en": "Woolen Blanket / Kambal",
        "hi": "कंबल / ऊनी चादर",
        "ta": "கம்பளி",
        "category": "daily",
        "description": "Spread heavy warm blanket over bed, wrap snugly around shoulders."
    },
    {
        "gloss": "QUILT_RAZAI",
        "en": "Cotton Quilt / Jaipuri Razai",
        "hi": "रजाई / जयपुरी रजाई",
        "ta": "பருத்தி மெத்தை போர்வை",
        "category": "daily",
        "description": "Fluff up lightweight warm cotton stuffed block-printed winter quilt."
    },
    {
        "gloss": "ROOM_HEATER",
        "en": "Electric Room Heater / Blower",
        "hi": "कमरे का हीटर",
        "ta": "அறை சூடேற்றி",
        "category": "daily",
        "description": "Warm both cold hands before glowing orange radiant heater coils."
    },
    {
        "gloss": "DESERT_COOLER",
        "en": "Desert Air Cooler / Khus Water Cooler",
        "hi": "कूलर / डेजर्ट कूलर",
        "ta": "ஏர் கூலர்",
        "category": "daily",
        "description": "Water dripping down grass pads as powerful fan blows cool fragrant breeze."
    },
    {
        "gloss": "CLAY_TANDOOR",
        "en": "Clay Tandoor Oven",
        "hi": "मिट्टी का तंदूर",
        "ta": "மண் தந்தூரி அடுப்பு",
        "category": "daily",
        "description": "Stick flat bread on inner hot clay wall with padded gaddi, pull out with iron skewers."
    },
    {
        "gloss": "BRICK_KILN",
        "en": "Brick Kiln / Bhatta Chimney",
        "hi": "ईंट का भट्ठा",
        "ta": "செங்கல் சூளை",
        "category": "civic",
        "description": "Tall smoking chimney over thousands of sun-dried red clay construction bricks."
    },
    {
        "gloss": "SUGAR_MILL",
        "en": "Sugarcane Mill / Cooperative Refinery",
        "hi": "चीनी मिल",
        "ta": "சர்க்கரை ஆலை",
        "category": "civic",
        "description": "Tractor trailers lined up with sugarcane stalks, heavy crushing rollers."
    },
    {
        "gloss": "TEXTILE_LUDHIANA",
        "en": "Hosiery & Woolen Mills / Ludhiana Hub",
        "hi": "लुधियाना होजरी एवं ऊनी उद्योग",
        "ta": "லுதியானா ஆடை உற்பத்தி",
        "category": "civic",
        "description": "Fast spinning knitting looms producing thermal garments and sweaters."
    },
    {
        "gloss": "SPORTS_GOODS_MEERUT",
        "en": "Meerut Sports Goods Industry / Cricket Bats",
        "hi": "मेरठ खेल उपकरण उद्योग",
        "ta": "மீரட் விளையாட்டுப் பொருட்கள்",
        "category": "civic",
        "description": "Carve English willow cricket bat, check balance and strike leather ball."
    },
    {
        "gloss": "LEATHER_KANPUR",
        "en": "Leather Footwear & Saddlery / Kanpur Hub",
        "hi": "कानपुर चमड़ा उद्योग",
        "ta": "கான்பூர் தோல் தொழில்",
        "category": "civic",
        "description": "Stitch durable leather shoes and belts with industrial needle."
    },
    {
        "gloss": "BRASS_MORADABAD",
        "en": "Moradabad Brassware / Peetal Nagari",
        "hi": "मुरादाबाद पीतल हस्तशिल्प",
        "ta": "மொராதாபாத் பித்தளை கலைப்பொருள்",
        "category": "civic",
        "description": "Engrave intricate floral patterns onto polished brass vase with chisel."
    },
    {
        "gloss": "CARPET_BHADOHI",
        "en": "Hand-knotted Carpets / Bhadohi & Mirzapur",
        "hi": "भदोही कालीन उद्योग",
        "ta": "பதோஹி கம்பளம்",
        "category": "civic",
        "description": "Knot individual wool threads on vertical handloom, trim velvet pile."
    },
    {
        "gloss": "LOCK_ALIGARH",
        "en": "Aligarh Padlocks / Tala Nagari",
        "hi": "अलीगढ़ के ताले",
        "ta": "அலிகார் பூட்டுகள்",
        "category": "civic",
        "description": "Insert sturdy brass key into heavy padlock and turn with solid click."
    },
    {
        "gloss": "GLASSWARE_FIROZABAD",
        "en": "Firozabad Glass Bangles / Suhag Nagari",
        "hi": "फिरोजाबाद की कांच की चूड़ियाँ",
        "ta": "பிரோசாபாத் கண்ணாடி வளையல்கள்",
        "category": "civic",
        "description": "Blow molten colored glass into rings, jingle bright bangles on wrist."
    },
    {
        "gloss": "POTTERY_KHURJA",
        "en": "Khurja Ceramic Pottery / Ceramic City",
        "hi": "खुर्जा चीनी मिट्टी बर्तन",
        "ta": "குர்ஜா பீங்கான் மண்பாண்டங்கள்",
        "category": "civic",
        "description": "Spin potter's wheel shaping elegant glazed ceramic crockery."
    },
    {
        "gloss": "APPLE_ORCHARD",
        "en": "Himachal Apple Orchards / Kotgarh & Kinnaur",
        "hi": "सेब के बाग",
        "ta": "ஆப்பிள் தோட்டம்",
        "category": "daily",
        "description": "Reach up into tree branches plucking crisp red apples into wicker basket."
    },
    {
        "gloss": "SAFFRON_VALLEY",
        "en": "Kashmir Saffron / Pampore Zafran",
        "hi": "कश्मीर केसर / जाफरान",
        "ta": "காஷ்மீர் குங்குமப்பூ",
        "category": "daily",
        "description": "Gently pluck delicate purple crocus flower and extract three crimson stigmas."
    },
    {
        "gloss": "SOLAR_PUMP",
        "en": "Solar Agriculture Pump / PM-KUSUM Scheme",
        "hi": "सौर कृषि पंप",
        "ta": "சூரிய சக்தி பாசன பம்ப்",
        "category": "civic",
        "description": "Blue solar panels tilt toward sun powering irrigation water flow."
    },
    {
        "gloss": "PANCHAYAT_GHAR",
        "en": "Panchayat Ghar / Village Council Hall",
        "hi": "पंचायत घर",
        "ta": "பஞ்சாயத்து அலுவலகம்",
        "category": "civic",
        "description": "Village assembly building under shade tree where local disputes are heard."
    },
    {
        "gloss": "SARPANCH",
        "en": "Sarpanch / Village Council Head",
        "hi": "सरपंच / ग्राम प्रधान",
        "ta": "பஞ்சாயத்து தலைவர்",
        "category": "civic",
        "description": "Elected village head wearing turban addressing Gram Sabha gathering."
    },
    {
        "gloss": "GRAM_SABHA",
        "en": "Gram Sabha / Village Citizens Assembly",
        "hi": "ग्राम सभा",
        "ta": "கிராம சபை",
        "category": "civic",
        "description": "All village adults raise hands voting on local development resolutions."
    }
]
