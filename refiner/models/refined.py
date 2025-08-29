from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base model for SQLAlchemy
Base = declarative_base()

# Zomato specific models
class ZomatoAccount(Base):
    __tablename__ = 'zomato_accounts'
    
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String, nullable=False)  # "ZOMATO"
    witnesses = Column(String, nullable=False)
    account_username = Column(String, nullable=False)
    user_id = Column(String, nullable=False)  # Zomato user ID
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    orders = relationship("ZomatoOrder", back_populates="account")

class ZomatoOrder(Base):
    __tablename__ = 'zomato_orders'
    
    order_id = Column(String, primary_key=True)
    account_id = Column(Integer, ForeignKey('zomato_accounts.account_id'), nullable=False)
    total_cost = Column(String, nullable=False)
    dish_string = Column(Text, nullable=False)
    restaurant_url = Column(String, nullable=False)
    delivery_address = Column(Text, nullable=False)
    delivery_status = Column(String, nullable=False)
    delivery_message = Column(String, nullable=True)
    delivery_label = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    account = relationship("ZomatoAccount", back_populates="orders")
