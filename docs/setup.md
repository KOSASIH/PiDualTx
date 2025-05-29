# PiDualTx Setup Guide

## Prerequisites

Before setting up the PiDualTx application, ensure you have the following installed:

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 1.29 or higher
- **Kubernetes**: A running cluster (Minikube, GKE, EKS, or AKS)
- **kubectl**: Command-line tool for Kubernetes
- **Helm**: Package manager for Kubernetes (optional, for easier deployments)
- **Node.js**: Version 14 or higher (for frontend development)
- **Java**: JDK 11 or higher (for backend services)

## Step 1: Clone the Repository

Clone the PiDualTx repository from GitHub:

```bash
git clone https://github.com/KOSASIH/pidualtx.git
cd pidualtx
```

## Step 2: Build Docker Images

Navigate to the root of the project and build the Docker images for the backend services and frontend application:

```bash
# Build backend services
cd backend
docker-compose build

# Build frontend application
cd ../frontend
npm install
npm run build
```

## Step 3: Deploy to Kubernetes

### 3.1: Set Up Namespace

Create a namespace for the PiDualTx application:

```bash
kubectl create namespace monitoring
kubectl create namespace pidualtx
```

### 3.2: Deploy Redis

Deploy Redis for caching:

```bash
kubectl apply -f kubernetes/redis-deployment.yaml
```

### 3.3: Deploy Backend Services

Deploy the backend services:

```bash
kubectl apply -f kubernetes/rate-service.yaml
kubectl apply -f kubernetes/ai-service.yaml
kubectl apply -f kubernetes/smartcontract-service.yaml
```

### 3.4: Deploy Frontend Application

Deploy the frontend application:

```bash
kubectl apply -f kubernetes/frontend-deployment.yaml
```

### 3.5: Set Up Ingress

Deploy the Ingress resource to manage external access:

```bash
kubectl apply -f kubernetes/ingress.yaml
```

### 3.6: Deploy Monitoring Tools

Deploy Prometheus and Grafana for monitoring:

```bash
kubectl apply -f kubernetes/monitoring/prometheus.yaml
kubectl apply -f kubernetes/monitoring/grafana.yaml
```

## Step 4: Access the Application

### 4.1: Get Ingress IP

Retrieve the external IP address for the Ingress:

```bash
kubectl get ingress -n pidualtx
```

### 4.2: Access the Frontend

Open your web browser and navigate to:

```
http://<INGRESS_IP>
```

### 4.3: Access Grafana

To access Grafana, use the same Ingress IP with the Grafana path (if configured):

```
http://<INGRESS_IP>/grafana
```

Log in with the default credentials:
- Username: `admin`
- Password: `admin`

## Step 5: Verify the Setup

Ensure all services are running correctly:

```bash
kubectl get pods -n pidualtx
kubectl get pods -n monitoring
```

Check the logs for any issues:

```bash
kubectl logs <pod-name> -n pidualtx
kubectl logs <pod-name> -n monitoring
```

## Troubleshooting

- If you encounter issues, check the Kubernetes events for errors:

```bash
kubectl get events -n pidualtx
kubectl get events -n monitoring
```

- Ensure that your Kubernetes cluster has sufficient resources allocated for the deployments.

---

*This setup guide is intended for developers and system administrators looking to deploy the PiDualTx application in a Kubernetes environment.*
```
