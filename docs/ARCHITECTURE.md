"""
# ARCHITECTURE GUIDE

## System Components

### 1. Data Ingestion Layer

**Purpose**: Pull real estate data from multiple sources continuously

**Components**:
- FSBO Pipeline: Zillow, Craigslist, Facebook Marketplace
- Tax Delinquent Pipeline: County assessor databases
- Vacant Property Pipeline: Utility records, MLS indicators
- Probate Pipeline: Court records
- Comparable Sales Pipeline: MLS, Zillow, private sources

**Flow**:
```
Raw Data → Extract → Transform → Validate → Load → Database
 (APIs)    (agents)  (cleaning)  (quality)  (bulk)
```

**Frequency**: Real-time to daily depending on source

---

### 2. Lead Scoring Engine

**Input**: Property data + source information
**Process**: Multi-factor scoring algorithm
**Output**: Lead score 0-100

**Scoring Factors**:
```
Total Score = Source(20) + Age(15) + Condition(20) + Market(30) + Circumstances(15)
```

**Example Scores**:
- Tax delinquent + vacant + 2 years = 85 (hot lead)
- FSBO + listed 3 months = 70 (warm lead)
- Brand new listing = 40 (initial interest)

---

### 3. AI Agent Orchestration

**Architecture**: Multi-agent system with specialized agents

```
Input Request
    ↓
Orchestrator Routes to:
├─ LeadScout (finds leads)
├─ OfferGenerator (prices properties)
├─ BuyerMatcher (identifies buyers)
├─ NegotiationAssistant (handles communications)
└─ SEOContent (generates traffic)
    ↓
Results Aggregated
    ↓
Output to User/Database
```

**Agent Communication**: Shared database + message queues

---

### 4. Real Estate Valuation Model

**Approach**: Hybrid model combining multiple methods

```
Method 1: Comparable Sales (40% weight)
- Recent sales in 0.5-1 mile radius
- Adjust for size, condition, features
- Weight more recent sales higher

Method 2: 70/30 Rule (35% weight)
- For fix & flip: Offer = ARV * 0.70 - Repairs
- Proven in wholesale industry
- Accounts for buyer profit needs

Method 3: Market Trends (25% weight)
- Zone appreciation/depreciation
- Seasonal factors
- Supply/demand indicators

Final Valuation = (Method 1 × 0.40) + (Method 2 × 0.35) + (Method 3 × 0.25)
```

---

### 5. Offer Generation Process

**Timeline**: < 5 minutes from lead input

```
Lead Input (address, condition, source)
    ↓
1. Fetch comparable sales data
    ↓
2. Calculate After-Repair Value (ARV)
    ↓
3. Estimate repair costs (contractor database)
    ↓
4. Estimate holding costs (taxes, insurance, etc.)
    ↓
5. Apply wholesale fee (3-7%)
    ↓
6. Calculate offer price = ARV - Costs - Fees - Target ROI
    ↓
7. Generate contract with standard terms
    ↓
8. Create PDF & prepare for transmission
    ↓
Offer Ready for Delivery
```

**Offer Components**:
- Purchase price
- Contingencies (30-day inspection period)
- Closing timeline (10-14 days)
- Earnest money ($5k-25k)
- Terms & conditions

---

### 6. Buyer Matching Algorithm

**Purpose**: Get properties in front of most likely buyers

**Matching Factors**:
```
Match Score = 
  (State Match × 25%) +
  (Property Type Match × 20%) +
  (Deal Size Alignment × 20%) +
  (ROI Fit × 20%) +
  (Buyer Activity × 15%)
```

**Ranking**: 
1. Perfect match (95-100): All criteria met
2. Strong match (80-94): Minor mismatch
3. Fair match (60-79): Some interest likely
4. Weak match (<60): Probably pass

---

### 7. Communication Automation

**Channel Priority**:
1. Email (immediate, professional, documented)
2. SMS (urgent, high-attention)
3. Phone call (escalated, seller resistant)
4. Voicemail (fallback, follow-up)

**Automation Triggers**:
```
Initial Contact
    ↓ (No response in 2 hours)
SMS Reminder
    ↓ (No response in 5 hours)
Email Follow-up
    ↓ (No response in 24 hours)
SMS Follow-up #2
    ↓ (No response in 48 hours)
Objection Handler (if objection detected)
```

---

### 8. Contract & DocuSign Integration

**Workflow**:
```
Offer Generated
    ↓
PDF Contract Created (DocuSign-ready)
    ↓
Recipient Email Sent (personalized)
    ↓
Signature Requested
    ↓
Status Monitored in Real-time
    ↓
Signature Received
    ↓
Contract Stored in Database
    ↓
Seller marked as "Under Contract"
```

**Handling**: Everything automated except final signing

---

### 9. Real-time Dashboard

**Components**:
- Lead pipeline (new, contacted, negotiating, under contract, closed)
- Offer statistics (sent, signed, rejected)
- Cash buyer matching (active investors, recent buys)
- Revenue tracking (fees, deals closed, pipeline value)
- Performance metrics (response rates, closing timeline)

---

### 10. SEO & Content Strategy

**Organic Traffic Goals**: 1,000-5,000 visitors/month within 6 months

**Content Pillars**:
1. **"Sell Fast" Pages** - "Sell my house fast [City]" (commercial intent)
2. **Educational Content** - "How to sell house without agent" (informational)
3. **Problem/Solution** - "Inherited house don't know what to do" (emotional)
4. **Social Proof** - Case studies and testimonials
5. **FAQ Content** - Answer common homeowner questions

**SEO Metrics Target**:
- Domain Authority: 20+ (within 1 year)
- Organic keywords ranking: 100+ (6 months)
- Monthly organic traffic: 2,000+ (6 months)
- Click-through rate: 3-5% (from search results)

---

## Data Models

### Lead Entity
```python
{
  "id": "UUID",
  "address": "123 Main St",
  "city": "Los Angeles",
  "state": "CA",
  "zip_code": "90210",
  "property_type": "single_family|multi_family|commercial|vacant",
  "bedrooms": 3,
  "bathrooms": 2,
  "square_feet": 1500,
  "year_built": 1990,
  "market_value": 350000,
  "estimated_arv": 400000,
  "estimated_repair_cost": 50000,
  "seller_name": "John Doe",
  "seller_email": "john@email.com",
  "seller_phone": "555-0101",
  "data_source": "FSBO|Tax Delinquent|Zillow|Craigslist",
  "lead_score": 85.5,  # 0-100
  "lead_status": "new|qualified|contacted|negotiating|under_contract|closed|rejected",
  "created_at": "2025-02-13T00:00:00Z",
  "last_contacted": "2025-02-13T10:30:00Z"
}
```

### Offer Entity
```python
{
  "id": "UUID",
  "lead_id": "lead_UUID",
  "offer_price": 285000.00,
  "arv": 400000.00,
  "repair_cost": 50000.00,
  "holding_cost": 10000.00,
  "wholesale_fee": 15000.00,
  "projected_profit": 40000.00,
  "roi_percent": 14.0,
  "status": "draft|sent|signed|accepted|rejected",
  "contract_docusign_id": "envelope_UUID",
  "contract_url": "https://docusign.com/...",
  "created_at": "2025-02-13T00:00:00Z",
  "sent_at": "2025-02-13T00:05:00Z"
}
```

### Buyer Entity
```python
{
  "id": "UUID",
  "name": "John Smith Investments",
  "email": "john@example.com",
  "phone": "555-0101",
  "company": "John Smith Capital",
  "target_states": ["CA", "TX", "FL"],
  "min_deal_size": 100000,
  "max_deal_size": 3000000,
  "preferred_property_types": ["single_family", "multi_family"],
  "min_roi_percent": 20,
  "total_deals_completed": 45,
  "estimated_portfolio_value": 15000000,
  "is_active": true,
  "notification_method": "email|sms|both",
  "created_at": "2025-01-01T00:00:00Z",
  "last_activity": "2025-02-13T14:30:00Z"
}
```

---

## API Flow Diagram

```
Client Request
    ↓
FastAPI Route Handler
    ↓
Authentication (JWT)
    ↓
Request Validation (Pydantic)
    ↓
Service Layer (Business Logic)
    ↓
AI Agent (if needed)
    ↓
Database Query/Update
    ↓
Response Formatting
    ↓
Return to Client
```

---

## Error Handling

**Validation Errors**: 400 Bad Request
**Authentication Errors**: 401 Unauthorized
**Authorization Errors**: 403 Forbidden
**Not Found**: 404 Not Found
**Conflict**: 409 Conflict (duplicate, state conflict)
**Server Errors**: 500 Internal Server Error

```python
{
  "detail": "Error message",
  "status": "error",
  "timestamp": "2025-02-13T00:00:00Z",
  "trace_id": "request_UUID"  # For debugging
}
```

---

## Performance Optimization

**Caching Strategy**:
- Lead searches cached 1 hour (Redis)
- Buyer profiles cached 24 hours
- Property comps cached 7 days
- SEO content cached indefinitely

**Database Optimization**:
- Indexes on frequently queried fields (status, score, created_at)
- Batch inserts for lead pipelines
- Connection pooling (20 connections)
- Query optimization (explain plans)

**Rate Limiting**:
- API: 100 requests/minute per IP
- Data pipelines: Respectful rate limiting (2-5 sec delays)
- External APIs: Respect their limits, use queues

---

This architecture is designed for **scaling to 100+ deals/month** with minimal human intervention.
"""
