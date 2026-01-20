# 🚀 Deployment Guide

## Overview

This guide covers multiple deployment options for Zero-Day Sentinel AI, from local development to cloud production.

---

## Option 1: Google Colab (Recommended for Demo)

### Advantages
✅ No local setup required  
✅ Free GPU/TPU access  
✅ Perfect for hackathon demos  
✅ Built-in secrets management  

### Steps

**1. Open Google Colab**
- Visit: https://colab.research.google.com/

**2. Install Dependencies (Cell 1)**
```bash
!pip install -q streamlit pyngrok pathway google-generativeai requests python-dateutil
```

**3. Configure Secrets (Sidebar)**
- Click 🔑 icon
- Add `GEMINI_API_KEY`
- Add `NGROK_AUTH_TOKEN`
- Toggle both to ON ✅

**4. Run Application (Cell 2)**
- Paste entire `zero_day_sentinel_pathway_core.py`
- Execute cell
- Click ngrok URL
- Click "Visit Site"

**5. Verify**
```
✅ ZERO-DAY SENTINEL AI IS LIVE!
🔗 URL: https://xxxx.ngrok-free.app
```

---

## Option 2: Local Development

### Prerequisites
- Python 3.9+
- pip or conda
- Terminal access

### Steps

**1. Clone/Download Repository**
```bash
git clone https://github.com/your-team/zero-day-sentinel-ai.git
cd zero-day-sentinel-ai
```

**2. Create Virtual Environment**
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# OR using conda
conda create -n zero-day python=3.9
conda activate zero-day
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment**
```bash
# Copy template
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use any text editor
```

**5. Run Application**
```bash
# Method 1: Direct execution (includes auto-launcher)
python zero_day_sentinel_pathway_core.py

# Method 2: Streamlit command (if extracted app code)
streamlit run app.py --server.port 8501
```

**6. Access**
- Open browser: http://localhost:8501
- Or use ngrok: https://your-ngrok-url.app

---

## Option 3: Docker Deployment

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY zero_day_sentinel_pathway_core.py .
COPY .env .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
CMD ["python", "zero_day_sentinel_pathway_core.py"]
```

### Build and Run

```bash
# Build image
docker build -t zero-day-sentinel:latest .

# Run container
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e NGROK_AUTH_TOKEN=$NGROK_AUTH_TOKEN \
  zero-day-sentinel:latest

# Or with docker-compose
docker-compose up -d
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  zero-day-sentinel:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - NGROK_AUTH_TOKEN=${NGROK_AUTH_TOKEN}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## Option 4: Cloud Deployment

### AWS EC2

**1. Launch Instance**
- AMI: Ubuntu 22.04
- Instance Type: t3.medium (recommended)
- Security Group: Allow port 8501

**2. SSH and Setup**
```bash
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/your-team/zero-day-sentinel-ai.git
cd zero-day-sentinel-ai

# Install dependencies
pip3 install -r requirements.txt

# Configure environment
nano .env  # Add your API keys

# Run with nohup (keeps running after logout)
nohup python3 zero_day_sentinel_pathway_core.py > app.log 2>&1 &
```

**3. Access**
- URL: `http://your-ec2-public-ip:8501`
- Or setup Elastic IP for permanent address

### Google Cloud Run

**1. Create `cloudbuild.yaml`**
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/zero-day-sentinel', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/zero-day-sentinel']

images:
  - 'gcr.io/$PROJECT_ID/zero-day-sentinel'
```

**2. Deploy**
```bash
# Build and deploy
gcloud builds submit --config cloudbuild.yaml
gcloud run deploy zero-day-sentinel \
  --image gcr.io/$PROJECT_ID/zero-day-sentinel \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY
```

### Azure Container Instances

```bash
# Create resource group
az group create --name zero-day-rg --location eastus

# Deploy container
az container create \
  --resource-group zero-day-rg \
  --name zero-day-sentinel \
  --image your-docker-hub/zero-day-sentinel:latest \
  --dns-name-label zero-day-demo \
  --ports 8501 \
  --environment-variables \
    GEMINI_API_KEY=$GEMINI_API_KEY \
    NGROK_AUTH_TOKEN=$NGROK_AUTH_TOKEN
```

---

## Option 5: Kubernetes Deployment

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zero-day-sentinel
spec:
  replicas: 2
  selector:
    matchLabels:
      app: zero-day-sentinel
  template:
    metadata:
      labels:
        app: zero-day-sentinel
    spec:
      containers:
      - name: app
        image: your-registry/zero-day-sentinel:latest
        ports:
        - containerPort: 8501
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: gemini-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: zero-day-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8501
  selector:
    app: zero-day-sentinel
```

---

## Production Considerations

### Security

**1. API Key Management**
- Use secret managers (AWS Secrets Manager, GCP Secret Manager)
- Rotate keys regularly
- Never commit keys to Git

**2. Network Security**
- Use HTTPS (setup SSL/TLS)
- Implement rate limiting
- Add authentication (OAuth, JWT)

**3. Application Security**
```python
# Add to Streamlit config
st.set_page_config(
    page_title="Zero-Day Sentinel",
    page_icon="🛡️",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': None,  # Disable help menu
        'Report a bug': None,  # Disable bug reporting
        'About': None  # Disable about section
    }
)
```

### Monitoring

**1. Application Monitoring**
```bash
# Add health check endpoint
curl http://localhost:8501/_stcore/health

# Monitor logs
tail -f app.log

# Resource usage
htop  # or top
```

**2. Pathway Metrics**
```python
# Add to code (if using Pathway Pro)
import pathway as pw
pw.monitoring.enable()
```

**3. Alerting**
- Setup CloudWatch/Stackdriver alerts
- Monitor error rates
- Track response times

### Scaling

**1. Horizontal Scaling**
- Multiple Streamlit instances behind load balancer
- Shared Pathway data store

**2. Vertical Scaling**
- Increase instance size
- More CPU/memory for heavy loads

**3. Caching**
```python
import streamlit as st

@st.cache_data(ttl=60)
def get_vulnerabilities():
    return engine.get_recent_vulnerabilities(100)
```

---

## Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port 8502
```

**2. API Key Errors**
```bash
# Verify environment variable
echo $GEMINI_API_KEY

# Re-export if needed
export GEMINI_API_KEY=your_key_here
```

**3. Pathway Import Errors**
```bash
# Reinstall Pathway
pip uninstall pathway
pip install pathway --break-system-packages
```

**4. ngrok Connection Failed**
```bash
# Check ngrok auth
ngrok config check

# Restart ngrok
pkill ngrok
# Run app again
```

---

## Performance Optimization

### 1. Caching Strategy
```python
@st.cache_resource
def init_pathway_engine():
    return PathwayStreamingEngine()

@st.cache_data(ttl=5)
def calculate_risk(tech_stack):
    return engine.calculate_risk_for_tech_stack(tech_stack)
```

### 2. Database Optimization
- Use connection pooling
- Implement query caching
- Optimize Pathway transformations

### 3. Frontend Optimization
- Lazy load heavy components
- Implement pagination
- Reduce auto-refresh frequency for large datasets

---

## Backup and Recovery

### Data Backup
```bash
# Backup event history
python -c "import json; from app import st; \
  json.dump(st.session_state.event_history, \
  open('backup.json', 'w'))"
```

### Disaster Recovery
- Regular snapshots (cloud instances)
- Automated backups (cron jobs)
- Multi-region deployment for HA

---

## Support

For deployment issues:
1. Check logs: `app.log` or Docker logs
2. Review environment variables
3. Verify network/firewall settings
4. Contact: [your-email@domain.com]

---

**Recommended for Hackathon:** Option 1 (Google Colab)  
**Recommended for Production:** Option 4 (Cloud) + Option 5 (Kubernetes)
