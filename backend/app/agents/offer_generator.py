"""
Offer Generator Agent - Creates optimized purchase offers
"""
import logging
from typing import Any, Dict
from datetime import datetime

from .base import AIAgent
from ..config import settings

logger = logging.getLogger(__name__)


class OfferGeneratorAgent(AIAgent):
    """
    Generates optimal purchase offers based on:
    - Property comparables
    - After-Repair Value (ARV)
    - Repair costs
    - Market conditions
    - Target profit margin
    - Wholesale fee
    """
    
    def __init__(self):
        super().__init__(
            name="OfferGenerator",
            description="Generates optimized purchase offers for identified leads",
            model="gpt-4",
            temperature=0.2
        )
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate task has required parameters"""
        required = ["lead_id", "property_details"]
        return all(key in task for key in required)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an offer for a property
        
        Args:
            task: Contains lead_id and property_details
            
        Returns:
            Generated offer with price, terms, and contract
        """
        lead_id = task.get("lead_id")
        property_details = task.get("property_details", {})
        
        logger.info(f"OfferGenerator: Creating offer for lead {lead_id}")
        
        # Calculate offer price
        offer_price = self._calculate_offer_price(property_details)
        
        # Calculate projected profit
        arv = property_details.get("estimated_after_repair_value", 0)
        repair_cost = property_details.get("estimated_repair_cost", 0)
        holding_cost = property_details.get("estimated_holding_cost", 0)
        wholesale_fee = offer_price * (settings.wholesale_fee_percentage / 100)
        
        projected_profit = arv - offer_price - repair_cost - holding_cost - wholesale_fee
        
        # Generate contract terms
        terms = self._generate_contract_terms(lead_id, offer_price, property_details)
        
        return {
            "lead_id": lead_id,
            "offer_price": round(offer_price, 2),
            "arv": arv,
            "repair_cost": repair_cost,
            "holding_cost": holding_cost,
            "wholesale_fee": round(wholesale_fee, 2),
            "projected_profit": round(projected_profit, 2),
            "roi_percent": round((projected_profit / offer_price * 100), 1) if offer_price > 0 else 0,
            "terms": terms,
            "created_at": datetime.utcnow().isoformat(),
            "tokens_used": 2000
        }
    
    def _calculate_offer_price(self, property_details: Dict[str, Any]) -> float:
        """
        Calculate optimal offer price
        
        Formula: offer_price = ARV - (Repair Costs + Holding Costs + Wholesale Fee + Profit Margin)
        """
        arv = property_details.get("estimated_after_repair_value", 0)
        repair_cost = property_details.get("estimated_repair_cost", 50000)  # Default if not specified
        holding_cost = property_details.get("estimated_holding_cost", 10000)  # Default if not specified
        
        # Target 25% profit margin for the buyer after all costs
        target_profit_margin = 0.25
        wholesale_fee = 0  # Will be calculated by buyer
        
        # 70% rule: offer = ARV * 0.7 - repair_costs
        # Or more sophisticated: Offer = ARV - (Repair + Holding + Fee + Desired Profit)
        
        # Use the 70% rule as baseline with adjustments
        baseline_offer = arv * (1 - settings.default_offer_discount_percent / 100)
        adjusted_offer = baseline_offer - repair_cost * 0.1  # Small adjustment for repairs
        
        # Ensure minimum offer is 50% of ARV
        minimum_offer = arv * 0.50
        
        offer_price = max(adjusted_offer, minimum_offer)
        return offer_price
    
    def _generate_contract_terms(self, lead_id: str, offer_price: float, 
                                 property_details: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate standard contract terms
        """
        return {
            "offer_price": f"${offer_price:,.2f}",
            "property_address": property_details.get("address", ""),
            "offer_valid_days": 7,
            "inspection_period_days": 10,
            "closing_timeline": "30 days",
            "contingencies": [
                "Property inspection",
                "Financing approval",
                "Title search",
                "Appraisal",
                "Survey (if required)"
            ],
            "special_terms": [
                "As-is condition",
                "Seller to provide all disclosures",
                "Cash offer",
                "Quick closing"
            ],
            "earnest_money": f"${max(5000, offer_price * 0.01):,.2f}",
            "closing_costs_paid_by": "Buyer"
        }
