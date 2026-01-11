# Demo Application

A simple Flask microservice demonstrating the DevOps Automation Suite.

## Features

- RESTful API with health/readiness endpoints
- Containerized with Docker (non-root user)
- Kubernetes-ready with manifests and Helm chart
- Security best practices (resource limits, non-root, no hardcoded secrets)

## Endpoints

- `GET /` - Hello world message with environment info
- `GET /health` - Health check endpoint
- `GET /ready` - Readiness check endpoint

## Running Locally

### With Python

```bash
cd app
pip install -r requirements.txt
python app.py
```

Access at: http://localhost:8080

### With Docker

```bash
cd app
docker build -t demo-app:latest .
docker run -p 8080:8080 demo-app:latest
```

Access at: http://localhost:8080

## Deploying to Kubernetes

### Using kubectl

```bash
kubectl apply -f kubernetes/
```

### Using Helm

```bash
helm install demo-app helm/
```

## Configuration

### Environment Variables

- `ENV_NAME`: Environment name (automatically set from namespace in Kubernetes)

### Helm Values

Edit `helm/values.yaml` to customize:
- Replica count
- Resource limits
- Image repository and tag
- Ingress settings

## Security Features

✓ Runs as non-root user (UID 1000)
✓ Resource requests and limits defined
✓ Read-only root filesystem
✓ No privilege escalation
✓ Health and readiness probes configured

## Development

The application uses:
- Flask 3.0.0 - Web framework
- Gunicorn 21.2.0 - WSGI HTTP server
