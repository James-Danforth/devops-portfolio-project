#!/bin/bash

# Setup Kind Kubernetes Cluster for DevOps Project
set -e

echo "🚀 Setting up Kind Kubernetes cluster for DevOps project..."

# Create Kind cluster configuration
cat << EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: 3000
    protocol: TCP
  - containerPort: 30001
    hostPort: 5000
    protocol: TCP
  - containerPort: 30002
    hostPort: 9090
    protocol: TCP
  - containerPort: 30003
    hostPort: 3001
    protocol: TCP
- role: worker
- role: worker
EOF

# Create Kind cluster
echo "📦 Creating Kind cluster..."
kind create cluster --name devops-project --config kind-config.yaml

# Wait for cluster to be ready
echo "⏳ Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=300s

# Install metrics server
echo "📊 Installing metrics server..."
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Install Prometheus and Grafana using Helm
echo "📈 Installing Prometheus and Grafana..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.ruleSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.probeSelectorNilUsesHelmValues=false

echo "✅ Kind cluster setup complete!"
echo "🔍 Cluster info:"
kubectl cluster-info
echo "📋 Nodes:"
kubectl get nodes
echo "📊 Pods in monitoring namespace:"
kubectl get pods -n monitoring

echo ""
echo "🎯 Next steps:"
echo "1. Run: kubectl apply -f k8s/ (to deploy the application)"
echo "2. Run: kubectl port-forward svc/frontend-service 3000:80"
echo "3. Run: kubectl port-forward svc/backend-service 5000:5000"
echo "4. Access Grafana: kubectl port-forward svc/prometheus-grafana 3001:80"
echo "   Username: admin, Password: prom-operator" 