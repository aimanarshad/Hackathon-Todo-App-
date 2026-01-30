#!/bin/bash

# Script for deploying the Todo application to Oracle Kubernetes Engine (OKE)

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

# Check if OCI CLI is installed
check_oci_cli() {
    if ! command -v oci &> /dev/null; then
        print_error "OCI CLI is not installed. Please install it first."
        echo "Visit: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm"
        exit 1
    fi
    print_status "OCI CLI is installed"
}

# Check if kubectl is installed
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install it first."
        echo "Visit: https://kubernetes.io/docs/tasks/tools/"
        exit 1
    fi
    print_status "kubectl is installed"
}

# Check if helm is installed
check_helm() {
    if ! command -v helm &> /dev/null; then
        print_error "Helm is not installed. Please install it first."
        echo "Visit: https://helm.sh/docs/intro/install/"
        exit 1
    fi
    print_status "Helm is installed"
}

# Check if docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install it first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_status "Docker is installed"
}

# Login to Oracle Cloud Container Registry
login_to_ocr() {
    local region=${OCI_REGION:-"iad"}
    local tenancy_ocid=${OCI_TENANCY_OCID}

    if [ -z "$tenancy_ocid" ]; then
        print_error "OCI_TENANCY_OCID environment variable is not set"
        exit 1
    fi

    print_status "Logging in to Oracle Cloud Container Registry..."
    docker login -u "$tenancy_ocid"/oracleidentitycloudservice -p "$OCI_USER_API_KEY" ocir.$region.oraclecloud.com
    if [ $? -ne 0 ]; then
        print_error "Failed to login to OCR"
        exit 1
    fi
    print_status "Successfully logged in to OCR"
}

# Build and push Docker images
build_and_push_images() {
    local registry=${IMAGE_REGISTRY:-"ocir.$OCI_REGION.oraclecloud.com/$OCI_TENANCY_OCID"}
    local tag=${IMAGE_TAG:-$(git rev-parse --short HEAD)}

    print_status "Building and pushing Docker images..."

    # Build backend image
    print_status "Building backend image..."
    docker build -t "$registry/todo-backend:$tag" -f docker/backend/Dockerfile ./backend
    docker push "$registry/todo-backend:$tag"

    # Build frontend image
    print_status "Building frontend image..."
    docker build -t "$registry/todo-frontend:$tag" -f docker/frontend/Dockerfile ./frontend
    docker push "$registry/todo-frontend:$tag"

    print_status "Images pushed to registry: $registry"
    echo "Backend: $registry/todo-backend:$tag"
    echo "Frontend: $registry/todo-frontend:$tag"
}

# Get OKE cluster kubeconfig
get_cluster_kubeconfig() {
    local cluster_id=$1

    if [ -z "$cluster_id" ]; then
        print_error "Cluster ID is required"
        exit 1
    fi

    print_status "Getting kubeconfig for cluster: $cluster_id"
    oci ce cluster create-kubeconfig --cluster-id "$cluster_id" --file ~/.kube/config --region "$OCI_REGION" --token-version 2.0.0

    if [ $? -ne 0 ]; then
        print_error "Failed to get kubeconfig for cluster"
        exit 1
    fi

    print_status "Updated kubectl config with OKE cluster configuration"
}

# Install Dapr on the cluster
install_dapr() {
    print_status "Installing Dapr on the cluster..."

    # Add Dapr Helm repo
    helm repo add dapr https://dapr.github.io/helm-charts/
    helm repo update

    # Install Dapr
    helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait

    if [ $? -ne 0 ]; then
        print_error "Failed to install Dapr"
        exit 1
    fi

    print_status "Dapr installed successfully"
}

# Deploy Kafka to the cluster (using Strimzi)
deploy_kafka() {
    print_status "Deploying Kafka to the cluster..."

    # Add Strimzi Helm repo
    helm repo add strimzi https://strimzi.io/charts/
    helm repo update

    # Install Strimzi operator
    helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace --wait

    if [ $? -ne 0 ]; then
        print_error "Failed to install Strimzi Kafka operator"
        exit 1
    fi

    # Deploy Kafka cluster
    kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.5.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.5"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

    if [ $? -ne 0 ]; then
        print_error "Failed to deploy Kafka cluster"
        exit 1
    fi

    print_status "Kafka deployed successfully"
}

# Deploy the application using Helm
deploy_application() {
    local cluster_id=$1
    local registry=${IMAGE_REGISTRY:-"ocir.$OCI_REGION.oraclecloud.com/$OCI_TENANCY_OCID"}
    local tag=${IMAGE_TAG:-$(git rev-parse --short HEAD)}

    print_status "Deploying application to cluster..."

    # Create namespace
    kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

    # Update Helm values with image tags
    local temp_values=$(mktemp)
    cp charts/todo-app/values.yaml "$temp_values"

    # Replace image tags in values file
    sed -i "s|repository:.*backend|repository: $registry/todo-backend|" "$temp_values"
    sed -i "s|tag:.*|tag: $tag|" "$temp_values"
    sed -i "s|repository:.*frontend|repository: $registry/todo-frontend|" "$temp_values"

    # Install/upgrade the application
    helm upgrade --install todo-app ./charts/todo-app \
        --namespace todo-app \
        --values "$temp_values" \
        --set dapr.enabled=true \
        --wait

    if [ $? -ne 0 ]; then
        print_error "Failed to deploy application"
        rm "$temp_values"
        exit 1
    fi

    rm "$temp_values"
    print_status "Application deployed successfully"
}

# Check deployment status
check_deployment_status() {
    print_status "Checking deployment status..."

    # Wait for pods to be ready
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-app -n todo-app --timeout=300s

    # Check if services are available
    kubectl get svc -n todo-app

    # Check pod status
    kubectl get pods -n todo-app

    print_status "Deployment status check completed"
}

# Create monitoring resources
setup_monitoring() {
    print_status "Setting up monitoring..."

    # Apply Prometheus configuration
    if [ -f "monitoring/prometheus/prometheus.yml" ]; then
        kubectl create configmap prometheus-config --from-file=monitoring/prometheus/prometheus.yml -n todo-app --dry-run=client -o yaml | kubectl apply -f -
    fi

    # Apply Grafana dashboard
    if [ -f "monitoring/grafana/dashboards/todo-app.json" ]; then
        kubectl create configmap grafana-dashboard --from-file=monitoring/grafana/dashboards/todo-app.json -n todo-app --dry-run=client -o yaml | kubectl apply -f -
    fi

    print_status "Monitoring setup completed"
}

# Main function
main() {
    print_status "Starting deployment to Oracle Kubernetes Engine..."

    # Check prerequisites
    check_oci_cli
    check_kubectl
    check_helm
    check_docker

    # Parse command line arguments
    local action=${1:-"deploy"}
    local cluster_id=$2

    case $action in
        "validate")
            print_status "Validating environment..."
            ;;
        "build")
            login_to_ocr
            build_and_push_images
            ;;
        "deploy")
            if [ -z "$cluster_id" ]; then
                print_error "Cluster ID is required for deploy action"
                echo "Usage: $0 deploy <cluster-id>"
                exit 1
            fi

            get_cluster_kubeconfig "$cluster_id"
            install_dapr
            deploy_kafka
            deploy_application "$cluster_id"
            check_deployment_status
            setup_monitoring
            ;;
        "rollback")
            print_status "Rolling back deployment..."
            helm rollback todo-app --namespace todo-app
            ;;
        *)
            echo "Usage: $0 {validate|build|deploy|rollback} [cluster-id]"
            echo "  validate  - Validate the environment"
            echo "  build     - Build and push Docker images"
            echo "  deploy    - Deploy application to OKE (requires cluster-id)"
            echo "  rollback  - Rollback to previous version"
            exit 1
            ;;
    esac

    print_status "Deployment process completed successfully!"
}

# Call main function with all arguments
main "$@"