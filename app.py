from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_hezshop_2026'

# Simple in-memory user database (for demo purposes)
users = {}

# ─── PRODUCT IMAGE MAP ────────────────────────────────────────────────────────
PRODUCT_IMAGE_MAP = {
    # Audio
    1:  "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",   # headphones
    14: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80",   # earbuds
    15: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80",   # speaker
    46: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",   # headphones
    47: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80",   # earbuds
    48: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80",   # soundbar
    49: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80",   # speaker
    50: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80",   # headset
    70: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=800&q=80",   # studio mic
    71: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80",   # budget speaker
    72: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80",   # budget earbuds
    # Wearables
    2:  "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80",
    3:  "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80",
    7:  "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&q=80",
    16: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80",
    41: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80",
    42: "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80",
    43: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80",
    44: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80",
    45: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&q=80",
    73: "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80",   # budget watch
    # Mobiles
    6:  "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80",
    21: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80",
    26: "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=800&q=80",
    27: "https://images.unsplash.com/photo-1565849904461-04a58ad377e0?w=800&q=80",
    28: "https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=800&q=80",
    29: "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=800&q=80",
    30: "https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=800&q=80",
    32: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80",
    33: "https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=800&q=80",
    34: "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?w=800&q=80",
    35: "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=800&q=80",
    74: "https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=800&q=80",   # budget phone
    75: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&q=80",   # entry phone
    # Electronics
    4:  "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&q=80",
    19: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80",
    20: "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&q=80",
    36: "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80",
    37: "https://images.unsplash.com/photo-1586210471891-78e8618aa8cd?w=800&q=80",
    38: "https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&q=80",
    39: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80",
    40: "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800&q=80",
    76: "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80",   # budget monitor
    # Fashion
    5:  "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80",
    9:  "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80",
    10: "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80",
    11: "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=800&q=80",
    17: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80",
    18: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&q=80",
    31: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80",
    77: "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80",   # budget jacket
    # Beauty
    12: "https://images.unsplash.com/photo-1599305090598-fe179d501227?w=800&q=80",
    22: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80",
    23: "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&q=80",
    51: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80",
    52: "https://images.unsplash.com/photo-1599305090598-fe179d501227?w=800&q=80",
    53: "https://images.unsplash.com/photo-1599305090598-fe179d501227?w=800&q=80",
    54: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80",
    55: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80",
    56: "https://images.unsplash.com/photo-1599305090598-fe179d501227?w=800&q=80",
    78: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&q=80",   # budget serum
    79: "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&q=80", # budget lipstick
    # Home
    8:  "https://images.unsplash.com/photo-1503602642458-232111445657?w=800&q=80",
    13: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",
    24: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80",
    25: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",
    57: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&q=80",
    58: "https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=800&q=80",
    59: "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&q=80",
    60: "https://images.unsplash.com/photo-1505691938895-1758d7feb511?w=800&q=80",
    61: "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&q=80",
    80: "https://images.unsplash.com/photo-1503602642458-232111445657?w=800&q=80",  # budget stool
    81: "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=800&q=80",  # budget purifier
}

def get_image(product_id, fallback):
    return PRODUCT_IMAGE_MAP.get(product_id, fallback)

# ─── PRODUCTS DATA ────────────────────────────────────────────────────────────
# All brand names are custom/original – no real brand names used.
products = [
    # ── AUDIO ──
    {"id": 1,  "name": "Nexus Sonic Pro Max",    "brand": "Nexus",    "desc": "Active Noise Cancellation • 40h Battery",   "price": 19999,  "old_price": 24999,  "discount": "20% OFF", "badge": "NEW",         "category": "audio",       "rating": 4.5},
    {"id": 14, "name": "Wavepod Freedom Buds",   "brand": "Wavepod",  "desc": "True Wireless • 8h Playtime",               "price": 8999,   "old_price": 12999,  "discount": "30% OFF", "badge": "POPULAR",     "category": "audio",       "rating": 4.5},
    {"id": 15, "name": "Boomvault Thunder 360",  "brand": "Boomvault","desc": "360° Sound • Waterproof",                   "price": 15999,  "old_price": 19999,  "discount": "20% OFF", "badge": None,          "category": "audio",       "rating": 4.2},
    {"id": 46, "name": "Audara UltraBeat",       "brand": "Audara",   "desc": "Noise Cancellation • 45h Battery",          "price": 12999,  "old_price": 15999,  "discount": "19% OFF", "badge": None,          "category": "audio",       "rating": 4.4},
    {"id": 47, "name": "Clarion Crystal Buds",   "brand": "Clarion",  "desc": "In-ear • 10h + 30h charging case",          "price": 5999,   "old_price": 8999,   "discount": "33% OFF", "badge": None,          "category": "audio",       "rating": 4.2},
    {"id": 48, "name": "Sonara Echo Bar Pro",    "brand": "Sonara",   "desc": "Dolby 5.1 • Wireless Subwoofer",            "price": 18999,  "old_price": 24999,  "discount": "24% OFF", "badge": None,          "category": "audio",       "rating": 4.3},
    {"id": 49, "name": "Boomvault Retro Blast",  "brand": "Boomvault","desc": "Retro Style • Powerful Bass",               "price": 6999,   "old_price": 9999,   "discount": "30% OFF", "badge": None,          "category": "audio",       "rating": 4.1},
    {"id": 50, "name": "Voxar Studio Headset",   "brand": "Voxar",    "desc": "Studio Tuning • USB-C",                     "price": 14999,  "old_price": 18999,  "discount": "21% OFF", "badge": None,          "category": "audio",       "rating": 4.5},
    {"id": 70, "name": "Voxar Condenser Mic",    "brand": "Voxar",    "desc": "Immersive 3D Audio • Studio Grade",         "price": 9999,   "old_price": 13999,  "discount": "28% OFF", "badge": "3D AUDIO",    "category": "audio",       "rating": 4.3},
    {"id": 71, "name": "Boomvault Mini Cube",    "brand": "Boomvault","desc": "Compact • Rechargeable",                    "price": 1499,   "old_price": 2499,   "discount": "40% OFF", "badge": None,          "category": "audio",       "rating": 2.8},
    {"id": 72, "name": "Clarion Lite Buds",      "brand": "Clarion",  "desc": "Entry-level • Tangle-free cable",           "price": 799,    "old_price": 1299,   "discount": "38% OFF", "badge": None,          "category": "audio",       "rating": 3.1},
    # ── WEARABLES ──
    {"id": 2,  "name": "Zenith Horizon Watch",   "brand": "Zenith",   "desc": "Always-on OLED • Titanium Case",            "price": 39999,  "old_price": 44999,  "discount": None,       "badge": None,          "category": "wearables",   "rating": 4.3},
    {"id": 3,  "name": "Aether Minimalist 2",    "brand": "Aether",   "desc": "Quartz Movement • Ceramic Finish",          "price": 12499,  "old_price": None,   "discount": None,       "badge": "BEST SELLER", "category": "wearables",   "rating": 4.6},
    {"id": 16, "name": "Fitora Pulse Tracker",   "brand": "Fitora",   "desc": "Heart Rate Monitor • GPS",                  "price": 7999,   "old_price": 9999,   "discount": "20% OFF", "badge": "NEW",         "category": "wearables",   "rating": 4.0},
    {"id": 41, "name": "Fitora Active Band",     "brand": "Fitora",   "desc": "GPS • Heart-rate Monitor",                  "price": 2999,   "old_price": 3999,   "discount": "25% OFF", "badge": None,          "category": "wearables",   "rating": 4.0},
    {"id": 42, "name": "Titan Sport Watch",      "brand": "Titan",    "desc": "Waterproof 10 ATM",                         "price": 5499,   "old_price": 7499,   "discount": "26% OFF", "badge": None,          "category": "wearables",   "rating": 4.1},
    {"id": 43, "name": "Aether Smart Ring",      "brand": "Aether",   "desc": "Sleep Tracking • NFC",                     "price": 7999,   "old_price": 9999,   "discount": "20% OFF", "badge": None,          "category": "wearables",   "rating": 4.3},
    {"id": 44, "name": "Fitora Health Tracker",  "brand": "Fitora",   "desc": "Blood Oxygen + ECG",                        "price": 6499,   "old_price": 8499,   "discount": "24% OFF", "badge": None,          "category": "wearables",   "rating": 4.2},
    {"id": 45, "name": "Lumique Smartband S1",   "brand": "Lumique",  "desc": "Color LCD • 45 Days Battery",               "price": 1999,   "old_price": 2999,   "discount": "33% OFF", "badge": None,          "category": "wearables",   "rating": 4.0},
    {"id": 73, "name": "Kronex Value Watch",     "brand": "Kronex",   "desc": "Digital Display • Water Resistant",         "price": 899,    "old_price": 1499,   "discount": "40% OFF", "badge": None,          "category": "wearables",   "rating": 2.9},
    # ── MOBILES ──
    {"id": 6,  "name": "Atrium Pro Max",         "brand": "Atrium",   "desc": "Titanium Silver, 256 GB",                   "price": 124990, "old_price": 139900, "discount": "10% OFF", "badge": "NEW RELEASE", "category": "mobiles",     "rating": 4.8},
    {"id": 21, "name": "Orbitex Lite Phone",     "brand": "Orbitex",  "desc": "Snapdragon 8 Gen 2 • 128GB",               "price": 69999,  "old_price": 79999,  "discount": "12% OFF", "badge": None,          "category": "mobiles",     "rating": 4.2},
    {"id": 26, "name": "Phantom X Pro",          "brand": "Phantom",  "desc": "Triple Camera Array • Ceramic Back",        "price": 89999,  "old_price": 99999,  "discount": "10% OFF", "badge": "PREMIUM",     "category": "mobiles",     "rating": 4.6},
    {"id": 27, "name": "Aura Crystal 5G",        "brand": "Aura",     "desc": "Glass Back Design • 120Hz Display",         "price": 74999,  "old_price": 84999,  "discount": "11% OFF", "badge": "TRENDING",    "category": "mobiles",     "rating": 4.4},
    {"id": 28, "name": "Nebula Edge Ultra",      "brand": "Nebula",   "desc": "Curved Glass Back • Ultra Thin",            "price": 119999, "old_price": 129999, "discount": "7% OFF",  "badge": "FLAGSHIP",    "category": "mobiles",     "rating": 4.7},
    {"id": 29, "name": "Zenith Matte Pro",       "brand": "Zenith",   "desc": "Matte Finish Back • 5G Ready",              "price": 59999,  "old_price": 69999,  "discount": "14% OFF", "badge": None,          "category": "mobiles",     "rating": 4.3},
    {"id": 30, "name": "Verdara Eco Phone",      "brand": "Verdara",  "desc": "Recycled Back • Eco-Friendly 5G",           "price": 79999,  "old_price": 89999,  "discount": "11% OFF", "badge": "ECO",         "category": "mobiles",     "rating": 4.5},
    {"id": 32, "name": "Pioneer Edge 5G",        "brand": "Pioneer",  "desc": "6.8-inch Retina • 128GB",                  "price": 59999,  "old_price": 64999,  "discount": "8% OFF",  "badge": None,          "category": "mobiles",     "rating": 4.1},
    {"id": 33, "name": "Phantom Lite",           "brand": "Phantom",  "desc": "Quad Camera • 60W Fast Charge",             "price": 49999,  "old_price": 54999,  "discount": "9% OFF",  "badge": None,          "category": "mobiles",     "rating": 4.2},
    {"id": 34, "name": "Orbitex Spark",          "brand": "Orbitex",  "desc": "Night Mode Camera • 5G-Ready",             "price": 52999,  "old_price": 57999,  "discount": "8% OFF",  "badge": None,          "category": "mobiles",     "rating": 4.0},
    {"id": 35, "name": "Nimbus Galaxy Fold",     "brand": "Nimbus",   "desc": "Foldable • 16GB RAM",                      "price": 119999, "old_price": 129999, "discount": "8% OFF",  "badge": None,          "category": "mobiles",     "rating": 4.5},
    {"id": 74, "name": "Kronex Budget X1",       "brand": "Kronex",   "desc": "4G LTE • 2GB RAM • 32GB",                  "price": 6999,   "old_price": 9999,   "discount": "30% OFF", "badge": None,          "category": "mobiles",     "rating": 2.7},
    {"id": 75, "name": "Orbitex Entry Go",       "brand": "Orbitex",  "desc": "5000mAh Battery • Dual Sim",               "price": 9999,   "old_price": 12999,  "discount": "23% OFF", "badge": None,          "category": "mobiles",     "rating": 3.3},
    # ── ELECTRONICS ──
    {"id": 4,  "name": "Lumina Optic X-1",       "brand": "Lumina",   "desc": "Full Frame • 4K 120fps HDR",               "price": 129999, "old_price": 145999, "discount": None,       "badge": None,          "category": "electronics", "rating": 4.7},
    {"id": 19, "name": "NovaBook Pro 15",        "brand": "NovaBook",  "desc": "Intel i7 • 16GB RAM • 512GB SSD",         "price": 89999,  "old_price": 109999, "discount": "18% OFF", "badge": None,          "category": "electronics", "rating": 4.6},
    {"id": 20, "name": "TabMaster 10",           "brand": "TabMaster","desc": "10.5 inch • 128GB Storage",                "price": 34999,  "old_price": 39999,  "discount": "12% OFF", "badge": None,          "category": "electronics", "rating": 4.3},
    {"id": 36, "name": "Argon Pro Monitor",      "brand": "Argon",    "desc": "27 inch • 4K UHD",                         "price": 34999,  "old_price": 44999,  "discount": "22% OFF", "badge": None,          "category": "electronics", "rating": 4.4},
    {"id": 37, "name": "PixelBeam Projector",    "brand": "PixelBeam","desc": "1080p • Portable",                          "price": 19999,  "old_price": 25999,  "discount": "23% OFF", "badge": None,          "category": "electronics", "rating": 4.1},
    {"id": 38, "name": "Sonara Sync Speaker",    "brand": "Sonara",   "desc": "Smart Wi-Fi • 360° Sound",                 "price": 12999,  "old_price": 16999,  "discount": "25% OFF", "badge": None,          "category": "electronics", "rating": 4.3},
    {"id": 39, "name": "Aero Cooling Dock",      "brand": "Aero",     "desc": "Laptop Cooling Base with RGB",             "price": 3499,   "old_price": 4999,   "discount": "30% OFF", "badge": None,          "category": "electronics", "rating": 4.0},
    {"id": 40, "name": "Quantum Router X",       "brand": "Quantum",  "desc": "Tri-Band • 2.6Gbps",                       "price": 9999,   "old_price": 12999,  "discount": "23% OFF", "badge": None,          "category": "electronics", "rating": 4.2},
    {"id": 76, "name": "Argon Value 24",         "brand": "Argon",    "desc": "24 inch • Full HD • 75Hz",                 "price": 8999,   "old_price": 12999,  "discount": "30% OFF", "badge": None,          "category": "electronics", "rating": 3.2},
    # ── FASHION ──
    {"id": 5,  "name": "Obsidian Leather Jacket","brand": "Obsidian", "desc": "Premium Cowhide • Vintage Wash",           "price": 8499,   "old_price": 10999,  "discount": "15% OFF", "badge": None,          "category": "fashion",     "rating": 4.2},
    {"id": 11, "name": "Velura Evening Gown",    "brand": "Velura",   "desc": "Emerald Green • Silk Blend",               "price": 12900,  "old_price": 15000,  "discount": "14% OFF", "badge": None,          "category": "fashion",     "rating": 4.1},
    {"id": 17, "name": "Denimax Urban Jeans",    "brand": "Denimax",  "desc": "Slim Fit • Organic Cotton",                "price": 4999,   "old_price": 6999,   "discount": "28% OFF", "badge": None,          "category": "fashion",     "rating": 4.2},
    {"id": 18, "name": "Floatex Cloud Sneakers", "brand": "Floatex",  "desc": "Memory Foam • Breathable",                 "price": 6999,   "old_price": 8999,   "discount": "22% OFF", "badge": "BEST SELLER", "category": "fashion",     "rating": 4.4},
    {"id": 31, "name": "Gripp Street Sneakers",  "brand": "Gripp",    "desc": "Athleisure Comfort • High Grip",           "price": 2599,   "old_price": 3999,   "discount": "35% OFF", "badge": None,          "category": "fashion",     "rating": 4.0},
    {"id": 77, "name": "Denimax Basic Hoodie",   "brand": "Denimax",  "desc": "Cotton Blend • Loose Fit",                 "price": 799,    "old_price": 1299,   "discount": "38% OFF", "badge": None,          "category": "fashion",     "rating": 2.9},
    # ── BEAUTY ──
    {"id": 12, "name": "Lumivera Face Serum",    "brand": "Lumivera", "desc": "Hyaluronic Acid • Vitamin C",              "price": 1250,   "old_price": 1500,   "discount": "16% OFF", "badge": "BEST SELLER", "category": "beauty",      "rating": 4.4},
    {"id": 22, "name": "Lumivera Day Glow",      "brand": "Lumivera", "desc": "SPF 30 • Hydrating Formula",               "price": 1899,   "old_price": 2299,   "discount": "17% OFF", "badge": None,          "category": "beauty",      "rating": 4.3},
    {"id": 23, "name": "Rosset Velvet Lipstick", "brand": "Rosset",   "desc": "Long-Lasting • 12 Shades",                 "price": 799,    "old_price": 999,    "discount": "20% OFF", "badge": "TRENDING",    "category": "beauty",      "rating": 4.5},
    {"id": 51, "name": "Lumivera Night Renew",   "brand": "Lumivera", "desc": "Retinol + Hyaluronic",                     "price": 1399,   "old_price": 1999,   "discount": "30% OFF", "badge": None,          "category": "beauty",      "rating": 4.2},
    {"id": 52, "name": "Botaniq Silk Oil",       "brand": "Botaniq",  "desc": "Vitamin E + Jojoba",                       "price": 1199,   "old_price": 1699,   "discount": "29% OFF", "badge": None,          "category": "beauty",      "rating": 4.1},
    {"id": 53, "name": "Lumivera Eye Serum",     "brand": "Lumivera", "desc": "Anti-Dark Circle Formula",                 "price": 999,    "old_price": 1399,   "discount": "29% OFF", "badge": None,          "category": "beauty",      "rating": 4.3},
    {"id": 54, "name": "Botaniq Aloe Gel",       "brand": "Botaniq",  "desc": "Soothing for All Skin",                   "price": 449,    "old_price": 699,    "discount": "36% OFF", "badge": None,          "category": "beauty",      "rating": 4.0},
    {"id": 55, "name": "Rosset Citrus Cleanser", "brand": "Rosset",   "desc": "Brightening & Gentle",                    "price": 599,    "old_price": 899,    "discount": "33% OFF", "badge": None,          "category": "beauty",      "rating": 4.1},
    {"id": 56, "name": "Lumivera Day Moisturiser","brand": "Lumivera","desc": "SPF 20 • Non-Greasy",                      "price": 1299,   "old_price": 1799,   "discount": "28% OFF", "badge": None,          "category": "beauty",      "rating": 4.2},
    {"id": 78, "name": "Rosset Basic Serum",     "brand": "Rosset",   "desc": "Lightweight • Daily Use",                  "price": 299,    "old_price": 499,    "discount": "40% OFF", "badge": None,          "category": "beauty",      "rating": 3.0},
    {"id": 79, "name": "Botaniq Tinted Balm",    "brand": "Botaniq",  "desc": "Natural Tint • SPF 15",                   "price": 249,    "old_price": 399,    "discount": "37% OFF", "badge": None,          "category": "beauty",      "rating": 2.6},
    # ── HOME ──
    {"id": 13, "name": "Arvesta Minimalist Sofa","brand": "Arvesta",  "desc": "Linen Fabric • Wooden Legs",               "price": 45000,  "old_price": 55000,  "discount": "18% OFF", "badge": None,          "category": "home",        "rating": 4.3},
    {"id": 24, "name": "Ergara Office Chair",    "brand": "Ergara",   "desc": "Adjustable Height • Lumbar Support",       "price": 24999,  "old_price": 29999,  "discount": "16% OFF", "badge": None,          "category": "home",        "rating": 4.4},
    {"id": 25, "name": "Arvesta Rustic Table",   "brand": "Arvesta",  "desc": "Solid Wood • Seats 6",                    "price": 65999,  "old_price": 79999,  "discount": "17% OFF", "badge": None,          "category": "home",        "rating": 4.2},
    {"id": 57, "name": "Modula Storage Shelf",   "brand": "Modula",   "desc": "Wall-Mounted • Adjustable",               "price": 8499,   "old_price": 10999,  "discount": "23% OFF", "badge": None,          "category": "home",        "rating": 4.1},
    {"id": 58, "name": "Arvesta Coastal Table",  "brand": "Arvesta",  "desc": "Oak Finish • Hidden Compartment",         "price": 15999,  "old_price": 19999,  "discount": "20% OFF", "badge": None,          "category": "home",        "rating": 4.3},
    {"id": 59, "name": "Eclipso Bedside Lamp",   "brand": "Eclipso",  "desc": "Dimmable • Smart Controls",               "price": 3499,   "old_price": 4599,   "discount": "24% OFF", "badge": None,          "category": "home",        "rating": 4.4},
    {"id": 60, "name": "Arvesta Wall Art Set",   "brand": "Arvesta",  "desc": "3-Piece Gallery Frames",                  "price": 4499,   "old_price": 5999,   "discount": "25% OFF", "badge": None,          "category": "home",        "rating": 4.0},
    {"id": 61, "name": "Aira Air Purifier",      "brand": "Aira",     "desc": "HEPA Filter • Quiet Mode",                "price": 12499,  "old_price": 15999,  "discount": "22% OFF", "badge": None,          "category": "home",        "rating": 4.5},
    {"id": 80, "name": "Modula Basic Stool",     "brand": "Modula",   "desc": "Foldable • Lightweight",                  "price": 999,    "old_price": 1799,   "discount": "44% OFF", "badge": None,          "category": "home",        "rating": 2.8},
    {"id": 81, "name": "Aira Basic Purifier",    "brand": "Aira",     "desc": "Carbon Filter • Compact",                 "price": 3999,   "old_price": 5999,   "discount": "33% OFF", "badge": None,          "category": "home",        "rating": 3.4},
]

# Inject images from the map
for p in products:
    p['image'] = get_image(p['id'], "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80")

# ─── DEALS (homepage featured) ────────────────────────────────────────────────
deals = [
    {"id": 7,  "name": "Kronex Series Watch",    "brand": "Kronex",   "desc": "Top Rated",     "price": 2499,  "old_price": 4999,  "discount": "50% OFF", "category": "wearables"},
    {"id": 8,  "name": "Arvesta Oak Stool",      "brand": "Arvesta",  "desc": "New Arrival",   "price": 8990,  "old_price": 12500, "discount": "28% OFF", "category": "home"},
    {"id": 9,  "name": "Gripp Velocity Runners", "brand": "Gripp",    "desc": "Bestseller",    "price": 4200,  "old_price": 6000,  "discount": "30% OFF", "category": "fashion"},
    {"id": 10, "name": "Visora Eclipse Shades",  "brand": "Visora",   "desc": "Limited Stock", "price": 1850,  "old_price": 3500,  "discount": "40% OFF", "category": "fashion"},
]

DEAL_IMAGE_MAP = {
    7:  "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&q=80",
    8:  "https://images.unsplash.com/photo-1503602642458-232111445657?w=800&q=80",
    9:  "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80",
    10: "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80",
}
for d in deals:
    d['image'] = DEAL_IMAGE_MAP.get(d['id'], "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&q=80")
    d['rating'] = 4.2


# ─── SPEC TABLE HELPER ────────────────────────────────────────────────────────
def build_specs(cat):
    if cat in ('mobiles', 'electronics'):
        return [
            {"title": "Display",  "icon": "smartphone",       "rows": {"Size": "6.7 inch", "Resolution": "2796 × 1290 px", "Type": "Super AMOLED"}},
            {"title": "Hardware", "icon": "cpu",              "rows": {"Chipset": "Atrium A17 Bionic", "Cores": "6-Core", "RAM": "8 GB LPDDR5X"}},
            {"title": "Camera",   "icon": "aperture",         "rows": {"Primary": "48 MP (f/1.78)", "Ultra Wide": "12 MP (f/2.2)", "Telephoto": "12 MP 3× Zoom"}},
        ]
    elif cat == 'fashion':
        return [
            {"title": "Material", "icon": "scissors",         "rows": {"Fabric": "Premium Source", "Care": "Machine wash cold", "Origin": "Imported"}},
            {"title": "Fit",      "icon": "user",             "rows": {"Style": "Standard Fit", "Type": "Everyday wear", "Comfort": "High"}},
        ]
    elif cat == 'beauty':
        return [
            {"title": "Ingredients","icon": "droplet",        "rows": {"Key": "Hyaluronic Acid", "Free from": "Parabens, Sulfates", "Type": "Serum"}},
            {"title": "Usage",    "icon": "sun",              "rows": {"Time": "Day & Night", "Skin Type": "All skin types"}},
        ]
    elif cat == 'home':
        return [
            {"title": "Dimensions","icon": "maximize",        "rows": {"Width": "80 cm", "Depth": "35 cm", "Height": "82 cm"}},
            {"title": "Build",    "icon": "box",              "rows": {"Frame": "Hardwood", "Upholstery": "Premium Linen", "Weight": "45 kg"}},
        ]
    else:  # wearables / audio
        return [
            {"title": "Battery",  "icon": "battery-charging", "rows": {"Life": "Up to 40 hours", "Charging": "Fast Charge USB-C", "Type": "Lithium-ion"}},
            {"title": "Connectivity","icon": "wifi",          "rows": {"Bluetooth": "5.3", "Range": "10 metres", "Multi-point": "Supported"}},
        ]


# ─── COLORS / OPTIONS HELPER ─────────────────────────────────────────────────
def build_colors_options(pid, base_image, cat):
    colors_map = {
        1:  ([{"name":"Midnight Black","hex":"#1e293b"}, {"name":"Arctic White","hex":"#e2e8f0"}, {"name":"Cherry Red","hex":"#f43f5e"}], "VARIANT", ["Wired","Wireless"]),
        2:  ([{"name":"Matte Black","hex":"#1e293b"}, {"name":"Silver","hex":"#e2e8f0"}], "EDITION", ["Standard","GPS","Cellular"]),
        3:  ([{"name":"Ceramic White","hex":"#f8fafc"}, {"name":"Midnight Black","hex":"#0f172a"}, {"name":"Rose Gold","hex":"#f59e0b"}], "SIZE", ["38mm","42mm"]),
        4:  ([{"name":"Pro Black","hex":"#0f172a"}, {"name":"Titanium Gray","hex":"#64748b"}], "LENS KIT", ["Body Only","With 50mm","With 24-70mm"]),
        5:  ([{"name":"Obsidian Black","hex":"#0f172a"}, {"name":"Crimson Red","hex":"#be123c"}, {"name":"Vintage Brown","hex":"#92400e"}], "SIZE", ["S","M","L","XL","XXL"]),
        6:  ([{"name":"Midnight Black","hex":"#111827"}, {"name":"Titanium","hex":"#94a3b8"}, {"name":"Ocean Blue","hex":"#0ea5e9"}], "STORAGE", ["128 GB","256 GB","512 GB"]),
        9:  ([{"name":"Crimson Red","hex":"#be123c"}, {"name":"Obsidian Black","hex":"#0f172a"}, {"name":"Pure White","hex":"#f8fafc"}], "SIZE", ["UK 7","UK 8","UK 9","UK 10"]),
        11: ([{"name":"Emerald Green","hex":"#064e3b"}, {"name":"Ruby Red","hex":"#be123c"}], "SIZE", ["S","M","L"]),
        12: ([{"name":"Clear Serum","hex":"#f0f9ff"}], "SIZE", ["30ml","50ml","100ml"]),
        13: ([{"name":"Linen Beige","hex":"#fef3c7"}, {"name":"Charcoal Gray","hex":"#64748b"}, {"name":"Navy Blue","hex":"#1e40af"}], "SIZE", ["2 Seater","3 Seater","Corner Sofa"]),
        14: ([{"name":"Midnight Black","hex":"#1e293b"}, {"name":"Pearl White","hex":"#f8fafc"}, {"name":"Ocean Blue","hex":"#0ea5e9"}], "VARIANT", ["Standard","Pro"]),
        15: ([{"name":"Jet Black","hex":"#0f172a"}, {"name":"Silver","hex":"#e2e8f0"}], "POWER", ["Battery","Wired"]),
        16: ([{"name":"Black","hex":"#1e293b"}, {"name":"Rose Gold","hex":"#f59e0b"}, {"name":"Blue","hex":"#3b82f6"}], "BAND SIZE", ["Small","Medium","Large"]),
        17: ([{"name":"Dark Blue","hex":"#1e40af"}, {"name":"Light Blue","hex":"#93c5fd"}, {"name":"Black","hex":"#0f172a"}], "SIZE", ["28","30","32","34","36"]),
        18: ([{"name":"White","hex":"#f8fafc"}, {"name":"Black","hex":"#0f172a"}, {"name":"Gray","hex":"#64748b"}], "SIZE", ["UK 6","UK 7","UK 8","UK 9","UK 10"]),
        19: ([{"name":"Space Gray","hex":"#475569"}, {"name":"Silver","hex":"#e2e8f0"}], "STORAGE", ["256 GB","512 GB","1 TB"]),
        20: ([{"name":"Black","hex":"#0f172a"}, {"name":"White","hex":"#f8fafc"}, {"name":"Blue","hex":"#3b82f6"}], "STORAGE", ["64 GB","128 GB","256 GB"]),
        21: ([{"name":"Phantom Black","hex":"#1e293b"}, {"name":"Pearl White","hex":"#f8fafc"}, {"name":"Mint Green","hex":"#10b981"}], "STORAGE", ["128 GB","256 GB"]),
        22: ([{"name":"Clear","hex":"#f0f9ff"}], "SIZE", ["50ml","100ml","200ml"]),
        23: ([{"name":"Ruby Red","hex":"#dc2626"}, {"name":"Nude","hex":"#d4a574"}, {"name":"Plum","hex":"#7c3aed"}], "SHADE", ["Light","Medium","Dark"]),
        24: ([{"name":"Black Mesh","hex":"#374151"}, {"name":"Gray Fabric","hex":"#9ca3af"}], "TYPE", ["Standard","Executive"]),
        25: ([{"name":"Walnut","hex":"#92400e"}, {"name":"Oak","hex":"#d4a574"}], "SIZE", ["4 Seater","6 Seater","8 Seater"]),
        26: ([{"name":"Phantom Black","hex":"#1e293b"}, {"name":"Ceramic White","hex":"#f8fafc"}, {"name":"Titanium Blue","hex":"#0ea5e9"}], "STORAGE", ["256 GB","512 GB","1 TB"]),
        27: ([{"name":"Crystal Clear","hex":"#f0f9ff"}, {"name":"Midnight Black","hex":"#0f172a"}, {"name":"Rose Gold","hex":"#f59e0b"}], "STORAGE", ["128 GB","256 GB","512 GB"]),
        28: ([{"name":"Cosmic Black","hex":"#0f172a"}, {"name":"Aurora White","hex":"#f8fafc"}, {"name":"Nebula Purple","hex":"#8b5cf6"}], "STORAGE", ["256 GB","512 GB","1 TB"]),
        29: ([{"name":"Matte Black","hex":"#374151"}, {"name":"Matte Gray","hex":"#6b7280"}, {"name":"Matte Blue","hex":"#3b82f6"}], "STORAGE", ["128 GB","256 GB"]),
        30: ([{"name":"Eco Black","hex":"#1f2937"}, {"name":"Eco Brown","hex":"#92400e"}, {"name":"Eco Green","hex":"#065f46"}], "STORAGE", ["128 GB","256 GB","512 GB"]),
    }
    if pid in colors_map:
        raw_colors, opt_name, choices = colors_map[pid]
        colors = [{"name": c["name"], "hex": c["hex"], "image": base_image} for c in raw_colors]
        return colors, {"name": opt_name, "choices": choices}
    default_color = [{"name": "Default", "hex": "#0f172a", "image": base_image}]
    if cat == 'fashion':
        return default_color, {"name": "SIZE", "choices": ["S","M","L","XL"]}
    elif cat in ('mobiles', 'electronics'):
        return default_color, {"name": "STORAGE", "choices": ["128 GB","256 GB"]}
    elif cat in ('wearables', 'audio'):
        return default_color, {"name": "VARIANT", "choices": ["Standard"]}
    elif cat == 'beauty':
        return default_color, {"name": "SIZE", "choices": ["30ml","50ml"]}
    elif cat == 'home':
        return default_color, {"name": "SIZE", "choices": ["Standard"]}
    return default_color, {"name": "VARIANT", "choices": ["Standard"]}


# ─── ROUTES ──────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    categories = {}
    for product in products:
        cat = product['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(product)
    for cat in categories:
        categories[cat] = categories[cat][:4]
    # Featured section products
    audio_featured   = [p for p in products if p['category'] == 'audio'][:4]
    home_featured    = [p for p in products if p['category'] == 'home'][:4]
    return render_template('home.html', categories=categories, deals=deals,
                           audio_featured=audio_featured, home_featured=home_featured)


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    return redirect(url_for('products_list', q=query))


@app.route('/products')
def products_list():
    search_query = request.args.get('q', '').strip().lower()
    category     = request.args.get('category', '').strip().lower() or None
    sort_by      = request.args.get('sort', 'newest')

    category_ranges = {
        'mobiles':     (5000,  150000),
        'electronics': (1000,  90000),
        'fashion':     (500,   15000),
        'home':        (800,   75000),
        'beauty':      (200,   9000),
        'wearables':   (800,   45000),
        'audio':       (700,   25000),
    }
    default_min, default_max = category_ranges.get(category or '', (0, 150000))

    min_price_arg = request.args.get('min_price', type=int)
    max_price_arg = request.args.get('max_price', type=int)
    min_rating    = request.args.get('min_rating', default=0.0, type=float)
    selected_brands = [b.lower() for b in request.args.getlist('brand') if b.strip()]

    min_price = min_price_arg if min_price_arg is not None else default_min
    max_price = max_price_arg if max_price_arg is not None else default_max

    available_brands = set()
    for p in products:
        if category and p.get('category') != category:
            continue
        brand_name = p.get('brand') or p.get('name', '').split()[0]
        available_brands.add(brand_name.title())

    all_p = products + [d for d in deals if not any(p['id'] == d['id'] for p in products)]
    filtered_products = []
    seen_ids = set()
    for p in all_p:
        if p['id'] in seen_ids:
            continue
        if search_query:
            haystack = (p.get('name','') + ' ' + p.get('desc','') + ' ' + p.get('category','') + ' ' + p.get('brand','')).lower()
            if search_query not in haystack:
                continue
        if category and p.get('category') != category:
            continue
        brand_name = p.get('brand') or p.get('name', '').split()[0]
        if selected_brands and brand_name.lower() not in selected_brands:
            continue
        if p.get('price', 0) < min_price or p.get('price', 0) > max_price:
            continue
        if p.get('rating', 4.0) < min_rating:
            continue
        filtered_products.append(p)
        seen_ids.add(p['id'])

    # Sorting
    if sort_by == 'price_asc':
        filtered_products.sort(key=lambda x: x.get('price', 0))
    elif sort_by == 'price_desc':
        filtered_products.sort(key=lambda x: x.get('price', 0), reverse=True)
    elif sort_by == 'rating':
        filtered_products.sort(key=lambda x: x.get('rating', 0), reverse=True)
    elif sort_by == 'discount':
        def disc_val(p):
            disc = p.get('discount', '') or ''
            try:
                return int(disc.replace('% OFF','').strip())
            except:
                return 0
        filtered_products.sort(key=disc_val, reverse=True)
    # newest = default order (as defined in products list, newest IDs last)
    else:
        filtered_products.sort(key=lambda x: x.get('id', 0), reverse=True)

    slider_percent = 100
    if default_max > default_min:
        slider_percent = int((max_price - default_min) / max(1, default_max - default_min) * 100)
        slider_percent = max(0, min(slider_percent, 100))

    return render_template('products.html',
        products=filtered_products,
        current_category=category,
        search_query=search_query,
        min_price=min_price,
        max_price=max_price,
        min_rating=min_rating,
        category_min=default_min,
        category_max=default_max,
        slider_percent=slider_percent,
        brand_options=sorted(available_brands),
        selected_brands=selected_brands,
        sort_by=sort_by,
    )


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    all_products = products + deals
    base_product = next((p for p in all_products if p['id'] == product_id), None)
    if not base_product:
        base_product = products[0]

    product = dict(base_product)
    cat = product.get('category', 'mobiles')
    pid = product.get('id')

    product['specs'] = build_specs(cat)
    colors, options = build_colors_options(pid, product['image'], cat)
    product['colors']  = colors
    product['options'] = options

    related_products = [p for p in products if p['category'] == cat and p['id'] != pid][:4]
    if len(related_products) < 4:
        others = [p for p in products if p['id'] != pid and p not in related_products]
        related_products += others[:4 - len(related_products)]

    return render_template('product_detail.html', product=product, related_products=related_products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            return render_template('login.html', error='Please fill in all fields.')
        hashed = hashlib.sha256(password.encode()).hexdigest()
        if username in users and users[username]['password'] == hashed:
            session['user'] = username
            session['user_name'] = users[username]['name']
            session['created_at'] = users[username].get('created_at', datetime.now().strftime('%B %d, %Y'))
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid email or password.')
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or not password:
            return render_template('signup.html', error='Please fill in all fields.')
        if len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters.')
        if email in users:
            return render_template('signup.html', error='Email already registered.')
        users[email] = {
            'name': name,
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'created_at': datetime.now().strftime('%B %d, %Y'),
        }
        return render_template('signup.html', success='Account created! You can now login.')
    return render_template('signup.html')


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    all_p = products + deals
    product = next((p for p in all_p if p['id'] == product_id), None)
    if product:
        option_val = request.form.get('product_option', '')
        cart_item = {
            "id":           product['id'],
            "name":         product['name'],
            "image":        product['image'],
            "price":        product['price'],
            "old_price":    product.get('old_price'),
            "discount_tag": product.get('discount'),
            "desc":         f"{product['category'].capitalize()} {option_val}".strip(),
            "quantity":     1,
            "option":       option_val,
        }
        cart_list = list(session['cart'])
        existing = next((i for i in cart_list if i['id'] == cart_item['id'] and i['option'] == cart_item['option']), None)
        if existing:
            existing['quantity'] += 1
        else:
            cart_list.append(cart_item)
        session['cart'] = cart_list
    if 'buy_now' in request.form:
        return redirect(url_for('cart'))
    return redirect(request.referrer or url_for('home'))


@app.route('/remove_cart_item/<int:index>')
def remove_cart_item(index):
    if 'cart' in session:
        cart_list = list(session['cart'])
        if 0 <= index < len(cart_list):
            cart_list.pop(index)
            session['cart'] = cart_list
    return redirect(url_for('cart'))


@app.route('/update_cart_item/<int:index>/<action>')
def update_cart_item(index, action):
    if 'cart' in session:
        cart_list = list(session['cart'])
        if 0 <= index < len(cart_list):
            if action == 'increment':
                cart_list[index]['quantity'] += 1
            elif action == 'decrement':
                if cart_list[index]['quantity'] > 1:
                    cart_list[index]['quantity'] -= 1
                else:
                    cart_list.pop(index)
            session['cart'] = cart_list
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    cart_items      = session.get('cart', [])
    total_price     = sum(item['price'] * item['quantity'] for item in cart_items)
    total_old_price = sum((item['old_price'] or item['price']) * item['quantity'] for item in cart_items)
    discount        = total_old_price - total_price
    return render_template('cart.html', cart_items=cart_items,
                           total_price=total_price, total_old_price=total_old_price, discount=discount)


@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user' not in session:
        return redirect(url_for('login'))
    email      = session.get('user')
    name       = session.get('user_name')
    created_at = session.get('created_at', users.get(email, {}).get('created_at', 'Now'))
    error = success = None

    if request.method == 'POST':
        section = request.form.get('section')
        if section == 'profile':
            new_name  = request.form.get('name', '').strip()
            new_email = request.form.get('email', '').strip().lower()
            if not new_name or not new_email:
                error = 'Name and email are required.'
            elif new_email != email and new_email in users:
                error = 'Email is already in use by another account.'
            else:
                user_data = users.pop(email)
                user_data['name'] = new_name
                users[new_email] = user_data
                session['user'] = new_email
                session['user_name'] = new_name
                email, name = new_email, new_name
                success = 'Profile updated successfully.'
        elif section == 'password':
            current_pwd = request.form.get('current_password', '')
            new_pwd     = request.form.get('new_password', '')
            confirm_pwd = request.form.get('confirm_password', '')
            if not current_pwd or not new_pwd or not confirm_pwd:
                error = 'All password fields are required.'
            elif new_pwd != confirm_pwd:
                error = 'New password and confirmation do not match.'
            elif len(new_pwd) < 6:
                error = 'New password must be at least 6 characters.'
            else:
                if users.get(email, {}).get('password') != hashlib.sha256(current_pwd.encode()).hexdigest():
                    error = 'Current password is incorrect.'
                else:
                    users[email]['password'] = hashlib.sha256(new_pwd.encode()).hexdigest()
                    success = 'Password changed successfully.'

    return render_template('account.html', email=email, name=name, created_at=created_at,
                           error=error, success=success)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_name', None)
    session.pop('created_at', None)
    return redirect(url_for('home'))


@app.context_processor
def inject_user_data():
    cart_items = session.get('cart', [])
    count      = sum(item['quantity'] for item in cart_items)
    return dict(cart_count=count, user=session.get('user'), user_name=session.get('user_name'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
