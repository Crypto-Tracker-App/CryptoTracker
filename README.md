# Azure Crypto Tracker Application

A cryptocurrency monitoring and portfolio management platform built on Azure cloud services. This microservices-based application provides real-time crypto tracking, portfolio management, price alerts, and user authentication.

## Project Overview

The Crypto Tracker Application is a full-stack solution designed to help users monitor cryptocurrency prices, manage their portfolios, and receive alerts for price movements. Built with modern cloud-native technologies, the application is containerized and orchestrated using Kubernetes on Azure Kubernetes Service (AKS).

**Live Application:** [https://crypto-tracker.norwayeast.cloudapp.azure.com/](http://crypto-tracker.norwayeast.cloudapp.azure.com/)

## Languages & Technologies

- **Frontend:** React 18+ with Vite, JavaScript/JSX
- **Backend Services:** Python 3.9+ with Flask framework
- **Database:** PostgreSQL
- **Container Orchestration:** Kubernetes on Azure Kubernetes Service (AKS)
- **Container Registry:** Azure Container Registry (ACR)
- **Authentication:** JWT-based security system
- **API Documentation:** Swagger/OpenAPI with Flasgger

## Microservices Architecture

Each service is independently deployable and stored in its own module:

1. **User Service** (`user-service/`) - User authentication, registration, and profile management
2. **Alert Service** (`alert-service/`) - Cryptocurrency price alerts and notifications
3. **Portfolio Service** (`portfolio-service/`) - User portfolio tracking and management
4. **Pricing Service** (`pricing-service/`) - Real-time cryptocurrency pricing and market data

Microservices include:
- Flask REST API with Swagger documentation
- JWT authentication middleware
- Health check endpoints
- Comprehensive unit tests using pytest
- Docker containerization

## Frontend

The React-based frontend (`frontend/`) provides:
- User authentication and registration pages
- Real-time portfolio dashboard
- Price tracking interface
- Alert management system
- Responsive design with Vite build tooling

## Installation & Setup

### Prerequisites
- Docker and Docker Compose
- kubectl configured for AKS cluster access
- Python 3.9+
- Node.js 16+

### Local Development

1. Clone the repository
2. Navigate to each service directory and install dependencies:
   ```bash
   cd <service-name>
   pip install -r requirements.txt
   ```
3. For frontend development:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Docker Build & Push

Each service includes a Dockerfile:
```bash
docker build -t cryptotracker.azurecr.io/<service>:<tag> ./service-name
docker push cryptotracker.azurecr.io/<service>:<tag>
```

### Kubernetes Deployment

Deploy to AKS cluster:
```bash
kubectl apply -f infrastructure/k8s/base/
```

For overlays and environment-specific configurations:
```bash
kubectl apply -k infrastructure/k8s/overlays/<environment>/
```

## API Documentation

Each microservice provides Swagger/OpenAPI documentation accessible at `/apidocs/` endpoint. All endpoints support session-based or JWT authentication.

## Testing

Run service-specific tests:
```bash
pytest tests/
```

Frontend testing with Vitest:
```bash
cd frontend
npm run test
```

## Project Documentation

- [ARCHITECTURE_OVERVIEW.md](ARCHITECTURE_OVERVIEW.md) - Detailed system architecture and design patterns
- [SERVICE_ISOLATION.md](SERVICE_ISOLATION.md) - Service boundaries and communication patterns
- [CIRCUIT_BREAKER_DEMO.md](CIRCUIT_BREAKER_DEMO.md) - Resilience patterns documentation

## Support & Monitoring

The application integrates with Azure services for:
- Centralized logging and monitoring
- Performance tracking
- Error reporting and diagnostics

For issues or contributions, please refer to the individual service README files in their respective directories.

---

**Last Updated:** January 2026
