"""
Leads API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from ..agents import get_orchestrator

router = APIRouter()


class LeadSearchRequest(BaseModel):
    """Request model for lead search"""
    search_type: str  # fsbo, tax_delinquent, vacant, probate, all
    location: str  # "City, State" format
    limit: Optional[int] = 20


class LeadResponse(BaseModel):
    """Response model for leads"""
    id: str
    address: str
    city: str
    state: str
    lead_score: float
    data_source: str


@router.post("/search", response_model=dict)
async def search_leads(request: LeadSearchRequest):
    """
    Search for motivated seller leads
    
    Args:
        request: Search parameters (search_type, location)
        
    Returns:
        List of qualified leads with scores
    """
    orchestrator = get_orchestrator()
    
    task = {
        "search_type": request.search_type,
        "location": request.location,
        "limit": request.limit
    }
    
    result = await orchestrator.agents["LeadScout"].run(task)
    return result


@router.get("/{lead_id}", tags=["leads"])
async def get_lead(lead_id: str):
    """Get detailed lead information by ID"""
    # This would fetch from database in production
    return {
        "lead_id": lead_id,
        "address": "123 Main St",
        "city": "Los Angeles",
        "state": "CA",
        "lead_score": 85.5,
        "status": "qualified",
        "data_source": "FSBO"
    }


@router.get("/", response_model=dict, tags=["leads"])
async def list_leads(skip: int = 0, limit: int = 20, status: Optional[str] = None):
    """List all leads with optional filtering"""
    # This would query database in production
    return {
        "total": 0,
        "skip": skip,
        "limit": limit,
        "leads": []
    }
