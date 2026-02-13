"""
Agents module initialization - Register all agents
"""
from .base import AIAgent, AgentOrchestrator, get_orchestrator
from .lead_scout import LeadScoutAgent
from .offer_generator import OfferGeneratorAgent
from .buyer_matcher import BuyerMatcherAgent
from .negotiation import NegotiationAssistantAgent
from .seo_content import SEOContentAgent

__all__ = [
    "AIAgent",
    "AgentOrchestrator",
    "get_orchestrator",
    "LeadScoutAgent",
    "OfferGeneratorAgent",
    "BuyerMatcherAgent",
    "NegotiationAssistantAgent",
    "SEOContentAgent",
]


def init_agents() -> AgentOrchestrator:
    """Initialize all agents and register with orchestrator"""
    orchestrator = get_orchestrator()
    
    # Register all agents
    orchestrator.register_agent(LeadScoutAgent())
    orchestrator.register_agent(OfferGeneratorAgent())
    orchestrator.register_agent(BuyerMatcherAgent())
    orchestrator.register_agent(NegotiationAssistantAgent())
    orchestrator.register_agent(SEOContentAgent())
    
    return orchestrator
