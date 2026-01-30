#!/bin/bash

# Helper script for kubectl-ai commands for cloud deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to get deployment status
get_deployment_status() {
    print_status "Checking deployment status..."
    kubectl get deployments -n todo-app
    kubectl get pods -n todo-app
    kubectl get services -n todo-app
}

# Function to scale deployment
scale_deployment() {
    local component=$1
    local replicas=$2

    if [ -z "$component" ] || [ -z "$replicas" ]; then
        print_error "Usage: $0 scale <backend|frontend> <replicas>"
        return 1
    fi

    local deployment_name="todo-app-${component}"
    print_status "Scaling $deployment_name to $replicas replicas..."
    kubectl scale deployment/$deployment_name -n todo-app --replicas=$replicas
}

# Function to restart deployment
restart_deployment() {
    local component=$1

    if [ -z "$component" ]; then
        print_error "Usage: $0 restart <backend|frontend>"
        return 1
    fi

    local deployment_name="todo-app-${component}"
    print_status "Restarting $deployment_name..."
    kubectl rollout restart deployment/$deployment_name -n todo-app
}

# Function to check logs
check_logs() {
    local component=$1
    local tail_lines=${2:-100}

    if [ -z "$component" ]; then
        print_error "Usage: $0 logs <backend|frontend> [tail_lines]"
        return 1
    fi

    local deployment_name="todo-app-${component}"
    print_status "Showing last $tail_lines log lines for $deployment_name..."
    kubectl logs -l app.kubernetes.io/name=todo-app,app.kubernetes.io/component=$component -n todo-app --tail=$tail_lines
}

# Function to get resource usage
get_resource_usage() {
    print_status "Getting resource usage for todo-app namespace..."
    kubectl top pods -n todo-app
    kubectl top nodes
}

# Function to debug deployment
debug_deployment() {
    local component=$1

    if [ -z "$component" ]; then
        print_error "Usage: $0 debug <backend|frontend>"
        return 1
    fi

    local deployment_name="todo-app-${component}"
    print_status "Debugging $deployment_name..."

    # Get deployment details
    kubectl describe deployment $deployment_name -n todo-app

    # Get pod details
    kubectl describe pods -l app.kubernetes.io/name=todo-app,app.kubernetes.io/component=$component -n todo-app

    # Get events
    kubectl get events -n todo-app --sort-by='.lastTimestamp'
}

# Function to run health checks
run_health_checks() {
    print_status "Running health checks..."

    # Check if deployments are ready
    local backend_ready=$(kubectl get deployment todo-app-backend -n todo-app -o jsonpath='{.status.readyReplicas}/{.spec.replicas}')
    local frontend_ready=$(kubectl get deployment todo-app-frontend -n todo-app -o jsonpath='{.status.readyReplicas}/{.spec.replicas}')

    echo "Backend Ready: $backend_ready"
    echo "Frontend Ready: $frontend_ready"

    # Check if services are available
    kubectl get svc -n todo-app

    # Check if Dapr sidecars are healthy
    print_status "Checking Dapr sidecars..."
    kubectl get pods -n todo-app -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.dapr\.io/enabled}{"\n"}{end}'
}

# Function to update image
update_image() {
    local component=$1
    local image_tag=$2

    if [ -z "$component" ] || [ -z "$image_tag" ]; then
        print_error "Usage: $0 update-image <backend|frontend> <image-tag>"
        return 1
    fi

    local deployment_name="todo-app-${component}"
    local registry=${IMAGE_REGISTRY:-"ghcr.io/$(echo $GITHUB_REPOSITORY | cut -d'/' -f1)/todo-$component"}

    print_status "Updating $deployment_name to image tag: $image_tag"
    kubectl set image deployment/$deployment_name "todo-app-${component}=${registry}:${image_tag}" -n todo-app
}

# Function to rollback deployment
rollback_deployment() {
    local component=$1

    if [ -z "$component" ]; then
        print_error "Usage: $0 rollback <backend|frontend>"
        return 1
    fi

    local deployment_name="todo-app-${component}"
    print_status "Rolling back $deployment_name..."
    kubectl rollout undo deployment/$deployment_name -n todo-app
}

# Main function
main() {
    local command=$1
    shift

    case $command in
        "status")
            get_deployment_status
            ;;
        "scale")
            scale_deployment "$@"
            ;;
        "restart")
            restart_deployment "$@"
            ;;
        "logs")
            check_logs "$@"
            ;;
        "resources")
            get_resource_usage
            ;;
        "debug")
            debug_deployment "$@"
            ;;
        "health")
            run_health_checks
            ;;
        "update-image")
            update_image "$@"
            ;;
        "rollback")
            rollback_deployment "$@"
            ;;
        "help"|"-h"|"--help")
            echo "kubectl-ai commands for Todo App deployment:"
            echo "  status              - Get deployment status"
            echo "  scale <comp> <rep>  - Scale component to replicas"
            echo "  restart <comp>      - Restart component"
            echo "  logs <comp> [n]     - Show logs (default last 100 lines)"
            echo "  resources           - Show resource usage"
            echo "  debug <comp>        - Debug component"
            echo "  health              - Run health checks"
            echo "  update-image <comp> <tag> - Update component image"
            echo "  rollback <comp>     - Rollback component"
            echo "  help                - Show this help"
            ;;
        *)
            print_error "Unknown command: $command"
            echo "Use '$0 help' for available commands"
            exit 1
            ;;
    esac
}

# Call main function with all arguments
main "$@"