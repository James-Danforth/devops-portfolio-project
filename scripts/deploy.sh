#!/bin/bash

# Deploy DevOps Application to Kubernetes
set -e

echo "🚀 Deploying DevOps application to Kubernetes..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please ensure your cluster is running."
    exit 1
fi

echo "📦 Applying Kubernetes manifests..."

# Create namespace and resources
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/configmaps/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/

echo "⏳ Waiting for deployments to be ready..."

# Wait for deployments
kubectl rollout status deployment/postgres-deployment -n devops-app --timeout=300s
kubectl rollout status deployment/backend-deployment -n devops-app --timeout=300s
kubectl rollout status deployment/frontend-deployment -n devops-app --timeout=300s

echo "✅ Deployment complete!"

# Show deployment status
echo ""
echo "📊 Deployment Status:"
echo "====================="
kubectl get pods -n devops-app
echo ""
kubectl get services -n devops-app
echo ""
kubectl get pvc -n devops-app

echo ""
echo "🎯 Access your application:"
echo "=========================="
echo "Frontend: kubectl port-forward svc/frontend-service 3000:80 -n devops-app"
echo "Backend API: kubectl port-forward svc/backend-service 5000:5000 -n devops-app"
echo ""
echo "📈 Monitor your application:"
echo "============================"
echo "Grafana: kubectl port-forward svc/prometheus-grafana 3001:80 -n monitoring"
echo "Prometheus: kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring"
echo ""
echo "🔍 Check logs:"
echo "=============="
echo "Backend logs: kubectl logs -f deployment/backend-deployment -n devops-app"
echo "Frontend logs: kubectl logs -f deployment/frontend-deployment -n devops-app" 