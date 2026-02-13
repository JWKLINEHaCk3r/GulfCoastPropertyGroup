"""
Offers API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..agents import get_orchestrator

router = APIRouter()


class OfferGenerationRequest(BaseModel):
    """Request model for offer generation"""
    lead_id: str
    property_details: dict


class OfferResponse(BaseModel):
    """Response model for offers"""
    offer_id: str
    lead_id: str
    offer_price: float
    arv: float
    projected_profit: float
    status: str


@router.post("/generate", response_model=dict)
async def generate_offer(request: OfferGenerationRequest):
    """
    Generate an optimized purchase offer for a lead
    
    Args:
        request: Lead ID and property details
        
    Returns:
        Generated offer with pricing and terms
    """
    orchestrator = get_orchestrator()
    
    task = {
        "lead_id": request.lead_id,
        "property_details": request.property_details
    }
    
    result = await orchestrator.agents["OfferGenerator"].run(task)
    return result


@router.get("/{offer_id}", tags=["offers"])
async def get_offer(offer_id: str):
    """Get offer details by ID"""
    return {
        "offer_id": offer_id,
        "lead_id": "lead_123",
        "offer_price": 250000.00,
        "arv": 400000.00,
        "modified_at": "2025-02-13T00:00:00"
    }


@router.patch("/{offer_id}/sign", tags=["offers"])
async def sign_offer(offer_id: str):
    """Sign an offer (integrate with DocuSign)"""
    return {
        "offer_id": offer_id,
        "status": "signed",
        "signed_at": "2025-02-13T00:00:00"
    }
