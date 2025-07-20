# Ultimate DevOps Portfolio Project

A comprehensive local DevOps pipeline with Kubernetes deployment, CI/CD, monitoring, and security scanning.

## Project Overview

This project demonstrates a complete DevOps workflow including:
- **Microservices Architecture**: Frontend + Backend + Database
- **Containerization**: Docker with multi-stage builds
- **CI/CD Pipeline**: GitHub Actions with automated testing and deployment
- **Infrastructure as Code**: Terraform for Kubernetes cluster management
- **Monitoring**: Prometheus + Grafana for observability
- **Security**: Trivy vulnerability scanning
- **GitOps**: ArgoCD for declarative deployments

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   (React)       │◄──►│   (Flask API)   │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Frontend  │  │   Backend   │  │  PostgreSQL │          │
│  │   Service   │  │   Service   │  │   Service   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring Stack                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Prometheus │  │   Grafana   │  │   ArgoCD    │          │
│  │   Metrics   │  │  Dashboards │  │   GitOps    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Application Layer
- **Frontend**: React.js with TypeScript
- **Backend**: Flask (Python) REST API
- **Database**: PostgreSQL

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Kind)
- **Infrastructure as Code**: Terraform
- **GitOps**: ArgoCD

### CI/CD
- **Pipeline**: GitHub Actions
- **Container Registry**: GitHub Container Registry (GHCR)
- **Security Scanning**: Trivy

### Monitoring & Observability
- **Metrics**: Prometheus
- **Visualization**: Grafana
- **Logging**: Fluentd (optional)

## Project Structure

```
devops-portfolio-project/
├── frontend/                 # React frontend application
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── backend/                  # Flask backend API
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/                     # Kubernetes manifests
│   ├── namespaces/
│   ├── deployments/
│   ├── services/
│   ├── configmaps/
│   └── secrets/
├── terraform/               # Infrastructure as Code
│   ├── modules/
│   ├── environments/
│   └── main.tf
├── monitoring/              # Monitoring stack
│   ├── prometheus/
│   ├── grafana/
│   └── dashboards/
├── .github/workflows/       # CI/CD pipelines
│   ├── ci-cd.yml
│   ├── security-scan.yml
│   └── deploy.yml
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
└── docker-compose.yml       # Local development
```

## Quick Start

### Prerequisites
- Docker Desktop
- kubectl
- Kind (Kubernetes in Docker)
- Terraform
- Node.js 18+
- Python 3.9+

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd devops-portfolio-project
```

### 2. Local Development
```bash
# Start local development environment
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# Grafana: http://localhost:3001
```

### 3. Kubernetes Deployment
```bash
# Create Kind cluster
kind create cluster --name devops-project

# Deploy with Terraform
cd terraform
terraform init
terraform apply

# Deploy ArgoCD (optional)
kubectl apply -f monitoring/argocd/
```

### 4. Access Services
```bash
# Port forward services
kubectl port-forward svc/frontend-service 3000:80
kubectl port-forward svc/backend-service 5000:80
kubectl port-forward svc/grafana-service 3001:80
```

## CI/CD Pipeline

The GitHub Actions workflow includes:
1. **Code Quality**: Linting and formatting
2. **Testing**: Unit and integration tests
3. **Security**: Trivy vulnerability scanning
4. **Build**: Docker image creation
5. **Deploy**: Automatic deployment to Kubernetes

## Monitoring

- **Prometheus**: Metrics collection
- **Grafana**: Dashboard visualization
- **Custom Metrics**: Application-specific metrics
- **Alerts**: Basic alerting rules

## Security Features

- **Container Scanning**: Trivy integration
- **Dependency Scanning**: GitHub Dependabot
- **Secret Management**: Kubernetes secrets
- **Network Policies**: Pod-to-pod communication rules

## What You'll Learn

✅ **Containerization**: Multi-stage Docker builds
✅ **Kubernetes**: Pods, Services, Deployments, ConfigMaps
✅ **CI/CD**: GitHub Actions workflows
✅ **Infrastructure as Code**: Terraform modules
✅ **Monitoring**: Prometheus + Grafana setup
✅ **Security**: Vulnerability scanning and best practices
✅ **GitOps**: Declarative deployments with ArgoCD

## Resume Highlights

This project demonstrates:
- **Real-world DevOps skills** with production-like workflows
- **Full-stack development** with modern technologies
- **Infrastructure automation** using industry-standard tools
- **Security-first approach** with automated scanning
- **Monitoring and observability** best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details