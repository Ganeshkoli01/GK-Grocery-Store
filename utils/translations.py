"""
GK GROCERY STORE – Multilingual Internationalization (i18n) Module
Supports English, Marathi (मराठी), and Hindi (हिंदी).
"""

import streamlit as st

LANGUAGES = {
    "en": "English",
    "mr": "मराठी (Marathi)",
    "hi": "हिंदी (Hindi)"
}

# Product Names Translation Catalog
PRODUCT_TRANSLATIONS = {
    "Saffola Gold Pro Healthy Oil 5L": {
        "en": "Saffola Gold Pro Healthy Oil 5L",
        "mr": "सफोला गोल्ड प्रो हेल्दी खाद्यतेल ५ लिटर",
        "hi": "सफोला गोल्ड प्रो हेल्दी कुकिंग ऑयल 5L"
    },
    "Cashews Whole W320 500g": {
        "en": "Cashews Whole W320 500g",
        "mr": "काजू पूर्ण W320 ५०० ग्रॅम",
        "hi": "काजू साबुत W320 500g"
    },
    "Almonds California Premium 500g": {
        "en": "Almonds California Premium 500g",
        "mr": "कॅलिफोर्निया प्रीमियम बदाम ५०० ग्रॅम",
        "hi": "कैलिफोर्निया प्रीमियम बादाम 500g"
    },
    "Hybrid Juicy Tomatoes": {
        "en": "Hybrid Juicy Tomatoes",
        "mr": "संकरित रसाळ टोमॅटो",
        "hi": "हाइब्रिड रसीले टमाटर"
    },
    "Jyoti Potatoes Fresh": {
        "en": "Jyoti Potatoes Fresh",
        "mr": "ज्योती ताजे बटाटे",
        "hi": "ज्योति ताजे आलू"
    },
    "Fresh Red Onions": {
        "en": "Fresh Red Onions",
        "mr": "ताजे लाल कांदे",
        "hi": "ताजे लाल प्याज"
    },
    "Head & Shoulders Shampoo 340ml": {
        "en": "Head & Shoulders Shampoo 340ml",
        "mr": "हेड अँड शोल्डर्स शॅम्पू ३४० मिली",
        "hi": "हेड एंड शोल्डर्स शैम्पू 340ml"
    },
    "Colgate Strong Teeth Toothpaste 300g": {
        "en": "Colgate Strong Teeth Toothpaste 300g",
        "mr": "कोलगेट स्ट्राँग टीथ टूथपेस्ट ३०० ग्रॅम",
        "hi": "कोलगेट स्ट्रॉन्ग टीथ टूथपेस्ट 300g"
    },
    "Dove Moisturizing Soap 3x100g": {
        "en": "Dove Moisturizing Soap 3x100g",
        "mr": "डव्ह मॉइश्चरायझिंग साबण ३ × १०० ग्रॅम",
        "hi": "डव मॉइस्चराइजिंग साबुन 3x100g"
    },
    "Colin Glass Cleaner 500ml": {
        "en": "Colin Glass Cleaner 500ml",
        "mr": "कॉलिन काच स्वच्छ करणारे लिक्विड ५०० मिली",
        "hi": "कॉलिन ग्लास क्लीनर 500ml"
    },
    "Dettol Antiseptic Liquid 550ml": {
        "en": "Dettol Antiseptic Liquid 550ml",
        "mr": "डेटॉल अँटिसेप्टिक लिक्विड ५५० मिली",
        "hi": "डेटॉल एंटीसेप्टिक लिक्विड 550ml"
    },
    "Vim Dishwash Gel 750ml": {
        "en": "Vim Dishwash Gel 750ml",
        "mr": "विम भांडी धुण्याचे जेल ७५० मिली",
        "hi": "विम डिशवॉश जेल 750ml"
    },
    "Surf Excel Matic Front Load 2kg": {
        "en": "Surf Excel Matic Front Load 2kg",
        "mr": "सर्फ एक्सेल मॅटिक फ्रंट लोड कपडे धुण्याची पावडर २ किलो",
        "hi": "सर्फ एक्सेल मैटिक फ्रंट लोड वाशिंग पाउडर 2kg"
    },
    "Catch Jeera (Cumin Seeds) 200g": {
        "en": "Catch Jeera (Cumin Seeds) 200g",
        "mr": "कॅच जिरे २०० ग्रॅम",
        "hi": "कैच जीरा 200g"
    },
    "Everest Garam Masala 100g": {
        "en": "Everest Garam Masala 100g",
        "mr": "एव्हरेस्ट गरम मसाला १०० ग्रॅम",
        "hi": "एवरेस्ट गरम मसाला 100g"
    },
    "Everest Red Chilli Powder 200g": {
        "en": "Everest Red Chilli Powder 200g",
        "mr": "एव्हरेस्ट लाल तिखट २०० ग्रॅम",
        "hi": "एवरेस्ट लाल मिर्च पाउडर 200g"
    },
    "Everest Turmeric Powder 200g": {
        "en": "Everest Turmeric Powder 200g",
        "mr": "एव्हरेस्ट हळद पावडर २०० ग्रॅम",
        "hi": "एवरेस्ट हल्दी पाउडर 200g"
    },
    "Frooti Mango Drink 1.2L": {
        "en": "Frooti Mango Drink 1.2L",
        "mr": "फ्रूटी आंब्याचे पेय १.२ लिटर",
        "hi": "फ्रूटी मैंगो ड्रिंक 1.2L"
    },
    "Bournvita Nutrition Drink 500g": {
        "en": "Bournvita Nutrition Drink 500g",
        "mr": "बॉर्नव्हिटा पौष्टिक पेय पावडर ५०० ग्रॅम",
        "hi": "बॉर्नविटा पोषण पेय पाउडर 500g"
    },
    "Bru Instant Coffee 200g": {
        "en": "Bru Instant Coffee 200g",
        "mr": "ब्रू इन्स्टंट कॉफी २०० ग्रॅम",
        "hi": "ब्रू इंस्टेंट कॉफी 200g"
    },
    "Tata Tea Gold 500g": {
        "en": "Tata Tea Gold 500g",
        "mr": "टाटा टी गोल्ड चहा ५०० ग्रॅम",
        "hi": "टाटा टी गोल्ड चाय 500g"
    },
    "Maggi 2-Minute Noodles 4-Pack": {
        "en": "Maggi 2-Minute Noodles 4-Pack",
        "mr": "मॅगी २ मिनिट नूडल्स ४ पॅकेट",
        "hi": "मैगी 2-मिनट नूडल्स 4-पैक"
    },
    "Lay's Classic Salted Chips": {
        "en": "Lay's Classic Salted Chips",
        "mr": "लेज क्लासिक सॉल्टेड बटाटा चिप्स",
        "hi": "लेज़ क्लासिक सॉल्टेड चिप्स"
    },
    "Parle-G Gold Biscuits 1kg": {
        "en": "Parle-G Gold Biscuits 1kg",
        "mr": "पार्ले-जी गोल्ड बिस्किटे १ किलो",
        "hi": "पारले-जी गोल्ड बिस्कुट 1kg"
    },
    "Haldiram's Bhujia Sev 400g": {
        "en": "Haldiram's Bhujia Sev 400g",
        "mr": "हल्दीराम भुजिया शेव ४०० ग्रॅम",
        "hi": "हल्दीराम भुजिया सेव 400g"
    },
    "Amul Masti Dahi Cup": {
        "en": "Amul Masti Dahi Cup",
        "mr": "अमूल मस्ती दही कप",
        "hi": "अमूल मस्ती दही कप"
    },
    "Fresh Malai Paneer": {
        "en": "Fresh Malai Paneer",
        "mr": "ताजे मलाई पनीर",
        "hi": "ताजा मलाई पनीर"
    },
    "Amul Salted Butter 500g": {
        "en": "Amul Salted Butter 500g",
        "mr": "अमूल खारट लोणी ५०० ग्रॅम",
        "hi": "अमूल मक्खन 500g"
    },
    "Amul Taaza Toned Milk": {
        "en": "Amul Taaza Toned Milk",
        "mr": "अमूल ताजा टोन्ड दूध",
        "hi": "अमूल ताजा टोंड दूध"
    },
    "Mustard Oil Kachi Ghani": {
        "en": "Mustard Oil Kachi Ghani",
        "mr": "कच्ची घाणीचे मोहरीचे तेल",
        "hi": "कच्ची घानी सरसों का तेल"
    },
    "Amul Pure Cow Ghee Tin": {
        "en": "Amul Pure Cow Ghee Tin",
        "mr": "अमूल शुद्ध गाईचे तूप (डबा)",
        "hi": "अमूल शुद्ध गाय का घी टिन"
    },
    "Gemini Groundnut Oil": {
        "en": "Gemini Groundnut Oil",
        "mr": "जेमिनी शेंगदाणा तेल",
        "hi": "जेमिनी मूंगफली का तेल"
    },
    "Fortune Sunflower Oil Pouch": {
        "en": "Fortune Sunflower Oil Pouch",
        "mr": "फॉर्च्यून सूर्यफूल तेल पाऊच",
        "hi": "फॉर्च्यून सूरजमुखी तेल पाउच"
    },
    "Kabuli Chana (Chickpeas)": {
        "en": "Kabuli Chana (Chickpeas)",
        "mr": "काबुली चणे",
        "hi": "काबुली चना"
    },
    "Urad Dal Black Split": {
        "en": "Urad Dal Black Split",
        "mr": "काळी उडीद डाळ (फोडलेली)",
        "hi": "उड़द दाल काली"
    },
    "Chana Dal Premium": {
        "en": "Chana Dal Premium",
        "mr": "प्रीमियम हरभरा डाळ",
        "hi": "चना दाल प्रीमियम"
    },
    "Moong Dal Washed": {
        "en": "Moong Dal Washed",
        "mr": "धुतलेली मूग डाळ",
        "hi": "मूंग दाल धुली"
    },
    "Toor Dal (Arhar Dal)": {
        "en": "Toor Dal (Arhar Dal)",
        "mr": "तूर डाळ",
        "hi": "तूर दाल (अरहर दाल)"
    },
    "Roasted Sooji (Rava)": {
        "en": "Roasted Sooji (Rava)",
        "mr": "भाजलेला रवा",
        "hi": "भुनी हुई सूजी (रवा)"
    },
    "Organic Poha (Flattened Rice)": {
        "en": "Organic Poha (Flattened Rice)",
        "mr": "सेंद्रिय पोहे",
        "hi": "जैविक पोहा"
    },
    "Aashirvaad Sharbati Atta (Wheat Flour)": {
        "en": "Aashirvaad Sharbati Atta (Wheat Flour)",
        "mr": "आशीर्वाद शरबती गव्हाचे पीठ",
        "hi": "आशीर्वाद शरबती गेहूं का आटा"
    },
    "Kolam Rice Premium": {
        "en": "Kolam Rice Premium",
        "mr": "प्रीमियम कोलम तांदूळ",
        "hi": "प्रीमियम कोलम चावल"
    },
    "India Gate Basmati Rice": {
        "en": "India Gate Basmati Rice",
        "mr": "इंडिया गेट बासमती तांदूळ",
        "hi": "इंडिया गेट बासमती चावल"
    }
}

# Category Translations
CATEGORY_TRANSLATIONS = {
    "Rice and Grains": {"en": "Rice and Grains", "mr": "तांदूळ आणि धान्य", "hi": "चावल और अनाज"},
    "Pulses": {"en": "Pulses", "mr": "डाळी आणि कडधान्ये", "hi": "दालें और फलियां"},
    "Dairy Products": {"en": "Dairy Products", "mr": "दुग्धजन्य पदार्थ", "hi": "डेयरी उत्पाद"},
    "Cooking Oil": {"en": "Cooking Oil", "mr": "खाद्यतेल आणि तूप", "hi": "कुकिंग ऑयल और घी"},
    "Snacks": {"en": "Snacks", "mr": "नाश्ता आणि फराळ", "hi": "स्नैक्स और नमकीन"},
    "Beverages": {"en": "Beverages", "mr": "पेये (चहा, कॉफी, सरबत)", "hi": "पेय पदार्थ (चाय, कॉफी)"},
    "Spices": {"en": "Spices", "mr": "मसाले आणि जिन्नस", "hi": "मसाले"},
    "Household Items": {"en": "Household Items", "mr": "घरगुती आणि स्वच्छता वस्तू", "hi": "घरेलू उत्पाद"},
    "Personal Care": {"en": "Personal Care", "mr": "वैयक्तिक काळजी आणि सौंदर्य", "hi": "पर्सनल केयर"},
    "Vegetables": {"en": "Vegetables", "mr": "भाज्या", "hi": "सब्जियां"},
    "Dry Fruits & Nuts": {"en": "Dry Fruits & Nuts", "mr": "सुका मेवा आणि नट्स", "hi": "ड्राई फ्रूट्स और मेवे"},
    "Bakery & Bread": {"en": "Bakery & Bread", "mr": "बेकरी आणि ब्रेड", "hi": "बेकरी और ब्रेड"}
}

# General UI Translations Dictionary
TRANSLATIONS = {
    # App Branding
    "app_title": {
        "en": "GK GROCERY STORE",
        "mr": "जीके किराणा स्टोअर",
        "hi": "जीके किराना स्टोर"
    },
    "app_subtitle": {
        "en": "Smart Grocery Management & Business Analytics",
        "mr": "स्मार्ट किराणा व्यवस्थापन आणि व्यवसाय विश्लेषण प्रणाली",
        "hi": "स्मार्ट किराना प्रबंधन और व्यवसाय विश्लेषिकी प्रणाली"
    },
    "app_tagline": {
        "en": "Smart Shopping. Smarter Business Decisions.",
        "mr": "स्मार्ट खरेदी. अधिक स्मार्ट व्यावसायिक निर्णय.",
        "hi": "स्मार्ट खरीदारी। स्मार्ट व्यावसायिक निर्णय।"
    },

    # Roles
    "role_owner": {"en": "OWNER (ADMIN)", "mr": "दुकानदार / मालक", "hi": "दुकानदार / मालिक"},
    "role_customer": {"en": "CUSTOMER", "mr": "ग्राहक", "hi": "ग्राहक"},
    "sign_out": {"en": "🚪 Sign Out", "mr": "🚪 बाहेर पडा (लॉगआउट)", "hi": "🚪 लॉग आउट"},

    # Owner Navigation Menu
    "nav_menu_title": {"en": "Navigation Menu", "mr": "मुख्य मेनू", "hi": "नेविगेशन मेनू"},
    "nav_dashboard": {"en": "📊 Executive Dashboard", "mr": "📊 व्यवसाय डॅशबोर्ड", "hi": "📊 मुख्य डैशबोर्ड"},
    "nav_pos": {"en": "💳 POS Counter Billing", "mr": "💳 बिलिंग काउंटर (POS)", "hi": "💳 पीओएस काउंटर बिलिंग"},
    "nav_products": {"en": "🏷️ Product Management", "mr": "🏷️ वस्तू / उत्पादन व्यवस्थापन", "hi": "🏷️ उत्पाद प्रबंधन"},
    "nav_inventory": {"en": "📦 Inventory Management", "mr": "📦 साठा / इन्व्हेंटरी व्यवस्थापन", "hi": "📦 इन्वेंटरी व स्टॉक प्रबंधन"},
    "nav_sales": {"en": "📈 Sales & Invoices", "mr": "📈 विक्री आणि बिले (पावत्या)", "hi": "📈 बिक्री और चालान"},
    "nav_pnl": {"en": "💰 Profit & Loss Analysis", "mr": "💰 नफा-तोटा विश्लेषण (P&L)", "hi": "💰 लाभ और हानि विश्लेषण"},
    "nav_expenses": {"en": "💸 Expense Management", "mr": "💸 दुकानाचे खर्च व्यवस्थापन", "hi": "💸 दुकान खर्च प्रबंधन"},
    "nav_performance": {"en": "⭐ Product Performance", "mr": "⭐ वस्तूंची विक्री कामगिरी", "hi": "⭐ उत्पाद प्रदर्शन"},
    "nav_reports": {"en": "📑 Business Reports & Exports", "mr": "📑 व्यवसाय अहवाल आणि एक्सेल", "hi": "📑 व्यापार रिपोर्ट और निर्यात"},
    "nav_powerbi": {"en": "📘 Power BI Integration Guide", "mr": "📘 पॉवर बीआय मार्गदर्शक", "hi": "📘 पावर बीआई गाइड"},

    # Customer Navigation
    "nav_customer_history": {"en": "📜 My Purchase History", "mr": "📜 माझी खरेदी आणि बिले", "hi": "📜 मेरा खरीद इतिहास"},
    "customer_menu_title": {"en": "Customer Menu", "mr": "ग्राहक मेनू", "hi": "ग्राहक मेनू"},

    # Common KPIs
    "kpi_total_revenue": {"en": "Total Sales Revenue", "mr": "एकूण विक्री उत्पन्न", "hi": "कुल बिक्री राजस्व"},
    "kpi_gross_profit": {"en": "Total Gross Profit", "mr": "एकूण ढोबळ नफा", "hi": "कुल सकल लाभ (Gross Profit)"},
    "kpi_net_profit": {"en": "Total Net Profit", "mr": "एकूण निव्वळ नफा", "hi": "कुल शुद्ध लाभ (Net Profit)"},
    "kpi_total_orders": {"en": "Total Customer Orders", "mr": "एकूण ग्राहक ऑर्डर्स", "hi": "कुल ग्राहक ऑर्डर्स"},
    "kpi_total_products": {"en": "Total Products (SKUs)", "mr": "एकूण उपलब्ध वस्तू (SKUs)", "hi": "कुल उत्पाद (SKUs)"},
    "kpi_low_stock": {"en": "Low Stock Alert", "mr": "कमी साठा इशारा", "hi": "कम स्टॉक अलर्ट"},
    "kpi_out_stock": {"en": "Out of Stock Alert", "mr": "साठा संपला इशारा", "hi": "आउट ऑफ स्टॉक अलर्ट"},
    "kpi_stock_valuation_cost": {"en": "Valuation (At Wholesale Cost)", "mr": "खरेदी मूल्यावर साठा किंमत", "hi": "थोक लागत पर स्टॉक मूल्यांकन"},
    "kpi_stock_valuation_retail": {"en": "Valuation (At Retail Selling)", "mr": "विक्री मूल्यावर साठा किंमत", "hi": "खुदरा मूल्य पर स्टॉक मूल्यांकन"},
    "kpi_expenses": {"en": "Operating Expenses", "mr": "दुकानाचे चालू खर्च", "hi": "परिचालन खर्च"},
    "kpi_cogs": {"en": "Cost of Goods Sold (COGS)", "mr": "विकलेल्या मालाची खरेदी किंमत", "hi": "बेचे गए माल की लागत (COGS)"},

    # Actions & Buttons
    "btn_add_item": {"en": "➕ Add Item to Bill", "mr": "➕ बिलात जोडा", "hi": "➕ बिल में जोड़ें"},
    "btn_complete_sale": {"en": "Complete Sale & Print Invoice", "mr": "विक्री पूर्ण करा आणि बिल छापा", "hi": "बिक्री पूर्ण करें और बिल प्रिंट करें"},
    "btn_download_pdf": {"en": "📥 Download Tax Invoice PDF", "mr": "📥 टॅक्स इनव्हॉइस PDF डाउनलोड करा", "hi": "📥 टैक्स इनवॉइस PDF डाउनलोड करें"},
    "btn_add_product": {"en": "Save New Product", "mr": "नवीन वस्तू सेव्ह करा", "hi": "नया उत्पाद सहेजें"},
    "btn_update_product": {"en": "Update Product", "mr": "वस्तू अपडेट करा", "hi": "उत्पाद अपडेट करें"},
    "btn_record_expense": {"en": "Record Expense", "mr": "खर्च नोंदवा", "hi": "खर्च दर्ज करें"},
    "btn_export_excel": {"en": "📊 Build & Prepare Excel Workbook", "mr": "📊 एक्सेल अहवाल तयार करा", "hi": "📊 एक्सेल वर्कबुक तैयार करें"},
    "btn_export_powerbi": {"en": "📦 Generate Power BI CSV Zip Bundle", "mr": "📦 पॉवर बीआय CSV पॅक तयार करा", "hi": "📦 पावर बीआई सीएसवी बंडल बनाएं"},

    # Form Fields
    "field_product_name": {"en": "Product Name", "mr": "वस्तूचे नाव", "hi": "उत्पाद का नाम"},
    "field_category": {"en": "Category", "mr": "प्रवर्ग / प्रकार", "hi": "श्रेणी"},
    "field_cost_price": {"en": "Cost Price (Wholesale) ₹", "mr": "खरेदी किंमत (घाऊक) ₹", "hi": "लागत मूल्य (थोक) ₹"},
    "field_selling_price": {"en": "Selling Price (Retail) ₹", "mr": "विक्री किंमत (किरकोळ) ₹", "hi": "बिक्री मूल्य (खुदरा) ₹"},
    "field_stock": {"en": "Available Stock", "mr": "उपलब्ध साठा", "hi": "उपलब्ध स्टॉक"},
    "field_min_stock": {"en": "Minimum Stock Alert", "mr": "किमान साठा इशारा पातळी", "hi": "न्यूनतम स्टॉक सीमा"},
    "field_unit": {"en": "Unit", "mr": "एकक", "hi": "इकाई"},
    "field_customer_name": {"en": "Customer Name", "mr": "ग्राहकाचे नाव", "hi": "ग्राहक का नाम"},
    "field_customer_phone": {"en": "Customer Mobile", "mr": "ग्राहकाचा मोबाईल", "hi": "ग्राहक का मोबाइल"},
    "field_payment_method": {"en": "Payment Mode", "mr": "पेमेंट पद्धत", "hi": "भुगतान माध्यम"},
    "field_discount": {"en": "Discount Amount ₹", "mr": "सूट (डिस्काउंट) ₹", "hi": "छूट (डिस्काउंट) ₹"},
    "field_subtotal": {"en": "Subtotal", "mr": "उप-एकूण", "hi": "उप-कुल"},
    "field_grand_total": {"en": "Grand Total", "mr": "एकूण रक्कम", "hi": "कुल योग"},

    # Statuses
    "status_in_stock": {"en": "In Stock", "mr": "साठा उपलब्ध", "hi": "स्टॉक उपलब्ध"},
    "status_low_stock": {"en": "Low Stock", "mr": "कमी साठा", "hi": "कम स्टॉक"},
    "status_out_of_stock": {"en": "Out of Stock", "mr": "साठा संपला", "hi": "आउट ऑफ स्टॉक"},
    "status_active": {"en": "Active", "mr": "सक्रिय", "hi": "सक्रिय"},
    "status_paid": {"en": "Paid", "mr": "भरले", "hi": "भुगतान किया"},

    # Timeframe filters
    "time_last_30_days": {"en": "Last 30 Days", "mr": "मागील ३० दिवस", "hi": "पिछले 30 दिन"},
    "time_today": {"en": "Today", "mr": "आज", "hi": "आज"},
    "time_yesterday": {"en": "Yesterday", "mr": "काल", "hi": "कल"},
    "time_last_7_days": {"en": "Last 7 Days", "mr": "मागील ७ दिवस", "hi": "पिछले 7 दिन"},
    "time_this_month": {"en": "This Month", "mr": "हा महिना", "hi": "इस महीने"},
    "time_this_year": {"en": "This Year", "mr": "हे वर्ष", "hi": "इस साल"},
    "time_all_time": {"en": "All Time", "mr": "सर्व कालावधी", "hi": "सभी समय"},
    "time_custom": {"en": "Custom Date Range", "mr": "सानुकूल तारीख श्रेणी", "hi": "कस्टम तिथि सीमा"},

    # Measurement Modes
    "mode_kg": {"en": "Kilograms (kg)", "mr": "किलोग्रॅम (kg)", "hi": "किलोग्राम (kg)"},
    "mode_gram": {"en": "Grams (g)", "mr": "ग्रॅम (g)", "hi": "ग्राम (g)"},
    "mode_litre": {"en": "Litres (L)", "mr": "लिटर (L)", "hi": "लीटर (L)"},
    "mode_ml": {"en": "Millilitres (ml)", "mr": "मिलीलीटर (ml)", "hi": "मिलीलीटर (ml)"},
    "billing_unit_type": {"en": "Select Measurement Unit", "mr": "वजन / मोजमाप एकक निवडा", "hi": "माप इकाई चुनें"}
}


def get_current_language() -> str:
    """Returns currently selected language code ('en', 'mr', 'hi')."""
    if "language" not in st.session_state:
        st.session_state.language = "en"
    return st.session_state.language


def t(key: str, lang: str = None) -> str:
    """Translates a UI key into the target language."""
    if not lang:
        lang = get_current_language()
    
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get("en", key))
    return key


def get_product_display_name(english_name: str, lang: str = None) -> str:
    """
    Returns localized product name based on selected language.
    For Marathi/Hindi, returns 'मराठी नाव (English Name)' for instant recognition.
    """
    if not lang:
        lang = get_current_language()

    if lang == "en":
        return english_name

    trans_entry = PRODUCT_TRANSLATIONS.get(english_name.strip())
    if trans_entry and lang in trans_entry:
        local_name = trans_entry[lang]
        return f"{local_name} ({english_name})"
    return english_name


def get_category_display_name(category: str, lang: str = None) -> str:
    """Returns localized category name."""
    if not lang:
        lang = get_current_language()

    if lang == "en":
        return category

    cat_entry = CATEGORY_TRANSLATIONS.get(category.strip())
    if cat_entry and lang in cat_entry:
        return f"{cat_entry[lang]} ({category})"
    return category

