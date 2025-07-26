from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

# Import models
from models.product import Product, ProductCreate, ProductUpdate
from models.cart import Cart, CartItem, CartItemAdd, CartItemUpdate
from models.order import Order, OrderCreate, OrderStatusUpdate, PaymentMethod, OrderStatus
from models.user import User, UserCreate, UserUpdate
from services.payment_service import PaymentService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Darling Boutique API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Initialize sample data flag
sample_data_initialized = False

async def initialize_sample_data():
    """Initialize sample products if database is empty"""
    global sample_data_initialized
    if sample_data_initialized:
        return
    
    # Check if products already exist
    existing_products = await db.products.count_documents({})
    if existing_products > 0:
        sample_data_initialized = True
        return
    
    # Sample products data
    sample_products = [
        {
            "name": "Collier Élégant Doré",
            "price": 25000,
            "category": "bijoux",
            "subcategory": "colliers",
            "image": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxqZXdlbHJ5fGVufDB8fHx8MTc1MzU2NTYyMHww&ixlib=rb-4.1.0&q=85",
            "description": "Magnifique collier doré pour toutes occasions",
            "inStock": True,
            "rating": 4.8,
            "reviews": 23
        },
        {
            "name": "Bagues Dorées Set de 3",
            "price": 15000,
            "category": "bijoux",
            "subcategory": "bagues",
            "image": "https://images.unsplash.com/photo-1543294001-f7cd5d7fb516?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHw0fHxqZXdlbHJ5fGVufDB8fHx8MTc1MzU2NTYyMHww&ixlib=rb-4.1.0&q=85",
            "description": "Ensemble de 3 bagues dorées élégantes",
            "inStock": True,
            "rating": 4.5,
            "reviews": 18
        },
        {
            "name": "Bracelet Argent Délicat",
            "price": 18000,
            "category": "bijoux",
            "subcategory": "bracelets",
            "image": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxqZXdlbHJ5fGVufDB8fHx8MTc1MzU2NTYyMHww&ixlib=rb-4.1.0&q=85",
            "description": "Bracelet en argent avec finition délicate",
            "inStock": True,
            "rating": 4.7,
            "reviews": 31
        },
        {
            "name": "AirPods Pro Sans Fil",
            "price": 85000,
            "category": "tech",
            "subcategory": "ecouteurs",
            "image": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwzfHx3aXJlbGVzcyUyMGVhcmJ1ZHN8ZW58MHx8fHwxNzUzNTY1NjI2fDA&ixlib=rb-4.1.0&q=85",
            "description": "Écouteurs sans fil de haute qualité avec réduction de bruit",
            "inStock": True,
            "rating": 4.9,
            "reviews": 156
        },
        {
            "name": "Casque Bluetooth Premium",
            "price": 75000,
            "category": "tech",
            "subcategory": "casques",
            "image": "https://images.unsplash.com/photo-1628329567705-f8f7150c3cff?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxibHVldG9vdGglMjBoZWFkcGhvbmVzfGVufDB8fHx8MTc1MzU2NTYzMHww&ixlib=rb-4.1.0&q=85",
            "description": "Casque audio bluetooth avec son haute fidélité",
            "inStock": True,
            "rating": 4.6,
            "reviews": 89
        },
        {
            "name": "Écouteurs Colorés Set",
            "price": 35000,
            "category": "tech",
            "subcategory": "ecouteurs",
            "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHw0fHx3aXJlbGVzcyUyMGVhcmJ1ZHN8ZW58MHx8fHwxNzUzNTY1NjI2fDA&ixlib=rb-4.1.0&q=85",
            "description": "Collection d'écouteurs sans fil colorés",
            "inStock": True,
            "rating": 4.3,
            "reviews": 67
        },
        {
            "name": "Ventilateur Miniature USB",
            "price": 12000,
            "category": "tech",
            "subcategory": "ventilateurs",
            "image": "https://images.unsplash.com/photo-1628329567705-f8f7150c3cff?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxibHVldG9vdGglMjBoZWFkcGhvbmVzfGVufDB8fHx8MTc1MzU2NTYzMHww&ixlib=rb-4.1.0&q=85",
            "description": "Ventilateur portable miniature avec câble USB",
            "inStock": True,
            "rating": 4.1,
            "reviews": 42
        }
    ]
    
    # Insert sample products
    for product_data in sample_products:
        product = Product(**product_data)
        await db.products.insert_one(product.dict())
    
    sample_data_initialized = True
    logging.info("Sample products initialized")

# Dependency to get session_id from headers or generate one
async def get_session_id(session_id: Optional[str] = None) -> str:
    if not session_id:
        return str(uuid.uuid4())
    return session_id

# Product routes
@api_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "name"
):
    """Get all products with optional filtering and sorting"""
    await initialize_sample_data()
    
    # Build filter query
    filter_query = {}
    if category:
        filter_query["category"] = category
    if subcategory:
        filter_query["subcategory"] = subcategory
    if search:
        filter_query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Build sort query
    sort_query = []
    if sort_by == "price-asc":
        sort_query = [("price", 1)]
    elif sort_by == "price-desc":
        sort_query = [("price", -1)]
    elif sort_by == "rating":
        sort_query = [("rating", -1)]
    else:  # name
        sort_query = [("name", 1)]
    
    products = await db.products.find(filter_query).sort(sort_query).to_list(1000)
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

# Cart routes
@api_router.get("/cart/{session_id}", response_model=Cart)
async def get_cart(session_id: str):
    """Get cart for a session"""
    cart = await db.carts.find_one({"session_id": session_id})
    if not cart:
        # Create empty cart
        new_cart = Cart(session_id=session_id, items=[], total=0.0)
        await db.carts.insert_one(new_cart.dict())
        return new_cart
    return Cart(**cart)

@api_router.post("/cart/{session_id}/add")
async def add_to_cart(session_id: str, item: CartItemAdd):
    """Add item to cart"""
    # Get product details
    product = await db.products.find_one({"id": item.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get or create cart
    cart = await db.carts.find_one({"session_id": session_id})
    if not cart:
        cart = Cart(session_id=session_id, items=[], total=0.0).dict()
    else:
        cart = Cart(**cart).dict()
    
    # Check if item already exists in cart
    existing_item = None
    for i, cart_item in enumerate(cart["items"]):
        if cart_item["product_id"] == item.product_id:
            existing_item = i
            break
    
    if existing_item is not None:
        # Update quantity
        cart["items"][existing_item]["quantity"] += item.quantity
        cart["items"][existing_item]["subtotal"] = cart["items"][existing_item]["quantity"] * cart["items"][existing_item]["product_price"]
    else:
        # Add new item
        cart_item = CartItem(
            product_id=item.product_id,
            product_name=product["name"],
            product_price=product["price"],
            product_image=product["image"],
            quantity=item.quantity,
            subtotal=product["price"] * item.quantity
        )
        cart["items"].append(cart_item.dict())
    
    # Recalculate total
    cart["total"] = sum(item["subtotal"] for item in cart["items"])
    cart["updated_at"] = datetime.utcnow()
    
    # Update in database
    await db.carts.replace_one(
        {"session_id": session_id},
        cart,
        upsert=True
    )
    
    return {"message": "Item added to cart", "cart": Cart(**cart)}

@api_router.put("/cart/{session_id}/update/{product_id}")
async def update_cart_item(session_id: str, product_id: str, update: CartItemUpdate):
    """Update item quantity in cart"""
    cart = await db.carts.find_one({"session_id": session_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = Cart(**cart).dict()
    
    # Find and update item
    item_found = False
    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] = update.quantity
            item["subtotal"] = item["product_price"] * update.quantity
            item_found = True
            break
    
    if not item_found:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    # Recalculate total
    cart["total"] = sum(item["subtotal"] for item in cart["items"])
    cart["updated_at"] = datetime.utcnow()
    
    # Update in database
    await db.carts.replace_one({"session_id": session_id}, cart)
    
    return {"message": "Cart updated", "cart": Cart(**cart)}

@api_router.delete("/cart/{session_id}/remove/{product_id}")
async def remove_from_cart(session_id: str, product_id: str):
    """Remove item from cart"""
    cart = await db.carts.find_one({"session_id": session_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = Cart(**cart).dict()
    
    # Remove item
    cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]
    
    # Recalculate total
    cart["total"] = sum(item["subtotal"] for item in cart["items"])
    cart["updated_at"] = datetime.utcnow()
    
    # Update in database
    await db.carts.replace_one({"session_id": session_id}, cart)
    
    return {"message": "Item removed from cart", "cart": Cart(**cart)}

@api_router.delete("/cart/{session_id}/clear")
async def clear_cart(session_id: str):
    """Clear all items from cart"""
    empty_cart = Cart(session_id=session_id, items=[], total=0.0)
    await db.carts.replace_one(
        {"session_id": session_id},
        empty_cart.dict(),
        upsert=True
    )
    return {"message": "Cart cleared", "cart": empty_cart}

# Order routes
@api_router.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    """Create a new order"""
    # Validate payment method and phone number
    if not PaymentService.validate_phone_number(order_data.phone_number, order_data.payment_method):
        raise HTTPException(
            status_code=400, 
            detail=f"Numéro de téléphone invalide pour {order_data.payment_method}"
        )
    
    # Calculate total
    total = sum(item.subtotal for item in order_data.items)
    
    # Create order
    order = Order(
        items=order_data.items,
        total=total,
        payment_method=order_data.payment_method,
        phone_number=order_data.phone_number,
        user_id=order_data.user_id,
        session_id=order_data.session_id,
        status=OrderStatus.PENDING
    )
    
    # Save order
    await db.orders.insert_one(order.dict())
    
    # Process payment
    try:
        payment_result = await PaymentService.process_mobile_payment(
            phone_number=order_data.phone_number,
            amount=total,
            payment_method=order_data.payment_method,
            order_number=order.order_number
        )
        
        if payment_result["success"]:
            # Update order status
            order.status = OrderStatus.CONFIRMED
            await db.orders.replace_one({"id": order.id}, order.dict())
            
            # Clear cart if session_id provided
            if order_data.session_id:
                await db.carts.delete_one({"session_id": order_data.session_id})
            
            return order
        else:
            # Payment failed, update order status
            order.status = OrderStatus.CANCELLED
            await db.orders.replace_one({"id": order.id}, order.dict())
            
            raise HTTPException(
                status_code=400,
                detail=f"Échec du paiement: {payment_result['error']}"
            )
    
    except Exception as e:
        # Update order status to cancelled
        order.status = OrderStatus.CANCELLED
        await db.orders.replace_one({"id": order.id}, order.dict())
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get a specific order"""
    order = await db.orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**order)

@api_router.get("/orders", response_model=List[Order])
async def get_orders(session_id: Optional[str] = None, user_id: Optional[str] = None):
    """Get orders for a session or user"""
    filter_query = {}
    if session_id:
        filter_query["session_id"] = session_id
    if user_id:
        filter_query["user_id"] = user_id
    
    orders = await db.orders.find(filter_query).sort([("created_at", -1)]).to_list(1000)
    return [Order(**order) for order in orders]

# Categories route
@api_router.get("/categories")
async def get_categories():
    """Get product categories"""
    return {
        "categories": [
            {
                "id": "bijoux",
                "name": "Bijoux",
                "subcategories": [
                    {"id": "colliers", "name": "Colliers"},
                    {"id": "bracelets", "name": "Bracelets"},
                    {"id": "bagues", "name": "Bagues"}
                ]
            },
            {
                "id": "tech",
                "name": "Tech",
                "subcategories": [
                    {"id": "ecouteurs", "name": "Écouteurs Sans Fil"},
                    {"id": "casques", "name": "Casques Bluetooth"},
                    {"id": "ventilateurs", "name": "Ventilateurs Miniatures"}
                ]
            }
        ]
    }

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Darling Boutique API is running!"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
