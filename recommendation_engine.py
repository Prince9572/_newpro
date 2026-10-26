import json
import os
from typing import List, Dict, Any, Optional
import numpy as np
from feature_engineering import FeatureExtractor

class RecommendationEngine:
    def __init__(self, seed_data_path: str = "../seed_data.json"):
        self.seed_data_path = seed_data_path
        self.products: List[Dict[str, Any]] = []
        self.product_map: Dict[str, Dict[str, Any]] = {}
        self.feature_extractor = FeatureExtractor()
        self.load_data()

    def load_data(self):
        # Try relative or absolute path
        paths_to_try = [
            self.seed_data_path,
            os.path.join(os.path.dirname(__file__), "..", "seed_data.json"),
            "/Users/princekumar/Downloads/Personal/OmniRec/seed_data.json"
        ]
        loaded = False
        for path in paths_to_try:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        self.products = json.load(f)
                    loaded = True
                    break
                except Exception as e:
                    print(f"Error loading seed file from {path}: {e}")
        if not loaded:
            print("Warning: Could not load seed_data.json. Engine running with empty catalog.")

        self.product_map = {p["id"]: p for p in self.products}
        if self.products:
            self.feature_extractor.fit_products(self.products)

    def set_products(self, products: List[Dict[str, Any]]):
        self.products = products
        self.product_map = {p["id"]: p for p in self.products}
        self.feature_extractor.fit_products(self.products)

    def recommend_for_user(
        self,
        user_id: str,
        user_profile: Dict[str, Any],
        limit: int = 10,
        exclude_product_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        if not self.products:
            return []

        exclude_set = set(exclude_product_ids or [])
        
        # User profile parameters
        preferred_categories = user_profile.get("preferred_categories", [])
        preferred_brands = user_profile.get("preferred_brands", [])
        min_budget = user_profile.get("min_budget", 0)
        max_budget = user_profile.get("max_budget", 200000)
        viewed_product_ids = user_profile.get("viewed_product_ids", [])
        wishlisted_product_ids = user_profile.get("wishlisted_product_ids", [])
        search_queries = user_profile.get("search_queries", [])
        
        # 1. Cold start check
        is_cold_start = len(viewed_product_ids) == 0 and len(wishlisted_product_ids) == 0

        # Construct synthetic user interest query text
        interest_tokens = []
        interest_tokens.extend(preferred_categories)
        interest_tokens.extend(preferred_brands)
        interest_tokens.extend(search_queries)
        
        for v_id in viewed_product_ids:
            if v_id in self.product_map:
                p = self.product_map[v_id]
                interest_tokens.append(p.get("title", ""))
                interest_tokens.extend(p.get("tags", []))
                
        for w_id in wishlisted_product_ids:
            if w_id in self.product_map:
                p = self.product_map[w_id]
                interest_tokens.append(p.get("title", ""))
                interest_tokens.extend(p.get("tags", []))
                
        user_text_query = " ".join(interest_tokens)
        content_sims = self.feature_extractor.transform_query(user_text_query) if user_text_query.strip() else np.zeros(len(self.products))

        scored_results = []

        for idx, product in enumerate(self.products):
            pid = product["id"]
            if pid in exclude_set:
                continue

            price = product.get("price", 0)
            category = product.get("category", "")
            brand = product.get("brand", "")
            discount = product.get("discount_pct", 0)
            rating = product.get("rating", 4.0)

            # Base score from Content Similarity
            content_score = float(content_sims[idx]) if len(content_sims) > idx else 0.0
            
            # Category affinity boost
            cat_boost = 0.35 if category in preferred_categories else 0.0
            
            # Brand affinity boost
            brand_boost = 0.25 if brand in preferred_brands else 0.0
            
            # Price sensitivity score (1.0 inside budget, decaying outside)
            if price <= 0:
                price_score = 0.5
            elif min_budget <= price <= max_budget:
                price_score = 1.0
            elif price < min_budget:
                price_score = max(0.2, price / min_budget)
            else:
                price_score = max(0.1, max_budget / price)
                
            # Rating & discount factor
            rating_factor = (rating / 5.0) * 0.15
            discount_factor = min(discount / 100.0, 0.5) * 0.15

            # Hybrid Score calculation
            if is_cold_start:
                final_score = (cat_boost * 0.40) + (brand_boost * 0.30) + (price_score * 0.20) + rating_factor
            else:
                final_score = (content_score * 0.40) + (cat_boost * 0.20) + (brand_boost * 0.15) + (price_score * 0.15) + rating_factor + discount_factor

            # Generate natural language human-readable explanation
            reason = self._generate_explanation(
                product, user_profile, content_score, cat_boost, brand_boost, price_score, is_cold_start
            )

            scored_results.append({
                "product_id": pid,
                "score": round(float(final_score), 4),
                "reason": reason,
                "matched_preferences": [
                    item for item in [
                        category if cat_boost > 0 else None,
                        brand if brand_boost > 0 else None,
                        f"Under ₹{max_budget:,.0f}" if price_score == 1.0 and max_budget < 200000 else None
                    ] if item is not None
                ],
                "confidence": "HIGH" if final_score > 0.4 else "MEDIUM" if final_score > 0.2 else "FAIR"
            })

        # Sort descending by score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:limit]

    def recommend_similar_products(self, product_id: str, limit: int = 6) -> List[Dict[str, Any]]:
        sims = self.feature_extractor.get_product_similarity(product_id)
        if len(sims) == 0:
            return []

        scored_results = []
        target_product = self.product_map.get(product_id, {})
        
        for idx, product in enumerate(self.products):
            pid = product["id"]
            if pid == product_id:
                continue
                
            sim_score = float(sims[idx])
            reason = f"Similar features and category to {target_product.get('title', 'this item')}"
            
            scored_results.append({
                "product_id": pid,
                "score": round(sim_score, 4),
                "reason": reason,
                "matched_preferences": [product.get("category"), product.get("brand")],
                "confidence": "HIGH" if sim_score > 0.3 else "MEDIUM"
            })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:limit]

    def _generate_explanation(
        self, product: Dict[str, Any], profile: Dict[str, Any], content_score: float, cat_boost: float, brand_boost: float, price_score: float, is_cold_start: bool
    ) -> str:
        title = product.get("title", "Product")
        brand = product.get("brand", "")
        category = product.get("category", "")
        price = product.get("price", 0)
        max_b = profile.get("max_budget", 200000)

        wishlisted = profile.get("wishlisted_product_ids", [])
        if wishlisted:
            for w_id in wishlisted:
                if w_id in self.product_map:
                    w_item = self.product_map[w_id]
                    if w_item.get("category") == category or w_item.get("brand") == brand:
                        return f"You may like this because it is similar to products you saved on {w_item.get('store_offers', [{}])[0].get('store', 'OmniRec')}"

        if cat_boost > 0 and price_score == 1.0 and max_b < 200000:
            return f"Recommended because you frequently view {category.lower()} and usually shop below ₹{max_b:,.0f}"
        if brand_boost > 0:
            return f"Top pick for you based on your preference for {brand}"
        if cat_boost > 0:
            return f"Matches your active interest in {category}"
        if is_cold_start and price <= max_b:
            return f"Top rated choice in {category} within your budget range"

        return f"Popular choice with high user ratings in {category}"
