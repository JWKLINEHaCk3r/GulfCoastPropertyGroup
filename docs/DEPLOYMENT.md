"""
# DEPLOYMENT GUIDE

## Development Environment

### Quick Start

```bash
python quickstart.py
```

This script will:
1. Setup virtual environment
2. Install dependencies
3. Initialize database
4. Start FastAPI server

Server runs on `http://localhost:8000`
API Docs available at `http://localhost:8000/docs`

---

## Docker Deployment

### Build and Run

```bash
# Build all images
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

**Services**:
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- API: `http://localhost:8000`

### Stop Services

```bash
docker-compose down
```

---

## Production Deployment (Linux/Ubuntu)

### 1. System Setup

```bash
sudo apt update
sudo apt install python3.11 python3-pip postgresql redis-server nginx
```

### 2. Application Setup

```bash
cd /opt
sudo git clone <repo> realestate-ecosystem
cd realestate-ecosystem

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Setup environment
sudo cp .env.example /opt/realestate-ecosystem/.env
sudo nano .env  # Edit with production values
```

### 3. PostgreSQL Setup

```bash
sudo -u postgres psql
CREATE DATABASE realestate;
CREATE USER realestate WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE realestate TO realestate;
\\q

# Verify connection
psql -U realestate -d realestate -h localhost
```

### 4. Redis Setup

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server

# Test connection
redis-cli ping
# Should return: PONG
```

### 5. Systemd Service

Create `/etc/systemd/system/realestate.service`:

```ini
[Unit]
Description=Real Estate AI Ecosystem
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/realestate-ecosystem

Environment="PATH=/opt/realestate-ecosystem/venv/bin"
ExecStart=/opt/realestate-ecosystem/venv/bin/uvicorn \\
    app.main:app \\
    --host 127.0.0.1 \\
    --port 8000 \\
    --workers 4

Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6. Nginx Configuration

Create `/etc/nginx/sites-available/realestate`:

```nginx
upstream realestate_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name realestate.example.com;

    location / {
        proxy_pass http://realestate_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://realestate_api/api/;
    }

    # SSL configuration (use certbot)
    # listen 443 ssl;
    # ssl_certificate /etc/letsencrypt/live/realestate.example.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/realestate.example.com/privkey.pem;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/realestate /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. Start Application

```bash
sudo systemctl enable realestate
sudo systemctl start realestate
sudo systemctl status realestate

# View logs
journalctl -u realestate -f
```

---

## AWS Deployment

### Option 1: ECS (Recommended for scale)

```bash
# Push image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker tag realestate-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/realestate:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/realestate:latest

# Create ECS task definition
# Create ECS service
# Create load balancer
# Point domain to load balancer
```

### Option 2: Elastic Beanstalk

```bash
pip install awseb

eb init -p docker realestate-ecosystem
eb create realestate-env
eb deploy

# Access application
eb open
```

### Option 3: EC2 (Simple, cheaper for small scale)

Use Linux/Ubuntu setup above on EC2 instance

---

## Google Cloud Deployment

### Cloud Run (Serverless)

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/realestate-backend

# Deploy
gcloud run deploy realestate-backend \\
  --image gcr.io/PROJECT_ID/realestate-backend \\
  --platform managed \\
  --region us-central1 \\
  --set-env-vars DATABASE_URL=postgresql://...,REDIS_URL=redis://...

# Setup Cloud SQL Proxy for database connection
```

---

## Monitoring & Logging

### Application Monitoring

```bash
# Install monitoring tools
pip install prometheus-client

# Monitor at: http://localhost:9090
```

### Log Aggregation

```bash
# Install ELK stack or use cloud service
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.0.0
```

### Health Checks

```bash
curl http://localhost:8000/api/v1/health
# Response: {"status": "healthy", ...}
```

---

## Performance Optimization

### Database
- Vacuum: `VACUUM ANALYZE;`
- Connection pool size: 20-40
- Max overflow: 40-80

### Application
- Worker processes: 4 (CPU count)
- Request timeout: 30 seconds
- Keep-alive timeout: 65 seconds

### Caching
- Lead searches: 1 hour
- Buyer profiles: 24 hours
- Comps data: 7 days

---

## Backup & Recovery

### PostgreSQL Backups

```bash
# Daily backup
pg_dump -U realestate realestate > /backups/realestate-$(date +\\%Y-\\%m-\\%d).sql

# Automated with cron
0 2 * * * pg_dump -U realestate realestate > /backups/realestate-$(date +\\%Y-\\%m-\\%d).sql

# Restore
psql -U realestate realestate < /backups/realestate-2025-02-13.sql
```

### Redis Backups

```bash
# Auto-saved to /var/lib/redis/dump.rdb
# Or manually: redis-cli BGSAVE
```

---

## Security Hardening

### Application
- ✅ Use HTTPS (Let's Encrypt)
- ✅ Set CORS properly
- ✅ Validate all inputs
- ✅ Use environment variables for secrets

### Database
- ✅ Strong passwords
- ✅ Restrict network access
- ✅ Enable SSL connections
- ✅ Regular backups

### Server
- ✅ Firewall rules (ufw)
- ✅ SSH key authentication
- ✅ Disable root login
- ✅ Regular updates

---

## Scaling Considerations

### Horizontal Scaling

1. **Multiple API Servers**
   - Use load balancer (ELB, HAProxy, Nginx)
   - Each runs uvicorn with 4 workers
   - Share database and Redis

2. **Database Scaling**
   - Read replicas for read-heavy operations
   - Connection pooling (PgBouncer)
   - Partitioning large tables (leads, interactions)

3. **Background Jobs**
   - Use Celery for data pipelines
   - Separate worker nodes
   - Distributed task queue

---

This guide covers development through production deployment. Adjust based on your hosting platform.
"""
