# Oracle Kubernetes Engine (OKE) Deployment Guide

This guide provides instructions for deploying the Todo application to Oracle Kubernetes Engine (OKE).

## Prerequisites

- Oracle Cloud Account with sufficient permissions
- Oracle Cloud CLI (OCI CLI) installed and configured
- `kubectl` installed
- `helm` installed
- Docker installed for local testing

## Setting up Oracle Cloud CLI

1. Install OCI CLI:
```bash
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" -- --accept-all-defaults
```

2. Configure OCI CLI:
```bash
oci setup config
```
Follow the prompts to enter your tenancy OCID, user OCID, region, and generate an API key.

## Creating an OKE Cluster

1. Create a new OKE cluster using the OCI Console or CLI:
```bash
oci ce cluster create --name todo-cluster \
  --compartment-id <your-compartment-ocid> \
  --vcn-id <your-vcn-ocid> \
  --service-lb-subnet-ids <subnet-ocid-1>,<subnet-ocid-2> \
  --kubernetes-version v1.26.2
```

2. Get the kubeconfig for your cluster:
```bash
oci ce cluster create-kubeconfig --cluster-id <your-cluster-ocid> --file $HOME/.kube/config --region us-sanjose-1
```

## Installing Dapr on OKE

1. Add the Dapr Helm repo:
```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update
```

2. Install Dapr on your OKE cluster:
```bash
helm install dapr dapr/dapr --namespace dapr-system --create-namespace --wait
```

## Preparing for Deployment

1. Build and push your Docker images to a container registry (e.g., GitHub Container Registry):
```bash
# Build backend image
docker build -t ghcr.io/<your-org>/todo-backend:<tag> ./backend

# Build frontend image
docker build -t ghcr.io/<your-org>/todo-frontend:<tag> ./frontend

# Push images
docker push ghcr.io/<your-org>/todo-backend:<tag>
docker push ghcr.io/<your-org>/todo-frontend:<tag>
```

2. Update the Helm values file with your image repository and tag:
```yaml
# In charts/todo-app/values.yaml
backend:
  image:
    repository: ghcr.io/<your-org>/todo-backend
    tag: <your-tag>
frontend:
  image:
    repository: ghcr.io/<your-org>/todo-frontend
    tag: <your-tag>
```

## Deploying the Application

1. Install the application using Helm:
```bash
helm upgrade --install todo-app ./charts/todo-app \
  --namespace todo-app --create-namespace \
  --set dapr.enabled=true \
  --wait
```

2. Verify the deployment:
```bash
kubectl get pods -n todo-app
kubectl get services -n todo-app
```

## Setting up Kafka on OKE

For production use, you'll want to deploy Kafka on your OKE cluster:

1. Add the Strimzi Helm repo:
```bash
helm repo add strimzi https://strimzi.io/charts/
helm repo update
```

2. Install Strimzi Kafka operator:
```bash
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace
```

3. Apply Kafka cluster configuration:
```bash
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
```

## Monitoring and Logging

1. To check application logs:
```bash
kubectl logs -f deployment/todo-app-backend -n todo-app
kubectl logs -f deployment/todo-app-frontend -n todo-app
```

2. To check Dapr sidecar logs:
```bash
kubectl logs -l app=todo-app-backend -n todo-app -c daprd
kubectl logs -l app=todo-app-frontend -n todo-app -c daprd
```

## Scaling the Application

You can scale your deployments based on demand:
```bash
kubectl scale deployment/todo-app-backend -n todo-app --replicas=3
kubectl scale deployment/todo-app-frontend -n todo-app --replicas=3
```

## Cleanup

To delete the application:
```bash
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
```

To delete the Kafka cluster:
```bash
kubectl delete kafka/todo-kafka -n kafka
helm uninstall strimzi -n kafka
```

## Troubleshooting

1. If pods are stuck in Pending state, check if you have sufficient resources:
```bash
kubectl describe nodes
```

2. If Dapr sidecars are not starting, check Dapr system status:
```bash
kubectl get pods -n dapr-system
```

3. If Kafka is not connecting, verify the Dapr pubsub component configuration matches the Kafka broker address.