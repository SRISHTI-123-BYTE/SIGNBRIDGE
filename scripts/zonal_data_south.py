# scripts/zonal_data_south.py
"""
Standard ISL — Southern Zone Chapter (isl-south) - 100 Domain Specific Signs
Focus: Tamil Nadu, Karnataka, Kerala, Telangana, Andhra Pradesh.
IT & tech corridors (Bengaluru, Cyberabad, OMR), premier South Indian deaf institutions (NISH, Little Flower, DEF),
coastal & maritime ecosystems, spice & coffee plantations, Dravidian classical arts & cuisine.
"""

SOUTH_SIGNS = [
    {
        "gloss": "CHENNAI",
        "en": "Chennai / Gateway to the South",
        "hi": "चेन्नई / मद्रास",
        "ta": "சென்னை",
        "category": "navigation",
        "description": "Fingerspell C-H, then mime cool Marina beach sea breeze with open hand waving."
    },
    {
        "gloss": "BENGALURU",
        "en": "Bengaluru / Silicon Valley of India",
        "hi": "बेंगलुरु / सिलिकॉन वैली",
        "ta": "பெங்களூரு",
        "category": "navigation",
        "description": "Fingerspell B-G-R, rapid keyboard typing transitioning into pleasant garden city foliage."
    },
    {
        "gloss": "HYDERABAD",
        "en": "Hyderabad / City of Pearls & Cyberabad",
        "hi": "हैदराबाद / मोतियों का शहर",
        "ta": "ஹைதராபாத்",
        "category": "navigation",
        "description": "Both hands outline the four tall minarets and grand arches of Charminar."
    },
    {
        "gloss": "THIRUVANANTHAPURAM",
        "en": "Thiruvananthapuram / Ananthapuri",
        "hi": "तिरुवनंतपुरम / त्रिवेंद्रम",
        "ta": "திருவனந்தபுரம்",
        "category": "navigation",
        "description": "Trace seven-headed serpent canopy gesture over heart, followed by NISH institute salute."
    },
    {
        "gloss": "KOCHI",
        "en": "Kochi / Queen of the Arabian Sea",
        "hi": "कोच्चि / कोचीन",
        "ta": "கொச்சி",
        "category": "navigation",
        "description": "Lower and raise cantilevered wooden Chinese fishing nets against ocean tide."
    },
    {
        "gloss": "COIMBATORE",
        "en": "Coimbatore / Manchester of South India",
        "hi": "कोयंबटूर",
        "ta": "கோயம்புத்தூர்",
        "category": "navigation",
        "description": "Spinning textile motor spindles and pump manufacturing machinery sign."
    },
    {
        "gloss": "MADURAI",
        "en": "Madurai / Temple City of Jasmine",
        "hi": "मदुरै / मीनाक्षी नगरी",
        "ta": "மதுரை",
        "category": "navigation",
        "description": "Meenakshi temple towering gopuram outline, sniff fragrant white mallipoo jasmine."
    },
    {
        "gloss": "VISAKHAPATNAM",
        "en": "Visakhapatnam / City of Destiny / Vizag",
        "hi": "विशाखापट्टनम / विज़ाग",
        "ta": "விசாகப்பட்டினம்",
        "category": "navigation",
        "description": "Dolphin's nose promontory hill overlooking deepwater naval harbor."
    },
    {
        "gloss": "VIJAYAWADA",
        "en": "Vijayawada / Kanaka Durga City",
        "hi": "विजयवाड़ा",
        "ta": "விஜயவாடா",
        "category": "navigation",
        "description": "Prakasam barrage water gates spanning the wide Krishna river."
    },
    {
        "gloss": "MYSURU",
        "en": "Mysuru / City of Palaces",
        "hi": "मैसूरू / महलों का शहर",
        "ta": "மைசூரு",
        "category": "navigation",
        "description": "Grand illuminated palace domes lit with thousands of golden bulbs."
    },
    {
        "gloss": "KAVERI_RIVER",
        "en": "Kaveri River / Sacred Southern Lifeblood",
        "hi": "कावेरी नदी",
        "ta": "காவிரி ஆறு",
        "category": "navigation",
        "description": "River flowing gently down from Talakaveri hills blessing fertile Thanjavur delta."
    },
    {
        "gloss": "KRISHNA_RIVER",
        "en": "Krishna River",
        "hi": "कृष्णा नदी",
        "ta": "கிருஷ்ணா ஆறு",
        "category": "navigation",
        "description": "Wide powerful river currents coursing through Deccan rocky valleys."
    },
    {
        "gloss": "GODAVARI_RIVER",
        "en": "Godavari River / Dakshin Ganga",
        "hi": "गोदावरी नदी / दक्षिण गंगा",
        "ta": "கோதாவரி ஆறு",
        "category": "navigation",
        "description": "Grand expansive waters with historic railway bridge spanning horizon."
    },
    {
        "gloss": "PERIYAR_RIVER",
        "en": "Periyar River / Kerala Evergreen Waters",
        "hi": "पेरियार नदी",
        "ta": "பெரியார் ஆறு",
        "category": "navigation",
        "description": "Clear forested river flowing past cardamom hills and wild elephant herds."
    },
    {
        "gloss": "WESTERN_GHATS",
        "en": "Western Ghats / Sahyadri Biodiversity Range",
        "hi": "पश्चिमी घाट / सह्याद्रि",
        "ta": "மேற்குத் தொடர்ச்சி மலை",
        "category": "navigation",
        "description": "Continuous wall of mist-covered lush green mountain ridges rising steeply."
    },
    {
        "gloss": "EASTERN_GHATS",
        "en": "Eastern Ghats / Discontinuous Hill Range",
        "hi": "पूर्वी घाट",
        "ta": "கிழக்குத் தொடர்ச்சி மலை",
        "category": "navigation",
        "description": "Broken rolling forested ridges sloping gently toward the Coromandel coast."
    },
    {
        "gloss": "ARABIAN_SEA_COAST",
        "en": "Arabian Sea Coast / Malabar Coastline",
        "hi": "अरब सागर तट / मालाबार तट",
        "ta": "அரபிக்கடல் கடற்கரை",
        "category": "navigation",
        "description": "Rolling ocean surf breaking against golden sands shaded by coconut palms."
    },
    {
        "gloss": "BAY_OF_BENGAL",
        "en": "Bay of Bengal / Coromandel Waters",
        "hi": "बंगाल की खाड़ी / कोरोमंडल तट",
        "ta": "வங்காள விரிகுடா",
        "category": "navigation",
        "description": "Wide open deep oceanic waves with coastal breeze."
    },
    {
        "gloss": "BACKWATERS_KERALA",
        "en": "Kerala Backwaters / Kayal Lagoon Network",
        "hi": "केरल बैकवाटर्स / कयाल",
        "ta": "கேரள உப்பங்கழிகள்",
        "category": "navigation",
        "description": "Both palms glide parallel through serene network of interconnected palm-fringed lagoons."
    },
    {
        "gloss": "HOUSEBOAT_KETTUVALLAM",
        "en": "Kettuvallam Houseboat / Thatch Roofed Barge",
        "hi": "केट्टुवल्लम हाउस Ferrara / हाउसबोट",
        "ta": "கெட்டுவள்ளம் படகு வீடு",
        "category": "navigation",
        "description": "Arched woven bamboo roof barge propelled slowly by long wooden pole."
    },
    {
        "gloss": "COASTAL_PORT",
        "en": "Coastal Commercial Harbor & Wharf",
        "hi": "तटीय बंदरगाह",
        "ta": "கடற்கரை துறைமுகம்",
        "category": "navigation",
        "description": "Gantry crane hoisting cargo container off vessel at deepwater quay."
    },
    {
        "gloss": "FISHERMAN_BOAT",
        "en": "Traditional Fishing Boat / Catamaran / Vallam",
        "hi": "मछुआरों की नाव / वल्लम",
        "ta": "மீன்பிடி படகு",
        "category": "navigation",
        "description": "Two curved hands form boat hull slicing through early morning surf, cast circular net."
    },
    {
        "gloss": "LIGHTHOUSE_COAST",
        "en": "Coastal Lighthouse Beacon",
        "hi": "प्रकाशस्तंभ / लाइटहाउस",
        "ta": "கலங்கரை விளக்கம்",
        "category": "navigation",
        "description": "Tall spiral tower with rotating beam of light sweeping across dark sea."
    },
    {
        "gloss": "COCONUT_GROVE",
        "en": "Coconut Palm Grove / Kalpavriksha",
        "hi": "नारियल का बाग",
        "ta": "தென்னந்தோப்பு",
        "category": "daily",
        "description": "Tall slender trunk swaying high, feathery fronds arching outward under heavy green coconuts."
    },
    {
        "gloss": "COCONUT_OIL",
        "en": "Pure Cold-Pressed Coconut Oil",
        "hi": "नारियल का तेल",
        "ta": "தேங்காய் எண்ணெய்",
        "category": "daily",
        "description": "Break fresh coconut, sniff pure aromatic oil, massage soothing drops into hair."
    },
    {
        "gloss": "SPICE_PLANTATION",
        "en": "Spice Plantation / Hill Estate",
        "hi": "मसालों के बागान",
        "ta": "மசாலாத் தோட்டம்",
        "category": "daily",
        "description": "Walk among fragrant terraced bushes plucking wild aromatic pods."
    },
    {
        "gloss": "BLACK_PEPPER",
        "en": "Black Pepper / King of Spices / Malabar Pepper",
        "hi": "काली मिर्च",
        "ta": "கருப்பு மிளகு",
        "category": "daily",
        "description": "Small pungent black peppercorns crushed between thumb and fingers, sharp spicy aroma."
    },
    {
        "gloss": "CARDAMOM",
        "en": "Green Cardamom / Queen of Spices / Elaichi",
        "hi": "हरी इलायची",
        "ta": "ஏலக்காய்",
        "category": "daily",
        "description": "Pluck oval ribbed green pod, split open to reveal aromatic sweet seeds."
    },
    {
        "gloss": "CLOVES_SPICE",
        "en": "Cloves / Lavangam",
        "hi": "लौंग",
        "ta": "கிராம்பு",
        "category": "daily",
        "description": "Small nail-shaped flower bud touched to tooth, relieving ache with pungent warmth."
    },
    {
        "gloss": "RUBBER_ESTATE",
        "en": "Rubber Plantation / Latex Tapping",
        "hi": "रबर बागान / लेटेक्स निष्कर्षण",
        "ta": "ரப்பர் தோட்டம்",
        "category": "daily",
        "description": "Carve spiral groove in tree bark, milky white latex dripping into coconut shell cup."
    },
    {
        "gloss": "COFFEE_PLANTATION",
        "en": "Coffee Estate / Arabica & Robusta Hills",
        "hi": "कॉफी बागान",
        "ta": "காபி தோட்டம்",
        "category": "daily",
        "description": "Pluck bright red ripe coffee cherries from shaded evergreen bushes."
    },
    {
        "gloss": "ARECA_NUT",
        "en": "Areca Nut / Supari Palm",
        "hi": "सुपारी का पेड़",
        "ta": "பாக்கு மரம்",
        "category": "daily",
        "description": "Slender tall palm tree, slice tough nut with brass betel cutter."
    },
    {
        "gloss": "BETEL_LEAF",
        "en": "Fresh Betel Leaf / Paan / Vetrillai",
        "hi": "पान का पत्ता",
        "ta": "வெற்றிலை",
        "category": "daily",
        "description": "Heart-shaped fresh green leaf smeared with edible slaked lime paste."
    },
    {
        "gloss": "CASHEW_NUT",
        "en": "Cashew Nut & Apple / Mundiri",
        "hi": "काजू",
        "ta": "முந்திரி",
        "category": "daily",
        "description": "Kidney-shaped nut hanging beneath juicy yellow cashew apple."
    },
    {
        "gloss": "TAPIOCA",
        "en": "Tapioca Root / Kappa / Maravalli",
        "hi": "कसावा / टैपिओका",
        "ta": "மரவள்ளிக்கிழங்கு",
        "category": "daily",
        "description": "Dig up long starchy root tuber, peel bark, boil into tender white chunks."
    },
    {
        "gloss": "PADDY_FIELD_DELTA",
        "en": "Paddy Fields / Thanjavur Rice Bowl",
        "hi": "धान के लहलहाते खेत / कावेरी डेल्टा",
        "ta": "நெல் வயல்",
        "category": "daily",
        "description": "Transplant bright green young rice seedlings in flooded knee-deep mud waters."
    },
    {
        "gloss": "SILICON_VALLEY_INDIA",
        "en": "Silicon Valley of India / Tech Ecosystem",
        "hi": "भारत की सिलिकॉन वैली",
        "ta": "இந்தியாவின் சிலிக்கான் பள்ளத்தாக்கு",
        "category": "academic",
        "description": "Microchip integrated circuit pins connecting to globe software networks."
    },
    {
        "gloss": "CYBERABAD",
        "en": "Cyberabad / Hyderabad High-Tech City",
        "hi": "साइबराबाद हाईटेक सिटी",
        "ta": "சைபராபாத்",
        "category": "academic",
        "description": "Futuristic glass towers flashing fiber optic connectivity lines."
    },
    {
        "gloss": "OMR_IT_CORRIDOR",
        "en": "Old Mahabalipuram Road / IT Expressway Chennai",
        "hi": "ओएमआर आईटी एक्सप्रेसवे",
        "ta": "ஓ.எம்.ஆர் ஐடி விரைவுச்சாலை",
        "category": "navigation",
        "description": "Six-lane expressway flanked by shimmering multinational tech campuses."
    },
    {
        "gloss": "ELECTRONIC_CITY",
        "en": "Electronic City / Bengaluru Tech Hub",
        "hi": "इलेक्ट्रॉनिक सिटी",
        "ta": "எலக்ட்ரானிக் சிட்டி",
        "category": "navigation",
        "description": "Elevated toll flyover landing directly into high-tech software enclave."
    },
    {
        "gloss": "TECH_PARK",
        "en": "Software Technology Park / IT SEZ",
        "hi": "टेक पार्क / सॉफ्टवेयर पार्क",
        "ta": "தொழில்நுட்ப பூங்கா",
        "category": "civic",
        "description": "Campus badge swipe at turnstile gate leading into manicured tech lawn."
    },
    {
        "gloss": "SOFTWARE_CAMPUS",
        "en": "Multinational Software Campus",
        "hi": "सॉफ्टवेयर विकास केंद्र",
        "ta": "மென்பொருள் வளாகம்",
        "category": "academic",
        "description": "Sprawling corporate headquarters with glass atriums and engineering bays."
    },
    {
        "gloss": "DATA_CENTER_CLOUD",
        "en": "Hyperscale Cloud Data Center",
        "hi": "क्लाउड डेटा सेंटर",
        "ta": "தரவு மையம்",
        "category": "academic",
        "description": "Rows of tall black server racks blinking green with high-speed cooling airflow."
    },
    {
        "gloss": "STARTUP_INCUBATOR",
        "en": "Startup Accelerator & Seed Incubator",
        "hi": "स्टार्टअप इनक्यूबेटर",
        "ta": "தொழில்முனைவோர் வழிகாட்டு மையம்",
        "category": "academic",
        "description": "Seed sprouting from palm, rocket launching into rapid venture scaling."
    },
    {
        "gloss": "BIOTECH_PARK",
        "en": "Genome Valley / Biotechnology Park",
        "hi": "बायोटेक पार्क / जीनोम वैली",
        "ta": "உயிரி தொழில்நுட்ப பூங்கா",
        "category": "academic",
        "description": "Double helix DNA strand rotating, vaccine research under cleanroom laminar hood."
    },
    {
        "gloss": "HARDWARE_CLUSTER",
        "en": "Electronics & Semiconductor Manufacturing",
        "hi": "इलेक्ट्रॉनिक्स हार्डवेयर क्लस्टर",
        "ta": "மின்னணு வன்பொருள் மையம்",
        "category": "academic",
        "description": "Robotic arm mounting microscopic surface chips onto green circuit board."
    },
    {
        "gloss": "NISH_INSTITUTE",
        "en": "NISH / National Institute of Speech and Hearing",
        "hi": "राष्ट्रीय वाक् एवं श्रवण संस्थान (निश केरल)",
        "ta": "என்.ஐ.எஸ்.எச் நிறுவனம்",
        "category": "academic",
        "description": "Fingerspell N-I-S-H, point to ear and lips, raise sign research banner."
    },
    {
        "gloss": "LITTLE_FLOWER_DEAF",
        "en": "Little Flower Convent Higher Secondary for the Deaf",
        "hi": "लिटिल फ्लावर डेफ स्कूल चेन्नई",
        "ta": "லிட்டில் பிளவர் காதுகேளாதோர் பள்ளி",
        "category": "academic",
        "description": "Blossoming little flower hand gesture blooming at heart, deaf student salute."
    },
    {
        "gloss": "DEF_HYDERABAD",
        "en": "Deaf EnAbled Foundation / DEF Hyderabad",
        "hi": "डेफ इनेबल्ड फाउंडेशन (डीईएफ)",
        "ta": "டி.இ.எஃப் அறக்கட்டளை",
        "category": "academic",
        "description": "Fingerspell D-E-F, open hands uplifting deaf youth toward professional empowerment."
    },
    {
        "gloss": "TAMIL_SYNTHESIS",
        "en": "Tamil Sign Synthesis & Phonetical Relay",
        "hi": "तमिल सांकेतिक संश्लेषण",
        "ta": "தமிழ் சைகை ஒருங்கிணைப்பு",
        "category": "meta",
        "description": "Fingerspell Tamil vowel curves, blending seamlessly with ISL manual signs."
    },
    {
        "gloss": "SIGN_RELAY_SOUTH",
        "en": "Southern Regional Sign Video Relay Service",
        "hi": "सांकेतिक रिले सेवा दक्षिण",
        "ta": "தென் மண்டல சைகை ரிலே",
        "category": "meta",
        "description": "Video screen interface, interpreter bridging call between deaf signer and official."
    },
    {
        "gloss": "TRILINGUAL_CAPTION",
        "en": "Trilingual Captioning / English, Hindi, Regional",
        "hi": "त्रिभाषी उपशीर्षक",
        "ta": "மும்மொழி வசனங்கள்",
        "category": "meta",
        "description": "Three horizontal scrolling text streams aligned under video broadcast."
    },
    {
        "gloss": "TEMPLE_GOPURAM",
        "en": "Temple Gopuram / Multi-Tiered Gateway Tower",
        "hi": "मंदिर गोपुरम / भव्य प्रवेश द्वार",
        "ta": "கோயில் கோபுரம்",
        "category": "navigation",
        "description": "Steep pyramidal tower ascending in tiered sculptural layers topped by golden kalasams."
    },
    {
        "gloss": "DRAVIDIAN_ARCHITECTURE",
        "en": "Dravidian Stone Architecture / Mandapam Pillars",
        "hi": "द्रविड़ स्थापत्य कला",
        "ta": "திராவிடக் கட்டடக்கலை",
        "category": "academic",
        "description": "Carved monolithic granite musical pillar resonating with chime note when tapped."
    },
    {
        "gloss": "TEMPLE_CHARIOT_RATH",
        "en": "Temple Chariot / Massive Car Festival / Ther",
        "hi": "विशाल मंदिर रथ / तेरु",
        "ta": "தேர் திருவிழா",
        "category": "greeting",
        "description": "Thousands pulling giant thick coir ropes rolling monumental wooden chariot forward."
    },
    {
        "gloss": "BRONZE_IDOL",
        "en": "Chola Lost-Wax Bronze Idol / Nataraja",
        "hi": "कांस्य मूर्ति / नटराज",
        "ta": "வெண்கலச் சிலை",
        "category": "academic",
        "description": "Nataraja cosmic dance posture, ring of fire encircling uplifted graceful foot."
    },
    {
        "gloss": "BHARATANATYAM",
        "en": "Bharatanatyam / Classical Tamil Dance",
        "hi": "भरतनाट्यम शास्त्रीय नृत्य",
        "ta": "பரதநாட்டியம்",
        "category": "greeting",
        "description": "Aramandi half-sitting stance, crisp mudras and rhythmic footwork with ankle bells."
    },
    {
        "gloss": "KATHAKALI",
        "en": "Kathakali / Classical Dance Drama of Kerala",
        "hi": "कथकली नृत्य नाट्य",
        "ta": "கதகளி",
        "category": "greeting",
        "description": "Green paccha face makeup, billowing skirt, dramatic eye dart movements and crown."
    },
    {
        "gloss": "KUCHIPUDI",
        "en": "Kuchipudi / Classical Dance of Andhra Pradesh",
        "hi": "कुचिपुड़ी शास्त्रीय नृत्य",
        "ta": "குச்சிப்புடி",
        "category": "greeting",
        "description": "Dance balancing gracefully with bare feet on the rim of a polished brass plate."
    },
    {
        "gloss": "MOHINIYATTAM",
        "en": "Mohiniyattam / Dance of the Enchantress",
        "hi": "मोहिनीअट्टम",
        "ta": "மோகினியாட்டம்",
        "category": "greeting",
        "description": "Gentle swaying torso in white and gold kasavu saree like palm trees in breeze."
    },
    {
        "gloss": "CARNATIC_MUSIC",
        "en": "Carnatic Classical Music / Raga & Tala",
        "hi": "कर्नाटक शास्त्रीय संगीत",
        "ta": "கர்நாடக இசை",
        "category": "greeting",
        "description": "Hand tapping rhythmic laghu-drutam counts on thigh while vocalizing intricate raga gamakas."
    },
    {
        "gloss": "MRIDANGAM",
        "en": "Mridangam / Two-Headed Classical Drum",
        "hi": "मृदंगम वाद्य",
        "ta": "மிருதங்கம்",
        "category": "greeting",
        "description": "Two hands strike both drumheads producing resonant bass 'dheem' and crisp treble 'thom'."
    },
    {
        "gloss": "VEENA",
        "en": "Saraswati Veena / Plucked String Instrument",
        "hi": "सरस्वती वीणा",
        "ta": "சரஸ்வதி வீணை",
        "category": "greeting",
        "description": "Left hand glides along frets while right fingers pluck metal strings over resonator gourd."
    },
    {
        "gloss": "NADASWARAM",
        "en": "Nadaswaram / Auspicious Wind Instrument",
        "hi": "नादस्वरम",
        "ta": "நாதஸ்வரம்",
        "category": "greeting",
        "description": "Hold long flared wooden pipe blowing powerful auspicious wedding fanfare."
    },
    {
        "gloss": "PONGAL_FESTIVAL",
        "en": "Pongal Harvest Festival / Thai Pongal",
        "hi": "पोंगल उत्सव",
        "ta": "பொங்கல் திருவிழா",
        "category": "greeting",
        "description": "Clay pot boil over with fresh sweet rice, crowd calls out joyous 'Pongalo Pongal!'."
    },
    {
        "gloss": "ONAM_FESTIVAL",
        "en": "Onam / Kerala Grand Harvest & King Mahabali",
        "hi": "ओणम पर्व",
        "ta": "ஓணம் பண்டிகை",
        "category": "greeting",
        "description": "Lay concentric rings of fresh yellow flower petals (Pookkalam) welcoming King Mahabali."
    },
    {
        "gloss": "UGADI_FESTIVAL",
        "en": "Ugadi / Telugu & Kannada New Year",
        "hi": "उगादि नववर्ष",
        "ta": "யுகாதி திருநாள்",
        "category": "greeting",
        "description": "Taste Ugadi Pacchadi blending sweet, sour, bitter, salty, pungent and astringent flavors."
    },
    {
        "gloss": "VISHU_KANI",
        "en": "Vishu / Malayali New Year & Vishukkani",
        "hi": "विशु पर्व",
        "ta": "விசு கனி",
        "category": "greeting",
        "description": "Open eyes at dawn before brass uruli filled with golden cucumber, mirror and coins."
    },
    {
        "gloss": "BATHUKAMMA",
        "en": "Bathukamma / Telangana Floral Festival",
        "hi": "बथुकम्मा फूलों का त्योहार",
        "ta": "பதுகம்மா மலர் திருவிழா",
        "category": "greeting",
        "description": "Conical tower of colorful seasonal flowers, women clap hands dancing in graceful circles."
    },
    {
        "gloss": "THRISSUR_POORAM",
        "en": "Thrissur Pooram / Festival of Temples",
        "hi": "त्रिशूर पूरम",
        "ta": "திருச்சூர் பூரம்",
        "category": "greeting",
        "description": "Majestic caparisoned elephants, changing colorful silk parasols (Kudamattom) in rhythm."
    },
    {
        "gloss": "JALLIKATTU",
        "en": "Jallikattu / Traditional Bull Embracing",
        "hi": "जल्लीकट्टू / पारंपरिक सांड उत्सव",
        "ta": "ஜல்லிக்கட்டு",
        "category": "greeting",
        "description": "Embrace strong hump of charging bull with courage and athletic agility."
    },
    {
        "gloss": "BOAT_RACE_VALLAM",
        "en": "Vallam Kali / Nehru Trophy Snake Boat Race",
        "hi": "वल्लम कली / नौका दौड़",
        "ta": "படகுப் போட்டி",
        "category": "greeting",
        "description": "A hundred oarsmen dip slender paddles in perfect unison powering long snake boat."
    },
    {
        "gloss": "FILTER_COFFEE",
        "en": "South Indian Filter Coffee / Degree Coffee",
        "hi": "फिल्टर कॉफी",
        "ta": "பில்டர் காபி",
        "category": "daily",
        "description": "Pour hot frothy coffee from high dabarah into tumbler forming velvety white foam."
    },
    {
        "gloss": "IDLI",
        "en": "Steamed Rice Idli / Soft Pillows",
        "hi": "इडली / वाष्प चावल केक",
        "ta": "இட்லி",
        "category": "daily",
        "description": "Steam white batter in round dimpled plates, demold cloud-soft fluffy idlis."
    },
    {
        "gloss": "DOSA",
        "en": "Crispy Dosa / Ghee Roast Crepe",
        "hi": "डोसा / घी रोस्ट",
        "ta": "தோசை",
        "category": "daily",
        "description": "Spread thin batter on hot tawa in fast circles, flip golden crispy golden crepe."
    },
    {
        "gloss": "SAMBAR",
        "en": "Sambar / Spiced Lentil & Vegetable Stew",
        "hi": "सांबर",
        "ta": "சாம்பார்",
        "category": "daily",
        "description": "Simmer toor dal with drumstick, shallots and freshly ground roasted spices."
    },
    {
        "gloss": "RASAM",
        "en": "Rasam / Pepper & Tamarind Broth",
        "hi": "रसम",
        "ta": "ரசம்",
        "category": "daily",
        "description": "Simmer tangy tomato tamarind broth with crushed black pepper and garlic, pour over rice."
    },
    {
        "gloss": "MEDU_VADA",
        "en": "Medu Vada / Crispy Lentil Donut",
        "hi": "मेदु वड़ा",
        "ta": "மெது வடை",
        "category": "daily",
        "description": "Poke hole in center of black gram batter dumpling, drop into sizzling oil until crispy."
    },
    {
        "gloss": "UPMA",
        "en": "Upma / Savory Semolina Breakfast",
        "hi": "उपमा",
        "ta": "உப்மா",
        "category": "daily",
        "description": "Roast semolina, temper mustard seeds and curry leaves, stir into warm savory mash."
    },
    {
        "gloss": "APPAM",
        "en": "Appam / Fermented Rice Pancake with Coconut Milk",
        "hi": "अप्पम",
        "ta": "ஆப்பம்",
        "category": "daily",
        "description": "Swirl batter in curved appachatti, spongy thick center with crispy paper-thin lace edges."
    },
    {
        "gloss": "PUTTU",
        "en": "Puttu / Steamed Rice & Coconut Cylinder",
        "hi": "पुट्टू",
        "ta": "புட்டு",
        "category": "daily",
        "description": "Layer coarse rice flour with grated coconut in bamboo cylinder, steam until aromatic."
    },
    {
        "gloss": "PAYASAM",
        "en": "Payasam / Kheer / Sweet Dessert Pudding",
        "hi": "पायसम / खीर",
        "ta": "பாயாசம்",
        "category": "daily",
        "description": "Ladle rich sweet pudding of milk, jaggery, cardamom and golden roasted cashews."
    },
    {
        "gloss": "BANANA_LEAF_MEAL",
        "en": "Traditional Banana Leaf Sadhya Feast",
        "hi": "केले के पत्ते पर पारम्परिक भोजन",
        "ta": "வாழை இலை சாப்பாடு",
        "category": "daily",
        "description": "Unroll broad fresh plantain leaf, sprinkle water, serve twenty delicious curries in order."
    },
    {
        "gloss": "CURRY_LEAVES",
        "en": "Fresh Curry Leaves / Kariveppilai",
        "hi": "कढ़ी पत्ता",
        "ta": "கறிவேப்பிலை",
        "category": "daily",
        "description": "Strip fragrant fresh glossy dark green leaves from stem, temper in hot coconut oil."
    },
    {
        "gloss": "TAMARIND",
        "en": "Tamarind Pod / Puli",
        "hi": "इमली",
        "ta": "புளி",
        "category": "daily",
        "description": "Crack brittle brown pod shell, squeeze sticky tangy pulp into warm water."
    },
    {
        "gloss": "COIR_INDUSTRY",
        "en": "Coir Industry / Coconut Fiber Products",
        "hi": "कॉयर उद्योग / नारियल जटा",
        "ta": "கயிறு தொழில்",
        "category": "civic",
        "description": "Extract golden fiber from coconut husks, spin into durable marine ropes and door mats."
    },
    {
        "gloss": "SILK_KANCHIPURAM",
        "en": "Kanchipuram Silk Saree / Pure Zari Weave",
        "hi": "कांचीपुरम रेशमी साड़ी",
        "ta": "காஞ்சிபுரம் பட்டு",
        "category": "daily",
        "description": "Weave heavy pure mulberry silk interlinked with lustrous gold zari border."
    },
    {
        "gloss": "SILK_MYSURU",
        "en": "Mysuru Crepe Silk Saree",
        "hi": "मैसूर सिल्क साड़ी",
        "ta": "மைசூர் பட்டு",
        "category": "daily",
        "description": "Drape ultra-soft lightweight shimmering crepe silk saree with royal elegance."
    },
    {
        "gloss": "HANDLOOM_POCHAMPALLY",
        "en": "Pochampally Ikat Handloom / Geometric Weave",
        "hi": "पोचमपल्ली इकत हथकरघा",
        "ta": "போச்சம்பள்ளி இக்கத்",
        "category": "daily",
        "description": "Tie-dye warp threads creating sharp diamond geometric patterns on wooden loom."
    },
    {
        "gloss": "AUTO_HUB_CHENNAI",
        "en": "Automobile Hub Chennai / Detroit of South Asia",
        "hi": "चेन्नई ऑटोमोबाइल उद्योग",
        "ta": "சென்னை வாகன உற்பத்தி",
        "category": "civic",
        "description": "Conveyor assembly line rolling out passenger cars and heavy commercial trucks."
    },
    {
        "gloss": "PHARMA_CITY_HYDERABAD",
        "en": "Hyderabad Pharma City / Vaccine Capital",
        "hi": "हैदराबाद फार्मा सिटी / टीका उत्पादन",
        "ta": "ஹைதராபாத் மருந்து உற்பத்தி",
        "category": "civic",
        "description": "Automated glass vial filling lines producing millions of life-saving vaccines."
    },
    {
        "gloss": "AEROSPACE_BENGALURU",
        "en": "Aerospace & Defence Hub Bengaluru / HAL & ISRO",
        "hi": "बेंगलुरु एयरोस्पेस हब",
        "ta": "பெங்களூரு விண்வெளி மையம்",
        "category": "academic",
        "description": "Assemble supersonic fighter aircraft fuselage and satellite payloads."
    },
    {
        "gloss": "SHIPYARD_COCHIN",
        "en": "Cochin Shipyard / Aircraft Carrier Construction",
        "hi": "कोचीन शिपयार्ड / नौसैनिक पोत निर्माण",
        "ta": "கொச்சின் கப்பல் கட்டும் தளம்",
        "category": "civic",
        "description": "Weld mammoth steel hull of indigenous aircraft carrier in dry dock."
    },
    {
        "gloss": "DEEPWATER_PORT_VIZAG",
        "en": "Visakhapatnam Deepwater Port & Harbor",
        "hi": "विशाखापट्टनम गहरा बंदरगाह",
        "ta": "விசாகப்பட்டினம் ஆழ்கடல் துறைமுகம்",
        "category": "navigation",
        "description": "Massive bulk cargo carrier maneuvering into landlocked natural harbor channel."
    },
    {
        "gloss": "MONSOON_SOUTHWEST",
        "en": "Southwest Monsoon / Edavappathi",
        "hi": "दक्षिण-पश्चिम मानसून",
        "ta": "தென்மேற்கு பருவமழை",
        "category": "daily",
        "description": "Heavy dark monsoon thunderclouds rolling in from Arabian Sea soaking parched soils."
    },
    {
        "gloss": "TROPICAL_HEAT",
        "en": "Tropical Coastal Climate & Humidity",
        "hi": "उष्णकटिबंधीय तटीय मौसम",
        "ta": "வெப்பமண்டல காலநிலை",
        "category": "daily",
        "description": "Warm ocean sea breeze wiping perspiration with handkerchief."
    },
    {
        "gloss": "VANAKKAM_SALUTE",
        "en": "Vanakkam / Traditional Tamil Greeting",
        "hi": "वणक्कम / तमिल अभिवादन",
        "ta": "வணக்கம்",
        "category": "greeting",
        "description": "Join both palms together at chest level with gentle bow of head."
    },
    {
        "gloss": "NAMASKARA",
        "en": "Namaskara / Kannada Greeting of Respect",
        "hi": "नमस्कारा / कन्नड़ अभिवादन",
        "ta": "நமஸ்காரா",
        "category": "greeting",
        "description": "Fold hands gracefully before heart with bright respectful smile."
    },
    {
        "gloss": "NAMASKARAM",
        "en": "Namaskaram / Malayalam Polite Greeting",
        "hi": "नमस्कारम / मलयालम अभिवादन",
        "ta": "நமஸ்காரம்",
        "category": "greeting",
        "description": "Both palms meet in reverence before chest acknowledging divinity in the other."
    },
    {
        "gloss": "AYURVEDA_WELLNESS",
        "en": "Ayurveda Wellness & Panchakarma",
        "hi": "आयुर्वेद चिकित्सा एवं पंचकर्म",
        "ta": "ஆயுர்வேத நலவாழ்வு",
        "category": "emergency",
        "description": "Warm herbal medicated oils poured in rhythmic stream over forehead (Shirodhara)."
    }
]
