from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric

# Assuming your database.py defines 'Base' correctly
from .database import Base 

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    
    starting_price = Column(Numeric(10, 2), nullable=False) 
    current_highest_bid = Column(Numeric(10, 2), default=0.0)
    
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="active")
    
    image_url = Column(String, nullable=True) 

    # 🟢 CRITICAL FIX: Added the missing user_id column
    user_id = Column(Integer, nullable=False) 
    
    # Relationship to Bids
    bids = relationship("Bid", back_populates="auction")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"), nullable=False)
    bidder_id = Column(String, nullable=False) 
    
    amount = Column(Numeric(10, 2), nullable=False) 
    
    timestamp = Column(DateTime, default=func.now())

    # Relationship back to Auction
    auction = relationship("Auction", back_populates="bids")