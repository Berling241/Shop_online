#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Darling Boutique E-commerce
Tests all backend APIs including Products, Cart, Orders, and Categories
"""

import requests
import json
import uuid
import time
from typing import Dict, Any, List

# Get backend URL from frontend .env
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("❌ Could not get backend URL from frontend/.env")
    exit(1)

API_BASE = f"{BASE_URL}/api"
print(f"🔗 Testing backend at: {API_BASE}")

class BackendTester:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.test_results = []
        self.sample_product_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def test_api_health(self):
        """Test if API is running"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Message: {data.get('message', 'No message')}"
            self.log_test("API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("API Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_categories_api(self):
        """Test Categories API"""
        try:
            response = requests.get(f"{API_BASE}/categories", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                categories = data.get('categories', [])
                bijoux_found = any(cat['id'] == 'bijoux' for cat in categories)
                tech_found = any(cat['id'] == 'tech' for cat in categories)
                
                if bijoux_found and tech_found:
                    details = f"Found {len(categories)} categories (bijoux, tech)"
                else:
                    success = False
                    details = "Missing expected categories (bijoux/tech)"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_test("Categories API", success, details)
            return success
        except Exception as e:
            self.log_test("Categories API", False, f"Error: {str(e)}")
            return False
    
    def test_products_api(self):
        """Test Products API - GET all products"""
        try:
            response = requests.get(f"{API_BASE}/products", timeout=10)
            success = response.status_code == 200
            
            if success:
                products = response.json()
                if isinstance(products, list) and len(products) > 0:
                    # Store first product ID for later tests
                    self.sample_product_id = products[0]['id']
                    details = f"Retrieved {len(products)} products"
                    
                    # Check if sample products are initialized
                    bijoux_count = sum(1 for p in products if p['category'] == 'bijoux')
                    tech_count = sum(1 for p in products if p['category'] == 'tech')
                    details += f" (bijoux: {bijoux_count}, tech: {tech_count})"
                else:
                    success = False
                    details = "No products found or invalid response format"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_test("Products API - Get All", success, details)
            return success
        except Exception as e:
            self.log_test("Products API - Get All", False, f"Error: {str(e)}")
            return False
    
    def test_products_filtering(self):
        """Test Products API filtering"""
        tests = [
            ("category=bijoux", "bijoux category filter"),
            ("category=tech", "tech category filter"),
            ("search=collier", "search functionality"),
            ("sort_by=price-asc", "price ascending sort"),
            ("sort_by=price-desc", "price descending sort"),
            ("sort_by=rating", "rating sort")
        ]
        
        all_passed = True
        for query, test_name in tests:
            try:
                response = requests.get(f"{API_BASE}/products?{query}", timeout=10)
                success = response.status_code == 200
                
                if success:
                    products = response.json()
                    details = f"Retrieved {len(products)} products with {test_name}"
                else:
                    details = f"Status: {response.status_code}"
                    all_passed = False
                    
                self.log_test(f"Products Filter - {test_name}", success, details)
            except Exception as e:
                self.log_test(f"Products Filter - {test_name}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_product_by_id(self):
        """Test getting specific product by ID"""
        if not self.sample_product_id:
            self.log_test("Product by ID", False, "No sample product ID available")
            return False
            
        try:
            response = requests.get(f"{API_BASE}/products/{self.sample_product_id}", timeout=10)
            success = response.status_code == 200
            
            if success:
                product = response.json()
                details = f"Retrieved product: {product.get('name', 'Unknown')}"
            else:
                details = f"Status: {response.status_code}"
                
            self.log_test("Product by ID", success, details)
            return success
        except Exception as e:
            self.log_test("Product by ID", False, f"Error: {str(e)}")
            return False
    
    def test_cart_operations(self):
        """Test complete cart operations cycle"""
        if not self.sample_product_id:
            self.log_test("Cart Operations", False, "No sample product ID available")
            return False
        
        all_passed = True
        
        # 1. Get empty cart
        try:
            response = requests.get(f"{API_BASE}/cart/{self.session_id}", timeout=10)
            success = response.status_code == 200
            if success:
                cart = response.json()
                details = f"Empty cart total: {cart.get('total', 0)}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Cart - Get Empty", success, details)
        except Exception as e:
            self.log_test("Cart - Get Empty", False, f"Error: {str(e)}")
            all_passed = False
        
        # 2. Add item to cart
        try:
            add_data = {
                "product_id": self.sample_product_id,
                "quantity": 2
            }
            response = requests.post(
                f"{API_BASE}/cart/{self.session_id}/add",
                json=add_data,
                timeout=10
            )
            success = response.status_code == 200
            if success:
                result = response.json()
                cart = result.get('cart', {})
                details = f"Added item, cart total: {cart.get('total', 0)}, items: {len(cart.get('items', []))}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Cart - Add Item", success, details)
        except Exception as e:
            self.log_test("Cart - Add Item", False, f"Error: {str(e)}")
            all_passed = False
        
        # 3. Update item quantity
        try:
            update_data = {"quantity": 3}
            response = requests.put(
                f"{API_BASE}/cart/{self.session_id}/update/{self.sample_product_id}",
                json=update_data,
                timeout=10
            )
            success = response.status_code == 200
            if success:
                result = response.json()
                cart = result.get('cart', {})
                details = f"Updated quantity, cart total: {cart.get('total', 0)}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Cart - Update Item", success, details)
        except Exception as e:
            self.log_test("Cart - Update Item", False, f"Error: {str(e)}")
            all_passed = False
        
        # 4. Get cart with items
        try:
            response = requests.get(f"{API_BASE}/cart/{self.session_id}", timeout=10)
            success = response.status_code == 200
            if success:
                cart = response.json()
                details = f"Cart with items - total: {cart.get('total', 0)}, items: {len(cart.get('items', []))}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Cart - Get With Items", success, details)
        except Exception as e:
            self.log_test("Cart - Get With Items", False, f"Error: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def test_order_creation(self):
        """Test order creation with mobile payment simulation"""
        if not self.sample_product_id:
            self.log_test("Order Creation", False, "No sample product ID available")
            return False
        
        # First get product details for order
        try:
            response = requests.get(f"{API_BASE}/products/{self.sample_product_id}", timeout=10)
            if response.status_code != 200:
                self.log_test("Order Creation", False, "Could not get product details")
                return False
            
            product = response.json()
            
            # Create order data
            order_data = {
                "items": [
                    {
                        "product_id": self.sample_product_id,
                        "product_name": product['name'],
                        "product_price": product['price'],
                        "product_image": product['image'],
                        "quantity": 1,
                        "subtotal": product['price']
                    }
                ],
                "payment_method": "moov",
                "phone_number": "01234567",  # Valid Moov number format
                "session_id": self.session_id
            }
            
            response = requests.post(f"{API_BASE}/orders", json=order_data, timeout=15)
            success = response.status_code == 200
            
            if success:
                order = response.json()
                details = f"Order created: {order.get('order_number', 'Unknown')}, Status: {order.get('status', 'Unknown')}"
                # Store order ID for later tests
                self.order_id = order.get('id')
            else:
                details = f"Status: {response.status_code}"
                if response.status_code == 400:
                    try:
                        error_detail = response.json().get('detail', 'Unknown error')
                        details += f", Error: {error_detail}"
                    except:
                        pass
                        
            self.log_test("Order Creation", success, details)
            return success
        except Exception as e:
            self.log_test("Order Creation", False, f"Error: {str(e)}")
            return False
    
    def test_order_retrieval(self):
        """Test order retrieval by ID and filtering"""
        if not hasattr(self, 'order_id') or not self.order_id:
            self.log_test("Order Retrieval", False, "No order ID available")
            return False
        
        all_passed = True
        
        # Test get order by ID
        try:
            response = requests.get(f"{API_BASE}/orders/{self.order_id}", timeout=10)
            success = response.status_code == 200
            if success:
                order = response.json()
                details = f"Retrieved order: {order.get('order_number', 'Unknown')}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Order - Get by ID", success, details)
        except Exception as e:
            self.log_test("Order - Get by ID", False, f"Error: {str(e)}")
            all_passed = False
        
        # Test get orders by session_id
        try:
            response = requests.get(f"{API_BASE}/orders?session_id={self.session_id}", timeout=10)
            success = response.status_code == 200
            if success:
                orders = response.json()
                details = f"Retrieved {len(orders)} orders for session"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Order - Get by Session", success, details)
        except Exception as e:
            self.log_test("Order - Get by Session", False, f"Error: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def test_payment_validation(self):
        """Test payment method validation"""
        test_cases = [
            ("moov", "01234567", True, "Valid Moov number"),
            ("moov", "07234567", False, "Invalid Moov number (should start with 01/02/05)"),
            ("airtel", "07234567", True, "Valid Airtel number"),
            ("airtel", "01234567", False, "Invalid Airtel number (should start with 07/09)"),
        ]
        
        all_passed = True
        
        for payment_method, phone, should_succeed, description in test_cases:
            try:
                if not self.sample_product_id:
                    continue
                    
                # Get product for order
                response = requests.get(f"{API_BASE}/products/{self.sample_product_id}", timeout=10)
                if response.status_code != 200:
                    continue
                    
                product = response.json()
                
                order_data = {
                    "items": [
                        {
                            "product_id": self.sample_product_id,
                            "product_name": product['name'],
                            "product_price": product['price'],
                            "product_image": product['image'],
                            "quantity": 1,
                            "subtotal": product['price']
                        }
                    ],
                    "payment_method": payment_method,
                    "phone_number": phone,
                    "session_id": str(uuid.uuid4())  # Use unique session for each test
                }
                
                response = requests.post(f"{API_BASE}/orders", json=order_data, timeout=15)
                
                if should_succeed:
                    success = response.status_code == 200
                    details = f"{description} - Expected success, got {response.status_code}"
                else:
                    success = response.status_code == 400
                    details = f"{description} - Expected validation error, got {response.status_code}"
                
                if not success:
                    all_passed = False
                    
                self.log_test(f"Payment Validation - {description}", success, details)
                
            except Exception as e:
                self.log_test(f"Payment Validation - {description}", False, f"Error: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_cart_cleanup(self):
        """Test cart removal and clearing operations"""
        if not self.sample_product_id:
            self.log_test("Cart Cleanup", False, "No sample product ID available")
            return False
        
        all_passed = True
        cleanup_session = str(uuid.uuid4())
        
        # Add item first
        try:
            add_data = {"product_id": self.sample_product_id, "quantity": 1}
            response = requests.post(f"{API_BASE}/cart/{cleanup_session}/add", json=add_data, timeout=10)
            if response.status_code != 200:
                self.log_test("Cart Cleanup Setup", False, "Could not add item for cleanup test")
                return False
        except Exception as e:
            self.log_test("Cart Cleanup Setup", False, f"Error: {str(e)}")
            return False
        
        # Test remove specific item
        try:
            response = requests.delete(f"{API_BASE}/cart/{cleanup_session}/remove/{self.sample_product_id}", timeout=10)
            success = response.status_code == 200
            if success:
                result = response.json()
                cart = result.get('cart', {})
                details = f"Item removed, cart items: {len(cart.get('items', []))}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Cart - Remove Item", success, details)
        except Exception as e:
            self.log_test("Cart - Remove Item", False, f"Error: {str(e)}")
            all_passed = False
        
        # Add item again for clear test
        try:
            add_data = {"product_id": self.sample_product_id, "quantity": 1}
            requests.post(f"{API_BASE}/cart/{cleanup_session}/add", json=add_data, timeout=10)
        except:
            pass
        
        # Test clear cart
        try:
            response = requests.delete(f"{API_BASE}/cart/{cleanup_session}/clear", timeout=10)
            success = response.status_code == 200
            if success:
                result = response.json()
                cart = result.get('cart', {})
                details = f"Cart cleared, items: {len(cart.get('items', []))}, total: {cart.get('total', 0)}"
            else:
                details = f"Status: {response.status_code}"
                all_passed = False
            self.log_test("Cart - Clear All", success, details)
        except Exception as e:
            self.log_test("Cart - Clear All", False, f"Error: {str(e)}")
            all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting Darling Boutique Backend API Tests")
        print("=" * 60)
        
        # Test sequence
        tests = [
            ("API Health", self.test_api_health),
            ("Categories API", self.test_categories_api),
            ("Products API", self.test_products_api),
            ("Products Filtering", self.test_products_filtering),
            ("Product by ID", self.test_product_by_id),
            ("Cart Operations", self.test_cart_operations),
            ("Order Creation", self.test_order_creation),
            ("Order Retrieval", self.test_order_retrieval),
            ("Payment Validation", self.test_payment_validation),
            ("Cart Cleanup", self.test_cart_cleanup),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running {test_name} tests...")
            if test_func():
                passed += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
            if result["details"] and not result["success"]:
                print(f"   └─ {result['details']}")
        
        print(f"\n🎯 Overall Result: {passed}/{total} test groups passed")
        
        if passed == total:
            print("🎉 All backend API tests PASSED!")
            return True
        else:
            print(f"⚠️  {total - passed} test group(s) FAILED")
            return False

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)