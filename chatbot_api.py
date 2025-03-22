from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import random

app = Flask(__name__)
CORS(app)

# System prompt
SYSTEM_PROMPT = """
You are an e-commerce chatbot for EShop, an Indian online store. Answer shopping-related queries using the provided product inventory in INR (converted from USD at 1 USD = 84 INR). Provide concise, relevant answers based on user input. Maintain context from previous messages. If unclear, make a best guess or ask for clarification.
"""

# Static exchange rate
USD_TO_INR = 84

# Product inventory (converted from your TypeScript data)
PRODUCTS = [
    {"id": "1", "name": "Premium Wireless Headphones", "price": 199.99 * USD_TO_INR, "description": "High-quality wireless headphones with noise cancellation", "category": "Electronics", "discount": 10},
    {"id": "2", "name": "Smart Watch Pro", "price": 299.99 * USD_TO_INR, "description": "Advanced smartwatch with health monitoring features", "category": "Electronics", "discount": 0},
    {"id": "3", "name": "Leather Laptop Bag", "price": 79.99 * USD_TO_INR, "description": "Stylish and durable leather laptop bag", "category": "Accessories", "discount": 15},
    {"id": "4", "name": "Wireless Mouse", "price": 49.99 * USD_TO_INR, "description": "Ergonomic wireless mouse for comfortable use", "category": "Electronics", "discount": 0},
    {"id": "5", "name": "Mechanical Keyboard", "price": 129.99 * USD_TO_INR, "description": "RGB mechanical keyboard with customizable switches", "category": "Electronics", "discount": 20},
    {"id": "6", "name": "4K Ultra HD Smart TV", "price": 799.99 * USD_TO_INR, "description": "Experience stunning picture quality with this 4K Ultra HD Smart TV.", "category": "Electronics", "discount": 5},
    {"id": "7", "name": "Bluetooth Speaker", "price": 89.99 * USD_TO_INR, "description": "Portable Bluetooth speaker with rich sound quality.", "category": "Electronics", "discount": 0},
    {"id": "8", "name": "Gaming Monitor", "price": 349.99 * USD_TO_INR, "description": "High refresh rate gaming monitor for an immersive experience.", "category": "Electronics", "discount": 0},
    {"id": "9", "name": "Smartphone X", "price": 999.99 * USD_TO_INR, "description": "Latest smartphone with cutting-edge features.", "category": "Electronics", "discount": 0},
    {"id": "10", "name": "Laptop Pro 15", "price": 1299.99 * USD_TO_INR, "description": "High-performance laptop for professionals.", "category": "Electronics", "discount": 0},
    {"id": "11", "name": "Tablet 10", "price": 499.99 * USD_TO_INR, "description": "Versatile tablet for work and play.", "category": "Electronics", "discount": 0},
    {"id": "12", "name": "Action Camera", "price": 299.99 * USD_TO_INR, "description": "Capture your adventures with this action camera.", "category": "Electronics", "discount": 0},
    {"id": "13", "name": "Wireless Earbuds", "price": 149.99 * USD_TO_INR, "description": "Compact wireless earbuds with great sound quality.", "category": "Electronics", "discount": 0},
    {"id": "14", "name": "Smart Home Hub", "price": 199.99 * USD_TO_INR, "description": "Control your smart home devices with this hub.", "category": "Electronics", "discount": 0},
    {"id": "15", "name": "Portable Charger", "price": 39.99 * USD_TO_INR, "description": "Keep your devices charged on the go.", "category": "Electronics", "discount": 0},
    {"id": "16", "name": "Smart Thermostat", "price": 129.99 * USD_TO_INR, "description": "Optimize your home’s heating and cooling.", "category": "Electronics", "discount": 0},
    {"id": "17", "name": "VR Headset", "price": 399.99 * USD_TO_INR, "description": "Immerse yourself in virtual reality.", "category": "Electronics", "discount": 0},
    {"id": "18", "name": "Digital Camera", "price": 599.99 * USD_TO_INR, "description": "Capture stunning photos with this digital camera.", "category": "Electronics", "discount": 0},
    {"id": "19", "name": "Smart Light Bulbs", "price": 29.99 * USD_TO_INR, "description": "Control your lighting with smart bulbs.", "category": "Electronics", "discount": 0},
    {"id": "20", "name": "Fitness Tracker", "price": 59.99 * USD_TO_INR, "description": "Monitor your fitness activities with this tracker.", "category": "Electronics", "discount": 0},
    {"id": "21", "name": "Smart Refrigerator", "price": 1999.99 * USD_TO_INR, "description": "Keep your food fresh with this smart refrigerator.", "category": "Electronics", "discount": 0},
    {"id": "22", "name": "Electric Kettle", "price": 49.99 * USD_TO_INR, "description": "Boil water quickly with this electric kettle.", "category": "Electronics", "discount": 0},
    {"id": "23", "name": "Smartwatch Series 5", "price": 399.99 * USD_TO_INR, "description": "Stay connected with this stylish smartwatch.", "category": "Electronics", "discount": 0},
    {"id": "24", "name": "Wireless Charging Pad", "price": 29.99 * USD_TO_INR, "description": "Charge your devices wirelessly with this pad.", "category": "Electronics", "discount": 0},
    {"id": "25", "name": "Home Security Camera", "price": 149.99 * USD_TO_INR, "description": "Keep an eye on your home with this security camera.", "category": "Electronics", "discount": 0},
    {"id": "26", "name": "Smart Door Lock", "price": 199.99 * USD_TO_INR, "description": "Secure your home with this smart door lock.", "category": "Electronics", "discount": 0},
    {"id": "27", "name": "Portable Projector", "price": 299.99 * USD_TO_INR, "description": "Enjoy movies anywhere with this portable projector.", "category": "Electronics", "discount": 0},
    {"id": "28", "name": "Smart Scale", "price": 49.99 * USD_TO_INR, "description": "Track your weight with this smart scale.", "category": "Electronics", "discount": 0},
    {"id": "29", "name": "Noise Cancelling Headphones", "price": 299.99 * USD_TO_INR, "description": "Block out distractions with these headphones.", "category": "Electronics", "discount": 0},
    {"id": "30", "name": "Smart Air Purifier", "price": 199.99 * USD_TO_INR, "description": "Breathe clean air with this smart air purifier.", "category": "Electronics", "discount": 0},
    {"id": "31", "name": "Electric Toothbrush", "price": 79.99 * USD_TO_INR, "description": "Achieve a better clean with this electric toothbrush.", "category": "Electronics", "discount": 0},
    {"id": "32", "name": "Smart Coffee Maker", "price": 149.99 * USD_TO_INR, "description": "Brew coffee from your phone with this smart coffee maker.", "category": "Electronics", "discount": 0},
    {"id": "33", "name": "Smart Vacuum Cleaner", "price": 299.99 * USD_TO_INR, "description": "Keep your home clean with this smart vacuum cleaner.", "category": "Electronics", "discount": 0},
    {"id": "34", "name": "Smart Pet Feeder", "price": 129.99 * USD_TO_INR, "description": "Feed your pets on schedule with this smart feeder.", "category": "Electronics", "discount": 0},
    {"id": "35", "name": "Smart Garden System", "price": 199.99 * USD_TO_INR, "description": "Grow plants easily with this smart garden system.", "category": "Electronics", "discount": 0},
    {"id": "36", "name": "Smart Mirror", "price": 299.99 * USD_TO_INR, "description": "Get ready with this smart mirror that displays information.", "category": "Electronics", "discount": 0},
    {"id": "37", "name": "Smart Wi-Fi Router", "price": 99.99 * USD_TO_INR, "description": "Enhance your internet connection with this smart router.", "category": "Electronics", "discount": 0},
    {"id": "38", "name": "Smartphone Gimbal", "price": 149.99 * USD_TO_INR, "description": "Stabilize your smartphone videos with this gimbal.", "category": "Electronics", "discount": 0},
    {"id": "39", "name": "Smartphone Tripod", "price": 39.99 * USD_TO_INR, "description": "Capture steady shots with this smartphone tripod.", "category": "Electronics", "discount": 0},
    {"id": "40", "name": "Smartphone Lens Kit", "price": 49.99 * USD_TO_INR, "description": "Enhance your smartphone photography with this lens kit.", "category": "Electronics", "discount": 0},
    {"id": "41", "name": "Smartphone Car Mount", "price": 29.99 * USD_TO_INR, "description": "Secure your smartphone in your car with this mount.", "category": "Electronics", "discount": 0},
    {"id": "42", "name": "Smartphone Screen Protector", "price": 19.99 * USD_TO_INR, "description": "Protect your smartphone screen with this protector.", "category": "Electronics", "discount": 0},
    {"id": "43", "name": "Smartphone Battery Case", "price": 49.99 * USD_TO_INR, "description": "Extend your smartphone battery life with this case.", "category": "Electronics", "discount": 0},
    {"id": "44", "name": "Smartphone Wallet Case", "price": 39.99 * USD_TO_INR, "description": "Keep your cards and phone together with this wallet case.", "category": "Electronics", "discount": 0},
    {"id": "45", "name": "Smartphone Cleaning Kit", "price": 19.99 * USD_TO_INR, "description": "Keep your smartphone clean with this cleaning kit.", "category": "Electronics", "discount": 0},
    {"id": "46", "name": "Smartphone Car Charger", "price": 29.99 * USD_TO_INR, "description": "Charge your smartphone in the car with this charger.", "category": "Electronics", "discount": 0},
    {"id": "47", "name": "Smartphone USB-C Hub", "price": 39.99 * USD_TO_INR, "description": "Expand your smartphone connectivity with this hub.", "category": "Electronics", "discount": 0},
    {"id": "48", "name": "Smartphone HDMI Adapter", "price": 29.99 * USD_TO_INR, "description": "Connect your smartphone to a TV with this adapter.", "category": "Electronics", "discount": 0},
    {"id": "49", "name": "Smartphone Bluetooth Adapter", "price": 19.99 * USD_TO_INR, "description": "Add Bluetooth capability to your smartphone with this adapter.", "category": "Electronics", "discount": 0},
    {"id": "50", "name": "Smartphone VR Headset", "price": 99.99 * USD_TO_INR, "description": "Experience virtual reality with this smartphone VR headset.", "category": "Electronics", "discount": 0},
]

# Shipping options
SHIPPING_OPTIONS = {
    "standard": {"cost": "Free over ₹5000, else ₹99", "time": "3-5 business days"},
    "express": {"cost": "₹199", "time": "1-2 business days"}
}

# Intent keywords
INTENT_KEYWORDS = {
    "buy": ["buy", "order", "purchase", "get", "want", "add"],
    "price": ["price", "cost", "how much", "rate"],
    "details": ["details", "specs", "specification", "features", "info", "describe"],
    "stock": ["stock", "available", "availability", "in stock"],
    "shipping": ["shipping", "delivery", "ship", "transport"],
    "cart": ["cart", "basket", "add to cart", "checkout", "bag"]
}

# Simulated cart
cart = []

# Store conversation history and context
conversation_history = []
last_product = None

def extract_usd_amount(message):
    match = re.search(r'\$(\d+)', message)
    if match:
        return int(match.group(1))
    return None

def find_product(message):
    message_lower = message.lower()
    for product in PRODUCTS:
        if product["name"].lower() in message_lower or any(word in message_lower for word in product["name"].lower().split()):
            return product
    return None

def get_discounted_price(product):
    if product["discount"] > 0:
        discounted_price = product["price"] * (1 - product["discount"] / 100)
        return discounted_price
    return product["price"]

def match_intent(message, intent):
    return any(keyword in message.lower() for keyword in INTENT_KEYWORDS[intent])

def get_ai_response(message):
    global conversation_history, last_product, cart
    
    if not conversation_history:
        conversation_history.append(SYSTEM_PROMPT)
    
    conversation_history.append(f"User: {message}")
    message_lower = message.lower()
    usd_amount = extract_usd_amount(message)
    product = find_product(message)
    
    # Greeting
    if "hi" in message_lower or "hello" in message_lower:
        return "Hi there! Welcome to EShop. How can I help you with your shopping today?"
    
    # Buy/Order intent
    if match_intent(message, "buy"):
        if product:
            last_product = product
            cart.append(last_product)
            price = get_discounted_price(product)
            discount_text = f" (after {product['discount']}% discount)" if product["discount"] > 0 else ""
            return f"At EShop, the {product['name']} costs ₹{price:,.2f}{discount_text}. Added to your cart. Want more details?"
        elif last_product and ("yes" in message_lower or "confirm" in message_lower):
            price = get_discounted_price(last_product)
            discount_text = f" (after {last_product['discount']}% discount)" if last_product["discount"] > 0 else ""
            return f"Got it! The {last_product['name']} (₹{price:,.2f}{discount_text}) is in your cart. Anything else to add?"
        else:
            return "What would you like to order from EShop today? We have items like 'Smartphone X', 'Laptop Pro 15', and more."
    
    # Price intent
    if match_intent(message, "price") and not match_intent(message, "shipping"):
        if product:
            last_product = product
            price = get_discounted_price(product)
            discount_text = f" (after {product['discount']}% discount)" if product["discount"] > 0 else ""
            return f"At EShop, the {product['name']} costs ₹{price:,.2f}{discount_text}. Want more details?"
        elif last_product:
            price = get_discounted_price(last_product)
            discount_text = f" (after {last_product['discount']}% discount)" if last_product["discount"] > 0 else ""
            return f"At EShop, the {last_product['name']} costs ₹{price:,.2f}{discount_text}. Want more details?"
        else:
            return "Which product’s price are you looking for? Try 'Smartphone X' or '4K Ultra HD Smart TV'."
    
    # Details intent
    if match_intent(message, "details") or ("yes" in message_lower and last_product and any(kw in " ".join(conversation_history[-2:]).lower() for kw in INTENT_KEYWORDS["buy"] + INTENT_KEYWORDS["price"])):
        if product:
            last_product = product
            return f"At EShop, the {product['name']} is: {product['description']} Anything else you’d like to know?"
        elif last_product:
            return f"At EShop, the {last_product['name']} is: {last_product['description']} Anything else you’d like to know?"
        else:
            return "Which product do you want details for? We have 'Mechanical Keyboard', 'Smart Watch Pro', etc."
    
    # Cart intent
    if match_intent(message, "cart"):
        if cart:
            cart_summary = ", ".join(f"{item['name']} (₹{get_discounted_price(item):,.2f})" for item in cart)
            total = sum(get_discounted_price(item) for item in cart)
            return f"Your EShop cart contains: {cart_summary}. Total: ₹{total:,.2f}. Ready to checkout?"
        else:
            return "Your cart is empty. What would you like to add? Check out 'Wireless Mouse' or 'Bluetooth Speaker'."
    
    # Shipping intent
    if match_intent(message, "shipping") or ("cost" in message_lower and "ship" in " ".join(conversation_history[-2:]).lower()):
        if "express" in message_lower:
            return f"Express shipping at EShop costs {SHIPPING_OPTIONS['express']['cost']} and takes {SHIPPING_OPTIONS['express']['time']}."
        elif "standard" in message_lower:
            return f"Standard shipping at EShop is {SHIPPING_OPTIONS['standard']['cost']} and takes {SHIPPING_OPTIONS['standard']['time']}."
        else:
            return f"At EShop, we offer Standard shipping ({SHIPPING_OPTIONS['standard']['cost']}, {SHIPPING_OPTIONS['standard']['time']}) and Express shipping ({SHIPPING_OPTIONS['express']['cost']}, {SHIPPING_OPTIONS['express']['time']}). Which one do you want to know about?"
    
    # USD conversion
    if usd_amount:
        inr_amount = usd_amount * USD_TO_INR
        return f"That’s around ₹{inr_amount:,.2f} in Indian Rupees. What item are we talking about?"
    
    # Fallback with intent guess
    if last_product:
        price = get_discounted_price(last_product)
        return f"Did you mean something about the {last_product['name']} (₹{price:,.2f})? I can help with price, details, shipping, or adding it to your cart."
    return "I’m not sure what you mean. Could you tell me more? You can ask about products like 'Smartphone X' or '4K Ultra HD Smart TV'."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    response = get_ai_response(message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(port=5000)