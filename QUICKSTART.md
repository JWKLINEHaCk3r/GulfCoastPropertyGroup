"""
# GETTING STARTED - QUICK REFERENCE

## 5-Minute Setup

### 1. Clone & Setup
```bash
cd real-estate-ecosystem
python quickstart.py

# Follow prompts to edit .env file
```

### 2. Start Server
```bash
# Backend runs on localhost:8000
# API docs available at http://localhost:8000/docs
```

### 3. Try API Calls

**Search for Leads**:
```bash
curl -X POST "http://localhost:8000/api/v1/leads/search" \\
  -H "Content-Type: application/json" \\
  -d '{
    "search_type": "fsbo",
    "location": "Los Angeles, CA"
  }'
```

**Generate Offer**:
```bash
curl -X POST "http://localhost:8000/api/v1/offers/generate" \\
  -H "Content-Type: application/json" \\
  -d '{
    "lead_id": "lead_123",
    "property_details": {
      "estimated_after_repair_value": 400000,
      "estimated_repair_cost": 50000,
      "address": "123 Main St"
    }
  }'
```

**Generate SEO Content**:
```bash
curl -X POST "http://localhost:8000/api/v1/seo/generate" \\
  -H "Content-Type: application/json" \\
  -d '{
    "content_type": "landing_page",
    "keyword": "sell house fast",
    "location": "Los Angeles, CA"
  }'
```

---

## Core Concepts

### Leads
- Properties discovered from FSBO, tax delinquent, vacant, probate sources
- Scored 0-100 based on motivation indicators
- Auto-contacted with offers when score > 65

### Offers
- Optimized cash offers generated for each qualified lead
- Based on ARV, repair costs, market conditions
- Typically 25-35% below market value

### Buyers
- Cash investors who purchase properties at your listed price
- Notified of new deals matching their criteria
- Pay wholesale finder's fees (3-7% markup)

### Deals
- Property transactions from contract to closing
- You profit the difference between offer and buyer's price
- Typical profit: $10k-50k per deal

---

## System Features Already Built

### ✅ AI Agents
- LeadScout: Identifies and scores motivated sellers
- OfferGenerator: Creates optimized cash offers
- BuyerMatcher: Ranks qualified buyers
- NegotiationAssistant: Automates seller communications
- SEOContent: Generates organic traffic content

### ✅ APIs
- Lead search & management
- Offer generation & tracking
- Buyer profiles & notifications
- Deal management
- SEO content generation
- Health checks

### ✅ Database
- PostgreSQL with full schema
- Leads, offers, interactions, buyers, deals
- Automatic timestamps & status tracking

### ✅ Integrations (Skeleton)
- DocuSign (contract signing)
- Twilio (SMS)
- SendGrid (email)
- Zillow (property data)

### ✅ Data Pipelines
- FSBO listings ingestion
- Tax delinquent property pipelines
- Comparable sales analysis
- Buyer profile enrichment

---

## Next Steps to Operationalize

### Week 1: Configuration
- [ ] Add your OpenAI/Anthropic API keys to .env
- [ ] Configure DocuSign integration
- [ ] Setup Twilio account
- [ ] Create SendGrid account & API key

### Week 2: Data Integration
- [ ] Connect Zillow API for property data
- [ ] Setup county public records API access
- [ ] Configure MLS data feed
- [ ] Implement real data pipeline

### Week 3: Testing
- [ ] Test full workflow (lead → offer → buyer)
- [ ] Verify email/SMS delivery
- [ ] Test DocuSign contract signing
- [ ] Validate scoring accuracy

### Week 4: Launch
- [ ] Setup domain & SSL
- [ ] Deploy to production
- [ ] Create landing pages
- [ ] Start lead generation campaigns

---

## API Reference Quick Links

- **Full API Docs**: http://localhost:8000/docs (when server running)
- **Health Check**: GET /api/v1/health
- **Search Leads**: POST /api/v1/leads/search
- **Generate Offer**: POST /api/v1/offers/generate
- **List Buyers**: GET /api/v1/buyers
- **Generate Content**: POST /api/v1/seo/generate

---

## Common Commands

```bash
# Start development server
cd backend && python -m uvicorn app.main:app --reload

# Run with Docker
docker-compose up -d

# Install dependencies
pip install -r backend/requirements.txt

# Run tests
pytest backend/

# Database shell
psql -U realestate -d realestate

# Check Redis connection
redis-cli ping

# View logs
tail -f app.log
```

---

## Architecture at a Glance

```
User/API Call
    ↓
FastAPI Route
    ↓
Service (Business Logic)
    ↓
AI Agent (LLM)
    ↓
Database/External API
    ↓
Response
```

**Data Flow for Lead Search**:
1. POST /leads/search API called
2. LeadScout agent activated
3. Searches FSBO, tax delinquent, vacant, probate sources
4. Scores each lead (0-100)
5. Filters leads (≥65 score)
6. Returns top 20 leads
7. User can then generate offers

---

## Troubleshooting

**API not responding**:
- Check if backend server is running
- Verify port 8000 is not in use
- Check logs: `journalctl -u realestate -f`

**Database connection failed**:
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Test connection: `psql -U realestate -d realestate`

**API keys not working**:
- Verify .env file has correct keys
- Check API service status
- Test individually in Postman

---

## Support

- **Docs**: See /docs folder for detailed guides
- **API**: Interactive docs at http://localhost:8000/docs
- **Issues**: Debug using server logs
- **Email**: support@realestate-ai.com

---

**Ready to start? Run: `python quickstart.py`**

Happy wholesaling! 🚀
"""
