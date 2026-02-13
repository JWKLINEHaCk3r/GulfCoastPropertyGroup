"""
SQLAlchemy ORM models for the application
"""
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Boolean, 
    ForeignKey, JSON, Enum, Text, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from .base import Base


class LeadStatusEnum(str, enum.Enum):
    """Lead status enumeration"""
    NEW = "new"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    NEGOTIATING = "negotiating"
    UNDER_CONTRACT = "under_contract"
    CLOSED = "closed"
    REJECTED = "rejected"
    EXPIRED = "expired"


class PropertyTypeEnum(str, enum.Enum):
    """Property type enumeration"""
    SINGLE_FAMILY = "single_family"
    MULTI_FAMILY = "multi_family"
    COMMERCIAL = "commercial"
    VACANT = "vacant"
    MOBILE_HOME = "mobile_home"
    OTHER = "other"


class Lead(Base):
    """Property/Seller Lead Model"""
    __tablename__ = "leads"
    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_score', 'lead_score'),
        Index('idx_created', 'created_at'),
    )
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Property basics
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    county = Column(String(100))
    
    # Property details
    property_type = Column(Enum(PropertyTypeEnum), default=PropertyTypeEnum.SINGLE_FAMILY)
    square_feet = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    year_built = Column(Integer)
    
    # Valuation
    estimated_after_repair_value = Column(Float)  # ARV
    market_value = Column(Float)
    tax_assessed_value = Column(Float)
    estimated_repair_cost = Column(Float)
    estimated_holding_cost = Column(Float)
    
    # Seller information
    seller_phone = Column(String(20))
    seller_email = Column(String(255))
    seller_name = Column(String(255))
    seller_motivated = Column(Boolean, default=False)
    
    # Lead scoring
    lead_score = Column(Float, default=0.0)  # 0-100
    lead_status = Column(Enum(LeadStatusEnum), default=LeadStatusEnum.NEW)
    
    # Source information
    data_source = Column(String(100))  # "FSBO", "Tax Delinquent", "Zillow Scrape", etc.
    mls_id = Column(String(50), unique=True, nullable=True)
    external_id = Column(String(255), unique=True, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted = Column(DateTime)
    
    # Relationships
    offers = relationship("Offer", back_populates="lead", cascade="all, delete-orphan")
    interactions = relationship("LeadInteraction", back_populates="lead", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lead {self.address}, {self.city}, {self.state} (Score: {self.lead_score})>"


class Offer(Base):
    """Offer generated for a lead"""
    __tablename__ = "offers"
    __table_args__ = (
        Index('idx_lead_id', 'lead_id'),
        Index('idx_created', 'created_at'),
    )
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False)
    
    # Offer details
    offer_price = Column(Float, nullable=False)
    projected_profit = Column(Float)
    terms = Column(Text)  # Contract terms
    
    # Document tracking
    contract_docusign_id = Column(String(100))
    contract_url = Column(String(500))
    contract_signed = Column(Boolean, default=False)
    
    # Status
    status = Column(String(50), default="draft")  # draft, sent, signed, accepted, rejected
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sent_at = Column(DateTime)
    signed_at = Column(DateTime)
    
    # Relationship
    lead = relationship("Lead", back_populates="offers")
    
    def __repr__(self):
        return f"<Offer ${self.offer_price} for Lead {self.lead_id}>"


class LeadInteraction(Base):
    """Track all interactions with leads (calls, emails, messages)"""
    __tablename__ = "lead_interactions"
    __table_args__ = (
        Index('idx_lead_id', 'lead_id'),
        Index('idx_created', 'created_at'),
    )
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String(36), ForeignKey("leads.id"), nullable=False)
    
    interaction_type = Column(String(50))  # "email", "sms", "call", "chat"
    direction = Column(String(10))  # "inbound", "outbound"
    message = Column(Text)
    response = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    lead = relationship("Lead", back_populates="interactions")
    
    def __repr__(self):
        return f"<Interaction {self.interaction_type} for Lead {self.lead_id}>"


class CashBuyer(Base):
    """Cash buyer/investor profile"""
    __tablename__ = "cash_buyers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic info
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    company_name = Column(String(255))
    
    # Investment preferences
    target_states = Column(JSON)  # List of states they invest in
    min_deal_size = Column(Float)
    max_deal_size = Column(Float)
    preferred_property_types = Column(JSON)
    min_roi_percent = Column(Float, default=20.0)
    
    # Activity tracking
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime)
    
    # Contact preferences
    auto_notify = Column(Boolean, default=True)
    notification_method = Column(String(50), default="email")  # email, sms, both
    
    def __repr__(self):
        return f"<CashBuyer {self.name}>"


class Deal(Base):
    """Completed or in-progress deals"""
    __tablename__ = "deals"
    __table_args__ = (
        Index('idx_lead_id', 'lead_id'),
        Index('idx_created', 'created_at'),
    )
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String(36), ForeignKey("leads.id"))
    
    # Deal details
    purchase_price = Column(Float)
    sale_price = Column(Float)
    wholesale_fee = Column(Float)
    buyer_id = Column(String(36), ForeignKey("cash_buyers.id"))
    
    # Status
    status = Column(String(50), default="pending")  # pending, closed, failed
    closing_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Deal Lead {self.lead_id}: ${self.wholesale_fee} fee>"


class SEOContent(Base):
    """Auto-generated SEO content pages"""
    __tablename__ = "seo_content"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    
    # SEO metadata
    meta_description = Column(String(500))
    keywords = Column(JSON)
    target_keyword = Column(String(255))
    
    # Stats
    word_count = Column(Integer)
    internal_links = Column(Integer, default=0)
    external_links = Column(Integer, default=0)
    
    # Publishing
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<SEOContent {self.slug}>"


class User(Base):
    """Platform users (admins, wholesalers, buyers)"""
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_email', 'email'),
    )
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Credentials
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255))
    
    # Role and permissions
    user_type = Column(String(50))  # admin, wholesaler, buyer, investor
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.email}>"
