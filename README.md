# CryptoTracker

A microservices-based application for cryptocurrency tracking and user management. Built with Flask, PostgreSQL, and deployed to Azure Kubernetes Service (AKS).

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Services](#services)
- [Creating New Services](#creating-new-services)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Development](#development)

---

## Project Overview

CryptoTracker is a modular microservices application designed to be scalable and cloud-native. It uses:

- **Microservices Architecture**: Independent services communicating via REST APIs
- **Containerization**: Docker for consistent environments
- **Orchestration**: Kubernetes on Azure (AKS) for production deployment
- **In-Cluster Database**: PostgreSQL running as a Kubernetes service
- **API Gateway**: NGINX Ingress for external traffic routing

**Current Services:**
- **User Service**: REST API for user management (CRUD, authentication)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    External Client                      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────┐
│            NGINX Ingress Controller (Public IP)         │
│              Routes /api/users → userservice            │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│    Microservices (Kubernetes Deployments)               │
│    - User Service (Flask, 2 replicas)                   │
│    - More services coming...                            │
└────────────────────────┬────────────────────────────────┘
                         │ Internal service-to-service
                         ▼
┌─────────────────────────────────────────────────────────┐
│      PostgreSQL (In-Cluster Service)                    │
│      - Persistent storage (Azure Disk)                  │
│      - Single pod with high availability setup          │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.14 | Application logic |
| **Web Framework** | Flask | REST API server |
| **Database** | PostgreSQL 16 | Data persistence |
| **ORM** | SQLAlchemy | Database abstraction |
| **Auth** | Flask-Bcrypt | Password hashing |
| **Containerization** | Docker | Container images |
| **Container Registry** | Azure Container Registry (ACR) | Image storage |
| **Orchestration** | Kubernetes (AKS) | Production deployment |
| **Ingress** | NGINX Ingress Controller | External traffic routing |

---

## Quick Start

### Local Development (Docker Compose)

```bash
# Start services locally
docker-compose up

# Services available at:
# - User Service: http://localhost:5001
```

### Kubernetes Deployment (AKS)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

```bash
# Quick summary:
az aks get-credentials --resource-group crypto-tracker --name Crypto-tracker
kubectl apply -f infrastructure/kubernetes/storage/postgres-pvc.yaml
kubectl apply -f infrastructure/kubernetes/deployments/postgres-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/postgres-service.yaml
kubectl apply -f infrastructure/kubernetes/deployments/userservice-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/userservice-service.yaml
kubectl apply -f infrastructure/kubernetes/ingress/ingress.yaml
```

---

## Creating New Services

### Step 1: Create Service Directory Structure

```bash
mkdir -p services/yourService/app
cd services/yourService
```

### Step 2: Create Flask Application

**`services/yourService/run.py`** - Entry point:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)  # Use unique port
```

**`services/yourService/app/__init__.py`** - App factory:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://dev_user:dev_password@postgres:5432/microservices_db'
    )
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
```

**`services/yourService/app/models.py`** - Database models:
```python
from app import db
from datetime import datetime

class YourModel(db.Model):
    __tablename__ = 'your_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
```

**`services/yourService/app/routes.py`** - API endpoints:
```python
from flask import Blueprint, request, jsonify
from app import db
from app.models import YourModel

main = Blueprint('main', __name__)

@main.route('/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({'status': 'healthy', 'database': db_status}), 200

@main.route('/api/items', methods=['GET'])
def get_items():
    items = YourModel.query.all()
    return jsonify({'items': [item.to_dict() for item in items]}), 200

@main.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = YourModel(name=data.get('name'))
    db.session.add(item)
    db.session.commit()
    return jsonify({'item': item.to_dict()}), 201
```

### Step 3: Create Requirements File

**`services/yourService/requirements.txt`**:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Bcrypt==1.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

### Step 4: Create Dockerfile

**`services/yourService/Dockerfile`**:
```dockerfile
FROM python:3.14.1-alpine3.23

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "run:app"]
```

### Step 5: Create Kubernetes Manifests

Create manifests in `infrastructure/kubernetes/`:

**Deployment** (`deployments/yourservice-deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yourservice
spec:
  replicas: 2
  selector:
    matchLabels:
      app: yourservice
  template:
    metadata:
      labels:
        app: yourservice
    spec:
      containers:
      - name: yourservice
        image: cryptotracker.azurecr.io/yourservice:latest
        ports:
        - containerPort: 5002
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: database-url
```

**Service** (`services/yourservice-service.yaml`):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: yourservice
spec:
  type: ClusterIP
  selector:
    app: yourservice
  ports:
  - port: 80
    targetPort: 5002
```

### Step 6: Build and Push to ACR

```bash
az acr login --name cryptotracker
docker build -t cryptotracker.azurecr.io/yourservice:latest ./services/yourService
docker push cryptotracker.azurecr.io/yourservice:latest
```

### Step 7: Deploy to Kubernetes

```bash
kubectl apply -f infrastructure/kubernetes/deployments/yourservice-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/yourservice-service.yaml

# Update ingress to route to the new service (optional)
```

---

## Kubernetes Deployment

### Prerequisites

- Azure CLI
- kubectl
- Docker
- Azure subscription with resource group in Norway East
- Azure Container Registry (ACR)

### Quick Deployment

For detailed step-by-step instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).

```bash
# 1. Set variables
$RESOURCE_GROUP="crypto-tracker"
$AKS_NAME="Crypto-tracker"

# 2. Get cluster credentials
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_NAME

# 3. Deploy PostgreSQL
kubectl apply -f infrastructure/kubernetes/storage/postgres-pvc.yaml
kubectl apply -f infrastructure/kubernetes/deployments/postgres-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/postgres-service.yaml

# 4. Deploy services
kubectl apply -f infrastructure/kubernetes/deployments/userservice-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/userservice-service.yaml

# 5. Deploy ingress
kubectl apply -f infrastructure/kubernetes/ingress/ingress.yaml
```

### Useful kubectl Commands

```bash
# View all resources
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get ingress

# View logs
kubectl logs -f deployment/userservice

# Scale deployment
kubectl scale deployment/userservice --replicas=3

# Restart deployment
kubectl rollout restart deployment/userservice

# Port forward (debug)
kubectl port-forward service/userservice 8080:80
```

### Manifest Reference

See [`infrastructure/kubernetes/README.md`](infrastructure/kubernetes/README.md) for detailed information about:
- ConfigMaps (configuration)
- Deployments (pod management)
- Services (networking)
- Storage (persistent volumes)
- Ingress (external routing)

---

## Development

### Project Structure

```
CryptoTracker/
├── services/
│   ├── userService/           # User management microservice
│   │   ├── app/
│   │   │   ├── __init__.py    # App factory
│   │   │   ├── models.py      # Database models
│   │   │   ├── routes.py      # API endpoints
│   │   └── run.py             # Entry point
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── (more services...)
├── infrastructure/
│   └── kubernetes/            # Kubernetes manifests
│       ├── deployments/
│       ├── services/
│       ├── storage/
│       ├── configmaps/
│       ├── ingress/
│       └── README.md
├── docker-compose.yml         # Local development
├── DEPLOYMENT_GUIDE.md        # AKS deployment guide
└── README.md                  # This file
```

### Local Development

```bash
# Start all services locally
docker-compose up

# Access services
curl http://localhost:5001/api/users  # User Service
```
---

## Environment Variables

Services use the following environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `postgresql://dev_user:dev_password@postgres:5432/microservices_db` | Database connection string |
| `FLASK_ENV` | `production` | Flask environment |

For Kubernetes, these are injected via Secrets and ConfigMaps.

---

## Support

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md).
For Kubernetes manifest details, see [infrastructure/kubernetes/README.md](infrastructure/kubernetes/README.md).