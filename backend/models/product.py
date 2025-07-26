from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price: float
    category: str  # 'bijoux' or 'tech'
    subcategory: str  # 'colliers', 'bracelets', 'bagues', 'ecouteurs', 'casques', 'ventilateurs'
    image: str
    description: str
    inStock: bool = True
    rating: float = Field(default=4.0, ge=0, le=5)
    reviews: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    name: str
    price: float
    category: str
    subcategory: str
    image: str
    description: str
    inStock: bool = True
    rating: Optional[float] = 4.0
    reviews: Optional[int] = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    inStock: Optional[bool] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None