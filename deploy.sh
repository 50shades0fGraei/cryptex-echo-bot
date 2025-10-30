#!/bin/bash

# Cryptex Echo Bot Deployment Script
# This script handles both cloud and local deployments

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is required but not installed."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker compose &> /dev/null; then
        print_error "Docker Compose is required but not installed."
        exit 1
    }
    
    # Check disk space
    available_space=$(df -BG . | awk 'NR==2 {print $4}' | tr -d 'G')
    if [ "$available_space" -lt 10 ]; then
        print_error "Insufficient disk space. 10GB required, ${available_space}GB available."
        exit 1
    fi
    
    print_success "System requirements met."
}

# Configure environment
setup_environment() {
    print_status "Setting up environment..."
    
    if [ ! -f .env ]; then
        cp .env.example .env
        print_status "Created .env file from template. Please edit with your settings."
        exit 1
    fi
    
    # Create necessary directories
    mkdir -p logs/pearl
    mkdir -p logs/royalty
    
    print_success "Environment configured."
}

# Deploy application
deploy_application() {
    print_status "Deploying Cryptex Echo Bot..."
    
    # Pull latest images
    docker compose pull
    
    # Build and deploy
    docker compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_success "Deployment successful!"
        print_status "Dashboard available at: http://localhost:3000"
        print_status "API available at: http://localhost:5050"
    else
        print_error "Deployment failed. Check logs with: docker compose logs"
        exit 1
    fi
}

# Monitor deployment
monitor_deployment() {
    print_status "Monitoring deployment..."
    
    # Check container health
    sleep 10
    if [ "$(docker compose ps --format '{{ .Status }}' | grep -c 'healthy')" -eq 2 ]; then
        print_success "All services are healthy."
    else
        print_error "Some services are not healthy. Check logs with: docker compose logs"
        exit 1
    fi
}

# Main deployment process
main() {
    print_status "Starting Cryptex Echo Bot deployment..."
    
    check_requirements
    setup_environment
    deploy_application
    monitor_deployment
    
    print_success "Deployment complete!"
    echo -e "\nImportant next steps:"
    echo "1. Configure your trading parameters in the dashboard"
    echo "2. Set up monitoring alerts"
    echo "3. Test with paper trading first"
    echo "4. Monitor the logs regularly"
    echo -e "\nThank you for choosing Cryptex Echo Bot!"
}

# Run deployment
main