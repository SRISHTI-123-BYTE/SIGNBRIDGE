# scripts/zonal_data_west.py
"""
Standard ISL — Western Zone Chapter (isl-west) - 100 Domain Specific Signs
Focus: Maharashtra, Gujarat, Goa, Daman & Diu.
Financial capital (BSE, NSE, Dalal Street, SEBI), diamond bourses, mega ports (JNPT, Kandla),
suburban local train lifeline, dabbawala logistics, industrial belts, western cuisine & festivals.
"""

WEST_SIGNS = [
    {
        "gloss": "MUMBAI",
        "en": "Mumbai / Financial Capital of India",
        "hi": "मुंबई / भारत की आर्थिक राजधानी",
        "ta": "மும்பை",
        "category": "navigation",
        "description": "Outline Gateway of India basalt arch overlooking the bustling Arabian Sea harbor."
    },
    {
        "gloss": "PUNE",
        "en": "Pune / Oxford of the East & Auto Hub",
        "hi": "पुणे / विद्यानगरी",
        "ta": "புனே",
        "category": "navigation",
        "description": "Fingerspell P-N, trace Shaniwar Wada fortress gates and college campus walkways."
    },
    {
        "gloss": "AHMEDABAD",
        "en": "Ahmedabad / Heritage City & Textile Hub",
        "hi": "अहमदाबाद",
        "ta": "அகமதாபாத்",
        "category": "navigation",
        "description": "Sabarmati Ashram spinning charkha, followed by modern riverfront promenade."
    },
    {
        "gloss": "SURAT",
        "en": "Surat / Diamond & Silk Textile City",
        "hi": "सूरत / हीरा एवं वस्त्र नगरी",
        "ta": "சூரத்",
        "category": "navigation",
        "description": "Glinting multifaceted diamond facet inspection with magnifying loupe."
    },
    {
        "gloss": "VADODARA",
        "en": "Vadodara / Cultural Capital of Gujarat / Baroda",
        "hi": "वडोदरा / बड़ौदा",
        "ta": "வதோதரா",
        "category": "navigation",
        "description": "Laxmi Vilas Palace majestic Indo-Saracenic royal facade."
    },
    {
        "gloss": "NAGPUR",
        "en": "Nagpur / Orange City & Zero Mile Center",
        "hi": "नागपुर / संतरा नगरी",
        "ta": "நாக்பூர்",
        "category": "navigation",
        "description": "Peel sweet juicy Nagpur orange, point to center stone of Indian subcontinent."
    },
    {
        "gloss": "NASHIK",
        "en": "Nashik / Wine Capital & Godavari Holy City",
        "hi": "नासिक / कुंभ नगरी",
        "ta": "நாசிக்",
        "category": "navigation",
        "description": "Grape bunches hanging on vine trellises by Godavari river ghats."
    },
    {
        "gloss": "PANAJI_GOA",
        "en": "Panaji Goa / Mandovi River Capital",
        "hi": "पणजी गोवा",
        "ta": "பனாஜி கோவா",
        "category": "navigation",
        "description": "Portuguese colonial whitewashed church belfry overlooking river cruises."
    },
    {
        "gloss": "RAJKOT",
        "en": "Rajkot / Saurashtra Industrial Center",
        "hi": "राजकोट",
        "ta": "ராஜ்கோட்",
        "category": "navigation",
        "description": "Diesel engine foundry and precision machine tools manufacturing motion."
    },
    {
        "gloss": "AURANGABAD_CSN",
        "en": "Chhatrapati Sambhajinagar / Aurangabad Caves City",
        "hi": "छत्रपति संभाजीनगर (औरंगाबाद)",
        "ta": "அவுரங்காபாத்",
        "category": "navigation",
        "description": "Outline world-heritage Ajanta and Ellora rock-cut cave monolithic temples."
    },
    {
        "gloss": "ARABIAN_SEA_WEST",
        "en": "Arabian Sea Western Coastline",
        "hi": "अरब सागर पश्चिम तट",
        "ta": "மேற்கு அரபிக்கடல்",
        "category": "navigation",
        "description": "Broad deep oceanic swell meeting rugged rocky western sea cliffs."
    },
    {
        "gloss": "GULF_OF_KUTCH",
        "en": "Gulf of Kutch Marine Sanctuary",
        "hi": "कच्छ की खाड़ी",
        "ta": "கட்ச் வளைகுடா",
        "category": "navigation",
        "description": "Enclosed sea inlet, coral reefs, mangroves and oil tanker berths."
    },
    {
        "gloss": "GULF_OF_KHAMBHAT",
        "en": "Gulf of Khambhat / High Tidal Estuary",
        "hi": "खंभात की खाड़ी",
        "ta": "கம்பாட் வளைகுடா",
        "category": "navigation",
        "description": "High tidal bore rushing through wide estuary funnel."
    },
    {
        "gloss": "NARMADA_RIVER",
        "en": "Narmada River / Holy Rewa",
        "hi": "नर्मदा नदी / रेवा",
        "ta": "நர்மதா ஆறு",
        "category": "navigation",
        "description": "Mighty river cutting through white marble rock gorge flowing westward into sea."
    },
    {
        "gloss": "TAPI_RIVER",
        "en": "Tapi River / Tapti Basin",
        "hi": "तापी नदी",
        "ta": "தாபி ஆறு",
        "category": "navigation",
        "description": "Westward flowing river nourishing rich black cotton agricultural soils."
    },
    {
        "gloss": "GODAVARI_ORIGIN",
        "en": "Godavari Origin / Trimbakeshwar Sacred Source",
        "hi": "गोदावरी उद्गम / त्र्यंबकेश्वर",
        "ta": "கோதாவரி பிறப்பிடம்",
        "category": "navigation",
        "description": "Spring water bubbling forth from Brahmagiri hill in sacred stone reservoir."
    },
    {
        "gloss": "KONKAN_COAST",
        "en": "Konkan Coastal Belt / Red Laterite Cliffs",
        "hi": "कोंकण तट",
        "ta": "கொங்கன் கடற்கரை",
        "category": "navigation",
        "description": "Scenic winding railway line crossing bridges between green hills and blue sea."
    },
    {
        "gloss": "RANN_OF_KUTCH",
        "en": "Great Rann of Kutch / White Salt Desert",
        "hi": "कच्छ का रण / सफेद रेगिस्तान",
        "ta": "கட்ச் வெள்ளை பாலைவனம்",
        "category": "navigation",
        "description": "Vast infinite horizon of gleaming white crystalline salt flats reflecting full moon."
    },
    {
        "gloss": "BOMBAY_STOCK_EXCHANGE",
        "en": "Bombay Stock Exchange / BSE Sensex",
        "hi": "बॉम्बे स्टॉक एक्सचेंज (बीएसई)",
        "ta": "மும்பை பங்குச் சந்தை",
        "category": "civic",
        "description": "Outline famous Phiroze Jeejeebhoy curved tower, fingerspell B-S-E, ticker tape rising."
    },
    {
        "gloss": "NATIONAL_STOCK_EXCHANGE",
        "en": "National Stock Exchange / NSE Nifty",
        "hi": "नेशनल स्टॉक एक्सचेंज (एनएसई)",
        "ta": "தேசிய பங்குச் சந்தை",
        "category": "civic",
        "description": "Fingerspell N-S-E, electronic trading screens updating thousands of orders."
    },
    {
        "gloss": "DALAL_STREET",
        "en": "Dalal Street / Financial District Arterial",
        "hi": "दलाल स्ट्रीट",
        "ta": "தலால் தெரு",
        "category": "civic",
        "description": "Narrow historic financial canyon in South Mumbai bustling with stock traders."
    },
    {
        "gloss": "SEBI_REGULATOR",
        "en": "SEBI / Securities and Exchange Board of India",
        "hi": "भारतीय प्रतिभूति और विनिमय बोर्ड (सेबी)",
        "ta": "செபி ஒழுங்குமுறை ஆணையம்",
        "category": "civic",
        "description": "Fingerspell S-E-B-I, regulatory eagle eye monitoring fair market trading."
    },
    {
        "gloss": "SHARE_BAZAAR",
        "en": "Share Bazaar / Equities Market",
        "hi": "शेयर बाज़ार / शेयर बाज़ार",
        "ta": "பங்குச் சந்தை",
        "category": "civic",
        "description": "Two hands open and close rapidly trading buy and sell equity orders."
    },
    {
        "gloss": "STOCK_BROKER",
        "en": "Stock Broker / Financial Intermediary",
        "hi": "शेयर दलाल / स्टॉक ब्रोकर",
        "ta": "பங்குத் தரகர்",
        "category": "civic",
        "description": "Phone at ear while executing simultaneous stock buy trades on terminal."
    },
    {
        "gloss": "BULL_MARKET",
        "en": "Bull Market / Teji / Soaring Indices",
        "hi": "तेजी / बुल मार्केट",
        "ta": "காளை சந்தை",
        "category": "civic",
        "description": "Two curved horns thrust upward aggressively, stock market chart surging high."
    },
    {
        "gloss": "BEAR_MARKET",
        "en": "Bear Market / Mandi / Market Correction",
        "hi": "मंदी / बेयर मार्केट",
        "ta": "கரடி சந்தை",
        "category": "civic",
        "description": "Heavy bear paws swiping down, index red candlesticks tumbling."
    },
    {
        "gloss": "IPO_LISTING",
        "en": "Initial Public Offering / IPO Ringing the Bell",
        "hi": "आईपीओ लिस्टिंग / शेयर आबंटन",
        "ta": "ஐ.பி.ஓ பொதுப் பங்கு",
        "category": "civic",
        "description": "Ring ceremonial brass listing bell on exchange podium celebrating public listing."
    },
    {
        "gloss": "MUTUAL_FUND",
        "en": "Mutual Fund / Systematic Investment Plan (SIP)",
        "hi": "म्यूचुअल फंड / एसआईपी",
        "ta": "மியூச்சுவல் ஃபண்ட்",
        "category": "civic",
        "description": "Gathering small monthly savings from many into a diversified basket of wealth."
    },
    {
        "gloss": "COMMODITY_EXCHANGE",
        "en": "Multi Commodity Exchange / MCX Gold & Oil",
        "hi": "कमोडिटी एक्सचेंज / वायदा बाज़ार",
        "ta": "பொருட்கள் வர்த்தக சந்தை",
        "category": "civic",
        "description": "Future delivery contract signing for cotton, crude oil, and precious bullion."
    },
    {
        "gloss": "FOREX_RESERVE",
        "en": "Foreign Exchange Reserves / RBI Vaults",
        "hi": "विदेशी मुद्रा भंडार",
        "ta": "அந்நிய செலாவணி இருப்பு",
        "category": "civic",
        "description": "Stack international currency reserves inside impenetrable central bank vault."
    },
    {
        "gloss": "CORPORATE_HQ",
        "en": "Corporate Headquarters / Conglomerate Office",
        "hi": "कॉर्पोरेट मुख्यालय",
        "ta": "நிறுவன தலைமை அலுவலகம்",
        "category": "civic",
        "description": "Gleaming multi-story glass skyscraper housing board of directors."
    },
    {
        "gloss": "BKC_BUSINESS_DISTRICT",
        "en": "Bandra Kurla Complex / BKC Financial Hub",
        "hi": "बांद्रा कुर्ला कॉम्प्लेक्स (बीकेसी)",
        "ta": "பி.கே.சி வர்த்தக மையம்",
        "category": "civic",
        "description": "Ultra-modern financial district with wide boulevards and global banking hubs."
    },
    {
        "gloss": "SURAT_DIAMOND_BOURSE",
        "en": "Surat Diamond Bourse / World's Largest Office Complex",
        "hi": "सूरत डायमंड बोर्स",
        "ta": "சூரத் வைர வர்த்தக மையம்",
        "category": "civic",
        "description": "Nine interconnected towers housing world's largest diamond trading floor."
    },
    {
        "gloss": "DIAMOND_CUTTING",
        "en": "Diamond Cutting & Precision Polishing",
        "hi": "हीरा तराशना एवं पॉलिशिंग",
        "ta": "வைரம் தீட்டுதல்",
        "category": "civic",
        "description": "High speed rotating scaife wheel grinding rough carbon crystal into brilliant 57 facets."
    },
    {
        "gloss": "GOLD_BULLION",
        "en": "Gold Bullion / Zaveri Bazaar Trade",
        "hi": "सोने की ईंट / बुलियन",
        "ta": "தங்கக் கட்டி",
        "category": "civic",
        "description": "Heavy yellow rectangular gold bar weighed precisely on micro-scale."
    },
    {
        "gloss": "COMMERCIAL_BANKING",
        "en": "Commercial Corporate Banking",
        "hi": "वाणिज्यिक बैंकिंग",
        "ta": "வணிக வங்கிச் சேவை",
        "category": "civic",
        "description": "Multi-tier corporate loan syndication and credit line stamping."
    },
    {
        "gloss": "BANK_LOAN",
        "en": "Bank Loan / Business Credit Facility",
        "hi": "बैंक ऋण / व्यापार कर्ज",
        "ta": "வங்கி கடன்",
        "category": "civic",
        "description": "Approve sanction letter and disburse capital into borrower account."
    },
    {
        "gloss": "VENTURE_CAPITAL",
        "en": "Venture Capital & Private Equity Fund",
        "hi": "उद्यम पूंजी / वेंचर कैपिटल",
        "ta": "வென்ச்சர் மூலதனம்",
        "category": "civic",
        "description": "Inject growth equity investment into high-potential enterprise founders."
    },
    {
        "gloss": "JNPT_PORT",
        "en": "JNPT Nhava Sheva / India's Premier Container Port",
        "hi": "जेएनपीटी न्हावा शेवा बंदरगाह",
        "ta": "ஜே.என்.பி.டி கொள்கலன் துறைமுகம்",
        "category": "navigation",
        "description": "Fingerspell J-N-P-T, giant quay crane lifting shipping containers onto rail freights."
    },
    {
        "gloss": "KANDLA_PORT",
        "en": "Deendayal Port Kandla / Major Western Gateway",
        "hi": "कांडला बंदरगाह (दीनदयाल पोर्ट)",
        "ta": "காண்ட்லா துறைமுகம்",
        "category": "navigation",
        "description": "Liquid bulk petroleum and dry cargo ocean vessels discharging at tidal jetties."
    },
    {
        "gloss": "CONTAINER_TERMINAL",
        "en": "Intermodal Container Terminal / Freight Station",
        "hi": "कंटेनर टर्मिनल / माल ढुलाई केंद्र",
        "ta": "கொள்கலன் முனையம்",
        "category": "navigation",
        "description": "Stack rows of multi-colored 40-foot shipping containers four levels high."
    },
    {
        "gloss": "CARGO_SHIP",
        "en": "Ocean Cargo Ship / Container Vessel",
        "hi": "मालवाहक जहाज / कार्गो पोत",
        "ta": "சரக்கு கப்பல்",
        "category": "navigation",
        "description": "Mammoth ocean freighter cutting through sea loaded with thousands of TEUs."
    },
    {
        "gloss": "CUSTOMS_CLEARING",
        "en": "Customs Port Clearance / Bill of Entry",
        "hi": "सीमा शुल्क निकासी / कस्टम क्लीयरेंस",
        "ta": "சுங்க அனுமதி",
        "category": "civic",
        "description": "Inspect import manifest, verify cargo seal, stamp official customs clearance."
    },
    {
        "gloss": "MARITIME_DOCKYARD",
        "en": "Naval & Commercial Maritime Dockyard",
        "hi": "नौसैनिक एवं वाणिज्यिक गोदी",
        "ta": "கப்பல் பழுதுபார்க்கும் தளம்",
        "category": "civic",
        "description": "Drain water from graving dock, scrape barnacles and paint ship hull."
    },
    {
        "gloss": "SHIPBREAKING_ALANG",
        "en": "Alang Ship Breaking Yard / Gujarat Coast",
        "hi": "अलंग जहाज पुनर्चक्रण यार्ड",
        "ta": "அலாங் கப்பல் உடைக்கும் தளம்",
        "category": "civic",
        "description": "Beach ocean liner on high tide mud, cut giant steel plates with gas torch."
    },
    {
        "gloss": "OFFSHORE_OIL_RIG",
        "en": "Offshore Oil Drilling Rig Platform",
        "hi": "अपतटीय तेल निष्कर्षण मंच",
        "ta": "கடல் எண்ணெய் துளையிடும் தளம்",
        "category": "civic",
        "description": "Four-legged steel oil platform standing in deep sea with burning gas flare."
    },
    {
        "gloss": "MUMBAI_HIGH",
        "en": "Mumbai High Offshore Field / ONGC",
        "hi": "मुंबई हाई तेल क्षेत्र",
        "ta": "மும்பை ஹை எண்ணெய் தளம்",
        "category": "civic",
        "description": "Drill miles beneath ocean seabed extracting crude petroleum."
    },
    {
        "gloss": "JAMNAGAR_REFINERY",
        "en": "Jamnagar Mega Petroleum Refinery / World's Largest",
        "hi": "जामनगर रिफाइनरी",
        "ta": "ஜாம்நகர் பெட்ரோலிய சுத்திகரிப்பு ஆலை",
        "category": "civic",
        "description": "Forest of distillation fractionating columns refining crude into fuels."
    },
    {
        "gloss": "PETROCHEMICAL_PLANT",
        "en": "Petrochemical Cracker & Polymer Complex",
        "hi": "पेट्रोकेमिकल संयंत्र",
        "ta": "பெட்ரோலிய ரசாயன ஆலை",
        "category": "civic",
        "description": "Crack naphtha into polymer granules for synthetic manufacturing."
    },
    {
        "gloss": "COTTON_TEXTILE_MILL",
        "en": "Cotton Textile Mill / Girangaon Heritage",
        "hi": "सूती कपड़ा मिल",
        "ta": "பருத்தி ஆடை ஆலை",
        "category": "civic",
        "description": "Carding raw white cotton bales into uniform spun yarn bobbins."
    },
    {
        "gloss": "POWER_LOOM",
        "en": "Power Loom Weaving Shed / Bhiwandi",
        "hi": "पावरलूम / विद्युत करघा",
        "ta": "விசைத்தறி",
        "category": "civic",
        "description": "Rapid clacking shuttle flying automatically weaving miles of gray cloth."
    },
    {
        "gloss": "AUTOMOBILE_CHAKAN",
        "en": "Automobile Manufacturing Belt / Pune Chakan",
        "hi": "चाकण ऑटोमोबाइल बेल्ट",
        "ta": "வாகன உற்பத்தி மண்டலம்",
        "category": "civic",
        "description": "Automated spot-welding robots joining stamped car body shells."
    },
    {
        "gloss": "PHARMA_GUJARAT",
        "en": "Gujarat Pharmaceutical Formulations Corridor",
        "hi": "गुजरात फार्मास्युटिकल उद्योग",
        "ta": "குஜராத் மருந்து உற்பத்தி",
        "category": "civic",
        "description": "Cleanroom blister packaging of certified generic tablets and capsules."
    },
    {
        "gloss": "CHEMICAL_CORRIDOR",
        "en": "Chemical & Specialty Intermediates / Dahej & Ankleshwar",
        "hi": "रासायनिक गलियारा / दहेज-अंकलेश्वर",
        "ta": "ரசாயன தொழில் மண்டலம்",
        "category": "civic",
        "description": "Network of chemical pipelines and specialized reaction vessels."
    },
    {
        "gloss": "SALT_PAN",
        "en": "Coastal Salt Pans / Mithagar",
        "hi": "नमक के खेत / मीठागर",
        "ta": "உப்பளம்",
        "category": "daily",
        "description": "Rake evaporating seawater into shining pyramids of pure white sea salt."
    },
    {
        "gloss": "LOCAL_TRAIN",
        "en": "Mumbai Local Train / Suburban Railway Lifeline",
        "hi": "मुंबई लोकल ट्रेन / उपनगरीय रेल",
        "ta": "மும்பை புறநகர் ரயில்",
        "category": "navigation",
        "description": "Fast electric commuter train roaring through stations packed with commuters."
    },
    {
        "gloss": "WESTERN_RAILWAY_LINE",
        "en": "Western Railway Suburban Line / Churchgate to Virar",
        "hi": "पश्चिम रेलवे उपनगरीय मार्ग",
        "ta": "மேற்கு ரயில்வே பாதை",
        "category": "navigation",
        "description": "Suburban tracks hugging western coast from Churchgate northwards."
    },
    {
        "gloss": "CENTRAL_RAILWAY_LINE",
        "en": "Central Railway Suburban Line / CSMT to Kalyan",
        "hi": "मध्य रेलवे उपनगरीय मार्ग",
        "ta": "மத்திய ரயில்வே பாதை",
        "category": "navigation",
        "description": "Four-track trunk line heading inland through Ghats to Kalyan."
    },
    {
        "gloss": "HARBOR_RAILWAY_LINE",
        "en": "Harbour Railway Line / CSMT to Panvel",
        "hi": "हार्बर रेलवे लाइन",
        "ta": "ஹார்பர் ரயில் பாதை",
        "category": "navigation",
        "description": "Curving coastal line crossing creek bridges into Navi Mumbai."
    },
    {
        "gloss": "FAST_LOCAL",
        "en": "Fast Local Train / Express Commuter Service",
        "hi": "फास्ट लोकल ट्रेन",
        "ta": "விரைவு மின்சார ரயில்",
        "category": "navigation",
        "description": "Train speeding past smaller suburban platforms without stopping."
    },
    {
        "gloss": "SLOW_LOCAL",
        "en": "Slow Local Train / All-Stations Commuter",
        "hi": "स्लो लोकल ट्रेन",
        "ta": "சாதாரண புறநகர் ரயில்",
        "category": "navigation",
        "description": "Commuter train pausing at every single intermediate neighborhood station."
    },
    {
        "gloss": "CHURCHGATE_TERMINUS",
        "en": "Churchgate Terminus / South Mumbai Western Hub",
        "hi": "चर्चगेट स्टेशन",
        "ta": "சர்ச்கேட் முனையம்",
        "category": "navigation",
        "description": "Terminal buffer stops with surging sea of commuters heading into Fort business district."
    },
    {
        "gloss": "CSMT_TERMINUS",
        "en": "Chhatrapati Shivaji Maharaj Terminus (CSMT) / Victoria Terminus",
        "hi": "सीएसएमटी स्टेशन / विक्टोरिया टर्मिनस",
        "ta": "சி.எஸ்.எம்.டி ரயில் நிலையம்",
        "category": "navigation",
        "description": "Victorian Gothic stone carvings, majestic central stained-glass dome and gargoyles."
    },
    {
        "gloss": "DABBAWALA_NETWORK",
        "en": "Mumbai Dabbawala / Six Sigma Tiffin Delivery",
        "hi": "मुंबई डब्बावाला / टिफिन डिलीवरी",
        "ta": "மும்பை டப்பாவாலா",
        "category": "civic",
        "description": "Balance long wooden tray of stainless steel tiffin boxes on head, sorting by color codes."
    },
    {
        "gloss": "DOUBLE_DECKER_BUS",
        "en": "BEST Red Double Decker Bus",
        "hi": "बेस्ट लाल डबल डेकर बस",
        "ta": "இரட்டை அடுக்கு பேருந்து",
        "category": "navigation",
        "description": "Iconic red bus with narrow winding stairs leading to upper front window seat."
    },
    {
        "gloss": "BANDRA_WORLI_SEA_LINK",
        "en": "Bandra-Worli Sea Link / Cable-Stayed Bridge",
        "hi": "बांद्रा-वर्ली सी लिंक",
        "ta": "பாந்த்ரா-வொர்லி கடல் பாலம்",
        "category": "navigation",
        "description": "Dramatic soaring concrete pylons and fan of steel cables spanning Mahim Bay."
    },
    {
        "gloss": "COASTAL_ROADWAY",
        "en": "Mumbai Coastal Road Project / Undersea Tunnel",
        "hi": "मुंबई कोस्टल रोड / समुद्री सुरंग",
        "ta": "மும்பை கடற்கரை சாலை",
        "category": "navigation",
        "description": "Twin undersea road tunnels emerging onto reclaimed high-speed seaside promenade."
    },
    {
        "gloss": "FERRY_CATAMARAN",
        "en": "Ferry Catamaran / Gateway to Alibaug & Elephanta",
        "hi": "फेरी कैटामरन / मोटर बोट",
        "ta": "படகு போக்குவரத்து",
        "category": "navigation",
        "description": "Twin-hulled passenger boat cutting through harbor waves past seagulls."
    },
    {
        "gloss": "METRO_MUMBAI",
        "en": "Mumbai Metro Line / Aqua & Blue Lines",
        "hi": "मुंबई मेट्रो",
        "ta": "மும்பை மெட்ரோ",
        "category": "navigation",
        "description": "Air-conditioned metro train gliding silently along elevated concrete guide-ways."
    },
    {
        "gloss": "GANESH_CHATURTHI",
        "en": "Ganesh Chaturthi / 10-Day Grand Festival",
        "hi": "गणेश चतुर्थी / गणेशोत्सव",
        "ta": "விநாயகர் சதுர்த்தி",
        "category": "greeting",
        "description": "Elephant trunk curve gesture, Modak sweet held in left hand, blessing right palm."
    },
    {
        "gloss": "GANESH_VISARJAN",
        "en": "Ganesh Visarjan / Chowpatty Beach Immersion Procession",
        "hi": "गणेश विसर्जन / गिरगांव चौपाटी",
        "ta": "விநாயகர் சிலை கரைப்பு",
        "category": "greeting",
        "description": "Dancing to thunderous dhol tasha beats, wading into ocean immersing beloved deity."
    },
    {
        "gloss": "NAVRATRI_GARBA",
        "en": "Navratri Garba / Circular Folk Dance of Gujarat",
        "hi": "नवरात्रि गरबा नृत्य",
        "ta": "நவராத்திரி கர்பா நடனம்",
        "category": "greeting",
        "description": "Clap hands in rhythmic syncopated steps moving in swirling circular chorus."
    },
    {
        "gloss": "DANDIYA_RAAS",
        "en": "Dandiya Raas / Wooden Sticks Folk Dance",
        "hi": "डांडिया रास",
        "ta": "தாண்டியா நடனம்",
        "category": "greeting",
        "description": "Strike two decorated polished wooden sticks against partner's sticks in upbeat rhythm."
    },
    {
        "gloss": "GUDI_PADWA",
        "en": "Gudi Padwa / Marathi New Year",
        "hi": "गुढी पाडवा / मराठी नववर्ष",
        "ta": "குடி பட்வா",
        "category": "greeting",
        "description": "Hoist bright silk cloth on bamboo pole topped with silver kalash and neem leaves."
    },
    {
        "gloss": "PARSI_NAVROZ",
        "en": "Parsi Navroz / Persian Spring New Year",
        "hi": "पारसी नवरोज़",
        "ta": "பார்சி நவ்ரோஸ்",
        "category": "greeting",
        "description": "Sprinkle rose water from silver gulabpash, embrace with sweet falooda."
    },
    {
        "gloss": "GOA_CARNIVAL",
        "en": "Goa Carnival / King Momo Parade",
        "hi": "गोवा कार्निवल",
        "ta": "கோவா கார்னிவல்",
        "category": "greeting",
        "description": "Colorful floats, King Momo proclaiming feast, music and masked revelers."
    },
    {
        "gloss": "VADA_PAV",
        "en": "Vada Pav / Mumbai Street Food Burger",
        "hi": "वड़ा पाव",
        "ta": "வடா பாவ்",
        "category": "daily",
        "description": "Golden fried spiced potato ball stuffed inside soft bun with fiery red garlic chutney."
    },
    {
        "gloss": "PAV_BHAJI",
        "en": "Pav Bhaji / Spiced Vegetable Mash & Buttered Pav",
        "hi": "पाव भाजी",
        "ta": "பாவ் பாஜி",
        "category": "daily",
        "description": "Mash vegetables with round iron masher on giant sizzling tawa with slab of amul butter."
    },
    {
        "gloss": "MISAL_PAV",
        "en": "Misal Pav / Sprouted Bean Fiery Curry with Farsan",
        "hi": "मिसळ पाव",
        "ta": "மிசல் பாவ்",
        "category": "daily",
        "description": "Pour fiery red rassa tarri over sprouted moth beans, top with crunchy farsan and lemon."
    },
    {
        "gloss": "POHA",
        "en": "Kanda Poha / Flattened Rice with Peanuts & Mustard",
        "hi": "कांदा पोहा",
        "ta": "போஹா",
        "category": "daily",
        "description": "Temper yellow turmeric flattened rice with onions, green chilies and roasted peanuts."
    },
    {
        "gloss": "MODAK",
        "en": "Ukadiche Modak / Steamed Rice Dumpling with Jaggery Coconut",
        "hi": "उकडीचे मोदक",
        "ta": "மோதகம்",
        "category": "daily",
        "description": "Pinch delicate fluted pleats into rice dough pouch, steam sweet jaggery-coconut filling."
    },
    {
        "gloss": "PURAN_POLI",
        "en": "Puran Poli / Sweet Stuffed Lentil Flatbread",
        "hi": "पूरन पोळी",
        "ta": "பூரன் போளி",
        "category": "daily",
        "description": "Stuff sweet nutmeg chana dal stuffing into soft dough, roll thin and roast with ghee."
    },
    {
        "gloss": "DHOKLA",
        "en": "Dhokla / Steamed Fermented Gram Flour Cake",
        "hi": "खमन ढोकला",
        "ta": "டோக்ளா",
        "category": "daily",
        "description": "Spongy bright yellow square cake tempered with mustard seeds and fresh green chilies."
    },
    {
        "gloss": "KHAMAN",
        "en": "Khaman / Soft Juicy Besan Snack",
        "hi": "खमण",
        "ta": "கமன்",
        "category": "daily",
        "description": "Ultra-fluffy steamed snack soaked in sweet tangy temper water."
    },
    {
        "gloss": "THEPLA",
        "en": "Methi Thepla / Fenugreek Spiced Flatbread",
        "hi": "मेथी थेपला",
        "ta": "தேப்லா",
        "category": "daily",
        "description": "Knead fresh bitter methi leaves into spiced whole wheat dough, roll thin travel breads."
    },
    {
        "gloss": "KHANDVI",
        "en": "Khandvi / Rolled Gram Flour & Yogurt Rolls",
        "hi": "खांडवी",
        "ta": "காண்ட்வி",
        "category": "daily",
        "description": "Spread cooked batter paper-thin on kitchen counter, roll into delicate yellow cylinders."
    },
    {
        "gloss": "FARSAN",
        "en": "Gujarati & Marathi Farsan / Savory Crispy Snacks",
        "hi": "फरसाण / नमकीन",
        "ta": "பர்சான்",
        "category": "daily",
        "description": "Crisp spiced sev, gathiya, and fried chickpea snacks served with chai."
    },
    {
        "gloss": "JALEBI_FAFDA",
        "en": "Fafda Jalebi / Sunday Morning Breakfast Combo",
        "hi": "फाफड़ा जलेबी",
        "ta": "பாப்டா ஜிலேபி",
        "category": "daily",
        "description": "Press long gram flour fafda with heel of palm, fry crisp, eat with sweet saffron jalebis."
    },
    {
        "gloss": "SHRIKHAND",
        "en": "Shrikhand / Strained Cardamom Saffron Yogurt Sweet",
        "hi": "श्रीखंड",
        "ta": "ஸ்ரீகண்ட்",
        "category": "daily",
        "description": "Hang yogurt in muslin cloth (chakka), whisk with sugar, saffron and crushed pistachios."
    },
    {
        "gloss": "ALPHONSO_MANGO",
        "en": "Alphonso Mango / Devgad & Ratnagiri Hapus",
        "hi": "हापुस आम / अल्फांसो आम",
        "ta": "அல்போன்சா மாம்பழம்",
        "category": "daily",
        "description": "Slice king of fruits revealing deep golden saffron pulp, inhale heavenly sweet scent."
    },
    {
        "gloss": "SOL_KADHI",
        "en": "Sol Kadhi / Kokum & Coconut Milk Digestive Drink",
        "hi": "सोल कढ़ी",
        "ta": "சோல் கடி",
        "category": "daily",
        "description": "Pink refreshing drink of tart kokum fruit extract blended with freshly squeezed coconut milk."
    },
    {
        "gloss": "GOAN_FISH_CURRY",
        "en": "Goan Fish Curry / Kokum & Coconut Masala",
        "hi": "गोवा फिश करी",
        "ta": "கோவா மீன் குழம்பு",
        "category": "daily",
        "description": "Simmer fresh kingfish in ground red chili coconut gravy with tangy kokum."
    },
    {
        "gloss": "CHIVDA",
        "en": "Poha Chivda / Spiced Roasted Rice Flake Mix",
        "hi": "पोहा चिवड़ा",
        "ta": "சிவ்டா",
        "category": "daily",
        "description": "Crispy roasted rice flakes tossed with turmeric, peanuts, dry coconut slices and curry leaves."
    },
    {
        "gloss": "BOMBAY_INSTITUTE_DEAF",
        "en": "Bombay Institute for Deaf and Mutes (est. 1885)",
        "hi": "बॉम्बे डेफ एंड म्यूट इंस्टीट्यूट",
        "ta": "மும்பை காதுகேளாதோர் நிறுவனம்",
        "category": "academic",
        "description": "Historic pioneering deaf school gesture, acknowledging earliest sign standardization archives."
    },
    {
        "gloss": "DEAF_MUTE_SOCIETY",
        "en": "Ahmedabad Deaf Mute Society (est. 1908)",
        "hi": "अहमदाबाद डेफ म्यूट सोसाइटी",
        "ta": "அகமதாபாத் காதுகேளாதோர் சங்கம்",
        "category": "academic",
        "description": "Historic deaf welfare society banner and vocational printing press workshop sign."
    },
    {
        "gloss": "WARLI_PAINTING",
        "en": "Warli Tribal Folk Art / White Pigment on Mud",
        "hi": "वारली चित्रकला",
        "ta": "வார்லி ஓவியம்",
        "category": "greeting",
        "description": "Paint stick figures and dancing circles with rice flour paste on mud background."
    },
    {
        "gloss": "PAITHANI_SAREE",
        "en": "Paithani Silk Saree / Peacock Zari Pallu",
        "hi": "पैठणी रेशमी साड़ी",
        "ta": "பைத்தானி பட்டு சேலை",
        "category": "daily",
        "description": "Intricate hand-woven tapestry pallu featuring oblique square border and iridescent peacock."
    },
    {
        "gloss": "BANDHANI_TIE_DYE",
        "en": "Bandhani / Bandhej Tie & Dye of Kutch & Jamnagar",
        "hi": "बांधनी / बंधेज वस्त्र",
        "ta": "பாந்தினி சேலை",
        "category": "daily",
        "description": "Pinch tiny dots of cloth with fingernails, bind with thread, dip in vibrant dyes."
    },
    {
        "gloss": "PATOLA_SILK",
        "en": "Patan Patola / Double Ikat Masterpiece",
        "hi": "पाटन का पटोला",
        "ta": "படோலா பட்டு",
        "category": "daily",
        "description": "Both warp and weft silk threads precision resist-dyed before weaving matching pattern."
    },
    {
        "gloss": "KOLHAPURI_CHAPPAL",
        "en": "Kolhapuri Chappals / Handcrafted Leather Footwear",
        "hi": "कोल्हापुरी चप्पल",
        "ta": "கோலாப்பூரி காலணி",
        "category": "daily",
        "description": "Braided vegetable-tanned buffalo leather slippers with decorative pompom."
    }
]
