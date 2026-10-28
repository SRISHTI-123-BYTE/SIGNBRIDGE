# scripts/zonal_data_northeast.py
"""
Standard ISL — North-Eastern Zone Chapter (isl-northeast) - 100 Domain Specific Signs
Focus: Assam, Meghalaya, Manipur, Mizoram, Nagaland, Tripura, Arunachal Pradesh, Sikkim.
Hill terrain navigation, living root bridges, tea valleys, Kaziranga wildlife, Muga silk,
bamboo crafts, Hornbill & Bihu festivals, indigenous tribal community traditions.
"""

NORTHEAST_SIGNS = [
    {
        "gloss": "GUWAHATI",
        "en": "Guwahati / Gateway to the North East / Pragjyotishpura",
        "hi": "गुवाहाटी / प्रागज्योतिषपुर",
        "ta": "குவஹாத்தி",
        "category": "navigation",
        "description": "Outline Kamakhya hill temple overlooking the majestic red river Brahmaputra."
    },
    {
        "gloss": "SHILLONG",
        "en": "Shillong / Scotland of the East / Rock Capital",
        "hi": "शिलांग / बादलों का घर",
        "ta": "ஷில்லாங்",
        "category": "navigation",
        "description": "Pine trees swaying in cool misty pine breeze with acoustic guitar strumming."
    },
    {
        "gloss": "IMPHAL",
        "en": "Imphal / Kangla Fort Capital",
        "hi": "इम्फाल",
        "ta": "இம்பால்",
        "category": "navigation",
        "description": "Sacred Kangla Sha dragon lion statues guarding moat bridge."
    },
    {
        "gloss": "AIZAWL",
        "en": "Aizawl / Ridge-Top City",
        "hi": "आइज़ोल",
        "ta": "ஐசால்",
        "category": "navigation",
        "description": "Houses cascading down steep cliff ridges connected by winding hillside steps."
    },
    {
        "gloss": "KOHIMA",
        "en": "Kohima / Land of the Angami Nagas",
        "hi": "कोहिमा",
        "ta": "கோஹிமா",
        "category": "navigation",
        "description": "Carved traditional wooden village gate (Kharu) atop high misty ridge."
    },
    {
        "gloss": "AGARTALA",
        "en": "Agartala / Ujjayanta Palace Capital",
        "hi": "अगरतला",
        "ta": "அகர்தலா",
        "category": "navigation",
        "description": "White neoclassical domes of Ujjayanta royal palace reflected in garden fountains."
    },
    {
        "gloss": "ITANAGAR",
        "en": "Itanagar / Land of the Dawn-Lit Mountains",
        "hi": "ईटानगर / सूर्योदय की भूमि",
        "ta": "இட்டாநகர்",
        "category": "navigation",
        "description": "Historic 14th century Ita Fort brick walls nestled among sub-Himalayan hills."
    },
    {
        "gloss": "GANGTOK",
        "en": "Gangtok / Hilltop Buddhist Kingdom Capital",
        "hi": "गंगटोक",
        "ta": "கேங்டாக்",
        "category": "navigation",
        "description": "Prayer wheels spinning in golden monastery with panoramic view of Khangchendzonga."
    },
    {
        "gloss": "DIBRUGARH",
        "en": "Dibrugarh / Tea City of India",
        "hi": "डिब्रूगढ़ / चाय की नगरी",
        "ta": "திப்ருகார்",
        "category": "navigation",
        "description": "Expansive green tea carpet stretching to banks of upper Brahmaputra."
    },
    {
        "gloss": "JORHAT",
        "en": "Jorhat / Cultural Capital of Assam",
        "hi": "जोरहाट",
        "ta": "ஜோர்ஹாட்",
        "category": "navigation",
        "description": "Historic tea research station and river ferry embarking for Majuli island."
    },
    {
        "gloss": "BRAHMAPUTRA_RIVER",
        "en": "Brahmaputra River / Son of Brahma / Luit",
        "hi": "ब्रह्मपुत्र नदी / लुइत",
        "ta": "பிரம்மபுத்திரா ஆறு",
        "category": "navigation",
        "description": "Vast ocean-like red river with massive braided sandbars and powerful current."
    },
    {
        "gloss": "BARAK_RIVER",
        "en": "Barak River / Southern Assam Lifeblood",
        "hi": "बराक नदी",
        "ta": "பராக் ஆறு",
        "category": "navigation",
        "description": "Meandering river coursing through green valleys connecting Cachar and Manipur hills."
    },
    {
        "gloss": "TEESTA_RIVER",
        "en": "Teesta River / Glacial Himalayan Waters",
        "hi": "तीस्ता नदी",
        "ta": "தீஸ்தா ஆறு",
        "category": "navigation",
        "description": "Emerald green white-water rapids rushing fiercely through Himalayan gorges."
    },
    {
        "gloss": "MAJULI_RIVER_ISLAND",
        "en": "Majuli Island / World's Largest River Island",
        "hi": "माजुली नदी द्वीप",
        "ta": "மஜுலி ஆற்றுத் தீவு",
        "category": "navigation",
        "description": "Enclosed island surrounded by Brahmaputra waters, Vaishnavite Satra monasteries and mask crafts."
    },
    {
        "gloss": "LOKTAK_LAKE",
        "en": "Loktak Lake / Floating Biomass Lake",
        "hi": "लोकटक झील",
        "ta": "லோக்டாக் ஏரி",
        "category": "navigation",
        "description": "Vast freshwater lake dotted with circular floating islands of vegetation and fishermen huts."
    },
    {
        "gloss": "PHUMDI_FLOATING_ISLAND",
        "en": "Phumdi / Floating Heterogeneous Masses of Vegetation",
        "hi": "फुमदी / तैरते द्वीप",
        "ta": "மிதக்கும் தீவு",
        "category": "daily",
        "description": "Walk softly on springy spongy floating mass of organic soil and roots over deep water."
    },
    {
        "gloss": "KHANGCHENDZONGA_PEAK",
        "en": "Mount Khangchendzonga / Sacred Five Treasures of Snow",
        "hi": "कंचनजंगा पर्वत शिखर",
        "ta": "கஞ்சன்சங்கா சிகரம்",
        "category": "navigation",
        "description": "Five massive snow peaks piercing the azure sky, worshipped as guardian deity."
    },
    {
        "gloss": "PATKAI_HILLS",
        "en": "Patkai Mountain Range / Indo-Burma Border",
        "hi": "पटकाई पहाड़ियाँ",
        "ta": "பட்காய் மலைத்தொடர்",
        "category": "navigation",
        "description": "Dense rainforest-covered rugged ridges forming international frontier border."
    },
    {
        "gloss": "GARO_HILLS",
        "en": "Garo Hills / Nokrek Biosphere",
        "hi": "गारो पहाड़ियाँ",
        "ta": "காரோ மலைகள்",
        "category": "navigation",
        "description": "Citrus gene sanctuary hills where wild oranges and ancient forests thrive."
    },
    {
        "gloss": "KHASI_HILLS",
        "en": "Khasi Hills / Abode of Clouds",
        "hi": "खासी पहाड़ियाँ",
        "ta": "காசி மலைகள்",
        "category": "navigation",
        "description": "Rolling plateau highlands dropping in dramatic sheer waterfalls into deep gorges."
    },
    {
        "gloss": "JAINTIA_HILLS",
        "en": "Jaintia Hills / Limestone Caves & Coal",
        "hi": "जयंतिया पहाड़ियाँ",
        "ta": "ஜெயந்தியா மலைகள்",
        "category": "navigation",
        "description": "Deep underground subterranean limestone caves with stalactites and crystal rivers."
    },
    {
        "gloss": "NAGA_HILLS",
        "en": "Naga Hills / Dzukou Valley",
        "hi": "नागा पहाड़ियाँ / ज़ुको घाटी",
        "ta": "நாகா மலைகள்",
        "category": "navigation",
        "description": "Endless rolling green valleys carpeted with seasonal rare Dzukou lilies."
    },
    {
        "gloss": "MIZO_HILLS",
        "en": "Mizo Hills / Lushai Hills",
        "hi": "मिज़ो पहाड़ियाँ / लुशाई हिल्स",
        "ta": "மிசோ மலைகள்",
        "category": "navigation",
        "description": "Parallel mountain ridges covered with flowering bamboo and pine forests."
    },
    {
        "gloss": "CHERRAPUNJI_RAINFALL",
        "en": "Cherrapunji / Sohra Extreme Monsoon Rainfall",
        "hi": "चेरापूंजी / सोहरा",
        "ta": "சிரபுஞ்சி",
        "category": "daily",
        "description": "Heavy torrential sheets of monsoon rain drumming on tin roofs and plunging down cliffs."
    },
    {
        "gloss": "MAWSYNRAM_CLOUDS",
        "en": "Mawsynram / Wettest Place on Planet Earth",
        "hi": "मासिनराम / विश्व का सर्वाधिक वर्षा वाला स्थान",
        "ta": "மௌசின்ராம்",
        "category": "daily",
        "description": "Dense monsoon clouds enveloping whole mountain village in continuous perpetual rain."
    },
    {
        "gloss": "LIVING_ROOT_BRIDGE",
        "en": "Living Root Bridge / Jingkieng Jri Bio-Engineering",
        "hi": "जीवित जड़ पुल / जिंगकिएंग जरी",
        "ta": "உயிருள்ள வேர் பாலம்",
        "category": "navigation",
        "description": "Guide living aerial roots of rubber fig tree across canyon until they entwine into a living stone-strong bridge."
    },
    {
        "gloss": "BAMBOO_FOOTBRIDGE",
        "en": "Bamboo Footbridge / Hanging River Crossing",
        "hi": "बांस का पैदल पुल",
        "ta": "மூங்கில் பாலம்",
        "category": "navigation",
        "description": "Step carefully across flexible woven bamboo bridge swinging gently over roaring mountain stream."
    },
    {
        "gloss": "CABLE_SUSPENSION_BRIDGE",
        "en": "Steel Cable Suspension Bridge",
        "hi": "केबल सस्पेंशन ब्रिज / झूला पुल",
        "ta": "தொங்கு பாலம்",
        "category": "navigation",
        "description": "Heavy steel cables anchored into canyon rock holding wooden pedestrian walkway."
    },
    {
        "gloss": "ROPEWAY_CABLE_CAR",
        "en": "Aerial Ropeway / Hill Cable Car",
        "hi": "रोपवे / केबल कार",
        "ta": "ரோப்வே கேபிள் கார்",
        "category": "navigation",
        "description": "Glass cabin gliding silently on aerial steel rope across thousands of feet of canyon abyss."
    },
    {
        "gloss": "HILL_PASS",
        "en": "Mountain Hill Pass / Sela Pass & Nathu La",
        "hi": "पहाड़ी दर्रा / सेला पास",
        "ta": "மலைக் கணவாய்",
        "category": "navigation",
        "description": "Narrow winding roadway cutting between towering snowy ridges above tree line."
    },
    {
        "gloss": "HAIRPIN_BEND_ROAD",
        "en": "Hairpin Bend / Switchback Mountain Road",
        "hi": "हेयरपिन मोड़ / घुमावदार पहाड़ी सड़क",
        "ta": "கொண்டை ஊசி வளைவு",
        "category": "navigation",
        "description": "Sharp 180-degree hairpin turns climbing steeply up mountain slopes."
    },
    {
        "gloss": "MOUNTAIN_RIDGELINE",
        "en": "Mountain Ridgeline / Knife-Edge Crest",
        "hi": "पर्वत कटक / रिज",
        "ta": "மலை முகடு",
        "category": "navigation",
        "description": "High knife-edge ridge with steep drops on both sides shrouded in mist."
    },
    {
        "gloss": "LANDSLIDE_BYPASS",
        "en": "Landslide / Hill Highway Bypass Clearance",
        "hi": "भूस्खलन / मलबा हटाना",
        "ta": "நிலச்சரிவு சீரமைப்பு",
        "category": "navigation",
        "description": "Mud and boulders tumbling down hillside, heavy bulldozers clearing single-lane bypass."
    },
    {
        "gloss": "FOGGY_VALLEY",
        "en": "Foggy Valley / Cloud Inversion",
        "hi": "धुंध भरी घाटी / मेघमय घाटी",
        "ta": "பனிமூட்ட பள்ளத்தாக்கு",
        "category": "daily",
        "description": "Looking down from sunny mountain peak onto endless white sea of clouds filling valley floor."
    },
    {
        "gloss": "STEP_TERRACE_FARM",
        "en": "Step Terrace Farming / Angami Ruza Terraces",
        "hi": "सीढ़ीदार खेत / सोपान कृषि",
        "ta": "படிமுறை விவசாயம்",
        "category": "daily",
        "description": "Concentric carved stone-walled flooded water terraces stepping down steep mountainside."
    },
    {
        "gloss": "ORGANIC_FARMING_SIKKIM",
        "en": "100% Organic Farming / Sikkim Green State",
        "hi": "100% जैविक खेती / सिक्किम",
        "ta": "முழுமையான இயற்கை விவசாயம்",
        "category": "civic",
        "description": "Zero chemical fertilizers, composting natural biomass to grow pure wholesome crops."
    },
    {
        "gloss": "KAZIRANGA_PARK",
        "en": "Kaziranga National Park / World Heritage Sanctuary",
        "hi": "काजीरंगा राष्ट्रीय उद्यान",
        "ta": "காசிரங்கா தேசிய பூங்கா",
        "category": "navigation",
        "description": "Tall elephant grass plains along Brahmaputra riverbanks protecting rare wildlife."
    },
    {
        "gloss": "ONE_HORNED_RHINO",
        "en": "Great Indian One-Horned Rhinoceros",
        "hi": "एक सींग वाला गैंडा",
        "ta": "ஒற்றைக் கொம்பு காண்டாமிருகம்",
        "category": "daily",
        "description": "Stout horn on snout, armor-plated folded skin folds grazing peacefully."
    },
    {
        "gloss": "RED_PANDA",
        "en": "Red Panda / State Animal of Sikkim",
        "hi": "लाल पांडा",
        "ta": "சிவப்பு பாண்டா",
        "category": "daily",
        "description": "Rusty red fur, bushy ringed tail, nibbling tender bamboo shoots high in oak tree."
    },
    {
        "gloss": "GREAT_HORNBILL_BIRD",
        "en": "Great Indian Hornbill / Sacred Bird of Nagas",
        "hi": "ग्रेट इंडियन हॉर्नबिल पक्षी",
        "ta": "இருவாச்சி பறவை",
        "category": "daily",
        "description": "Massive yellow-and-black casque beak, whooshing wings flying across forest canopy."
    },
    {
        "gloss": "CLOUDED_LEOPARD",
        "en": "Clouded Leopard / Tree Canopy Predator",
        "hi": "धूमिल तेंदुआ",
        "ta": "மேகச் சிறுத்தை",
        "category": "daily",
        "description": "Large cloud-shaped rosettes, extraordinarily long tail balancing stealthily on tree branch."
    },
    {
        "gloss": "SANGAI_DEER",
        "en": "Sangai Deer / Dancing Brow-Antlered Deer of Keibul Lamjao",
        "hi": "संगाई हिरण / नृत्य हिरण",
        "ta": "சங்காய் மான்",
        "category": "daily",
        "description": "Graceful crown antlers, leaping delicately across bouncing floating phumdi mats."
    },
    {
        "gloss": "GOLDEN_LANGUR",
        "en": "Gee's Golden Langur / Sacred Primate of Assam",
        "hi": "सुनहरा लंगूर",
        "ta": "தங்க மந்தி",
        "category": "daily",
        "description": "Lustrous golden-cream fur with black face swinging between high canopy trees."
    },
    {
        "gloss": "WILD_WATER_BUFFALO",
        "en": "Wild Water Buffalo / Arna",
        "hi": "जंगली जल भैंस / अर्ण",
        "ta": "காட்டு நீர் எருமை",
        "category": "daily",
        "description": "Massive crescent-curved horns spanning two meters, wallowing in river marsh."
    },
    {
        "gloss": "ORCHID_GREENHOUSE",
        "en": "Orchid Greenhouse / Rare Epiphytic Flora",
        "hi": "आर्किड ग्रीनहाउस / दुर्लभ पुष्प",
        "ta": "ஆர்க்கிட் மலர் தோட்டம்",
        "category": "daily",
        "description": "Delicate multi-colored exotic orchid blossoms hanging from moist mossy branches."
    },
    {
        "gloss": "EVERGREEN_RAINFOREST",
        "en": "Dense Evergreen Rainforest / Tropical Canopy",
        "hi": "सदाबहार वर्षावन",
        "ta": "பசுமை மாறா காடு",
        "category": "daily",
        "description": "Multi-tier towering dipterocarp trees, dangling woody lianas, rich humid biodiversity."
    },
    {
        "gloss": "SACRED_GROVE",
        "en": "Law Kyntang / Khasi Sacred Forest Grove",
        "hi": "पवित्र उपवन / लॉ किन्तांग",
        "ta": "புனிதக் காடு",
        "category": "greeting",
        "description": "Ancient pristine virgin forest protected by ancestral reverence where nothing is removed."
    },
    {
        "gloss": "BAMBOO_GROVE",
        "en": "Giant Bamboo Grove / Muli & Bhaluka",
        "hi": "विशाल बांस का झुरमुट",
        "ta": "மூங்கில் தோப்பு",
        "category": "daily",
        "description": "Towering green bamboo culms creaking gracefully in the wind."
    },
    {
        "gloss": "CANE_FURNITURE",
        "en": "Cane & Bamboo Handicrafts",
        "hi": "बेंत एवं बांस हस्तशिल्प",
        "ta": "பிரம்பு மரச்சாமான்கள்",
        "category": "daily",
        "description": "Weave polished flexible cane strips into comfortable armchairs and decorative baskets."
    },
    {
        "gloss": "JAAPI_HAT",
        "en": "Jaapi / Traditional Conical Bamboo Hat of Assam",
        "hi": "जापी / असमिया शंकु टोपी",
        "ta": "ஜாபி மூங்கில் தொப்பி",
        "category": "daily",
        "description": "Wide conical sunhat woven from tokou leaves and bamboo, trimmed with red and white felt."
    },
    {
        "gloss": "MUGA_GOLDEN_SILK",
        "en": "Muga Golden Silk / Royal Silk of Assam",
        "hi": "मूगा गोल्डन सिल्क / असम का शाही रेशम",
        "ta": "முகா தங்க பட்டு",
        "category": "daily",
        "description": "Naturally glittering golden yellow wild silk that shines brighter with every wash."
    },
    {
        "gloss": "ERI_SILK_AHIMSA",
        "en": "Eri Silk / Ahimsa Peace Silk / Endi Cloth",
        "hi": "एरी सिल्क / अहिंसा रेशम",
        "ta": "எரி பட்டு (அகிம்சை பட்டு)",
        "category": "daily",
        "description": "Spin warm woolly textured silk extracted without harming the moth inside cocoon."
    },
    {
        "gloss": "PAT_SILK",
        "en": "Pat Silk / White Mulberry Silk of Assam",
        "hi": "पाट रेशम / सफेद शहतूत सिल्क",
        "ta": "பாட் பட்டு",
        "category": "daily",
        "description": "Brilliant natural white silk woven into bridal wear with crimson Kingkhap motifs."
    },
    {
        "gloss": "MEKHELA_SADOR",
        "en": "Mekhela Sador / Two-Piece Traditional Attire",
        "hi": "मेखेला चादर / पारंपरिक परिधान",
        "ta": "மேகலா சடோர்",
        "category": "daily",
        "description": "Drape pleated cylindrical skirt (Mekhela) around waist, tuck triangular top drape (Sador) around chest."
    },
    {
        "gloss": "NAGA_SHAWL_WEAVE",
        "en": "Naga Tribal Shawl / Tsungkotepsu & Angami Pattern",
        "hi": "नागा शॉल बुनाई",
        "ta": "நாகா சால்வை",
        "category": "daily",
        "description": "Bold red, black and white horizontal stripes woven with stylized tiger, elephant and human figures."
    },
    {
        "gloss": "TRIPURA_RIGNAL",
        "en": "Rignai & Rikutu / Traditional Attire of Tripura",
        "hi": "रिगनाई एवं रिकुतु वस्त्र",
        "ta": "ரிக்னாய் உடை",
        "category": "daily",
        "description": "Wrap colorful hand-woven cloth around waist with matching chest wrap."
    },
    {
        "gloss": "MIZO_PUAN",
        "en": "Mizo Puan / Handwoven Wrap Skirt / Puanchei",
        "hi": "मिज़ो पुआन / पारंपरिक स्कर्ट",
        "ta": "மிசோ புவான்",
        "category": "daily",
        "description": "Vibrant black and white checkered handloom wrap worn for festive celebrations."
    },
    {
        "gloss": "LOIN_LOOM_WEAVING",
        "en": "Backstrap Loin Loom Weaving / Tribal Craft",
        "hi": "बैकस्ट्रैप लोइन लूम बुनाई",
        "ta": "இடுப்பு தறி நெசவு",
        "category": "daily",
        "description": "Weaver sits on floor with strap around lower back controlling warp tension with own body."
    },
    {
        "gloss": "HANDLOOM_SHUTTLE",
        "en": "Handloom Wooden Shuttle Throwing",
        "hi": "हथकरघा शटल",
        "ta": "நெசவு நாடா",
        "category": "daily",
        "description": "Shoot polished wooden shuttle through parted shed of threads, beat reed firmly."
    },
    {
        "gloss": "ASSAM_ORTHODOX_TEA",
        "en": "Assam Orthodox Black Tea / Rich Malty Brew",
        "hi": "असम ऑर्थोडॉक्स ब्लैक टी",
        "ta": "அசாம் தேநீர்",
        "category": "daily",
        "description": "Whole golden tipped tea leaves steeping into rich dark amber malty liquor."
    },
    {
        "gloss": "TEA_ESTATE_VALLEY",
        "en": "Tea Estate Valley / Sprawling Green Slopes",
        "hi": "चाय बागान घाटी",
        "ta": "தேயிலைத் தோட்ட பள்ளத்தாக்கு",
        "category": "daily",
        "description": "Vast emerald green manicured tea bushes spreading across hill slopes under shade trees."
    },
    {
        "gloss": "TWO_LEAVES_ONE_BUD",
        "en": "Two Leaves and a Bud / Premium Plucking Standard",
        "hi": "दो पत्तियां और एक कली",
        "ta": "இரண்டு இலைகள் ஒரு மொட்டு",
        "category": "daily",
        "description": "Carefully pinch tender terminal shoot consisting of two soft leaves and unopened golden bud."
    },
    {
        "gloss": "TEA_FACTORY_DRYER",
        "en": "Tea Processing Withering Troughs & Fluidized Bed Dryer",
        "hi": "चाय प्रसंस्करण ड्रायर",
        "ta": "தேயிலை உலர் இயந்திரம்",
        "category": "civic",
        "description": "Blow warm conditioned air across green leaf withering troughs to reduce moisture."
    },
    {
        "gloss": "LARGE_CARDAMOM",
        "en": "Large Black Cardamom / Badi Elaichi of Sikkim",
        "hi": "बड़ी इलायची / सिक्किम इलायची",
        "ta": "கருப்பு ஏலக்காய்",
        "category": "daily",
        "description": "Large rough black smoked aromatic pods grown in high shaded mountain valleys."
    },
    {
        "gloss": "KING_CHILLI_BHUT_JOLOKIA",
        "en": "Bhut Jolokia / Ghost Pepper / King Chilli of Assam & Nagaland",
        "hi": "भूत जोलोकिया / राजा मिर्च",
        "ta": "பூட் ஜோலோக்கியா மிளகாய்",
        "category": "daily",
        "description": "Fiery crimson wrinkled pepper, touch tip to tongue and fan blazing spicy mouth."
    },
    {
        "gloss": "BAMBOO_SHOOT_FERMENT",
        "en": "Fermented Bamboo Shoot / Khorisa / Bastanga",
        "hi": "खोरिसा / किण्वित बांस का अंकुर",
        "ta": "மூங்கில் குருத்து ஊறுகாய்",
        "category": "daily",
        "description": "Grate tender inner ivory bamboo shoot, ferment into aromatic sour culinary seasoning."
    },
    {
        "gloss": "SMOKED_PORK_TRADITIONAL",
        "en": "Smoked Meat with Axone / Fermented Soybean",
        "hi": "स्मोक्ड मीट एवं एक्सोने",
        "ta": "பாரம்பரிய சமையல்",
        "category": "daily",
        "description": "Meat cured over kitchen hearth smoke, simmered with pungent fermented soy cake."
    },
    {
        "gloss": "FISH_TENGA",
        "en": "Masor Tenga / Sour Fish Curry with Elephant Apple",
        "hi": "मासोर टेंगा / खट्टी मछली करी",
        "ta": "புளிப்பு மீன் குழம்பு",
        "category": "daily",
        "description": "Light refreshing sour fish broth simmered with tomato, lemon, and outenga (elephant apple)."
    },
    {
        "gloss": "PITHA_RICE_CAKE",
        "en": "Pitha / Steamed & Roasted Rice Rolls / Til Pitha",
        "hi": "पीठा / तिल पीठा",
        "ta": "பிதா அரிசி கேக்",
        "category": "daily",
        "description": "Spread sticky rice flour on griddle, fill with roasted black sesame and jaggery, roll cylindrical."
    },
    {
        "gloss": "LARU_SWEET",
        "en": "Narikol Laru / Coconut & Jaggery Sweet Balls",
        "hi": "लारू / नारियल के लड्डू",
        "ta": "தேங்காய் உருண்டை",
        "category": "daily",
        "description": "Roll freshly grated coconut cooked in warm molten jaggery into round sweet balls."
    },
    {
        "gloss": "BLACK_RICE_MANIPUR",
        "en": "Chak-Hao / Manipuri Black Aromatic Rice",
        "hi": "चक-हाओ / मणिपुर का काला चावल",
        "ta": "கருப்பு அரிசி",
        "category": "daily",
        "description": "Cook deep royal purple sweet nutty aromatic whole grain rice dessert."
    },
    {
        "gloss": "GONGURA_ROSSELLE",
        "en": "Roselle Leaves / Tengamora / Sour Greens",
        "hi": "तेंगमोरा / खट्टी पत्तियां",
        "ta": "புளிச்சக்கீரை",
        "category": "daily",
        "description": "Tart sour red calyxes and green leaves stewed into tangy comforting broth."
    },
    {
        "gloss": "STICKY_RICE_BORA",
        "en": "Bora Saul / Glutinous Sticky Rice of Assam",
        "hi": "बोरा साउल / चिपचिपा चावल",
        "ta": "ஒட்டும் அரிசி",
        "category": "daily",
        "description": "Soak indigenous glutinous rice in water, steam inside green bamboo tube over fire."
    },
    {
        "gloss": "RONGALI_BIHU",
        "en": "Rongali Bihu / Bohag Bihu Spring Festival of Merriment",
        "hi": "रोंगाली बिहू / बोहाग बिहू",
        "ta": "ரொங்காலி பிஹு",
        "category": "greeting",
        "description": "Joyous celebration welcoming Assamese New Year, youth singing and dancing in fields."
    },
    {
        "gloss": "BHOGALI_BIHU",
        "en": "Bhogali Bihu / Magh Bihu Harvest Feast & Meji Bonfires",
        "hi": "भोगाली बिहू / माघ बिहू",
        "ta": "போகாலி பிஹு",
        "category": "greeting",
        "description": "Light towering conical thatch bonfires (Meji) at dawn, feast on pitha and chira with neighbors."
    },
    {
        "gloss": "KONGALI_BIHU",
        "en": "Kongali Bihu / Kati Bihu Earthen Lamp Offering",
        "hi": "कोंगाली बिहू / काति बिहू",
        "ta": "கொங்காலி பிஹு",
        "category": "greeting",
        "description": "Place clay oil lamps (saki) at base of sacred Tulsi plant and in growing paddy fields praying for protection."
    },
    {
        "gloss": "BIHU_DANCE_DHOL",
        "en": "Bihu Dance / Fast Hip Movement & Dhol Beats",
        "hi": "बिहू नृत्य एवं ढोल",
        "ta": "பிஹு நடனம்",
        "category": "greeting",
        "description": "Swirling rapid hip thrusts, open palm flexes, dancing to brisk syncopated beats of Dhol drum."
    },
    {
        "gloss": "PEPA_HORN_PIPE",
        "en": "Pepa / Buffalo Horn Aerophone Pipe",
        "hi": "पेपा वाद्य / सींग की बांसुरी",
        "ta": "எருமை கொம்பு இசைக்கருவி",
        "category": "greeting",
        "description": "Blow through buffalo horn mouthpiece producing high-pitched wailing Bihu melody."
    },
    {
        "gloss": "HORNBILL_FESTIVAL",
        "en": "Hornbill Festival of Nagaland / Festival of Festivals",
        "hi": "हॉर्नबिल महोत्सव नागालैंड",
        "ta": "ஹார்ன்பில் திருவிழா",
        "category": "greeting",
        "description": "Seventeen Naga tribes gather in full warrior regalia at Kisama heritage village singing war chants."
    },
    {
        "gloss": "WANGALA_DRUM_FESTIVAL",
        "en": "Wangala 100 Drums Festival / Garo Post-Harvest Utsav",
        "hi": "वांगला 100 ड्रम महोत्सव",
        "ta": "வங்காளா 100 முரசு திருவிழா",
        "category": "greeting",
        "description": "Men and women beat hundred long wooden barrel drums in unison, honoring sun god Misi Saljong."
    },
    {
        "gloss": "CHAPCHAR_KUT_DANCE",
        "en": "Chapchar Kut / Spring Bamboo Festival of Mizoram",
        "hi": "चापचार कुट महोत्सव",
        "ta": "சாப்சார் குட்",
        "category": "greeting",
        "description": "Perform graceful group folk dances welcoming spring after clearing hill forests."
    },
    {
        "gloss": "SANGAI_FESTIVAL",
        "en": "Sangai Festival / Manipur Tourism & Martial Arts Extravaganza",
        "hi": "संगाई महोत्सव मणिपुर",
        "ta": "சங்காய் திருவிழா",
        "category": "greeting",
        "description": "Showcase Thang-Ta sword fighting, classical Raas Leela dance, and polo tournament."
    },
    {
        "gloss": "LOSAR_NEW_YEAR",
        "en": "Losar / Tibetan & Monpa New Year Festival",
        "hi": "लोसार नववर्ष",
        "ta": "லோசார் புத்தாண்டு",
        "category": "greeting",
        "description": "Hoist colorful prayer flags, share auspicious barley grain (Chemar), monastic cham dances."
    },
    {
        "gloss": "MOATSU_FESTIVAL",
        "en": "Moatsu Festival of the Ao Nagas / Sowing Season",
        "hi": "मोआत्सु उत्सव",
        "ta": "மோட்சு திருவிழா",
        "category": "greeting",
        "description": "Celebrate completion of seed sowing with community dances around village central fire."
    },
    {
        "gloss": "TORGYA_MONASTERY",
        "en": "Torgya Monastic Mask Dance of Tawang",
        "hi": "तोरग्या मुखौटा नृत्य तवांग",
        "ta": "டோர்க்யா நடனம்",
        "category": "greeting",
        "description": "Lamas in elaborate animal and wrathful deity masks twirl driving away evil spirits."
    },
    {
        "gloss": "CHERAW_BAMBOO_DANCE",
        "en": "Cheraw Dance / Fast Bamboo Pole Stepping of Mizoram",
        "hi": "चेराव बांस नृत्य",
        "ta": "மூங்கில் நடனம்",
        "category": "greeting",
        "description": "Dancers leap swiftly in and out of rhythmic clapping horizontal bamboo poles."
    },
    {
        "gloss": "TRIBAL_COUNCIL_GAONBURA",
        "en": "Gaon Bura / Village Council of Elders",
        "hi": "गाँव बूढ़ा / ग्रामीण परिषद्",
        "ta": "கிராமப் பெரியவர் மன்றம்",
        "category": "civic",
        "description": "Venerated elder council resolving clan disputes by customary indigenous law."
    },
    {
        "gloss": "MORUNG_DORMITORY",
        "en": "Morung / Traditional Youth Dormitory & Cultural Academy",
        "hi": "मोरुंग / युवा छात्रावास",
        "ta": "பாரம்பரிய இளைஞர் இல்லம்",
        "category": "academic",
        "description": "Great wooden pillared lodge where youth learn oral histories, warfare, and woodcarving."
    },
    {
        "gloss": "VILLAGE_HEADMAN",
        "en": "Village Headman / Angh / Nokma",
        "hi": "ग्राम प्रधान / मुखिया",
        "ta": "கிராமத் தலைவர்",
        "category": "civic",
        "description": "Hereditary chieftain wearing hornbill feather crown and brass warrior collar."
    },
    {
        "gloss": "COMMUNITY_GRANARY",
        "en": "Community Granary / Paddy Storage Barn",
        "hi": "सामुदायिक अन्नागार",
        "ta": "சமூக நெற்களஞ்சியம்",
        "category": "daily",
        "description": "Elevated wooden stilt barns built outside village to safeguard harvest from fire."
    },
    {
        "gloss": "COMMUNITY_FEAST",
        "en": "Traditional Village Community Feast",
        "hi": "सामुदायिक भोज",
        "ta": "சமூக விருந்து",
        "category": "daily",
        "description": "Entire village cooks together in massive outdoor iron cauldrons, sharing food as one."
    },
    {
        "gloss": "PEACE_ACCORD",
        "en": "Peace Accord & Regional Reconciliation",
        "hi": "शांति समझौता",
        "ta": "அமைதி ஒப்பந்தம்",
        "category": "civic",
        "description": "Shake hands firmly, lay down arms, sign historic pact for prosperity and development."
    },
    {
        "gloss": "BORDER_TRADE_POST",
        "en": "Border Trade Land Customs Station / Moreh & Nathu La",
        "hi": "सीमा व्यापार चौकी / मोरेह व नाथू ला",
        "ta": "எல்லை வர்த்தக மையம்",
        "category": "civic",
        "description": "Cross international border gate with trade goods under mutual customs treaty."
    },
    {
        "gloss": "TOWANG_MONASTERY",
        "en": "Tawang Monastery / Second Largest in the World",
        "hi": "तवांग मठ / बौद्ध विहार",
        "ta": "தவாங் மடாலயம்",
        "category": "navigation",
        "description": "Fortress-like Tibetan Buddhist monastery standing on mountain peak at 10,000 feet."
    },
    {
        "gloss": "RUMTEK_MONASTERY",
        "en": "Rumtek Monastery / Dharma Chakra Centre Sikkim",
        "hi": "रुमटेक मठ सिक्किम",
        "ta": "ரும்தெக் மடாலயம்",
        "category": "navigation",
        "description": "Golden stupa, exquisite thangka paintings, and monks chanting resonant bass prayers."
    },
    {
        "gloss": "KAMAKHYA_SHRINE",
        "en": "Kamakhya Temple / Nilachal Hill Tantric Seat",
        "hi": "कामाख्या देवी मंदिर / नीलाचल पहाड़ी",
        "ta": "காமாக்யா கோயில்",
        "category": "navigation",
        "description": "Beehive beehive shikhara stone temple over subterranean spring sanctum."
    },
    {
        "gloss": "UNAKOTI_CARVINGS",
        "en": "Unakoti Bas-Relief Rock Carvings of Tripura",
        "hi": "उनाकोटी शैलकर्तित मूर्तियाँ",
        "ta": "உனகோட்டி பாறைச் சிற்பங்கள்",
        "category": "navigation",
        "description": "Colossal 30-foot Shiva rock carving chiseled directly into vertical hillside cliff."
    },
    {
        "gloss": "NEERMAHAL_PALACE",
        "en": "Neermahal / Twijilikma Water Palace of Tripura",
        "hi": "नीरमहल जल महल",
        "ta": "நீர் மஹால் அரண்மனை",
        "category": "navigation",
        "description": "Red and white fairy-tale marble palace floating in center of Rudrasagar Lake."
    },
    {
        "gloss": "NORTHEAST_DEAF_CONSORTIUM",
        "en": "North East Deaf Consortium / ISLRTC Chapter",
        "hi": "उत्तर-पूर्व बधिर संघ",
        "ta": "வடகிழக்கு காதுகேளாதோர் கூட்டமைப்பு",
        "category": "meta",
        "description": "Deaf leaders from eight sister states joining hands in unified regional sign advancement."
    },
    {
        "gloss": "SIGN_HARMONY_NORTHEAST",
        "en": "Sign Harmony Across the Eight Sister States",
        "hi": "अष्टलक्ष्मी सांकेतिक सद्भाव",
        "ta": "எட்டு மாநில சைகை ஒற்றுமை",
        "category": "meta",
        "description": "Interlocking circular sign embrace celebrating linguistic unity in hill and valley diversity."
    }
]
