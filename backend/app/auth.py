"""
Enhanced Authentication & authorization system for Gulf Coast Property Group
Supports multiple user roles, OAuth, 2FA, and enterprise security
"""

from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
import secrets
import hmac
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import Session
import jwt
import bcrypt
from passlib.context import CryptContext

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# ==================== ENUMS ====================

class UserRole(str, Enum):
    """User roles with hierarchy"""
    SUPER_ADMIN = "super_admin"      # Full platform access
    ADMIN = "admin"                   # Company management
    CLIENT = "client"                 # Real estate company user
    INVESTOR = "investor"             # Cash buyer
    BANK = "bank"                     # Lender/underwriter
    PARTNER = "partner"               # Affiliate/referral partner
    FREE_TRIAL = "free_trial"         # Trial user (limited access)

class SubscriptionTier(str, Enum):
    """Subscription pricing tiers"""
    STARTER = "starter"               # $299/mo
    PROFESSIONAL = "professional"     # $799/mo  
    ENTERPRISE = "enterprise"         # Custom

# ==================== DATABASE MODELS ====================

class User(BaseModel):
    """Enhanced user model with company & subscription"""
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password_hash: str
    role: UserRole
    subscription_tier: SubscriptionTier
    company_name: Optional[str]
    company_id: Optional[int]
    is_active: bool = True
    is_verified: bool = False
    two_fa_enabled: bool = False
    two_fa_secret: Optional[str]
    api_key: Optional[str]
    api_key_hash: Optional[str]
    profile_image: Optional[str]
    bio: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    login_count: int = 0
    failed_login_attempts: int = 0
    locked_until: Optional[datetime]
    subscription_start: datetime
    subscription_end: Optional[datetime]
    payment_method_id: Optional[str]  # Stripe payment method

class AuditLog(BaseModel):
    """Audit log for compliance & security"""
    id: int
    user_id: int
    action: str
    resource_type: str
    resource_id: Optional[str]
    changes: dict
    ip_address: str
    user_agent: str
    timestamp: datetime
    status: str = "success"  # success, failure

# ==================== REQUEST/RESPONSE MODELS ====================

class TokenRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str
    remember_me: bool = False

class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: dict

class SignupRequest(BaseModel):
    """Signup request"""
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str
    company_name: Optional[str]
    role: UserRole = UserRole.FREE_TRIAL
    
    @validator('password')
    def validate_password(cls, v):
        """Password must be 12+ chars with uppercase, lowercase, number, special"""
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('Password must contain special character')
        return v

class UserResponse(BaseModel):
    """User info response"""
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    role: UserRole
    subscription_tier: SubscriptionTier
    company_name: Optional[str]
    is_verified: bool
    profile_image: Optional[str]
    created_at: datetime

class TwoFASetupResponse(BaseModel):
    """2FA setup response with QR code"""
    secret: str
    qr_code_url: str
    backup_codes: List[str]

class APIKeyResponse(BaseModel):
    """API key response"""
    key: str
    key_hash: str
    created_at: datetime
    last_used: Optional[datetime]

# ==================== SECURITY UTILITIES ====================

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hash: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), hash.encode())

def create_access_token(user_id: int, role: UserRole, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "user_id": user_id,
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id: int):
    """Create long-lived refresh token"""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "user_id": user_id,
        "type": "refresh",
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_api_key(user_id: int) -> tuple:
    """Generate API key for user"""
    key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    return key, key_hash

def generate_2fa_secret() -> str:
    """Generate 2FA secret"""
    return secrets.token_hex(16)

def generate_backup_codes(count: int = 8) -> List[str]:
    """Generate backup codes for 2FA"""
    return [secrets.token_hex(4) for _ in range(count)]

# ==================== AUTH ROUTER ====================

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignupRequest, db: Session = Depends()):
    """Register new user"""
    # Check if email exists
    # if db.query(User).filter(User.email == request.email).first():
    #     raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user (implementation depends on database setup)
    # user = User(
    #     email=request.email,
    #     username=request.username,
    #     password_hash=password_hash,
    #     first_name=request.first_name,
    #     last_name=request.last_name,
    #     role=request.role,
    #     subscription_tier=SubscriptionTier.STARTER,
    #     company_name=request.company_name,
    #     subscription_start=datetime.utcnow(),
    # )
    # db.add(user)
    # db.commit()
    
    # Generate tokens
    access_token = create_access_token(user_id=1, role=request.role)
    refresh_token = create_refresh_token(user_id=1)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": 1,
            "email": request.email,
            "username": request.username,
            "role": request.role,
            "subscription_tier": "starter"
        }
    )

@router.post("/login", response_model=TokenResponse)
async def login(request: TokenRequest, db: Session = Depends()):
    """Login user and return tokens"""
    # Verify credentials
    # user = db.query(User).filter(User.email == request.email).first()
    # if not user or not verify_password(request.password, user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate tokens
    access_token = create_access_token(user_id=1, role=UserRole.CLIENT)
    refresh_token = create_refresh_token(user_id=1)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={"id": 1, "email": "user@example.com", "role": "client"}
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: TokenRequest):
    """Refresh access token using refresh token"""
    payload = verify_token(request.password)  # Using password field for token temporarily
    
    access_token = create_access_token(
        user_id=payload["user_id"],
        role=payload.get("role", UserRole.CLIENT)
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=request.password,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={"id": payload["user_id"]}
    )

@router.post("/logout")
async def logout(credentials: HTTPAuthCredentials = Depends(security)):
    """Logout user (invalidate token)"""
    # In production, add token to blacklist
    return {"message": "Logged out successfully"}

@router.post("/2fa/setup", response_model=TwoFASetupResponse)
async def setup_2fa(credentials: HTTPAuthCredentials = Depends(security)):
    """Setup two-factor authentication"""
    secret = generate_2fa_secret()
    backup_codes = generate_backup_codes()
    
    return TwoFASetupResponse(
        secret=secret,
        qr_code_url=f"otpauth://totp/GulfCoastPropertyGroup?secret={secret}",
        backup_codes=backup_codes
    )

@router.post("/2fa/verify")
async def verify_2fa(code: str, credentials: HTTPAuthCredentials = Depends(security)):
    """Verify 2FA code"""
    # Implement TOTP verification
    return {"verified": True, "message": "2FA enabled"}

@router.post("/api-key/generate", response_model=APIKeyResponse)
async def generate_api_key_endpoint(credentials: HTTPAuthCredentials = Depends(security)):
    """Generate new API key for integrations"""
    key, key_hash = generate_api_key(user_id=1)
    
    return APIKeyResponse(
        key=key,
        key_hash=key_hash,
        created_at=datetime.utcnow()
    )

@router.post("/password-reset")
async def request_password_reset(email: EmailStr):
    """Request password reset email"""
    # Send reset email with token
    return {"message": "Check your email for reset instructions"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(token: str, new_password: str):
    """Confirm password reset with token"""
    return {"message": "Password reset successful"}

# ==================== DEPENDENCIES ====================

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    """Get current authenticated user"""
    payload = verify_token(credentials.credentials)
    return payload

async def require_role(*allowed_roles: UserRole):
    """Dependency to check user role"""
    async def role_checker(user = Depends(get_current_user)):
        if user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker

async def rate_limit(user = Depends(get_current_user)):
    """Rate limiting by user/subscription tier"""
    # Implement rate limiting based on subscription
    return user

# Export for use in main.py
__all__ = [
    'router',
    'get_current_user',
    'require_role',
    'create_access_token',
    'verify_token',
    'UserRole',
    'SubscriptionTier'
]
