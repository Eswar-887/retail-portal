from datetime import datetime
from sqlalchemy import (Column, Integer, String, Numeric, Boolean,
                        DateTime, ForeignKey, Text)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="customer")
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    logo_url = Column(String(500))
    description = Column(Text)
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    image_url = Column(String(500))
    cost = Column(Numeric(10, 2), nullable=False)
    tax_percent = Column(Numeric(5, 2), nullable=False, default=0)
    stock_quantity = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("Category", back_populates="products")


class StockHistory(Base):
    __tablename__ = "stock_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    old_qty = Column(Integer, nullable=False)
    new_qty = Column(Integer, nullable=False)
    change = Column(Integer, nullable=False)
    reason = Column(String(200))
    changed_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_total = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="placed")
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    tax_percent = Column(Numeric(5, 2), nullable=False)
    order = relationship("Order", back_populates="items")