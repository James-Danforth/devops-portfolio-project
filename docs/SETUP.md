# 🚀 Setup Guide

This guide will walk you through setting up the complete DevOps portfolio project on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have the following tools installed:

### Required Tools
- **Docker Desktop** (v20.10+)
- **Git** (v2.30+)
- **Node.js** (v18+)
- **Python** (v3.9+)
- **kubectl** (v1.25+)
- **Kind** (v0.17+)
- **Terraform** (v1.0+)
- **Helm** (v3.10+)

### Optional Tools
- **Visual Studio Code** with extensions:
  - Docker
  - Kubernetes
  - Python
  - TypeScript and JavaScript

## 🛠️ Installation Guide

### 1. Install Docker Desktop
```bash
# Windows/macOS: Download from https://www.docker.com/products/docker-desktop
# Linux: Follow distribution-specific instructions
```

### 2. Install Node.js
```bash
# Using nvm (recommended)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Or download from https://nodejs.org/
```

### 3. Install Python
```bash
# Using pyenv (recommended)
curl https://pyenv.run | bash
pyenv install 3.9.0
pyenv global 3.9.0

# Or download from https://www.python.org/
```

### 4. Install kubectl
```bash
# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# macOS
brew install kubectl

# Windows
# Download from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

### 5. Install Kind
```bash
# Linux/macOS
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Windows
# Download from https://kind.sigs.k8s.io/dl/v0.17.0/kind-windows-amd64
```

### 6. Install Terraform
```bash
# Linux
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# macOS
brew install terraform

# Windows
# Download from https://www.terraform.io/downloads.html
```

### 7. Install Helm
```bash
# Linux/macOS
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Windows
# Download from https://helm.sh/docs/intro/install/
```

## 🚀 Quick Start

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd devops-portfolio-project
```

### Step 2: Set Up Local Development Environment
```bash
# Start all services with Docker Compose
docker-compose up -d

# Verify services are running
docker-compose ps
```

### Step 3: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

### Step 4: Set Up Kubernetes Cluster
```bash
# Run the setup script
chmod +x scripts/setup-kind.sh
./scripts/setup-kind.sh
```

### Step 5: Deploy to Kubernetes
```bash
# Deploy the application
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 🔧 Development Workflow

### Local Development
1. **Start Services**: `docker-compose up -d`
2. **Make Changes**: Edit code in your IDE
3. **Test Changes**: Services auto-reload
4. **Stop Services**: `docker-compose down`

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

## 🐳 Docker Commands

### Build Images
```bash
# Build backend
docker build -t devops-backend ./backend

# Build frontend
docker build -t devops-frontend ./frontend
```

### Run Containers
```bash
# Run backend
docker run -p 5000:5000 devops-backend

# Run frontend
docker run -p 3000:80 devops-frontend
```

## ☸️ Kubernetes Commands

### Cluster Management
```bash
# Create cluster
kind create cluster --name devops-project

# Delete cluster
kind delete cluster --name devops-project

# Get cluster info
kubectl cluster-info
```

### Application Deployment
```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n devops-app

# View logs
kubectl logs -f deployment/backend-deployment -n devops-app
```

### Port Forwarding
```bash
# Frontend
kubectl port-forward svc/frontend-service 3000:80 -n devops-app

# Backend
kubectl port-forward svc/backend-service 5000:5000 -n devops-app

# Grafana
kubectl port-forward svc/prometheus-grafana 3001:80 -n monitoring
```

## 🏗️ Terraform Commands

### Infrastructure Management
```bash
# Initialize Terraform
cd terraform
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Destroy infrastructure
terraform destroy
```

## 📊 Monitoring Setup

### Prometheus Configuration
1. Access Prometheus: http://localhost:9090
2. Check targets are up
3. Verify metrics collection

### Grafana Setup
1. Access Grafana: http://localhost:3001
2. Login: admin/admin
3. Import dashboards from `monitoring/dashboards/`

## 🔐 Security Configuration

### GitHub Secrets Setup
For CI/CD to work, add these secrets to your GitHub repository:

1. **KUBE_CONFIG**: Base64 encoded kubeconfig
```bash
kubectl config view --raw | base64
```

2. **GHCR_TOKEN**: GitHub Container Registry token
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Create token with `write:packages` permission

## 🚨 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Reset Docker
docker system prune -a
docker volume prune
```

#### Kubernetes Issues
```bash
# Reset Kind cluster
kind delete cluster --name devops-project
./scripts/setup-kind.sh
```

#### Port Conflicts
```bash
# Check what's using a port
lsof -i :3000
netstat -tulpn | grep :3000
```

#### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

### Logs and Debugging
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Kubernetes logs
kubectl logs -f deployment/backend-deployment -n devops-app
```

## 📚 Next Steps

1. **Customize the Application**: Modify the code to add your own features
2. **Add More Services**: Implement additional microservices
3. **Enhance Monitoring**: Create custom dashboards and alerts
4. **Security Hardening**: Implement additional security measures
5. **Production Deployment**: Deploy to a cloud provider
6. **Documentation**: Add more detailed documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs
3. Check GitHub Issues
4. Create a new issue with detailed information

---

**Happy coding! 🚀** 