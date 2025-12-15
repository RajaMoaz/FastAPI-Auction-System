import uvicorn
import socketio
import random
import time
import traceback
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from socketio import ASGIApp, AsyncServer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation

# Import your local modules
from . import models  # Assumes main.py is inside auction_backend_python
from .database import engine, get_db
from .schemas import BidCreate, Auction, AuctionCreate

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
BACKEND_PORT = 8000
CORS_ORIGINS = [
    "*",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://localhost:8080"
]

# Initialize Async Socket.IO Server
sio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=CORS_ORIGINS
)

# Initialize FastAPI Application
app = FastAPI()

# Global Decimal Serialization Fix
app.json_encoders = {
    Decimal: lambda v: str(v),
}

# Add standard CORS middleware for REST API endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combined ASGI app with Socket.IO
socketio_app = ASGIApp(
    socketio_server=sio,
    socketio_path='/ws/socket.io',
    other_asgi_app=app
)

# Database Initialization
models.Base.metadata.create_all(bind=engine)

# Socket.IO Event Handlers
@sio.event
async def connect(sid, environ):
    logging.info(f"[Socket.IO] New connection: {sid}")

@sio.event
async def disconnect(sid):
    logging.info(f"[Socket.IO] Disconnected: {sid}")

# REST API Endpoints
@app.get("/")
async def root():
    return {"message": "Auction System Backend (FastAPI) is Running"}

# Get Auction Details Endpoint
@app.get("/api/auctions/{auction_id}", response_model=Auction, tags=["Auctions"])
def get_auction(auction_id: int, db: Session = Depends(get_db)):
    auction = db.query(models.Auction).filter(models.Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail="Auction Not Found")
    return auction

# Create Auction Endpoint with Server-Side End Time & User_ID fix
@app.post("/api/auctions", response_model=Auction, tags=["Auctions"])
def create_auction(
    auction_data: AuctionCreate,
    db: Session = Depends(get_db)
):
    logging.info("--- ATTEMPTING AUCTION CREATION ---")
    try:
        # 1. Server-side calculations
        end_time_dt = datetime.now() + timedelta(hours=24)
        
        # 2. Safely convert the float price from the client to Decimal for the DB
        try:
            # IMPORTANT: Convert float to string before Decimal to preserve precision.
            starting_price_decimal = Decimal(str(auction_data.starting_price))
        except InvalidOperation:
            raise HTTPException(status_code=400, detail="Starting price is not a valid number.")

        # 3. Create Auction model instance, filling in server-side values
        db_auction = models.Auction(
            title=auction_data.title,
            description=auction_data.description,
            starting_price=starting_price_decimal,
            current_highest_bid=starting_price_decimal,
            image_url=auction_data.image_url,
            end_time=end_time_dt, 
            status="active",
            # --- CRITICAL FIX: user_id is now a recognized column in models.py ---
            user_id=1 
        )
        
        db.add(db_auction)
        db.commit()
        db.refresh(db_auction)
        logging.info(f"--- SUCCESS: Auction ID {db_auction.id} committed. ---")
        
        return db_auction

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Database/Internal Error during auction creation: {e}")
        logging.error(traceback.format_exc()) 
        db.rollback() 
        # Return a clean 500 error that the frontend can read
        raise HTTPException(status_code=500, detail=f"Internal server error. Check server logs.")

# Place a Bid Endpoint (Code for this is unchanged, still uses socket.io emit)
@app.post("/api/bids/{auction_id}", response_model=Auction, tags=["Bidding"])
async def place_bid(
    auction_id: int,
    bid_data: BidCreate,
    db: Session = Depends(get_db)
):
    auction = db.query(models.Auction).filter(models.Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=404, detail=f"Auction ID {auction_id} not found.")

    if bid_data.amount > auction.current_highest_bid:
        auction.current_highest_bid = bid_data.amount
        db.commit()
        db.refresh(auction)
        
        # Emit real-time bid via Socket.IO
        await sio.emit(
            'new_bid',
            {
                'auctionId': auction.id,
                'newBid': str(auction.current_highest_bid), 
                'bidderId': bid_data.bidder_id
            }
        )
        return auction
    else:
        raise HTTPException(status_code=400, detail="Bid amount must be higher than the current highest bid.")

# Run Server 
if __name__ == "__main__":
    # If main.py is inside auction_backend_python, run from root folder using:
    # uvicorn auction_backend_python.main:socketio_app --reload
    uvicorn.run("main:socketio_app", host="0.0.0.0", port=BACKEND_PORT, reload=True)