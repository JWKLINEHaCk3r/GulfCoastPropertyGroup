"""
Payment & Subscription Management System
Revenue from 5 streams: Wholesale fees, Subscriptions, Lead sales, Reports, Affiliates
"""

from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Enum as SQLEnum
import stripe
from auth import get_current_user, require_role, UserRole, SubscriptionTier, ACCESS_TOKEN_EXPIRE_MINUTES

# Configuration
stripe.api_key = "sk_test_your_stripe_key"

# ==================== ENUMS ====================

class PaymentMethod(str, Enum):
    """Payment methods"""
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    ACH = "ach"
    PAYPAL = "paypal"

class TransactionType(str, Enum):
    """Transaction types"""
    SUBSCRIPTION = "subscription"
    WHOLESALE_FEE = "wholesale_fee"
    LEAD_PURCHASE = "lead_purchase"
    REPORT_SALE = "report_sale"
    AFFILIATE_COMMISSION = "affiliate_commission"
    REFUND = "refund"

class CommissionType(str, Enum):
    """Commission types"""
    WHOLESALE_FINDER_FEE = "wholesale_finder_fee"  # 3-7% of deal
    INVESTOR_SUBSCRIPTION = "investor_subscription"  # Monthly
    LEAD_SALE = "lead_sale"  # Per lead ($100-500)
    REPORT_SALE = "report_sale"  # Market reports
    AFFILIATE = "affiliate"  # Partner referrals

# ==================== PRICING ====================

PRICING_TIERS = {
    SubscriptionTier.STARTER: {
        "price": 29900,  # $299/month in cents
        "leads_per_day": 30,
        "features": [
            "Automated outreach",
            "Basic offer generation",
            "Email & SMS",
            "Basic analytics"
        ]
    },
    SubscriptionTier.PROFESSIONAL: {
        "price": 79900,  # $799/month
        "leads_per_day": 100,
        "features": [
            "Everything in Starter",
            "Smart offer generation",
            "Advanced analytics",
            "Contract signing",
            "Investor matching",
            "Priority support"
        ]
    },
    SubscriptionTier.ENTERPRISE: {
        "price": 0,  # Custom pricing
        "leads_per_day": float('inf'),
        "features": [
            "Everything in Pro",
            "Unlimited leads",
            "White-label option",
            "Dedicated account manager",
            "Custom integrations",
            "API access"
        ]
    }
}

# ==================== DATABASE MODELS ====================

class Subscription(BaseModel):
    """User subscription"""
    id: int
    user_id: int
    tier: SubscriptionTier
    stripe_subscription_id: str
    stripe_customer_id: str
    status: str  # active, cancelled, past_due
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = False
    cancelled_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class Payment(BaseModel):
    """Payment transaction"""
    id: int
    user_id: int
    subscription_id: Optional[int]
    amount: int  # Amount in cents
    currency: str = "usd"
    payment_method: PaymentMethod
    stripe_payment_intent_id: str
    status: str  # succeeded, processing, requires_action, cancelled
    description: str
    invoice_url: Optional[str]
    receipt_url: Optional[str]
    created_at: datetime
    updated_at: datetime

class Commission(BaseModel):
    """Commission tracking"""
    id: int
    user_id: int
    deal_id: Optional[int]
    lead_id: Optional[int]
    commission_type: CommissionType
    amount: Decimal  # Amount in dollars
    percentage: Optional[Decimal]  # If percentage-based
    status: str  # pending, approved, paid, rejected
    payment_id: Optional[int]
    created_at: datetime
    paid_at: Optional[datetime]
    notes: Optional[str]

class Invoice(BaseModel):
    """Invoice for transparency"""
    id: int
    user_id: int
    subscription_id: int
    amount: int
    currency: str
    invoice_number: str
    stripe_invoice_id: str
    status: str  # draft, open, paid, uncollectible, void
    issued_at: datetime
    due_date: datetime
    paid_at: Optional[datetime]
    pdf_url: Optional[str]

# ==================== REQUEST/RESPONSE MODELS ====================

class SubscriptionPlanResponse(BaseModel):
    """Available subscription plan"""
    tier: SubscriptionTier
    price: int  # In cents
    price_formatted: str
    leads_per_day: int
    features: List[str]

class CheckoutSessionRequest(BaseModel):
    """Request to create checkout session"""
    tier: SubscriptionTier
    success_url: str = "https://example.com/success"
    cancel_url: str = "https://example.com/cancel"

class CheckoutSessionResponse(BaseModel):
    """Stripe checkout session"""
    session_id: str
    checkout_url: str

class UpgradeSubscriptionRequest(BaseModel):
    """Request to upgrade subscription"""
    new_tier: SubscriptionTier

class PaymentMethodRequest(BaseModel):
    """Add payment method"""
    token: str  # Stripe token
    is_default: bool = False

class CommissionResponse(BaseModel):
    """Commission details"""
    id: int
    commission_type: CommissionType
    amount: Decimal
    percentage: Optional[Decimal]
    status: str
    created_at: datetime
    deal_id: Optional[int]
    lead_id: Optional[int]

class RevenueMetricsResponse(BaseModel):
    """Revenue analytics for user"""
    total_revenue: Decimal
    monthly_recurring: Decimal
    total_commissions: Decimal
    pending_commissions: Decimal
    paid_commissions: Decimal
    commission_breakdown: dict  # By type
    monthly_trend: List[dict]  # Last 12 months

# ==================== PAYMENT ROUTER ====================

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])

@router.get("/plans", response_model=List[SubscriptionPlanResponse])
async def get_subscription_plans():
    """Get available subscription plans"""
    plans = []
    for tier, details in PRICING_TIERS.items():
        plans.append(SubscriptionPlanResponse(
            tier=tier,
            price=details["price"],
            price_formatted=f"${details['price']/100:.2f}/month",
            leads_per_day=details["leads_per_day"],
            features=details["features"]
        ))
    return plans

@router.post("/checkout", response_model=CheckoutSessionResponse)
async def create_checkout_session(
    request: CheckoutSessionRequest,
    user = Depends(get_current_user)
):
    """Create Stripe checkout session"""
    tier_price = PRICING_TIERS[request.tier]["price"]
    
    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": f"Gulf Coast {request.tier.value} Plan",
                    "description": f"{PRICING_TIERS[request.tier]['leads_per_day']} leads/day"
                },
                "unit_amount": tier_price,
                "recurring": {
                    "interval": "month",
                    "interval_count": 1
                }
            },
            "quantity": 1
        }],
        customer_email=user.get("email"),
        mode="subscription",
        success_url=request.success_url,
        cancel_url=request.cancel_url
    )
    
    return CheckoutSessionResponse(
        session_id=session.id,
        checkout_url=session.url
    )

@router.post("/upgrade")
async def upgrade_subscription(
    request: UpgradeSubscriptionRequest,
    user = Depends(get_current_user)
):
    """Upgrade to higher subscription tier"""
    # In production: Handle proration, update subscription
    return {"message": f"Upgraded to {request.new_tier.value}", "effective_date": datetime.utcnow()}

@router.post("/downgrade")
async def downgrade_subscription(
    new_tier: SubscriptionTier,
    user = Depends(get_current_user)
):
    """Downgrade subscription"""
    return {"message": f"Downgraded to {new_tier.value}", "effective_date": (datetime.utcnow() + timedelta(days=30))}

@router.post("/cancel")
async def cancel_subscription(
    cancel_at_period_end: bool = True,
    user = Depends(get_current_user)
):
    """Cancel subscription"""
    if cancel_at_period_end:
        return {"message": "Subscription will be cancelled at end of billing period"}
    else:
        return {"message": "Subscription cancelled immediately"}

@router.get("/current")
async def get_current_subscription(user = Depends(get_current_user)):
    """Get user's current subscription"""
    return {
        "tier": "professional",
        "status": "active",
        "leads_per_day": 100,
        "current_period_end": (datetime.utcnow() + timedelta(days=25)).isoformat(),
        "next_billing_date": (datetime.utcnow() + timedelta(days=25)).isoformat(),
        "auto_renew": True
    }

@router.get("/invoices")
async def list_invoices(
    limit: int = 10,
    user = Depends(get_current_user)
):
    """List user's invoices"""
    return {
        "invoices": [
            {
                "id": "inv_001",
                "amount": 79900,
                "issued_at": "2026-02-01",
                "status": "paid",
                "pdf_url": "https://example.com/invoice.pdf"
            }
        ],
        "total": 1
    }

# ==================== COMMISSION ROUTER ====================

commission_router = APIRouter(prefix="/api/commissions", tags=["commissions"])

@commission_router.get("/", response_model=List[CommissionResponse])
async def list_commissions(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    user = Depends(get_current_user)
):
    """List user commissions"""
    # In production: Query database
    return [
        CommissionResponse(
            id=1,
            commission_type=CommissionType.WHOLESALE_FINDER_FEE,
            amount=Decimal("12000.00"),
            percentage=Decimal("4.0"),
            status="pending",
            created_at=datetime.utcnow(),
            deal_id=1
        )
    ]

@commission_router.get("/{commission_id}")
async def get_commission_details(
    commission_id: int,
    user = Depends(get_current_user)
):
    """Get commission details"""
    return {
        "id": commission_id,
        "type": "wholesale_finder_fee",
        "deal": {"address": "1234 Main St", "value": 300000},
        "amount": 12000,
        "percentage": 4.0,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }

@commission_router.get("/revenue/metrics", response_model=RevenueMetricsResponse)
async def get_revenue_metrics(user = Depends(get_current_user)):
    """Get revenue metrics dashboard"""
    return RevenueMetricsResponse(
        total_revenue=Decimal("125000.00"),
        monthly_recurring=Decimal("799.00"),
        total_commissions=Decimal("85000.00"),
        pending_commissions=Decimal("24000.00"),
        paid_commissions=Decimal("61000.00"),
        commission_breakdown={
            "wholesale_finder_fee": Decimal("60000.00"),
            "investor_subscription": Decimal("15000.00"),
            "lead_sale": Decimal("10000.00")
        },
        monthly_trend=[
            {"month": "Jan 2026", "revenue": Decimal("25000.00")},
            {"month": "Feb 2026", "revenue": Decimal("32000.00")}
        ]
    )

@commission_router.post("/{commission_id}/approve")
async def approve_commission(
    commission_id: int,
    user = Depends(require_role(UserRole.ADMIN, UserRole.SUPER_ADMIN))
):
    """Admin: Approve commission for payout"""
    return {"message": "Commission approved", "commission_id": commission_id}

@commission_router.post("/{commission_id}/reject")
async def reject_commission(
    commission_id: int,
    reason: str,
    user = Depends(require_role(UserRole.ADMIN, UserRole.SUPER_ADMIN))
):
    """Admin: Reject commission"""
    return {"message": "Commission rejected", "reason": reason}

@commission_router.post("/batch/payout")
async def batch_payout(
    min_amount: Decimal = Decimal("100.00"),
    user = Depends(require_role(UserRole.ADMIN, UserRole.SUPER_ADMIN))
):
    """Admin: Process batch payouts for all approved commissions"""
    return {
        "message": "Payout processed",
        "total_users": 45,
        "total_amount": Decimal("125000.00"),
        "datetime": datetime.utcnow().isoformat()
    }

# ==================== WEBHOOK HANDLERS ====================

webhook_router = APIRouter(prefix="/api/webhooks/stripe", tags=["webhooks"])

@webhook_router.post("/events")
async def handle_stripe_webhook(event: dict):
    """Handle Stripe webhook events"""
    event_type = event.get("type")
    
    if event_type == "invoice.payment_succeeded":
        # Handle successful payment
        pass
    elif event_type == "invoice.payment_failed":
        # Handle failed payment
        pass
    elif event_type == "customer.subscription.deleted":
        # Handle subscription cancellation
        pass
    
    return {"received": True}

# Export routers
__all__ = ["router", "commission_router", "webhook_router", "PRICING_TIERS"]
