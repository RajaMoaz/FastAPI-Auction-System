from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal 

# --- Helper: Custom JSON encoder for Decimal objects ---
def decimal_encoder(v):
    """Encodes Decimal to string for JSON serialization."""
    return str(v)

# Schema for a Bid submitted by the user
class BidCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, description="The bid amount must be positive.")
    bidder_id: str = Field(..., min_length=1)
    
    class Config:
        json_encoders = {Decimal: decimal_encoder}

# Schema for the Auction details that form the base of the item
class AuctionBase(BaseModel):
    title: str
    description: str
    starting_price: Decimal
    image_url: str | None = None

# --- CRITICAL: Schema for creating a new Auction item ---
class AuctionCreate(BaseModel):
    title: str
    description: str
    # CRITICAL FIX: Matches the float type sent by the HTML form
    starting_price: float 
    
    image_url: str | None = None

# Schema representing an Auction from the database (response model)
class Auction(AuctionBase):
    id: int
    user_id: int # Included to match the column in models.py
    current_highest_bid: Decimal
    status: str
    end_time: datetime

    class Config:
        from_attributes = True
        json_encoders = {Decimal: decimal_encoder}