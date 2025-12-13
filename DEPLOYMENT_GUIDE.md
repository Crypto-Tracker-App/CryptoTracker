# Azure Kubernetes Service (AKS) Deployment Guide

## 📋 Prerequisites

Before starting, ensure you have:

- **Azure CLI** installed and authenticated (`az login`)
- **kubectl** installed and configured
- **Docker** installed (for building container images)
- **Azure subscription** with sufficient credits
- **Resource group** created: `crypto-tracker` in Norway East
- **Azure Container Registry (ACR)** created: `cryptotracker.azurecr.io`
- **Git** for cloning/managing the repository
- **PowerShell** or **Bash** terminal

**Verify installations:**
```bash
az --version
kubectl version --client
docker --version
```

---

## 📋 Step-by-Step Instructions

### 0) Set variables
```bash
$RESOURCE_GROUP="crypto-tracker"
$LOCATION="norwayeast"
$ACR_NAME="cryptotracker"
$ACR_LOGIN_SERVER="cryptotracker.azurecr.io"
$AKS_NAME="Crypto-tracker"
$PG_PASSWORD="..." # Find it when running kubectl get secret db-secrets -o yaml
```

### 1) Create or update AKS and link ACR
> ACR already exists. Create AKS if needed, then attach ACR permissions.
```bash
# Create AKS (skip if it already exists)
az aks create \
	--resource-group $RESOURCE_GROUP \
	--name $AKS_NAME \
	--location $LOCATION \
	--node-count 2 \
	--enable-managed-identity \
	--attach-acr $ACR_NAME \
	--generate-ssh-keys

# If AKS already exists, attach ACR
az aks update \
	--resource-group $RESOURCE_GROUP \
	--name $AKS_NAME \
	--attach-acr $ACR_NAME

# Get cluster credentials (automatically creates ~/.kube/config)
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_NAME
```

### 2) Build and push the image to ACR
```bash
# Log in to ACR
az acr login --name $ACR_NAME

# Build and push (from repo root)
docker build -t $ACR_LOGIN_SERVER/userservice:latest ./services/userService
docker push $ACR_LOGIN_SERVER/userservice:latest
```

### 3) Create Kubernetes secrets and config
```bash
# Create secrets for PostgreSQL password and connection string
kubectl create secret generic db-secrets --from-literal=postgres-password="$PG_PASSWORD" --from-literal=database-url="postgresql://dev_user:$PG_PASSWORD@postgres:5432/microservices_db"

# Apply ConfigMap
kubectl apply -f infrastructure/kubernetes/configmaps/userservice-configmap.yaml
```

### 4) Deploy PostgreSQL to the cluster
```bash
# Deploy storage, PostgreSQL deployment, and service
kubectl apply -f infrastructure/kubernetes/storage/postgres-pvc.yaml
kubectl apply -f infrastructure/kubernetes/deployments/postgres-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/postgres-service.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
```

### 5) Deploy user service and ingress
```bash
kubectl apply -f infrastructure/kubernetes/deployments/userservice-deployment.yaml
kubectl apply -f infrastructure/kubernetes/services/userservice-service.yaml

# Install NGINX Ingress Controller (cloud provider manifest)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml

kubectl apply -f infrastructure/kubernetes/ingress/ingress.yaml
```

### 6) Verify
```bash
kubectl get pods
kubectl get services
kubectl get ingress

# Get ingress controller public IP
kubectl get service -n ingress-nginx ingress-nginx-controller
```

---

## What Each File Does:

### �️ [infrastructure/kubernetes/storage/postgres-pvc.yaml](infrastructure/kubernetes/storage/postgres-pvc.yaml)
- Requests 5Gi persistent storage for PostgreSQL data
- Uses Azure Disk (default storage class in AKS)

### 🐘 [infrastructure/kubernetes/deployments/postgres-deployment.yaml](infrastructure/kubernetes/deployments/postgres-deployment.yaml)
- Runs PostgreSQL 16 Alpine with persistent storage
- Database: microservices_db, User: dev_user
- Includes health probes for reliability

### 🗄️ [infrastructure/kubernetes/services/postgres-service.yaml](infrastructure/kubernetes/services/postgres-service.yaml)
- Exposes PostgreSQL within the cluster at `postgres:5432`

### 🔧 [infrastructure/kubernetes/deployments/userservice-deployment.yaml](infrastructure/kubernetes/deployments/userservice-deployment.yaml)
- Runs 2 replicas with resource requests/limits and health probes
- Uses your ACR image: cryptotracker.azurecr.io/userservice:latest
- Connects to in-cluster PostgreSQL

### 🌐 [infrastructure/kubernetes/services/userservice-service.yaml](infrastructure/kubernetes/services/userservice-service.yaml)
- Exposes the service internally on port 80 → container 5001

### ⚙️ [infrastructure/kubernetes/configmaps/userservice-configmap.yaml](infrastructure/kubernetes/configmaps/userservice-configmap.yaml)
- Non-sensitive configuration (Flask env, log level)

### 🔐 [infrastructure/kubernetes/secrets/db-secrets.yaml.template](infrastructure/kubernetes/secrets/db-secrets.yaml.template)
- Template for database credentials (do not commit the real secret)
- Now contains: postgres-password and database-url for in-cluster PostgreSQL

### 🚪 [infrastructure/kubernetes/ingress/ingress.yaml](infrastructure/kubernetes/ingress/ingress.yaml)
- Routes /api/users to the userservice via NGINX ingress
