from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class CartItem(BaseModel):
    product_id: str
    product_name: str
    product_price: float
    product_image: str
    quantity: int = Field(ge=1)
    subtotal: float

class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None  # Pour les utilisateurs connectés
    session_id: Optional[str] = None  # Pour les utilisateurs anonymes
    items: List[CartItem] = []
    total: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)