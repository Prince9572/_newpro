import re
from typing import Dict, Any, List, Optional

CATEGORY_KEYWORDS = {
    "Electronics": ["laptop", "laptops", "phone", "smartphone", "earbuds", "headphones", "audio", "macbook", "m3", "tws", "gadgets"],
    "Footwear": ["shoe", "shoes", "sneakers", "running", "footwear", "boots", "jogging"],
    "Fashion": ["shirt", "tshirt", "t-shirt", "jeans", "denim", "dress", "outfit", "outfits", "clothing", "apparel", "wear"],
    "Beauty": ["skincare", "serum", "facewash", "moisturizer", "mascara", "makeup", "beauty", "cream", "cleanser"],
    "Home": ["coffee", "espresso", "appliances", "kitchen", "home"],
    "Fitness": ["yoga", "mat", "gym", "fitness", "workout", "sports"]
}

BRAND_KEYWORDS = ["apple", "sony", "samsung", "boat", "asus", "lenovo", "nike", "adidas", "puma", "levi's", "levis", "hrx", "zara", "the ordinary", "minimalist", "maybelline", "mamaearth", "nespresso", "decathlon"]

class NLPQueryParser:
    @staticmethod
    def parse_query(query: str) -> Dict[str, Any]:
        normalized = query.lower().strip()
        
        # 1. Price extraction (e.g. "under ₹3,000", "below 5000", "under 70k", "less than 1500")
        max_price = None
        min_price = None
        
        # Match 'k' or '000' notation
        k_match = re.search(r'(under|below|less than|<|budget|max|within)\s*(₹|rs\.?|inr)?\s*(\d+(\.\d+)?)\s*k\b', normalized)
        if k_match:
            max_price = float(k_match.group(3)) * 1000
        else:
            number_match = re.search(r'(under|below|less than|<|budget|max|within)\s*(₹|rs\.?|inr)?\s*([\d,]+)', normalized)
            if number_match:
                val_str = number_match.group(3).replace(',', '')
                max_price = float(val_str)
                
        # If no explicit "under" keyword, but regex matches prices like ₹3000
        if max_price is None:
            price_match = re.search(r'(₹|rs\.?|inr)\s*([\d,]+)', normalized)
            if price_match:
                max_price = float(price_match.group(2).replace(',', ''))

        # 2. Category matching
        detected_category = None
        for cat, keywords in CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in normalized:
                    detected_category = cat
                    break
            if detected_category:
                break
                
        # 3. Brand matching
        detected_brand = None
        for brand in BRAND_KEYWORDS:
            if brand in normalized:
                detected_brand = brand.title()
                break
                
        # 4. Extract intent tags
        intent_tags = []
        if "programming" in normalized or "developer" in normalized or "coding" in normalized:
            intent_tags.append("programming")
        if "college" in normalized or "student" in normalized:
            intent_tags.append("college")
        if "running" in normalized or "sports" in normalized:
            intent_tags.append("running")
        if "skincare" in normalized:
            intent_tags.append("skincare")
        if "best" in normalized or "top" in normalized:
            intent_tags.append("top-rated")
            
        confidence = 0.85 if (detected_category or max_price or detected_brand) else 0.60

        return {
            "original_query": query,
            "category": detected_category,
            "brand": detected_brand,
            "max_price": max_price,
            "min_price": min_price,
            "intent_tags": intent_tags,
            "keywords": [w for w in re.split(r'\W+', normalized) if len(w) > 2 and w not in ["under", "show", "find", "best", "need", "for"]],
            "confidence": confidence
        }
