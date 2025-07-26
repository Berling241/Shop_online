from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

class PaymentMethod(str, Enum):
    MOOV_MONEY = "moov"
    AIRTEL_MONEY = "airtel"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    product_price: float
    product_image: str
    quantity: int = Field(ge=1)
    subtotal: float

class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_number: str = Field(default_factory=lambda: f"DRB{str(uuid.uuid4())[:8].upper()}")
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    items: List[OrderItem]
    total: float
    payment_method: PaymentMethod
    phone_number: str
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OrderCreate(BaseModel):
    items: List[OrderItem]
    payment_method: PaymentMethod
    phone_number: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus