# Quick Start Guide

## Get Started in 5 Minutes

### 1. Prerequisites
- Docker Desktop installed and running
- Git installed

### 2. Clone and Setup
```bash
# Clone the repository (replace with your actual repo URL)
git clone <your-repo-url>
cd devops-portfolio-project

# On Windows, run the setup script
# On Linux/Mac, make scripts executable first:
# chmod +x scripts/*.sh
```

### 3. Start Everything
```bash
# Start all services
docker-compose up -d

# Seed the database with sample data
docker-compose exec backend python seed_data.py
```

### 4. Access Your Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## What You've Built

This is a **complete DevOps portfolio project** featuring:

### **Modern Microservices Architecture**
- React frontend with TypeScript
- Flask backend with RESTful API
- PostgreSQL database

### **Containerization & Orchestration**
- Multi-stage Docker builds
- Kubernetes deployment ready
- Docker Compose for local development

### **CI/CD Pipeline**
- GitHub Actions automation
- Security scanning with Trivy
- Automated testing and deployment

### **Monitoring & Observability**
- Prometheus metrics collection
- Grafana dashboards
- Application health monitoring

### **Infrastructure as Code**
- Terraform configuration
- Kubernetes manifests
- Automated provisioning

## Development Commands

### Local Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build
```

### Backend Development
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run locally
python app.py

# Run tests
python -m pytest tests/ -v
```

### Frontend Development
```bash
# Install dependencies
cd frontend
npm install

# Run locally
npm start

# Run tests
npm test
```

## Kubernetes Deployment

### Set Up Local Cluster
```bash
# Create Kind cluster
kind create cluster --name devops-project

# Deploy application
kubectl apply -f k8s/

# Port forward services
kubectl port-forward svc/frontend-service 3000:80 -n devops-app
kubectl port-forward svc/backend-service 5000:5000 -n devops-app
```

## Monitoring

### Access Monitoring Tools
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

### View Metrics
- Application metrics: `/api/metrics` endpoint
- Custom dashboards in Grafana
- Real-time monitoring

## Useful Scripts

### Windows
```powershell
# Initial setup
.\scripts\initial-setup.ps1

# Deploy to Kubernetes
.\scripts\deploy.ps1
```

### Linux/Mac
```bash
# Initial setup
./scripts/initial-setup.sh

# Deploy to Kubernetes
./scripts/deploy.sh
```

## Documentation

- **README.md** - Complete project overview
- **docs/SETUP.md** - Detailed setup instructions
- **docs/ARCHITECTURE.md** - System architecture
- **PROJECT_STATUS.md** - Current status and next steps

## Next Steps

1. **Explore the Application**: Visit http://localhost:3000
2. **Check Monitoring**: View dashboards in Grafana
3. **Review Code**: Examine the implementation
4. **Customize**: Add your own features
5. **Deploy**: Set up Kubernetes cluster
6. **Enhance**: Add more advanced features

## Portfolio Impact

This project demonstrates:
- Real-world DevOps skills
- Full-stack development
- Infrastructure automation
- Security best practices
- Monitoring and observability
- Modern CI/CD practices

---

**You now have a comprehensive DevOps portfolio that showcases industry-standard skills and practices!** 