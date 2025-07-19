from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Data storage
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Sample credit card data
credit_cards = [
    {
        "id": "1",
        "name": "Flipkart Axis Bank Credit Card",
        "issuer": "Axis Bank",
        "category": "cashback",
        "joining_fee": "First Year Free - LIMITED TIME ONLY",
        "rewards_rate": "5% Cashback on Flipkart & Cleartrip, 4% Cashback on Preferred Partners",
        "benefits": [
            "5% cashback on Flipkart",
            "4% cashback on preferred partners",
            "No annual fee first year"
        ],
        "image": "flipkart-axis-card",
        "apply_link": "https://swipekarbhai.com/apply/flipkart-axis",
        "is_lifetime_free": False,
        "is_popular": True
    },
    {
        "id": "2",
        "name": "HDFC Bank Millennia Credit Card",
        "issuer": "HDFC Bank",
        "category": "cashback",
        "joining_fee": "₹1,000 + GST",
        "rewards_rate": "5% Cashback Up to 1,000 CashPoints at Top Ten Online Merchants",
        "benefits": [
            "5% cashback on online shopping",
            "1% cashback on other spends",
            "Airport lounge access"
        ],
        "image": "hdfc-millennia-card",
        "apply_link": "https://swipekarbhai.com/apply/hdfc-millennia",
        "is_lifetime_free": False,
        "is_popular": True
    },
    {
        "id": "3",
        "name": "SBI SimplyCLICK Credit Card",
        "issuer": "SBI Card",
        "category": "rewards",
        "joining_fee": "₹499 + GST",
        "rewards_rate": "10X Reward Points on Partner Brands",
        "benefits": [
            "10X reward points on partner brands",
            "1 reward point per ₹100 spent",
            "Annual fee waiver on spending ₹1 lakh"
        ],
        "image": "sbi-simplyclick-card",
        "apply_link": "https://swipekarbhai.com/apply/sbi-simplyclick",
        "is_lifetime_free": False,
        "is_popular": True
    },
    {
        "id": "4",
        "name": "IDFC FIRST Classic Credit Card",
        "issuer": "IDFC First Bank",
        "category": "rewards",
        "joining_fee": "Lifetime Free",
        "rewards_rate": "3X Reward Points on every spend of ₹150",
        "benefits": [
            "Lifetime free card",
            "3X reward points on all spends",
            "No joining fee"
        ],
        "image": "idfc-classic-card",
        "apply_link": "https://swipekarbhai.com/apply/idfc-classic",
        "is_lifetime_free": True,
        "is_popular": True
    },
    {
        "id": "5",
        "name": "AU Bank LIT Credit Card",
        "issuer": "AU Bank",
        "category": "rewards",
        "joining_fee": "Nil",
        "rewards_rate": "1 Reward Point/₹100 Spent",
        "benefits": [
            "No joining fee",
            "10X accelerated reward points",
            "Customizable benefits"
        ],
        "image": "au-lit-card",
        "apply_link": "https://swipekarbhai.com/apply/au-lit",
        "is_lifetime_free": True,
        "is_popular": True
    },
    {
        "id": "6",
        "name": "EazyDiner IndusInd Platinum Credit Card",
        "issuer": "IndusInd Bank",
        "category": "dining",
        "joining_fee": "Nil",
        "rewards_rate": "2 Reward Points/Rs. 100 Spent",
        "benefits": [
            "No joining fee",
            "2X EazyPoints on dining",
            "Complimentary EazyDiner Prime membership"
        ],
        "image": "eazydiner-indusind-card",
        "apply_link": "https://swipekarbhai.com/apply/eazydiner-indusind",
        "is_lifetime_free": True,
        "is_popular": True
    }
]

# News articles
news_articles = [
    {
        "id": "1",
        "title": "Kotak Mahindra Unveils Cashback+ and Air+ Credit Cards for Shoppers and Travelers",
        "date": "2025-07-19",
        "summary": "Kotak Mahindra Bank has launched new credit cards targeting shoppers and travelers with enhanced cashback and travel benefits.",
        "image": "kotak-new-cards",
        "category": "news",
        "read_time": "3 min read"
    },
    {
        "id": "2",
        "title": "AU Bank, Yes Bank, and IndusInd Join Air India Maharaja Club as New Points Transfer Partners",
        "date": "2025-07-18",
        "summary": "Three major banks have joined Air India's loyalty program, allowing cardholders to transfer points to Maharaja Club.",
        "image": "air-india-partnership",
        "category": "news",
        "read_time": "4 min read"
    },
    {
        "id": "3",
        "title": "Extra 10% Off on Samsung Devices with Axis Bank Credit Cards",
        "date": "2025-07-17",
        "summary": "Axis Bank cardholders can now enjoy additional discounts on Samsung devices across all major platforms.",
        "image": "samsung-axis-offer",
        "category": "offers",
        "read_time": "2 min read"
    }
]

# Guide articles
guide_articles = [
    {
        "id": "1",
        "title": "Exploring RuPay JCB Credit Cards – Features & Benefits",
        "date": "2025-07-17",
        "summary": "Complete guide to RuPay JCB credit cards, their features, benefits, and how they compare to other networks.",
        "category": "guides",
        "read_time": "5 min read"
    },
    {
        "id": "2",
        "title": "SBI SimplySAVE Vs Axis My Zone – Which Entry-Level Card is Better?",
        "date": "2025-07-15",
        "summary": "Detailed comparison between two popular entry-level credit cards for first-time users.",
        "category": "comparisons",
        "read_time": "6 min read"
    },
    {
        "id": "3",
        "title": "Cashback SBI Vs Amazon Pay ICICI Credit Card – The Ultimate Showdown",
        "date": "2025-07-13",
        "summary": "Comprehensive comparison between two of the most popular cashback credit cards in India.",
        "category": "comparisons",
        "read_time": "7 min read"
    }
]

# Partners data
partners = [
    {"name": "HDFC", "logo": "hdfc-logo", "link": "/partners/hdfc"},
    {"name": "AXIS Bank", "logo": "axis-logo", "link": "/partners/axis"},
    {"name": "ICICI", "logo": "icici-logo", "link": "/partners/icici"},
    {"name": "AMEX", "logo": "amex-logo", "link": "/partners/amex"},
    {"name": "SBI", "logo": "sbi-logo", "link": "/partners/sbi"},
    {"name": "IDFC", "logo": "idfc-logo", "link": "/partners/idfc"},
    {"name": "IndusIND", "logo": "indusind-logo", "link": "/partners/indusind"},
    {"name": "AU Bank", "logo": "au-logo", "link": "/partners/au"},
    {"name": "BoB Card", "logo": "bob-logo", "link": "/partners/bob"},
    {"name": "Standard Chartered", "logo": "sc-logo", "link": "/partners/sc"},
    {"name": "HSBC", "logo": "hsbc-logo", "link": "/partners/hsbc"},
    {"name": "Yes Bank", "logo": "yes-logo", "link": "/partners/yes"}
]

# API Routes

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to swipekarbhai API",
        "version": "1.0.0",
        "endpoints": {
            "cards": "/api/cards",
            "news": "/api/news",
            "guides": "/api/guides",
            "partners": "/api/partners"
        }
    })

@app.route('/api/cards')
def get_cards():
    """Get all credit cards with optional filtering"""
    category = request.args.get('category')
    is_lifetime_free = request.args.get('is_lifetime_free')
    is_popular = request.args.get('is_popular')
    
    filtered_cards = credit_cards
    
    if category:
        filtered_cards = [card for card in filtered_cards if card['category'] == category]
    
    if is_lifetime_free:
        filtered_cards = [card for card in filtered_cards if card['is_lifetime_free'] == (is_lifetime_free.lower() == 'true')]
    
    if is_popular:
        filtered_cards = [card for card in filtered_cards if card['is_popular'] == (is_popular.lower() == 'true')]
    
    return jsonify({
        "cards": filtered_cards,
        "total": len(filtered_cards)
    })

@app.route('/api/cards/<card_id>')
def get_card(card_id):
    """Get a specific credit card by ID"""
    card = next((card for card in credit_cards if card['id'] == card_id), None)
    if card:
        return jsonify(card)
    return jsonify({"error": "Card not found"}), 404

@app.route('/api/cards/search')
def search_cards():
    """Search credit cards by name or issuer"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({"cards": [], "total": 0})
    
    results = [card for card in credit_cards 
               if query in card['name'].lower() or query in card['issuer'].lower()]
    
    return jsonify({
        "cards": results,
        "total": len(results),
        "query": query
    })

@app.route('/api/news')
def get_news():
    """Get news articles with optional filtering"""
    category = request.args.get('category')
    limit = int(request.args.get('limit', 10))
    
    filtered_news = news_articles
    
    if category:
        filtered_news = [article for article in filtered_news if article['category'] == category]
    
    return jsonify({
        "news": filtered_news[:limit],
        "total": len(filtered_news)
    })

@app.route('/api/news/<article_id>')
def get_news_article(article_id):
    """Get a specific news article by ID"""
    article = next((article for article in news_articles if article['id'] == article_id), None)
    if article:
        return jsonify(article)
    return jsonify({"error": "Article not found"}), 404

@app.route('/api/guides')
def get_guides():
    """Get guide articles with optional filtering"""
    category = request.args.get('category')
    limit = int(request.args.get('limit', 10))
    
    filtered_guides = guide_articles
    
    if category:
        filtered_guides = [guide for guide in filtered_guides if guide['category'] == category]
    
    return jsonify({
        "guides": filtered_guides[:limit],
        "total": len(filtered_guides)
    })

@app.route('/api/guides/<guide_id>')
def get_guide(guide_id):
    """Get a specific guide by ID"""
    guide = next((guide for guide in guide_articles if guide['id'] == guide_id), None)
    if guide:
        return jsonify(guide)
    return jsonify({"error": "Guide not found"}), 404

@app.route('/api/partners')
def get_partners():
    """Get all partner banks"""
    return jsonify({
        "partners": partners,
        "total": len(partners)
    })

@app.route('/api/categories')
def get_categories():
    """Get all credit card categories"""
    categories = list(set(card['category'] for card in credit_cards))
    return jsonify({
        "categories": categories
    })

@app.route('/api/apply', methods=['POST'])
def apply_card():
    """Handle credit card application"""
    data = request.json
    
    # Validate required fields
    required_fields = ['card_id', 'name', 'email', 'phone']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Generate application ID
    application_id = str(uuid.uuid4())
    
    # Save application data
    application = {
        "id": application_id,
        "card_id": data['card_id'],
        "name": data['name'],
        "email": data['email'],
        "phone": data['phone'],
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # In a real application, this would save to a database
    # For now, we'll just return success
    return jsonify({
        "message": "Application submitted successfully",
        "application_id": application_id,
        "status": "pending"
    })

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    data = request.json
    
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # In a real application, this would send an email or save to database
    return jsonify({
        "message": "Thank you for contacting us. We'll get back to you soon!"
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
