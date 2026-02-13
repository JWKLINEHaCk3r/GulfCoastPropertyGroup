"""
Application configuration management
"""
from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Basic App Config
    app_name: str = "Real Estate AI Ecosystem"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    secret_key: Optional[str] = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/realestate"
    redis_url: str = "redis://localhost:6379/0"
    sqlalchemy_echo: bool = False
    
    # API Keys & Secrets
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Third-party Integrations
    docusign_api_key: Optional[str] = None
    docusign_account_id: Optional[str] = None
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    
    sendgrid_api_key: Optional[str] = None
    sendgrid_from_email: str = "noreply@realestate.com"
    
    zillow_api_key: Optional[str] = None
    redfin_api_key: Optional[str] = None
    
    # Business Config
    min_lead_score_threshold: int = 65
    wholesale_fee_percentage: float = 6.0
    default_offer_discount_percent: int = 30
    
    # Scraping Config
    scraper_delay_seconds: float = 2.0
    max_requests_per_minute: int = 60
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Feature Flags
    enable_lead_scout: bool = True
    enable_offer_generation: bool = True
    enable_buyer_matching: bool = True
    enable_negotiation_bot: bool = True
    enable_seo_automation: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    # In non-development environments, require a secret_key to be present
    if settings.environment and settings.environment.lower() != "development" and not settings.secret_key:
        raise RuntimeError("SECRET_KEY (secret_key) must be set in environment for non-development environments")
    return settings


# Expose settings for easy import
settings = get_settings()
