#!/usr/bin/env python3
"""
Test script for swipekarbhai API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5001"

def test_endpoint(endpoint, description):
    """Test a specific API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"\n✅ {description}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'cards' in data:
                print(f"   Items: {len(data['cards'])}")
            elif 'news' in data:
                print(f"   Items: {len(data['news'])}")
            elif 'guides' in data:
                print(f"   Items: {len(data['guides'])}")
            elif 'partners' in data:
                print(f"   Items: {len(data['partners'])}")
            else:
                print(f"   Response: {data}")
        return True
    except Exception as e:
        print(f"\n❌ {description}")
        print(f"   Error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🧪 Testing swipekarbhai API Endpoints")
    print("=" * 50)
    
    tests = [
        ("/", "Root endpoint"),
        ("/api/cards", "Get all credit cards"),
        ("/api/cards?category=cashback", "Get cashback cards"),
        ("/api/cards?is_lifetime_free=true", "Get lifetime free cards"),
        ("/api/cards/search?q=hdfc", "Search HDFC cards"),
        ("/api/news", "Get news articles"),
        ("/api/guides", "Get guide articles"),
        ("/api/partners", "Get partner banks"),
        ("/api/categories", "Get card categories"),
    ]
    
    passed = 0
    total = len(tests)
    
    for endpoint, description in tests:
        if test_endpoint(endpoint, description):
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
