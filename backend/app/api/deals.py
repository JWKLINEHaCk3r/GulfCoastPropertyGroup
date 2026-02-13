"""
Deals API endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class DealCreate(BaseModel):
    """Create deal model"""
    lead_id: str
    buyer_id: str
    purchase_price: float
    sale_price: float


@router.post("/", tags=["deals"])
async def create_deal(deal: DealCreate):
    """Create a new deal"""
    wholesale_fee = deal.sale_price - deal.purchase_price
    
    return {
        "deal_id": "deal_123",
        "lead_id": deal.lead_id,
        "buyer_id": deal.buyer_id,
        "purchase_price": deal.purchase_price,
        "sale_price": deal.sale_price,
        "wholesale_fee": wholesale_fee,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/{deal_id}", tags=["deals"])
async def get_deal(deal_id: str):
    """Get deal details"""
    return {
        "deal_id": deal_id,
        "status": "closed",
        "wholesale_fee": 15000.00,
        "closing_date": "2025-02-13T00:00:00"
    }


@router.get("/", tags=["deals"])
async def list_deals(status: Optional[str] = None, skip: int = 0, limit: int = 20):
    """List all deals"""
    return {
        "total": 0,
        "skip": skip,
        "limit": limit,
        "deals": []
    }
