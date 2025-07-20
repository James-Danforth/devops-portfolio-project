#!/bin/bash

# Initial Setup Script for DevOps Portfolio Project
set -e

echo "Welcome to the DevOps Portfolio Project!"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker installation..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if required tools are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker Desktop first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. Frontend development may not work locally."
    else
        print_success "Node.js is installed"
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. Backend development may not work locally."
    else
        print_success "Python 3 is installed"
    fi
    
    print_success "Prerequisites check completed"
}

# Build and start services
start_services() {
    print_status "Building and starting services with Docker Compose..."
    
    # Build images
    docker-compose build
    
    # Start services
    docker-compose up -d
    
    print_success "Services started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for backend
    print_status "Waiting for backend service..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
            print_success "Backend service is ready"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        print_warning "Backend service may not be ready yet. You can check manually."
    fi
    
    # Wait for frontend
    print_status "Waiting for frontend service..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend service is ready"
            break
        fi
        sleep 2
        timeout=$((timeout - 2))
    done
    
    if [ $timeout -le 0 ]; then
        print_warning "Frontend service may not be ready yet. You can check manually."
    fi
}

# Seed the database
seed_database() {
    print_status "Seeding database with sample data..."
    
    # Wait a bit for the database to be ready
    sleep 10
    
    # Run the seeding script
    if docker-compose exec -T backend python seed_data.py; then
        print_success "Database seeded successfully"
    else
        print_warning "Database seeding failed. You can run it manually later."
    fi
}

# Show service status
show_status() {
    print_status "Checking service status..."
    docker-compose ps
}

# Show access information
show_access_info() {
    echo ""
    echo "Setup Complete!"
    echo "==============="
    echo ""
    echo "Your DevOps Portfolio Project is now running!"
    echo ""
    echo "Access your application:"
    echo "   • Frontend: http://localhost:3000"
    echo "   • Backend API: http://localhost:5000"
    echo "   • API Health Check: http://localhost:5000/api/health"
    echo "   • Grafana: http://localhost:3001 (admin/admin)"
    echo "   • Prometheus: http://localhost:9090"
    echo ""
    echo "Useful commands:"
    echo "   • View logs: docker-compose logs -f"
    echo "   • Stop services: docker-compose down"
    echo "   • Restart services: docker-compose restart"
    echo "   • Rebuild services: docker-compose up --build"
    echo ""
    echo "Next steps:"
    echo "   1. Explore the application at http://localhost:3000"
    echo "   2. Check out the monitoring dashboards"
    echo "   3. Review the documentation in the docs/ folder"
    echo "   4. Set up Kubernetes cluster with: ./scripts/setup-kind.sh"
    echo ""
    echo "Documentation:"
    echo "   • README.md - Project overview"
    echo "   • docs/SETUP.md - Detailed setup guide"
    echo "   • docs/ARCHITECTURE.md - System architecture"
    echo "   • PROJECT_STATUS.md - Current status and next steps"
    echo ""
}

# Main execution
main() {
    echo "Starting initial setup..."
    echo ""
    
    check_docker
    check_prerequisites
    start_services
    wait_for_services
    seed_database
    show_status
    show_access_info
}

# Run main function
main "$@" 