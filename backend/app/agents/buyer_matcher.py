"""
Buyer Matcher Agent - Matches properties with qualified cash buyers
"""
import logging
from typing import Any, Dict, List
from datetime import datetime

from .base import AIAgent

logger = logging.getLogger(__name__)


class BuyerMatcherAgent(AIAgent):
    """
    Matches properties with the most qualified cash buyers based on:
    - Geographic preferences
    - Property type preferences
    - Deal size requirements
    - ROI expectations
    - Investment history
    """
    
    def __init__(self):
        super().__init__(
            name="BuyerMatcher",
            description="Matches properties with qualified cash buyers",
            model="gpt-4",
            temperature=0.2
        )
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate task has required parameters"""
        required = ["property"]
        return all(key in task for key in required)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Match a property with qualified buyers
        
        Args:
            task: Contains property details
            
        Returns:
            List of matched buyers with match scores
        """
        property_info = task.get("property", {})
        available_buyers = task.get("available_buyers", self._get_mock_buyers())
        
        logger.info(f"BuyerMatcher: Matching property at {property_info.get('address')}")
        
        # Score each buyer against the property
        matches = []
        for buyer in available_buyers:
            score = self._calculate_match_score(property_info, buyer)
            if score > 50:  # Only return buyers with >50% match
                matches.append({
                    "buyer_id": buyer.get("id"),
                    "buyer_name": buyer.get("name"),
                    "match_score": round(score, 1),
                    "contact_method": buyer.get("notification_method", "email"),
                    "match_factors": self._get_match_factors(property_info, buyer)
                })
        
        # Sort by match score descending
        matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)
        
        return {
            "property_id": property_info.get("id", "unknown"),
            "property_address": property_info.get("address", ""),
            "total_buyers_available": len(available_buyers),
            "qualified_matches": len(matches),
            "top_matches": matches[:5],
            "all_matches": matches,
            "tokens_used": len(matches) * 1000
        }
    
    def _calculate_match_score(self, property_info: Dict[str, Any], 
                               buyer: Dict[str, Any]) -> float:
        """
        Calculate match score (0-100) between property and buyer
        
        Factors:
        - Geographic match (25 points)
        - Property type match (20 points)
        - Deal size alignment (20 points)
        - ROI alignment (20 points)
        - Buyer activity level (15 points)
        """
        score = 0
        
        # Geographic match (25 points)
        property_state = property_info.get("state", "").upper()
        target_states = buyer.get("target_states", [])
        if property_state in target_states or not target_states:
            score += 25
        else:
            score -= 10
        
        # Property type match (20 points)
        property_type = property_info.get("property_type", "")
        preferred_types = buyer.get("preferred_property_types", [])
        if property_type in preferred_types or not preferred_types:
            score += 20
        else:
            score += 10
        
        # Deal size alignment (20 points)
        property_value = property_info.get("estimated_after_repair_value", 0)
        min_size = buyer.get("min_deal_size", 0)
        max_size = buyer.get("max_deal_size", 10000000)
        
        if min_size <= property_value <= max_size:
            # Closer to buyer's preferred range = better
            mid_point = (min_size + max_size) / 2
            distance = abs(property_value - mid_point)
            max_distance = (max_size - min_size) / 2
            alignment = 1 - (distance / max_distance if max_distance > 0 else 1)
            score += alignment * 20
        else:
            score += 5
        
        # ROI alignment (20 points)
        buyer_roi = buyer.get("min_roi_percent", 20)
        # This would come from the offer generator in real scenario
        estimated_roi = property_info.get("roi_percent", 25)
        
        if estimated_roi >= buyer_roi:
            score += 20
        elif estimated_roi >= (buyer_roi * 0.8):
            score += 12
        else:
            score += 5
        
        # Buyer activity level (15 points)
        if buyer.get("is_active", False):
            score += 15
        
        return min(score, 100)
    
    def _get_match_factors(self, property_info: Dict[str, Any], 
                           buyer: Dict[str, Any]) -> Dict[str, str]:
        """Get detailed match factors for transparency"""
        factors = {}
        
        # Geographic
        if property_info.get("state", "").upper() in buyer.get("target_states", []):
            factors["geography"] = "MATCH - State in target list"
        else:
            factors["geography"] = "DIFFERENT - Outside target states"
        
        # Property type
        if property_info.get("property_type", "") in buyer.get("preferred_property_types", []):
            factors["property_type"] = "MATCH"
        else:
            factors["property_type"] = "ACCEPTABLE - Will consider"
        
        # Deal size
        prop_value = property_info.get("estimated_after_repair_value", 0)
        min_size = buyer.get("min_deal_size", 0)
        max_size = buyer.get("max_deal_size", 10000000)
        
        if min_size <= prop_value <= max_size:
            factors["deal_size"] = f"MATCH - Within ${min_size:,} - ${max_size:,} range"
        else:
            factors["deal_size"] = f"OUTSIDE - Buyer range ${min_size:,} - ${max_size:,}"
        
        return factors
    
    def _get_mock_buyers(self) -> List[Dict[str, Any]]:
        """Return mock buyer data for demonstration"""
        return [
            {
                "id": "buyer_001",
                "name": "John Smith Investments",
                "target_states": ["CA", "TX", "FL", "AZ"],
                "min_deal_size": 100000,
                "max_deal_size": 2000000,
                "preferred_property_types": ["single_family", "multi_family"],
                "min_roi_percent": 20,
                "is_active": True,
                "notification_method": "email"
            },
            {
                "id": "buyer_002",
                "name": "Cash Flow Capital Partners",
                "target_states": ["CA", "WA", "OR"],
                "min_deal_size": 200000,
                "max_deal_size": 3000000,
                "preferred_property_types": ["multi_family"],
                "min_roi_percent": 15,
                "is_active": True,
                "notification_method": "sms"
            },
            {
                "id": "buyer_003",
                "name": "Quick Close Real Estate LLC",
                "target_states": [],  # All states
                "min_deal_size": 50000,
                "max_deal_size": 5000000,
                "preferred_property_types": ["single_family", "vacant"],
                "min_roi_percent": 25,
                "is_active": True,
                "notification_method": "email"
            },
        ]
