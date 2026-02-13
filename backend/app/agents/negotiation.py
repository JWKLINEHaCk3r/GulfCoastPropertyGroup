"""
Negotiation Assistant Agent - Handles seller communications and negotiations
"""
import logging
from typing import Any, Dict
from datetime import datetime

from .base import AIAgent

logger = logging.getLogger(__name__)


class NegotiationAssistantAgent(AIAgent):
    """
    Handles automated communication with sellers:
    - Initial outreach with offers
    - Objection handling
    - Follow-ups
    - Price negotiations
    - Terms adjustments
    """
    
    def __init__(self):
        super().__init__(
            name="NegotiationAssistant",
            description="Handles seller communications and negotiations",
            model="gpt-4",
            temperature=0.5
        )
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate task has required parameters"""
        required = ["lead_id", "interaction_type"]
        return all(key in task for key in required)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate negotiation communication
        
        Args:
            task: Contains lead_id, interaction_type (initial_offer, followup, objection, etc.)
            
        Returns:
            Personalized message/communication
        """
        lead_id = task.get("lead_id")
        interaction_type = task.get("interaction_type")
        lead_data = task.get("lead_data", {})
        offer_data = task.get("offer_data", {})
        
        logger.info(f"NegotiationAssistant: {interaction_type} for lead {lead_id}")
        
        if interaction_type == "initial_offer":
            return self._generate_initial_offer(lead_id, lead_data, offer_data)
        elif interaction_type == "followup":
            return self._generate_followup(lead_id, lead_data, task.get("days_since_offer", 3))
        elif interaction_type == "objection":
            return self._handle_objection(lead_id, lead_data, task.get("objection_type", "price"))
        elif interaction_type == "negotiation":
            return self._generate_negotiation(lead_id, lead_data, offer_data, task.get("new_price"))
        else:
            return {"error": "Unknown interaction type"}
    
    def _generate_initial_offer(self, lead_id: str, lead_data: Dict[str, Any],
                                offer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate initial offer communication"""
        
        subject = f"We Can Buy Your Home at {lead_data.get('address', '')} Quickly"
        
        body = f"""
Dear {lead_data.get('seller_name', 'Home Owner')},

I hope this message finds you well. I represent a team of real estate investors and entrepreneurs who specialize in purchasing homes quickly and fairly.

YOUR PROPERTY
Address: {lead_data.get('address', '')}
City, State: {lead_data.get('city', '')}, {lead_data.get('state', '')}
Property Type: {lead_data.get('property_type', 'residential')}

OUR OFFER
Purchase Price: ${offer_data.get('offer_price', 'calculating'):,.0f}
Timeline: 7-14 days from acceptance
Condition: We buy as-is - no repairs needed
Closing Costs: We cover all closing costs

WHY WORK WITH US?
✓ Fast closing - no months of waiting
✓ No agent commissions - save 6% of sale price
✓ Fair offer - based on current market conditions
✓ No contingencies - cash buyer
✓ Simple process - minimal paperwork

NEXT STEPS
We'd love to discuss your situation and see if this could be a good fit. 
Let's schedule a quick call: {lead_data.get('seller_phone', 'contact us')}

Best regards,
Real Estate Acquisition Team
"""
        
        return {
            "interaction_type": "initial_offer",
            "lead_id": lead_id,
            "message_type": "email",
            "subject": subject,
            "body": body,
            "priority": "high",
            "suggested_followup_days": 5,
            "tokens_used": 1500
        }
    
    def _generate_followup(self, lead_id: str, lead_data: Dict[str, Any], 
                          days_passed: int) -> Dict[str, Any]:
        """Generate followup communication"""
        
        subject = f"Following Up - Purchase Offer for {lead_data.get('address', '')}"
        
        body = f"""
Hi {lead_data.get('seller_name', 'there')},

I wanted to follow up on our offer from a few days ago. I understand selling a property can involve a lot of decisions.

I'm available to discuss:
- Our offer in detail
- Your timeline
- Any questions about our process
- Alternative terms or offers

I'm committed to making this as easy as possible for you. Feel free to reply to this message or call me directly: {lead_data.get('seller_phone', 'contact info')}.

Looking forward to connecting.

Best,
Real Estate Acquisition Team
"""
        
        return {
            "interaction_type": "followup",
            "lead_id": lead_id,
            "message_type": "sms" if days_passed > 7 else "email",
            "subject": subject,
            "body": body,
            "timing": f"Day {days_passed}",
            "suggested_followup_days": 5,
            "tokens_used": 1000
        }
    
    def _handle_objection(self, lead_id: str, lead_data: Dict[str, Any], 
                         objection_type: str) -> Dict[str, Any]:
        """Generate objection handling response"""
        
        objection_responses = {
            "price": {
                "subject": "Your Home is Worth More - Let's Talk",
                "body": """
I completely understand your concern about price. Here's what you need to know:

Our offer accounts for:
1. Market conditions RIGHT NOW
2. The actual condition of the property
3. Our ability to close quickly (no contingencies)

When you factor in:
- Agent commissions (6%)
- Closing costs
- Time to sell (average 60-90 days)
- Multiple showings/inspections
- Marketing costs

The actual NET proceeds from a traditional sale may be LESS than our offer.

Let me show you the real numbers. Are you open to a quick 15-minute call?
"""
            },
            "timeline": {
                "subject": "Why a Quick Sale Might Help You",
                "body": """
I hear concerns about our timeline often. Here's why fast closing is actually beneficial:

✓ Certainty - No deal falling through after inspections
✓ Less stress - No months of uncertainty
✓ Costs - Every month of carrying costs money
✓ Flexibility - You can plan your next move

We close in 7-14 days. Most sellers find this refreshingly simple.

What's your ideal timeline? Let's see if we can work with it.
"""
            },
            "condition": {
                "subject": "You Don't Need to Fix Anything",
                "body": """
Great news - you don't need to repair or prepare anything!

We buy properties in ANY condition:
- Cosmetic issues
- Structural concerns
- Needed updates
- Inherited properties
- Tired of the work

You don't fix it. We do. No stress, no contractor headaches.

This is actually one of the biggest benefits of selling to investors.

Want to move forward?
"""
            }
        }
        
        response = objection_responses.get(objection_type, objection_responses.get("price"))
        
        return {
            "interaction_type": "objection_response",
            "lead_id": lead_id,
            "objection_type": objection_type,
            "message_type": "email",
            "subject": response.get("subject", ""),
            "body": response.get("body", ""),
            "tokens_used": 1200
        }
    
    def _generate_negotiation(self, lead_id: str, lead_data: Dict[str, Any],
                             offer_data: Dict[str, Any], new_price: float) -> Dict[str, Any]:
        """Generate negotiation counter-offer"""
        
        subject = f"Updated Offer for {lead_data.get('address', '')}"
        
        body = f"""
We've reviewed everything and want to move forward.

We're ready to submit an updated offer:

REVISED OFFER
Price: ${new_price:,.0f}
Closing Timeline: 10 business days
Terms: All other terms remain the same

This offer is good for 5 days from today.

Are you interested in moving forward with this offer?

Please confirm ASAP so we can start the paperwork.

Real Estate Team
"""
        
        return {
            "interaction_type": "negotiation",
            "lead_id": lead_id,
            "new_offer_price": new_price,
            "previous_offer": offer_data.get("offer_price", 0),
            "price_increase": new_price - offer_data.get("offer_price", 0),
            "message_type": "email",
            "subject": subject,
            "body": body,
            "urgency": "high",
            "tokens_used": 1000
        }
