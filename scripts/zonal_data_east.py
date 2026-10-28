# scripts/zonal_data_east.py
"""
Standard ISL — Eastern Zone Chapter (isl-east) - 100 Domain Specific Signs
Focus: West Bengal, Odisha, Bihar, Jharkhand.
Historic Calcutta Deaf School (1893), Hooghly riverine transport, Howrah bridge,
coal & steel industrial core, Darjeeling tea, jute mills, Durga Puja, Rabindra Sangeet, eastern cuisine.
"""

EAST_SIGNS = [
    {
        "gloss": "KOLKATA",
        "en": "Kolkata / City of Joy & Cultural Capital",
        "hi": "कोलकाता / कलकत्ता",
        "ta": "கொல்கத்தா",
        "category": "navigation",
        "description": "Outline cantilever arms of Howrah bridge over the flowing Hooghly river."
    },
    {
        "gloss": "BHUBANESWAR",
        "en": "Bhubaneswar / Temple City of Odisha",
        "hi": "भुवनेश्वर / एकाम्र क्षेत्र",
        "ta": "புவனேஸ்வர்",
        "category": "navigation",
        "description": "Outline soaring curvilinear stone deula spire of Lingaraj temple."
    },
    {
        "gloss": "PATNA",
        "en": "Patna / Ancient Pataliputra",
        "hi": "पटना / पाटलिपुत्र",
        "ta": "பாட்னா",
        "category": "navigation",
        "description": "Fingerspell P-T, trace beehive shape of historic Golghar granary by Ganga."
    },
    {
        "gloss": "RANCHI",
        "en": "Ranchi / City of Waterfalls",
        "hi": "राँची / झरनों का शहर",
        "ta": "ராஞ்சி",
        "category": "navigation",
        "description": "Water cascading down rocky cliffs of Hundru Falls, cool forested plateau."
    },
    {
        "gloss": "JAMSHEDPUR",
        "en": "Jamshedpur / Steel City / Tatanagar",
        "hi": "जमशेदपुर / टाटानगर",
        "ta": "ஜெம்ஷெட்பூர்",
        "category": "navigation",
        "description": "Molten iron glowing red from blast furnace pouring into steel ladle."
    },
    {
        "gloss": "CUTTACK",
        "en": "Cuttack / Millennium Silver City",
        "hi": "कटक / चांदी का शहर",
        "ta": "கட்டாக்",
        "category": "navigation",
        "description": "Fine silver filigree (Tarakasi) wire crafting between Mahanadi and Kathajodi rivers."
    },
    {
        "gloss": "SILIGURI",
        "en": "Siliguri / Gateway to North-East & Dooars",
        "hi": "सिलीगुड़ी",
        "ta": "சிலிகுரி",
        "category": "navigation",
        "description": "Crossroads junction leading into Darjeeling hills and tea gardens."
    },
    {
        "gloss": "DARJEELING",
        "en": "Darjeeling / Queen of the Hills",
        "hi": "दार्जिलिंग",
        "ta": "டார்ஜிலிங்",
        "category": "navigation",
        "description": "Toy train steam puffing winding up misty hills overlooking Kanchenjunga."
    },
    {
        "gloss": "ASANSOL",
        "en": "Asansol / Coal & Railway Industrial Hub",
        "hi": "आसनसोल",
        "ta": "அசன்சோல்",
        "category": "navigation",
        "description": "Heavy electric locomotives shunt long coal rake trains on multi-track yard."
    },
    {
        "gloss": "DHANBAD",
        "en": "Dhanbad / Coal Capital of India",
        "hi": "धनबाद / कोयला राजधानी",
        "ta": "தன்பாத்",
        "category": "navigation",
        "description": "Deep underground coal pit elevator shaft descending into subterranean seams."
    },
    {
        "gloss": "HOOGHLY_RIVER",
        "en": "Hooghly River / Ganga Distributary Channel",
        "hi": "हुगली नदी",
        "ta": "ஹூக்ளி ஆறு",
        "category": "navigation",
        "description": "Broad muddy tidal river flowing under bridges past historic ghats."
    },
    {
        "gloss": "GANGA_DELTA",
        "en": "Ganga-Brahmaputra Delta / Sunderbans Delta",
        "hi": "गंगा डेल्टा",
        "ta": "கங்கை கழிமுகம்",
        "category": "navigation",
        "description": "Braided labyrinth of rivers branching outward into Bay of Bengal."
    },
    {
        "gloss": "MAHANADI_RIVER",
        "en": "Mahanadi River / Great River of Odisha",
        "hi": "महानदी",
        "ta": "மகாநதி",
        "category": "navigation",
        "description": "Expansive blue waters backed up behind Hirakud Dam, world's longest earthen dam."
    },
    {
        "gloss": "DAMODAR_RIVER",
        "en": "Damodar River / Mineral River Valley",
        "hi": "दामोदर नदी",
        "ta": "தாமோதர் ஆறு",
        "category": "navigation",
        "description": "River coursing past coalfields and hydroelectric barrage spillways."
    },
    {
        "gloss": "SUBARNAREKHA",
        "en": "Subarnarekha River / Streak of Gold",
        "hi": "सुवर्णरेखा नदी",
        "ta": "சுபர்ணரேகா ஆறு",
        "category": "navigation",
        "description": "Sift gold dust grains from riverbed gravel against shimmering current."
    },
    {
        "gloss": "SUNDARBANS_MANGROVE",
        "en": "Sundarbans Mangrove Forest / World Heritage",
        "hi": "सुंदरबन मैंग्रोव वन",
        "ta": "சுந்தரவனக் காடுகள்",
        "category": "navigation",
        "description": "Pneumatophore aerial breathing roots sticking out of tidal mud among dense sundari trees."
    },
    {
        "gloss": "ROYAL_BENGAL_TIGER",
        "en": "Royal Bengal Tiger / National Animal",
        "hi": "रॉयल बंगाल टाइगर / बाघ",
        "ta": "வங்காளப் புலி",
        "category": "daily",
        "description": "Tiger whisker gesture, claw swipe with stealthy predator stride."
    },
    {
        "gloss": "CHILIKA_LAKE",
        "en": "Chilika Lake / Asia's Largest Brackish Lagoon",
        "hi": "चिल्लिका झील",
        "ta": "சிலிகா ஏரி",
        "category": "navigation",
        "description": "Irrawaddy dolphins breaching water while migratory birds flock over blue lagoon."
    },
    {
        "gloss": "HOWRAH_BRIDGE",
        "en": "Howrah Bridge / Rabindra Setu Cantilever",
        "hi": "हावड़ा ब्रिज / रवींद्र सेतु",
        "ta": "ஹவுரா பாலம்",
        "category": "navigation",
        "description": "Massive riveted steel cantilever suspension without any pillars in riverbed."
    },
    {
        "gloss": "VIDYASAGAR_SETU",
        "en": "Vidyasagar Setu / Second Hooghly Cable Bridge",
        "hi": "विद्यासागर सेतु",
        "ta": "வித்யாசாகர் பாலம்",
        "category": "navigation",
        "description": "Slender composite pylons and harp cable stays spanning wide river."
    },
    {
        "gloss": "RIVER_FERRY_STEAMER",
        "en": "Hooghly River Passenger Ferry / Steamer Service",
        "hi": "हुगली नदी स्टीमर / नौका सेवा",
        "ta": "படகுப் போக்குவரத்து",
        "category": "navigation",
        "description": "Double decker wooden ferry boat chugging between Howrah and Bagbazar ghats."
    },
    {
        "gloss": "COUNTRY_BOAT_NAUKA",
        "en": "Country Wooden Boat / Nauka / Dinghy",
        "hi": "देशी लकड़ी की नाव / नौका",
        "ta": "நாட்டுப் படகு",
        "category": "navigation",
        "description": "Boatman poling slender pointed wooden dinghy through tranquil river waters."
    },
    {
        "gloss": "TRAM_KOLKATA",
        "en": "Kolkata Tramway / Asia's Oldest Operating Tram",
        "hi": "कोलकाता ट्राम",
        "ta": "கொல்கத்தா ட்ராம்",
        "category": "navigation",
        "description": "Trolley pole sparks on overhead wire, bell dings as wooden tram clatters on street rails."
    },
    {
        "gloss": "CIRCULAR_RAILWAY",
        "en": "Kolkata Circular Railway / Riverfront Line",
        "hi": "कोलकाता सर्कुलर रेलवे",
        "ta": "வட்ட புறநகர் ரயில்",
        "category": "navigation",
        "description": "Train tracks hugging Hooghly riverbank beneath shade of ancient banyan trees."
    },
    {
        "gloss": "CALCUTTA_DEAF_SCHOOL",
        "en": "Calcutta Deaf & Dumb School (est. 1893)",
        "hi": "कलकत्ता डेफ एंड डम्ब स्कूल (स्था. 1893)",
        "ta": "கொல்கத்தா காதுகேளாதோர் பள்ளி (1893)",
        "category": "academic",
        "description": "Historic red brick school facade on APC Road, acknowledging dawn of Indian deaf education."
    },
    {
        "gloss": "HISTORIC_SIGN_ARCHIVE",
        "en": "Historic Sign Archive / Pioneering ISL Roots",
        "hi": "ऐतिहासिक सांकेतिक अभिलेखागार",
        "ta": "வரலாற்று சைகை ஆவணம்",
        "category": "academic",
        "description": "Carefully turning 130-year-old illustrated sign manuals preserving early gestures."
    },
    {
        "gloss": "DEAF_TEACHER_TRAINING",
        "en": "Deaf Teacher Training College / Pedagogy",
        "hi": "बधिर शिक्षक प्रशिक्षण महाविद्यालय",
        "ta": "காதுகேளாதோர் ஆசிரியர் பயிற்சி",
        "category": "academic",
        "description": "Pioneering educators training deaf pupil teachers in bilingual sign pedagogy."
    },
    {
        "gloss": "CHOTA_NAGPUR_PLATEAU",
        "en": "Chota Nagpur Plateau / Mineral Heart of India",
        "hi": "छोटा नागपुर पठार",
        "ta": "சோட்டா நாக்பூர் பீடபூமி",
        "category": "navigation",
        "description": "Elevated red earth plateau rich in coal, iron ore, bauxite and sal forests."
    },
    {
        "gloss": "COAL_MINE_COLLIERY",
        "en": "Underground Coal Mine & Opencast Colliery",
        "hi": "कोयला खदान / कोलियरी",
        "ta": "நிலக்கரி சுரங்கம்",
        "category": "civic",
        "description": "Pickaxe striking deep seam of shiny black coal chunks underground."
    },
    {
        "gloss": "MINERS_HELMET",
        "en": "Coal Miner's Safety Helmet with Battery Lamp",
        "hi": "खनिक सुरक्षा हेलमेट व बत्ती",
        "ta": "சுரங்கத் தொழிலாளர் தலைக்கவசம்",
        "category": "civic",
        "description": "Strap on yellow hardhat, switch on bright headlight beam piercing underground darkness."
    },
    {
        "gloss": "COAL_WAGON_RAIL",
        "en": "Coal Freight Wagon Train / BOXN Rake",
        "hi": "कोयला मालगाड़ी",
        "ta": "நிலக்கரி சரக்கு ரயில்",
        "category": "navigation",
        "description": "Fifty open-top steel wagons loaded with black coal rolling toward thermal plants."
    },
    {
        "gloss": "IRON_ORE_MINE",
        "en": "Iron Ore Opencast Mine / Hematite Benches",
        "hi": "लौह अयस्क खदान / नोवामुंडी",
        "ta": "இரும்புத் தாது சுரங்கம்",
        "category": "civic",
        "description": "Giant excavators loading rich red-brown hematite ore into dump trucks."
    },
    {
        "gloss": "STEEL_PLANT_FOUNDRY",
        "en": "Integrated Steel Plant / Tatanagar & Durgapur",
        "hi": "एकीकृत इस्पात संयंत्र",
        "ta": "ஒருங்கிணைந்த எஃகு ஆலை",
        "category": "civic",
        "description": "Massive smoking industrial plant rolling out heavy steel I-beams and railway rails."
    },
    {
        "gloss": "BLAST_FURNACE",
        "en": "Blast Furnace / Molten Pig Iron Smelting",
        "hi": "ब्लास्ट फर्नेस / वात्या भट्ठी",
        "ta": "ஊது உலை",
        "category": "civic",
        "description": "Tap roaring white-hot fiery molten metal flowing into refractory runners."
    },
    {
        "gloss": "MICA_MINE",
        "en": "Mica Mines / Koderma & Giridih",
        "hi": "अभ्रक खदान (माइका)",
        "ta": "மைக்கா சுரங்கம்",
        "category": "civic",
        "description": "Split transparent glistening heat-resistant silicate sheets apart with knife."
    },
    {
        "gloss": "THERMAL_POWER_PLANT",
        "en": "Super Thermal Power Station / Coal Generation",
        "hi": "सुपर थर्मल पावर प्लांट",
        "ta": "அனல் மின் நிலையம்",
        "category": "civic",
        "description": "Hyperbolic cooling towers venting white steam clouds producing gigawatts of power."
    },
    {
        "gloss": "HEAVY_ENGINEERING",
        "en": "Heavy Engineering Corporation / HEC Ranchi",
        "hi": "भारी उद्योग निगम / एचईसी",
        "ta": "கனரக பொறியியல் ஆலை",
        "category": "civic",
        "description": "Massive forge press shaping mammoth steel castings for launch pads and mining shovels."
    },
    {
        "gloss": "JUTE_MILL",
        "en": "Jute Mill on Hooghly Bank",
        "hi": "पटसन मिल / जूट मिल",
        "ta": "சணல் ஆலை",
        "category": "civic",
        "description": "Weave golden natural plant fiber into strong biodegradable packing burlap."
    },
    {
        "gloss": "GOLDEN_FIBER_JUTE",
        "en": "Golden Fiber Jute / Pat / Kashta",
        "hi": "सुनहरा रेशा जूट / पटसन",
        "ta": "தங்க இழை சணல்",
        "category": "daily",
        "description": "Ret tall green reed stalks in water ponds, strip glistening golden fibers to dry."
    },
    {
        "gloss": "GUNNY_BAG_BORA",
        "en": "Gunny Sack / Burlap Jute Bag / Bora",
        "hi": "बोरा / जूट का थैला",
        "ta": "சணல் சாக்குப்பை",
        "category": "daily",
        "description": "Stitch thick coarse brown bag loaded with foodgrains with large curved packing needle."
    },
    {
        "gloss": "TEA_GARDEN_DARJEELING",
        "en": "Darjeeling Tea Garden / Champagne of Teas",
        "hi": "दार्जिलिंग चाय बागान",
        "ta": "டார்ஜிலிங் தேயிலைத் தோட்டம்",
        "category": "daily",
        "description": "Misty steep green mountain slopes, pluck two tender leaves and a bud with fingers."
    },
    {
        "gloss": "TEA_AUCTION_KOLKATA",
        "en": "Kolkata Tea Auction Center / Nilhat House",
        "hi": "कोलकाता चाय नीलामी केंद्र",
        "ta": "தேயிலை ஏல மையம்",
        "category": "civic",
        "description": "Rap wooden gavel calling out winning export bids for fine orthodox muscatel teas."
    },
    {
        "gloss": "TEA_LEAF_PLUCKING",
        "en": "Tea Leaf Plucking / Basket on Head",
        "hi": "चाय पत्ती तोड़ना",
        "ta": "தேயிலை பறித்தல்",
        "category": "daily",
        "description": "Rhythmically pluck fresh green flush and toss into woven wicker basket strapped to forehead."
    },
    {
        "gloss": "CTC_TEA_PROCESSING",
        "en": "CTC Tea Factory / Crush, Tear, Curl",
        "hi": "सीटीसी चाय प्रसंस्करण",
        "ta": "சி.டி.சி தேயிலை உற்பத்தி",
        "category": "daily",
        "description": "Crush, tear, and curl fermented leaves into dark aromatic tea granules."
    },
    {
        "gloss": "PADDY_WETLAND",
        "en": "Aman & Boro Paddy Wetlands / Bengal Plains",
        "hi": "अमन व बोरो धान के खेत",
        "ta": "ஈரநில நெல் வயல்",
        "category": "daily",
        "description": "Flooded green paddy fields reflecting monsoon clouds, harvest golden sheaves."
    },
    {
        "gloss": "BETEL_LEAF_BOROJ",
        "en": "Betel Leaf Conservatory / Paan Boroj",
        "hi": "पान का बरोझ",
        "ta": "வெற்றிலைக் கொடிக்கால்",
        "category": "daily",
        "description": "Thatch-roofed humid bamboo conservatory cultivating climbing sweet betel vines."
    },
    {
        "gloss": "SILK_MURSHIDABAD",
        "en": "Murshidabad Silk / Baluchari Saree",
        "hi": "मुर्शिदाबाद सिल्क / बालूचरी साड़ी",
        "ta": "முர்ஷிதாபாத் பட்டு",
        "category": "daily",
        "description": "Weave mythological royal chariot scenes into rich jacquard silk pallu."
    },
    {
        "gloss": "TUSSAR_SILK",
        "en": "Tussar Wild Silk / Kosa Silk of Jharkhand & Odisha",
        "hi": "तसर सिल्क / कोसा रेशम",
        "ta": "தசர் பட்டு",
        "category": "daily",
        "description": "Boil golden wild forest silkworm cocoons, spin rich textured natural gold silk thread."
    },
    {
        "gloss": "RABINDRA_SANGEET",
        "en": "Rabindra Sangeet / Songs of Tagore",
        "hi": "रवींद्र संगीत",
        "ta": "ரவீந்திர சங்கீதம்",
        "category": "greeting",
        "description": "Harmonium chords accompanying poetic lyrical song celebrating seasons and inner spirit."
    },
    {
        "gloss": "SHANTINIKETAN_ASHRAM",
        "en": "Santiniketan / Visva-Bharati Open Air School",
        "hi": "शांतिनिकेतन / विश्व भारती",
        "ta": "சாந்திநிகேதன்",
        "category": "academic",
        "description": "Study seated peacefully beneath blooming mango groves in communion with nature."
    },
    {
        "gloss": "BENGAL_RENAISSANCE",
        "en": "Bengal Renaissance / Intellectual Flowering",
        "hi": "बंगाल पुनर्जागरण",
        "ta": "வங்காள மறுமலர்ச்சி",
        "category": "academic",
        "description": "Torch of reason, literature, scientific inquiry, and social reform shining bright."
    },
    {
        "gloss": "LITERARY_JOURNAL",
        "en": "Literary Magazine / Boi Mela Kolkata Book Fair",
        "hi": "साहित्यिक पत्रिका / पुस्तक मेला",
        "ta": "இலக்கிய இதழ் / புத்தகக் கண்காட்சி",
        "category": "academic",
        "description": "Leaf through newly published poetry journal amidst huge crowds at winter book fair."
    },
    {
        "gloss": "POETRY_RECITATION",
        "en": "Kobita Abritti / Dramatic Poetry Recitation",
        "hi": "कविता पाठ / आवृत्ति",
        "ta": "கவிதை வாசிப்பு",
        "category": "academic",
        "description": "Expressive gestures and non-manual facial emotional cadences reciting classical verse."
    },
    {
        "gloss": "ODISSI_DANCE",
        "en": "Odissi Classical Dance / Tribhanga Stance",
        "hi": "ओडिसी शास्त्रीय नृत्य",
        "ta": "ஒடிசி நடனம்",
        "category": "greeting",
        "description": "Tribhanga three-bend stance with silver filigree headpiece and sculptural temple poses."
    },
    {
        "gloss": "CHHAU_MASK_DANCE",
        "en": "Chhau Martial Folk Dance / Purulia & Mayurbhanj",
        "hi": "छऊ मुखौटा नृत्य",
        "ta": "சாவ் நடனம்",
        "category": "greeting",
        "description": "Wear vibrant painted clay mask, perform acrobatic combat leaps to beat of dhol."
    },
    {
        "gloss": "PATTACHITRA_SCROLL",
        "en": "Pattachitra Scroll Painting / Raghurajpur Craft",
        "hi": "पट्टचित्र स्क्रोल चित्रकला",
        "ta": "பட்டாச்சித்ரா ஓவியம்",
        "category": "greeting",
        "description": "Unroll long painted cloth scroll singing visual mythological ballad."
    },
    {
        "gloss": "TERRACOTTA_TEMPLE",
        "en": "Bishnupur Terracotta Temple Architecture",
        "hi": "बिष्णुपुर टेराकोटा मंदिर",
        "ta": "சுடுமண் கோயில் சிற்பம்",
        "category": "academic",
        "description": "Burnt clay bricks carved with intricate bas-relief panels of epic lore."
    },
    {
        "gloss": "DHAK_DRUM",
        "en": "Dhak / Traditional Festival Barrel Drum",
        "hi": "ढाक वाद्य",
        "ta": "டாக் மேளம்",
        "category": "greeting",
        "description": "Hang massive feather-decorated wooden drum on shoulder, strike with two cane sticks."
    },
    {
        "gloss": "BAUL_SONG",
        "en": "Baul Mystic Folk Music of Bengal",
        "hi": "बाउल गान / सूफी लोकगीत",
        "ta": "பாவுல் நாட்டுப்புற பாடல்",
        "category": "greeting",
        "description": "Wanderer in saffron robes swirling in ecstatic dance seeking inner spirit."
    },
    {
        "gloss": "EKTARA_INSTRUMENT",
        "en": "Ektara / Single-Stringed Plucked Instrument",
        "hi": "एकतारा वाद्य",
        "ta": "ஏக்தாரா",
        "category": "greeting",
        "description": "Pluck single steel wire strung between split bamboo frame over dried gourd."
    },
    {
        "gloss": "FOOTBALL_DERBY",
        "en": "Kolkata Football Derby / Boro Match",
        "hi": "कोलकाता फुटबॉल डर्बी",
        "ta": "கொல்கத்தா கால்பந்து போட்டி",
        "category": "greeting",
        "description": "Pass football, strike curling kick into top corner of goal net to roaring crowd."
    },
    {
        "gloss": "MOHUN_BAGAN_CLUB",
        "en": "Mohun Bagan Athletic Club (est. 1889) / Mariners",
        "hi": "मोहन बागान एथलेटिक क्लब",
        "ta": "மோகன் பகான் கிளப்",
        "category": "greeting",
        "description": "Green and maroon sailing sailboat crest gesture, historic IFA Shield victory."
    },
    {
        "gloss": "EAST_BENGAL_CLUB",
        "en": "East Bengal FC (est. 1920) / Red & Gold Brigade",
        "hi": "ईस्ट बंगाल फुटबॉल क्लब",
        "ta": "ஈஸ்ட் பெங்கால் கால்பந்து கிளப்",
        "category": "greeting",
        "description": "Red and gold blazing torch crest held high by proud supporters."
    },
    {
        "gloss": "SALT_LAKE_STADIUM",
        "en": "Salt Lake Stadium / Vivekananda Yuba Bharati Krirangan",
        "hi": "साल्ट लेक स्टेडियम",
        "ta": "சால்ட் லேக் அரங்கம்",
        "category": "navigation",
        "description": "Colossal three-tier bowl stadium echoing with 85,000 cheering football fans."
    },
    {
        "gloss": "FISH_MARKET_MACHHER_BAZAR",
        "en": "Machher Bazar / Fresh Fish Wholesale Market",
        "hi": "मछली बाज़ार",
        "ta": "மீன் சந்தை",
        "category": "daily",
        "description": "Rows of fresh silvery fish on crushed ice weighed on hanging scales."
    },
    {
        "gloss": "HILSHA_FISH",
        "en": "Hilsa / Ilish / Queen of Fish",
        "hi": "इलिश मछली / हिल्सा",
        "ta": "இல்சா மீன்",
        "category": "daily",
        "description": "Silvery broad river fish with shimmering scales, sliced into signature steaks."
    },
    {
        "gloss": "ROHU_CARP",
        "en": "Rohu Carp / Rui Fresh Water Fish",
        "hi": "रोहू मछली",
        "ta": "ரோகு மீன்",
        "category": "daily",
        "description": "Freshwater river carp with pinkish scales and tender sweet flesh."
    },
    {
        "gloss": "PRAWN_CHINGRI",
        "en": "Golda & Bagda Jumbo Prawns / Chingri Malai",
        "hi": "झींगा मछली / चिंगरी",
        "ta": "இறால்",
        "category": "daily",
        "description": "Large curved freshwater prawn cooked in rich spiced coconut cream sauce."
    },
    {
        "gloss": "MUSTARD_FISH_CURRY",
        "en": "Shorshe Ilish / Fish in Pungent Mustard Paste",
        "hi": "सरसों वाली मछली / शौरषे इलिश",
        "ta": "கடுகு மீன் குழம்பு",
        "category": "daily",
        "description": "Steam fish in freshly ground pungent yellow mustard and green chili sauce."
    },
    {
        "gloss": "RICE_BHAAT",
        "en": "Bhaat / Daily Steamed Rice",
        "hi": "भात / उबले चावल",
        "ta": "சாதம்",
        "category": "daily",
        "description": "Fluffy grains of fragrant boiled white rice served hot on plate."
    },
    {
        "gloss": "LUCHI_ALUR_DOM",
        "en": "Luchi Alur Dom / Puffed Deep Fried Flatbread with Potatoes",
        "hi": "लूची आलूर दम",
        "ta": "பூரி உருளைக்கிழங்கு மசாலா",
        "category": "daily",
        "description": "Fluffy white all-purpose flour fried bread eaten with slow-cooked spiced baby potatoes."
    },
    {
        "gloss": "KACHORI_CHANA",
        "en": "Radhaballabhi / Hing Kachori with Chholar Dal",
        "hi": "राधावल्लभी / कचौड़ी",
        "ta": "கச்சோரி",
        "category": "daily",
        "description": "Asafoetida lentils stuffed inside crisp bread, served with sweet coconut Bengal gram dal."
    },
    {
        "gloss": "LITTI_CHOKHA",
        "en": "Litti Chokha / Roasted Wheat Balls with Sattu & Eggplant",
        "hi": "लिट्टी चोखा",
        "ta": "லிட்டி சோக்கா",
        "category": "daily",
        "description": "Bake sattu-stuffed dough balls over cow-dung embers, dip in pure desi ghee, mash eggplant."
    },
    {
        "gloss": "SATTU_DRINK",
        "en": "Sattu / Roasted Gram Flour Energy Drink",
        "hi": "सत्तू का शरबत",
        "ta": "வறுத்த கடலை மாவு பானம்",
        "category": "daily",
        "description": "Stir roasted chickpea flour in chilled water with black salt, lemon and roasted cumin."
    },
    {
        "gloss": "PAHALA_RASGULLA",
        "en": "Pahala Rasgulla / Odisha Brown Cardamom Rasagola",
        "hi": "पहाला रसगुल्ला",
        "ta": "பஹாலா ரசகுல்லா",
        "category": "daily",
        "description": "Melt-in-mouth tender light brown fresh cottage cheese dumplings in warm sugar syrup."
    },
    {
        "gloss": "KOLKATA_RASGULLA",
        "en": "Kolkata Spongy White Rasgulla / Nobin Chandra Das",
        "hi": "कोलकाता रसगुल्ला / स्पंज रसगुल्ला",
        "ta": "கொல்கத்தா ரசகுல்லா",
        "category": "daily",
        "description": "Squeeze spongy white cottage cheese ball, bursts with sweet cardamom syrup."
    },
    {
        "gloss": "SANDESH",
        "en": "Sandesh / Nolen Gur & Chhana Sweet",
        "hi": "संदेश मिठाई",
        "ta": "சந்தேஷ்",
        "category": "daily",
        "description": "Molded fresh sweet curds infused with aromatic winter date palm jaggery."
    },
    {
        "gloss": "MISHTI_DOI",
        "en": "Mishti Doi / Baked Caramelized Sweet Yogurt",
        "hi": "मिष्टी दोई / मीठा दही",
        "ta": "மிஷ்டி தோய்",
        "category": "daily",
        "description": "Earthen clay pot filled with thick creamy sweet caramelized pinkish yogurt."
    },
    {
        "gloss": "CHHENA_PODA",
        "en": "Chhena Poda / Baked Cottage Cheese Cake of Odisha",
        "hi": "छेना पोड़ा / बेक्ड पनीर मिठाई",
        "ta": "சேனா போடா",
        "category": "daily",
        "description": "Caramelized charred crust on slow-baked cardamom cottage cheese cake."
    },
    {
        "gloss": "PAKMAL_PAKHALA_BHAT",
        "en": "Pakhala Bhat / Fermented Water Rice with Curd & Fish Fry",
        "hi": "पखाला भात / ओड़िया जल भात",
        "ta": "பழைய சாதம்",
        "category": "daily",
        "description": "Cool fermented rice in clay bowl seasoned with curd, roasted cumin, green chili and lemon."
    },
    {
        "gloss": "DALMA",
        "en": "Dalma / Traditional Odia Lentil & Vegetable Stew",
        "hi": "दालमा / ओड़िया दाल-सब्जी",
        "ta": "தால்மா",
        "category": "daily",
        "description": "Boil toor dal with raw papaya, pumpkin, drumsticks tempered with roasted panch phoron."
    },
    {
        "gloss": "DURGA_PUJA",
        "en": "Durga Puja / UNESCO Intangible Cultural Heritage",
        "hi": "दुर्गा पूजा / दुर्गोत्सव",
        "ta": "துர்கா பூஜை",
        "category": "greeting",
        "description": "Goddess Durga ten armed posture with weapons slaying buffalo demon Mahishasura."
    },
    {
        "gloss": "PUJA_PANDAL",
        "en": "Puja Pandal / Grand Thematic Art Pavilion",
        "hi": "पूजा पंडाल",
        "ta": "பூஜை பந்தல்",
        "category": "greeting",
        "description": "Sprawling temporary architectural palace created by master artisans and lighting."
    },
    {
        "gloss": "DHUNUCHI_DANCE",
        "en": "Dhunuchi Naach / Incense Smoke Dance",
        "hi": "धुनाची नृत्य",
        "ta": "துனுச்சி நடனம்",
        "category": "greeting",
        "description": "Balance clay flared incense holder filled with burning coconut husk and fragrant frankincense."
    },
    {
        "gloss": "SINDOOR_KHELA",
        "en": "Sindoor Khela / Vijaya Dashami Vermilion Rite",
        "hi": "सिंदूर खेला",
        "ta": "சிந்தூர் கேலா",
        "category": "greeting",
        "description": "Women smear bright scarlet vermilion on Goddess and on each other's cheeks with conch blowing."
    },
    {
        "gloss": "KALI_PUJA",
        "en": "Kali Puja / Shyama Puja Midnight Worship",
        "hi": "काली पूजा / श्यामा पूजा",
        "ta": "காளி பூஜை",
        "category": "greeting",
        "description": "Mother Kali tongue extended, standing on Lord Shiva, holding scimitar in dark night."
    },
    {
        "gloss": "SARASWATI_PUJA",
        "en": "Saraswati Puja / Vasant Panchami Book Blessing",
        "hi": "सरस्वती पूजा / वसंत पंचमी",
        "ta": "சரஸ்வதி பூஜை",
        "category": "academic",
        "description": "Place textbooks, notebooks and pens at feet of Goddess of Learning dressed in yellow."
    },
    {
        "gloss": "JAGANNATH_RATH_YATRA",
        "en": "Jagannath Rath Yatra Puri / Chariot of the Universe",
        "hi": "जगन्नाथ रथ यात्रा पूरी",
        "ta": "ஜெகநாதர் ரத யாத்திரை",
        "category": "greeting",
        "description": "Nandighosa chariot pulled by millions of devotees along Grand Road Bada Danda."
    },
    {
        "gloss": "PURI_BEACH",
        "en": "Puri Golden Beach / Blue Flag Beach",
        "hi": "पुरी समुद्र तट",
        "ta": "பூரி கடற்கரை",
        "category": "navigation",
        "description": "Golden surf crashing on white sand, sand artist sculpting giant figures."
    },
    {
        "gloss": "KONARK_SUN_TEMPLE",
        "en": "Konark Sun Temple / Black Pagoda Chariot Wheels",
        "hi": "कोणार्क सूर्य मंदिर",
        "ta": "கொனார்க் சூரியக் கோயில்",
        "category": "academic",
        "description": "Monumental chariot wheels functioning as intricate sundials telling exact time."
    },
    {
        "gloss": "CHHATH_GHAT",
        "en": "Chhath Ghat on River Ganga / Patna Ghats",
        "hi": "छठ घाट / गंगा तट",
        "ta": "சத் படித்துறை",
        "category": "greeting",
        "description": "Thousands of earthen oil lamps lining illuminated stone river steps at dawn."
    },
    {
        "gloss": "SHRAVANI_MELA",
        "en": "Shravani Mela Deoghar / 100km Kanwar Yatra",
        "hi": "श्रावणी मेला देवघर / कांवड़ यात्रा",
        "ta": "சராவணி மேளா",
        "category": "greeting",
        "description": "Devotees in saffron clothes carrying holy Ganga water on bamboo balance pole."
    },
    {
        "gloss": "DOKRA_METAL_CRAFT",
        "en": "Dokra Non-Ferrous Metal Craft / Lost-Wax Bell Metal",
        "hi": "डोकरा धातु हस्तशिल्प",
        "ta": "டோக்ரா உலோகக் கலை",
        "category": "greeting",
        "description": "Ancient 4,000-year-old brass casting technique creating folk figurines with beeswax threads."
    },
    {
        "gloss": "KANTHA_EMBROIDERY",
        "en": "Kantha Embroidery / Running Stitch Quilts",
        "hi": "कांथा कढ़ाई",
        "ta": "காந்தா தையல் கலை",
        "category": "daily",
        "description": "Delicate wave running stitches transforming old cotton sarees into decorative quilts."
    },
    {
        "gloss": "SAMBALPURI_IKAT",
        "en": "Sambalpuri Ikat Handloom / Bandhakala",
        "hi": "संबलपुरी इकत हथकरघा",
        "ta": "சம்பல்பூர் இக்கத்",
        "category": "daily",
        "description": "Tie-dye warp and weft creating traditional conch shell, wheel and fish motifs."
    },
    {
        "gloss": "MADHUBANI_PAINTING",
        "en": "Madhubani Painting / Mithila Folk Art",
        "hi": "मधुबनी चित्रकला / मिथिला कला",
        "ta": "மதுபானி ஓவியம்",
        "category": "greeting",
        "description": "Geometric floral and deity drawings filled with bright natural dyes using twigs and nibs."
    },
    {
        "gloss": "MANJUSHA_ART",
        "en": "Manjusha Art / Angika Snake & Temple Border Art",
        "hi": "मंजूषा कला / अंगिका कला",
        "ta": "மஞ்சுஷா ஓவியக் கலை",
        "category": "greeting",
        "description": "Jute box scrolls painted in three sacred colors: pink, green, and yellow."
    },
    {
        "gloss": "TRIBAL_HERITAGE",
        "en": "Santhal & Munda Tribal Culture / Sarhul Festival",
        "hi": "संथाल एवं मुंडा जनजातीय संस्कृति / सरहुल",
        "ta": "பழங்குடியினர் பாரம்பரியம்",
        "category": "greeting",
        "description": "Worship blooming Sal flowers, circle dance with drums in sacred grove (Jaher Than)."
    },
    {
        "gloss": "BODH_GAYA_TEMPLE",
        "en": "Mahabodhi Temple Bodh Gaya / Seat of Enlightenment",
        "hi": "महाबोधि मंदिर बोधगया",
        "ta": "மகாபோதி கோயில் புத்தகயா",
        "category": "navigation",
        "description": "Meditative posture beneath sacred Bodhi tree diamond throne vajrasana."
    },
    {
        "gloss": "NALANDA_ANCIENT_SEAT",
        "en": "Nalanda Ancient University Ruins / Buddhist Seat",
        "hi": "नालंदा प्राचीन विश्वविद्यालय",
        "ta": "நாலந்தா பல்கலைக்கழகம்",
        "category": "academic",
        "description": "Monastic brick stupas and halls of ancient global seat of learning."
    }
]
