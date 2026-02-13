"""
Service layer for business logic - Lead service
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..database import Lead, LeadStatusEnum, PropertyTypeEnum, AsyncSessionLocal
from ..agents import get_orchestrator

logger = logging.getLogger(__name__)


class LeadService:
    """Service for managing leads"""
    
    @staticmethod
    async def search_leads(search_type: str, location: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for motivated seller leads using Lead Scout Agent
        
        Args:
            search_type: Type of search (fsbo, tax_delinquent, vacant, probate, all)
            location: Geographic location for search
            limit: Maximum number of results
            
        Returns:
            List of qualified leads with scores
        """
        orchestrator = get_orchestrator()
        
        task = {
            "search_type": search_type,
            "location": location,
            "limit": limit
        }
        
        try:
            result = await orchestrator.agents["LeadScout"].run(task)
            return result.get("leads", [])
        except Exception as e:
            logger.error(f"Lead search failed: {e}")
            return []
    
    @staticmethod
    async def create_lead(lead_data: Dict[str, Any]) -> Lead:
        """Save a lead to database"""
        async with AsyncSessionLocal() as session:
            lead = Lead(
                address=lead_data.get("address"),
                city=lead_data.get("city"),
                state=lead_data.get("state"),
                zip_code=lead_data.get("zip_code"),
                property_type=lead_data.get("property_type", PropertyTypeEnum.SINGLE_FAMILY),
                square_feet=lead_data.get("square_feet"),
                bedrooms=lead_data.get("bedrooms"),
                bathrooms=lead_data.get("bathrooms"),
                year_built=lead_data.get("year_built"),
                estimated_after_repair_value=lead_data.get("estimated_after_repair_value"),
                market_value=lead_data.get("market_value"),
                estimated_repair_cost=lead_data.get("estimated_repair_cost"),
                seller_phone=lead_data.get("seller_phone"),
                seller_email=lead_data.get("seller_email"),
                seller_name=lead_data.get("seller_name"),
                lead_score=lead_data.get("lead_score", 0.0),
                lead_status=LeadStatusEnum.NEW,
                data_source=lead_data.get("data_source"),
                mls_id=lead_data.get("mls_id"),
                external_id=lead_data.get("external_id"),
            )
            
            session.add(lead)
            await session.commit()
            await session.refresh(lead)
            return lead
    
    @staticmethod
    async def get_lead_by_id(lead_id: str) -> Optional[Lead]:
        """Retrieve a lead by ID"""
        async with AsyncSessionLocal() as session:
            return await session.get(Lead, lead_id)
    
    @staticmethod
    async def update_lead_status(lead_id: str, status: LeadStatusEnum):
        """Update lead status"""
        async with AsyncSessionLocal() as session:
            lead = await session.get(Lead, lead_id)
            if lead:
                lead.lead_status = status
                lead.updated_at = datetime.utcnow()
                await session.commit()
                return lead
            return None
    
    @staticmethod
    async def get_qualified_leads(min_score: int = 65, limit: int = 20) -> List[Lead]:
        """Get leads above minimum quality threshold"""
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            
            query = select(Lead).where(
                Lead.lead_score >= min_score,
                Lead.lead_status == LeadStatusEnum.NEW
            ).limit(limit)
            
            result = await session.execute(query)
            return result.scalars().all()


class OfferService:
    """Service for managing offers"""
    
    @staticmethod
    async def generate_offer(lead_id: str, property_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an offer using Offer Generator Agent"""
        orchestrator = get_orchestrator()
        
        task = {
            "lead_id": lead_id,
            "property_details": property_details
        }
        
        try:
            result = await orchestrator.agents["OfferGenerator"].run(task)
            return result
        except Exception as e:
            logger.error(f"Offer generation failed: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def match_buyers(property_info: Dict[str, Any]) -> Dict[str, Any]:
        """Match property with qualified buyers"""
        orchestrator = get_orchestrator()
        
        task = {
            "property": property_info
        }
        
        try:
            result = await orchestrator.agents["BuyerMatcher"].run(task)
            return result
        except Exception as e:
            logger.error(f"Buyer matching failed: {e}")
            return {"error": str(e)}


class NegotiationService:
    """Service for managing negotiations"""
    
    @staticmethod
    async def generate_communication(lead_id: str, interaction_type: str, 
                                     lead_data: Dict[str, Any], 
                                     offer_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate negotiation communication"""
        orchestrator = get_orchestrator()
        
        task = {
            "lead_id": lead_id,
            "interaction_type": interaction_type,
            "lead_data": lead_data,
            "offer_data": offer_data or {}
        }
        
        try:
            result = await orchestrator.agents["NegotiationAssistant"].run(task)
            return result
        except Exception as e:
            logger.error(f"Communication generation failed: {e}")
            return {"error": str(e)}


class SEOService:
    """Service for SEO content generation"""
    
    @staticmethod
    async def generate_content(content_type: str, keyword: str, 
                              location: Optional[str] = None) -> Dict[str, Any]:
        """Generate SEO-optimized content"""
        orchestrator = get_orchestrator()
        
        task = {
            "content_type": content_type,
            "keyword": keyword,
            "location": location or "USA"
        }
        
        try:
            result = await orchestrator.agents["SEOContent"].run(task)
            return result
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return {"error": str(e)}
