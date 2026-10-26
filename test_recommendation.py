import pytest
from fastapi.testclient import TestClient
from main import app
from nlp_query_parser import NLPQueryParser

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert "catalog_size" in data

def test_nlp_query_parser():
    parsed = NLPQueryParser.parse_query("Find running shoes under ₹3,000")
    assert parsed["category"] == "Footwear"
    assert parsed["max_price"] == 3000.0
    assert "running" in parsed["keywords"] or "shoes" in parsed["keywords"]

def test_nlp_query_parser_k_notation():
    parsed = NLPQueryParser.parse_query("laptop for programming under 70k")
    assert parsed["category"] == "Electronics"
    assert parsed["max_price"] == 70000.0
    assert "programming" in parsed["intent_tags"]

def test_user_recommendations():
    payload = {
        "user_id": "test_user_123",
        "user_profile": {
            "user_id": "test_user_123",
            "preferred_categories": ["Electronics", "Footwear"],
            "preferred_brands": ["Apple", "Nike"],
            "min_budget": 1000.0,
            "max_budget": 50000.0,
            "viewed_product_ids": [],
            "wishlisted_product_ids": [],
            "search_queries": ["running shoes"]
        },
        "limit": 5
    }
    response = client.post("/api/v1/recommendations/user", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert len(data["recommendations"]) <= 5
    if len(data["recommendations"]) > 0:
        first = data["recommendations"][0]
        assert "product_id" in first
        assert "score" in first
        assert "reason" in first
