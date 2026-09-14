import json

products = [
    # Electronics - Laptops & Phones
    {
        "id": "prod_elec_001",
        "group_id": "group_apple_m3_air",
        "title": "Apple MacBook Air M3 (16GB Unified RAM, 512GB SSD) - Midnight",
        "brand": "Apple",
        "category": "Electronics",
        "sub_category": "Laptops",
        "price": 124900,
        "original_price": 134900,
        "discount_pct": 7,
        "rating": 4.8,
        "rating_count": 1420,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop&q=80",
        "description": "Supercharged by the M3 chip. Built for Apple Intelligence. Ultra-thin design, liquid retina display, and up to 18 hours of battery life.",
        "tags": ["laptop", "programming", "apple", "macbook", "m3", "ultrabook", "developer", "coding"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_mac_m3_16",
                "price": 124900,
                "original_price": 134900,
                "url": "https://www.amazon.in/dp/B0CX23V6LH",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Appario Retail"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_mac_m3_16",
                "price": 125990,
                "original_price": 134900,
                "url": "https://www.flipkart.com/apple-2024-macbook-air-m3",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "SuperComNet"
            }
        ],
        "specifications": {
            "Processor": "Apple M3 Chip (8-Core CPU, 10-Core GPU)",
            "RAM": "16GB Unified",
            "Storage": "512GB SSD",
            "Display": "13.6-inch Liquid Retina",
            "Weight": "1.24 kg"
        }
    },
    {
        "id": "prod_elec_002",
        "group_id": "group_sony_wh1000xm5",
        "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones - Black",
        "brand": "Sony",
        "category": "Electronics",
        "sub_category": "Audio",
        "price": 26990,
        "original_price": 34990,
        "discount_pct": 23,
        "rating": 4.7,
        "rating_count": 3890,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80",
        "description": "Industry-leading noise canceling with two processors and 8 microphones for unprecedented noise reduction and exceptional call quality.",
        "tags": ["headphones", "audio", "sony", "anc", "wireless", "music", "bluetooth", "travel"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_sony_xm5",
                "price": 26990,
                "original_price": 34990,
                "url": "https://www.amazon.in/dp/B09XS7JWHH",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Electronics Bazaar"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_sony_xm5",
                "price": 27490,
                "original_price": 34990,
                "url": "https://www.flipkart.com/sony-wh-1000xm5",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "OmniTech"
            }
        ],
        "specifications": {
            "Driver": "30mm Precision Driver",
            "Battery Life": "30 hours with ANC",
            "Noise Cancellation": "Dual Processor Auto NC Optimizer",
            "Connectivity": "Bluetooth 5.2 & 3.5mm Aux"
        }
    },
    {
        "id": "prod_elec_003",
        "group_id": "group_samsung_s24_ultra",
        "title": "Samsung Galaxy S24 Ultra 5G (12GB RAM, 256GB Storage) - Titanium Gray",
        "brand": "Samsung",
        "category": "Electronics",
        "sub_category": "Smartphones",
        "price": 119999,
        "original_price": 129999,
        "discount_pct": 8,
        "rating": 4.6,
        "rating_count": 2100,
        "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop&q=80",
        "description": "Welcome to the era of mobile AI. Galaxy AI arrives on S24 Ultra with Circle to Search, Live Translate, and 200MP Quad Tele camera.",
        "tags": ["smartphone", "samsung", "galaxy", "s24", "camera", "flagship", "android", "5g"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_s24_ultra",
                "price": 119999,
                "original_price": 129999,
                "url": "https://www.amazon.in/dp/B0CS5X6Y1L",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "STPL"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_s24_ultra",
                "price": 118999,
                "original_price": 129999,
                "url": "https://www.flipkart.com/samsung-galaxy-s24-ultra",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "FKSeller"
            }
        ],
        "specifications": {
            "Processor": "Snapdragon 8 Gen 3 for Galaxy",
            "Display": "6.8-inch Dynamic AMOLED 2X 120Hz",
            "Camera": "200MP + 50MP + 12MP + 10MP",
            "Battery": "5000 mAh"
        }
    },
    {
        "id": "prod_elec_004",
        "group_id": "group_boat_nirvana_ion",
        "title": "boAt Nirvana Ion ANC TWS Earbuds with 120H Playtime - Charcoal Black",
        "brand": "boAt",
        "category": "Electronics",
        "sub_category": "Audio",
        "price": 2299,
        "original_price": 7990,
        "discount_pct": 71,
        "rating": 4.3,
        "rating_count": 8940,
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80",
        "description": "Experience deep bass, up to 32dB Active Noise Cancellation, quad mics with ENx technology, and crystal clear call quality.",
        "tags": ["earbuds", "tws", "boat", "wireless", "audio", "budget", "anc", "music"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_boat_ion",
                "price": 2299,
                "original_price": 7990,
                "url": "https://www.amazon.in/dp/B0C39YMLP3",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "boAt Official Store"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_boat_ion",
                "price": 2399,
                "original_price": 7990,
                "url": "https://www.flipkart.com/boat-nirvana-ion",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "SuperNet"
            }
        ],
        "specifications": {
            "Playtime": "Up to 120 Hours total",
            "ANC": "32dB Active Noise Cancellation",
            "Latency": "60ms Beast Mode",
            "Water Resistance": "IPX4"
        }
    },
    {
        "id": "prod_elec_005",
        "group_id": "group_asus_rog_strix",
        "title": "ASUS ROG Strix G16 (2024) Gaming Laptop (16GB RAM, 1TB SSD, RTX 4060)",
        "brand": "ASUS",
        "category": "Electronics",
        "sub_category": "Laptops",
        "price": 114990,
        "original_price": 139900,
        "discount_pct": 18,
        "rating": 4.5,
        "rating_count": 640,
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&auto=format&fit=crop&q=80",
        "description": "Dominating gaming performance with Intel Core i7 13th Gen, NVIDIA GeForce RTX 4060, ROG Intelligent Cooling, and 165Hz FHD display.",
        "tags": ["gaming", "laptop", "asus", "rog", "rtx4060", "programming", "high-performance", "developer"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_asus_g16",
                "price": 114990,
                "original_price": 139900,
                "url": "https://www.amazon.in/dp/B0CSBG45G6",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Appario Retail"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_asus_g16",
                "price": 116500,
                "original_price": 139900,
                "url": "https://www.flipkart.com/asus-rog-strix-g16",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "OmniTech"
            }
        ],
        "specifications": {
            "Processor": "Intel Core i7-13650HX",
            "GPU": "NVIDIA GeForce RTX 4060 (8GB GDDR6)",
            "RAM": "16GB DDR5 4800MHz",
            "Storage": "1TB PCIe 4.0 NVMe SSD"
        }
    },
    {
        "id": "prod_elec_006",
        "group_id": "group_lenovo_ideapad_slim_3",
        "title": "Lenovo IdeaPad Slim 3 Intel Core i5 13th Gen (16GB RAM, 512GB SSD) - Arctic Grey",
        "brand": "Lenovo",
        "category": "Electronics",
        "sub_category": "Laptops",
        "price": 54990,
        "original_price": 68990,
        "discount_pct": 20,
        "rating": 4.4,
        "rating_count": 3120,
        "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80",
        "description": "Sleek and powerful laptop for college students and software engineers with FHD IPS Anti-glare display and Dolby Audio.",
        "tags": ["laptop", "lenovo", "programming", "college", "intel", "i5", "student", "workstation"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_lenovo_slim3",
                "price": 54990,
                "original_price": 68990,
                "url": "https://www.amazon.in/dp/B0D15K9LMP",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Lenovo India"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_lenovo_slim3",
                "price": 53990,
                "original_price": 68990,
                "url": "https://www.flipkart.com/lenovo-ideapad-slim-3",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "RetailNet"
            }
        ],
        "specifications": {
            "Processor": "Intel Core i5-13420H",
            "RAM": "16GB LPDDR5",
            "Storage": "512GB SSD",
            "Display": "15.6-inch FHD (1920x1080)"
        }
    },

    # Footwear & Sports
    {
        "id": "prod_foot_001",
        "group_id": "group_nike_pegasus_40",
        "title": "Nike Air Zoom Pegasus 40 Men's Running Shoes - White/Obsidian",
        "brand": "Nike",
        "category": "Footwear",
        "sub_category": "Running Shoes",
        "price": 8995,
        "original_price": 11895,
        "discount_pct": 24,
        "rating": 4.6,
        "rating_count": 1250,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80",
        "description": "A springy ride for every run, the Peg's familiar, just-for-you feel returns to help you accomplish your goals. React tech with dual Zoom Air units.",
        "tags": ["nike", "running", "shoes", "sneakers", "sports", "footwear", "pegasus", "jogging"],
        "store_offers": [
            {
                "store": "Myntra",
                "store_product_id": "myn_pegasus_40",
                "price": 8995,
                "original_price": 11895,
                "url": "https://www.myntra.com/sports-shoes/nike/nike-men-pegasus-40",
                "in_stock": True,
                "delivery_days": 3,
                "seller": "Nike India Official"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_pegasus_40",
                "price": 9299,
                "original_price": 11895,
                "url": "https://www.flipkart.com/nike-air-zoom-pegasus-40",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "RetailNet"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_pegasus_40",
                "price": 8990,
                "original_price": 11895,
                "url": "https://www.amazon.in/dp/B0C23F7GH",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Nike Authorized"
            }
        ],
        "specifications": {
            "Outer Material": "Engineered Mesh",
            "Sole Material": "Rubber with React Foam",
            "Closure": "Lace-Up",
            "Arch Type": "Neutral Support"
        }
    },
    {
        "id": "prod_foot_002",
        "group_id": "group_adidas_ultraboost_light",
        "title": "Adidas Ultraboost Light Running Shoes - Core Black / Solar Red",
        "brand": "Adidas",
        "category": "Footwear",
        "sub_category": "Running Shoes",
        "price": 10999,
        "original_price": 18999,
        "discount_pct": 42,
        "rating": 4.7,
        "rating_count": 940,
        "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop&q=80",
        "description": "Experience epic energy with the lightest Ultraboost ever. The Light BOOST midsole generates maximum propulsion on every stride.",
        "tags": ["adidas", "ultraboost", "running", "shoes", "sports", "footwear", "cushioned", "marathon"],
        "store_offers": [
            {
                "store": "Myntra",
                "store_product_id": "myn_ultraboost_light",
                "price": 10999,
                "original_price": 18999,
                "url": "https://www.myntra.com/sports-shoes/adidas/adidas-ultraboost-light",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Adidas India"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_ultraboost_light",
                "price": 11499,
                "original_price": 18999,
                "url": "https://www.amazon.in/dp/B0BXZ78K9M",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Appario Retail"
            }
        ],
        "specifications": {
            "Upper": "Primeknit+ Textile",
            "Midsole": "Light BOOST",
            "Outsole": "Continental Better Rubber"
        }
    },
    {
        "id": "prod_foot_003",
        "group_id": "group_puma_softride_pro",
        "title": "Puma Softride Enzo NXT Men's Running Shoes - Black & Gold",
        "brand": "Puma",
        "category": "Footwear",
        "sub_category": "Running Shoes",
        "price": 2799,
        "original_price": 5499,
        "discount_pct": 49,
        "rating": 4.2,
        "rating_count": 4820,
        "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=800&auto=format&fit=crop&q=80",
        "description": "Pairing Softride EVA technology for extreme cushioning and all-day comfort with a progressive upper design featuring bold Puma branding.",
        "tags": ["puma", "running", "shoes", "footwear", "budget", "sports", "sneakers", "gym"],
        "store_offers": [
            {
                "store": "Flipkart",
                "store_product_id": "fk_puma_enzo",
                "price": 2799,
                "original_price": 5499,
                "url": "https://www.flipkart.com/puma-softride-enzo-nxt",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "SuperComNet"
            },
            {
                "store": "Myntra",
                "store_product_id": "myn_puma_enzo",
                "price": 2899,
                "original_price": 5499,
                "url": "https://www.myntra.com/sports-shoes/puma/puma-softride-enzo",
                "in_stock": True,
                "delivery_days": 3,
                "seller": "Puma Sports"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_puma_enzo",
                "price": 2750,
                "original_price": 5499,
                "url": "https://www.amazon.in/dp/B08DF76LK",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Puma Official"
            }
        ],
        "specifications": {
            "Insole": "SoftFoam+ Comfort Sockliner",
            "Closure": "Lace-Up",
            "Weight": "285g"
        }
    },

    # Fashion & Apparel
    {
        "id": "prod_fash_001",
        "group_id": "group_levis_511_slim",
        "title": "Levi's Men 511 Slim Fit Mid-Rise Dark Wash Jeans",
        "brand": "Levi's",
        "category": "Fashion",
        "sub_category": "Men's Clothing",
        "price": 2399,
        "original_price": 3999,
        "discount_pct": 40,
        "rating": 4.4,
        "rating_count": 5120,
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80",
        "description": "A modern slim with room to move, the 511 Slim Fit Jeans are a classic since now. Woven with stretch for all-day motion.",
        "tags": ["jeans", "levis", "denim", "fashion", "slim fit", "men", "casual", "college outfits"],
        "store_offers": [
            {
                "store": "Myntra",
                "store_product_id": "myn_levis_511",
                "price": 2399,
                "original_price": 3999,
                "url": "https://www.myntra.com/jeans/levis/levis-511-slim-fit",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Levis Official"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_levis_511",
                "price": 2499,
                "original_price": 3999,
                "url": "https://www.amazon.in/dp/B08DFG78K",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Appario Retail"
            }
        ],
        "specifications": {
            "Material": "99% Cotton, 1% Elastane",
            "Fit": "Slim Fit",
            "Wash Care": "Machine Wash Cold"
        }
    },
    {
        "id": "prod_fash_002",
        "group_id": "group_hrx_cotton_oversized_tee",
        "title": "HRX by Hrithik Roshan Pure Cotton Oversized Streetwear T-Shirt - Sage Green",
        "brand": "HRX",
        "category": "Fashion",
        "sub_category": "Men's Clothing",
        "price": 699,
        "original_price": 1499,
        "discount_pct": 53,
        "rating": 4.3,
        "rating_count": 3100,
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80",
        "description": "Stay trendy in this relaxed-fit oversized t-shirt crafted from 220 GSM bio-washed heavy cotton fabric for supreme drape and comfort.",
        "tags": ["tshirt", "hrx", "oversized", "streetwear", "fashion", "college outfits", "budget", "men"],
        "store_offers": [
            {
                "store": "Myntra",
                "store_product_id": "myn_hrx_tee",
                "price": 699,
                "original_price": 1499,
                "url": "https://www.myntra.com/tshirts/hrx/hrx-oversized-tee",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Flashstar Commerce"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_hrx_tee",
                "price": 749,
                "original_price": 1499,
                "url": "https://www.flipkart.com/hrx-oversized-tshirt",
                "in_stock": True,
                "delivery_days": 3,
                "seller": "RetailNet"
            }
        ],
        "specifications": {
            "Fabric": "100% Bio-Washed Cotton (220 GSM)",
            "Neck": "Ribbed Crew Neck",
            "Fit": "Oversized Drop-Shoulder"
        }
    },
    {
        "id": "prod_fash_003",
        "group_id": "group_zara_linen_blend_shirt",
        "title": "ZARA Women Linen Blend Relaxed Shirt - Oat Beige",
        "brand": "ZARA",
        "category": "Fashion",
        "sub_category": "Women's Clothing",
        "price": 2990,
        "original_price": 3590,
        "discount_pct": 16,
        "rating": 4.5,
        "rating_count": 780,
        "image_url": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=800&auto=format&fit=crop&q=80",
        "description": "Relaxed lapel collar shirt made of spun linen blend fabric. Long cuffed sleeves, chest patch pocket, and front button closure.",
        "tags": ["zara", "women", "shirt", "linen", "fashion", "minimalist", "office", "summer", "college outfits"],
        "store_offers": [
            {
                "store": "Myntra",
                "store_product_id": "myn_zara_linen",
                "price": 2990,
                "original_price": 3590,
                "url": "https://www.myntra.com/shirts/zara/zara-linen-shirt",
                "in_stock": True,
                "delivery_days": 3,
                "seller": "ZARA India"
            }
        ],
        "specifications": {
            "Composition": "55% Linen, 45% Viscose",
            "Pattern": "Solid Neutral",
            "Sleeve": "Long Adjustable Cuffed"
        }
    },

    # Beauty & Skincare
    {
        "id": "prod_beauty_001",
        "group_id": "group_ordinary_niacinamide",
        "title": "The Ordinary Niacinamide 10% + Zinc 1% Oil Control Serum (30ml)",
        "brand": "The Ordinary",
        "category": "Beauty",
        "sub_category": "Skincare",
        "price": 600,
        "original_price": 700,
        "discount_pct": 14,
        "rating": 4.6,
        "rating_count": 12400,
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80",
        "description": "High-strength vitamin and mineral blemish formula that reduces the appearance of skin blemishes, congestion, and visible shine.",
        "tags": ["skincare", "serum", "niacinamide", "ordinary", "beauty", "oil-control", "acne", "best skincare"],
        "store_offers": [
            {
                "store": "Nykaa",
                "store_product_id": "nyk_ord_niacinamide",
                "price": 600,
                "original_price": 700,
                "url": "https://www.nykaa.com/the-ordinary-niacinamide-10percent-zinc-1percent/p/5003152",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Nykaa E-Retail"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_ord_niacinamide",
                "price": 650,
                "original_price": 700,
                "url": "https://www.amazon.in/dp/B01MDTVZUZ",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "BeautySpot"
            }
        ],
        "specifications": {
            "Volume": "30 ml",
            "Key Ingredients": "10% Niacinamide + 1% Zinc PCA",
            "Skin Type": "Oily, Combination, Blemish-Prone",
            "Formulation": "Lightweight Water-Based Serum"
        }
    },
    {
        "id": "prod_beauty_002",
        "group_id": "group_minimalist_salicylic_cleanser",
        "title": "Minimalist 2% Salicylic Acid Face Wash for Oil Control & Blackheads (100ml)",
        "brand": "Minimalist",
        "category": "Beauty",
        "sub_category": "Skincare",
        "price": 299,
        "original_price": 349,
        "discount_pct": 14,
        "rating": 4.5,
        "rating_count": 8900,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&auto=format&fit=crop&q=80",
        "description": "LHA & Salicylic acid facial cleanser formulated to unclog pores, eliminate excess sebum, and prevent acne breakouts without stripping moisture.",
        "tags": ["skincare", "cleanser", "facewash", "minimalist", "salicylic", "beauty", "budget", "best skincare"],
        "store_offers": [
            {
                "store": "Nykaa",
                "store_product_id": "nyk_min_facewash",
                "price": 299,
                "original_price": 349,
                "url": "https://www.nykaa.com/minimalist-2percent-salicylic-acid-face-wash/p/1243109",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Minimalist Official"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_min_facewash",
                "price": 299,
                "original_price": 349,
                "url": "https://www.amazon.in/dp/B08F9H7XZP",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Be Minimalist"
            }
        ],
        "specifications": {
            "Volume": "100 ml",
            "Active Ingredient": "2% Salicylic Acid (BHA) + Capryloyl Salicylic Acid",
            "pH Level": "4.5 - 5.0"
        }
    },
    {
        "id": "prod_beauty_003",
        "group_id": "group_maybelline_lash_sensational",
        "title": "Maybelline New York Lash Sensational Waterproof Mascara - Very Black",
        "brand": "Maybelline",
        "category": "Beauty",
        "sub_category": "Makeup",
        "price": 449,
        "original_price": 649,
        "discount_pct": 31,
        "rating": 4.4,
        "rating_count": 15400,
        "image_url": "https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=800&auto=format&fit=crop&q=80",
        "description": "Exclusive fanning brush with ten layers of bristles reveals layers of lashes for a sensational full-fan effect.",
        "tags": ["makeup", "mascara", "maybelline", "beauty", "eyes", "waterproof"],
        "store_offers": [
            {
                "store": "Nykaa",
                "store_product_id": "nyk_mayb_mascara",
                "price": 449,
                "original_price": 649,
                "url": "https://www.nykaa.com/maybelline-lash-sensational-waterproof-mascara",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Maybelline India"
            },
            {
                "store": "Myntra",
                "store_product_id": "myn_mayb_mascara",
                "price": 479,
                "original_price": 649,
                "url": "https://www.myntra.com/makeup/maybelline/mascara",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "BeautyStar"
            }
        ],
        "specifications": {
            "Finish": "Volumizing & Lengthening",
            "Shade": "Very Black",
            "Formulation": "Waterproof Liquid"
        }
    },
    {
        "id": "prod_beauty_004",
        "group_id": "group_mamaearth_vitamin_c_moisturizer",
        "title": "Mamaearth Vitamin C Daily Glow Face Cream with Vitamin C & Turmeric (80g)",
        "brand": "Mamaearth",
        "category": "Beauty",
        "sub_category": "Skincare",
        "price": 249,
        "original_price": 299,
        "discount_pct": 17,
        "rating": 4.3,
        "rating_count": 6700,
        "image_url": "https://images.unsplash.com/photo-1608248597349-f5195461ed13?w=800&auto=format&fit=crop&q=80",
        "description": "Deeply moisturizes and illuminates dull skin with natural antioxidant properties of Vitamin C and Turmeric.",
        "tags": ["skincare", "moisturizer", "mamaearth", "vitamin c", "beauty", "glow", "budget", "best skincare"],
        "store_offers": [
            {
                "store": "Nykaa",
                "store_product_id": "nyk_mamaearth_vitc",
                "price": 249,
                "original_price": 299,
                "url": "https://www.nykaa.com/mamaearth-vitamin-c-daily-glow-face-cream/p/823091",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Honasa Consumer"
            },
            {
                "store": "Amazon",
                "store_product_id": "amz_mamaearth_vitc",
                "price": 239,
                "original_price": 299,
                "url": "https://www.amazon.in/dp/B09V7D3XZM",
                "in_stock": True,
                "delivery_days": 1,
                "seller": "Mamaearth Store"
            }
        ],
        "specifications": {
            "Weight": "80 g",
            "Toxin Free": "MadeSafe Certified, Paraben & SLS Free",
            "Key Ingredients": "Vitamin C, Turmeric, Niacinamide"
        }
    },

    # Home & Living
    {
        "id": "prod_home_001",
        "group_id": "group_nespresso_vertuo_pop",
        "title": "Nespresso Vertuo Pop Espresso & Coffee Machine by De'Longhi - Spicy Red",
        "brand": "Nespresso",
        "category": "Home",
        "sub_category": "Kitchen Appliances",
        "price": 14999,
        "original_price": 19999,
        "discount_pct": 25,
        "rating": 4.6,
        "rating_count": 520,
        "image_url": "https://images.unsplash.com/photo-1517668808822-9e428824603b?w=800&auto=format&fit=crop&q=80",
        "description": "Compact and colorful Vertuo Pop machine brews 4 cup sizes from Espresso to Mug at the touch of a single button using Centrifusion technology.",
        "tags": ["coffee", "espresso", "nespresso", "home", "kitchen", "appliances", "gourmet"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_nespresso_pop",
                "price": 14999,
                "original_price": 19999,
                "url": "https://www.amazon.in/dp/B0BSM189QW",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Nespresso Authorized"
            }
        ],
        "specifications": {
            "Water Tank Capacity": "0.6 Liters",
            "Heat Up Time": "30 Seconds",
            "Technology": "Centrifusion Extraction"
        }
    },

    # Fitness & Outdoors
    {
        "id": "prod_fit_001",
        "group_id": "group_decathlon_tpe_yoga_mat",
        "title": "Decathlon Domyos 8mm Non-Slip TPE Alignment Yoga & Exercise Mat",
        "brand": "Decathlon",
        "category": "Fitness",
        "sub_category": "Yoga & Gym",
        "price": 1499,
        "original_price": 2499,
        "discount_pct": 40,
        "rating": 4.7,
        "rating_count": 2300,
        "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&auto=format&fit=crop&q=80",
        "description": "High-density Eco-TPE yoga mat with laser-engraved alignment guides for optimal posture, cushion, and superior grip during workout sessions.",
        "tags": ["yoga", "fitness", "decathlon", "mat", "workout", "gym", "budget", "exercise"],
        "store_offers": [
            {
                "store": "Amazon",
                "store_product_id": "amz_decathlon_mat",
                "price": 1499,
                "original_price": 2499,
                "url": "https://www.amazon.in/dp/B08K75GH8W",
                "in_stock": True,
                "delivery_days": 2,
                "seller": "Decathlon India"
            },
            {
                "store": "Flipkart",
                "store_product_id": "fk_decathlon_mat",
                "price": 1549,
                "original_price": 2499,
                "url": "https://www.flipkart.com/decathlon-yoga-mat",
                "in_stock": True,
                "delivery_days": 3,
                "seller": "Decathlon Sports"
            }
        ],
        "specifications": {
            "Thickness": "8 mm",
            "Material": "TPE Eco-Friendly Cushion",
            "Dimensions": "183cm x 61cm"
        }
    }
]

with open("/Users/princekumar/Downloads/Personal/OmniRec/seed_data.json", "w") as f:
    json.dump(products, f, indent=2)

print("Generated clean JSON seed_data.json successfully with", len(products), "products.")
