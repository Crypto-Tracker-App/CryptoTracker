# Kubernetes Manifests for CryptoTracker AKS Deployment

## Overview

This directory contains Kubernetes manifests for deploying the CryptoTracker microservices architecture to Azure Kubernetes Service (AKS) in Norway East. The application uses:
- **User Service**: Flask-based REST API for user management (CRUD operations, authentication)
- **PostgreSQL**: In-cluster database for data persistence
- **NGINX Ingress**: Routes external traffic to services

---

## Manifest Files

### 📦 ConfigMaps
- Store non-sensitive configuration (environment variables, config files)
- Used by pods to read application settings
- Easy to update without rebuilding container images

### 🚀 Deployments
- Define how to run application pods (replicas, image, resources)
- Manage pod lifecycle (creation, updates, rollbacks)
- Include health checks (liveness and readiness probes)

### 🌐 Services
- Expose pods internally (ClusterIP) or externally (LoadBalancer, NodePort)
- Handle load balancing across pod replicas
- Provide stable DNS names for pod-to-pod communication

### 💾 Storage
- PersistentVolumeClaims request persistent storage from the cluster
- Data survives pod restarts and rescheduling
- Automatically provisions cloud storage (Azure Disk)

### 🚪 Ingress
- Route external HTTP(S) traffic to services
- Path-based or host-based routing rules
- Can add TLS, rate limiting, authentication

---

## Quick Reference: kubectl Commands

```bash
# View all resources
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get pvc
kubectl get ingress

# View logs
kubectl logs -f deployment/userservice
kubectl logs -f deployment/postgres

# Describe a pod
kubectl describe pod <pod-name>

# Port forward (debug)
kubectl port-forward service/userservice 8080:80

# Scale deployment
kubectl scale deployment/userservice --replicas=3

# Restart deployment
kubectl rollout restart deployment/userservice
```