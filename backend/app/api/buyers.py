"""
Cash Buyers API endpoints
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()


class BuyerProfile(BaseModel):
    """Cash buyer profile"""
    name: str
    email: str
    phone: Optional[str] = None
    target_states: List[str] = []
    min_deal_size: float = 0
    max_deal_size: float = 10000000
    preferred_property_types: List[str] = []
    min_roi_percent: float = 20.0


@router.post("/", tags=["buyers"])
async def register_buyer(buyer: BuyerProfile):
    """Register a new cash buyer"""
    return {
        "buyer_id": "buyer_123",
        "name": buyer.name,
        "email": buyer.email,
        "status": "registered",
        "created_at": "2025-02-13T00:00:00"
    }


@router.get("/{buyer_id}", tags=["buyers"])
async def get_buyer(buyer_id: str):
    """Get buyer profile"""
    return {
        "buyer_id": buyer_id,
        "name": "John Smith Investments",
        "email": "john@example.com",
        "total_deals": 12,
        "is_active": True
    }


@router.get("/", tags=["buyers"])
async def list_buyers(state: Optional[str] = None, skip: int = 0, limit: int = 20):
    """List all cash buyers with optional filtering"""
    return {
        "total": 0,
        "skip": skip,
        "limit": limit,
        "buyers": []
    }


@router.post("/{buyer_id}/notify", tags=["buyers"])
async def notify_buyer(buyer_id: str, property_id: str):
    """Notify a buyer about a new property"""
    return {
        "buyer_id": buyer_id,
        "property_id": property_id,
        "notification_sent": True,
        "method": "email"
    }
