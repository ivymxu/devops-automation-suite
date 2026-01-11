# Architecture Overview

## System Components

### 1. CLI Tool (`cli/deploy.py`)
- Command-line interface for deployment operations
- Handles environment lifecycle (deploy, teardown, validate, list)
- Multi-cloud provider support (AWS, GCP, Azure)

### 2. Infrastructure as Code (`iac/`)
Terraform modules for provisioning Kubernetes clusters:
- **AWS Module**: EKS cluster with VPC, subnets, and managed node groups
- **GCP Module**: GKE cluster with VPC, workload identity
- **Azure Module**: AKS cluster with virtual networks

### 3. Policy as Code (`policies/`)
OPA/Rego policies for security enforcement:
- No root containers
- Resource requirements (CPU/memory)
- No hardcoded secrets

### 4. CI/CD Templates (`ci-cd/`)
Pipeline configurations for:
- GitHub Actions
- GitLab CI
- Jenkins

### 5. Demo Application (`demo-app/`)
Sample Flask microservice demonstrating:
- Containerization (Docker)
- Kubernetes deployment
- Helm charts
- Health/readiness probes

## Deployment Flow

```
┌──────────────┐
│  Developer   │
│  Opens PR    │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│     CI/CD Pipeline Triggered        │
│  1. Run Policy Checks (OPA)         │
│  2. Build Container Image           │
│  3. Provision Infrastructure        │
│  4. Deploy Application (Helm)       │
│  5. Generate Preview URL            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Ephemeral Environment Running     │
│   - Isolated Kubernetes namespace   │
│   - Full application stack          │
│   - Database & secrets              │
│   - Accessible preview URL          │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     PR Merged/Closed                │
│  1. Teardown application            │
│  2. Clean up namespace              │
│  3. Destroy infrastructure          │
└─────────────────────────────────────┘
```

## Security Architecture

### Policy Enforcement Points

1. **Pre-deployment**: Conftest validates manifests against OPA policies
2. **Runtime**: Kubernetes admission controllers enforce security contexts
3. **Post-deployment**: Continuous monitoring for compliance

### Security Features

- **Non-root containers**: All containers run as non-privileged users
- **Resource limits**: Prevents resource exhaustion attacks
- **Secret management**: No hardcoded secrets, uses Kubernetes Secrets
- **Network policies**: Isolated namespaces for each environment
- **RBAC**: Role-based access control for cluster operations

## Multi-Cloud Support

### Provider Abstraction

The CLI and Terraform modules provide a unified interface across clouds:

```
┌──────────────────────────────────────────────┐
│            CLI Abstraction Layer              │
└──────┬───────────────┬──────────────┬────────┘
       │               │              │
       ▼               ▼              ▼
┌──────────┐    ┌──────────┐   ┌──────────┐
│   AWS    │    │   GCP    │   │  Azure   │
│   EKS    │    │   GKE    │   │   AKS    │
└──────────┘    └──────────┘   └──────────┘
```

### Cloud-Specific Configurations

- **AWS**: EKS with VPC, NAT Gateway, managed node groups
- **GCP**: GKE with workload identity, binary authorization
- **Azure**: AKS with system-assigned identity, autoscaling

## Scalability

### Horizontal Scaling
- Node autoscaling in all cloud providers
- Pod autoscaling based on CPU/memory metrics
- Multiple replicas for high availability

### Cost Optimization
- Ephemeral environments auto-teardown on PR close
- Single NAT Gateway for AWS (cost-effective)
- Preemptible/spot instances support (configurable)

## Monitoring & Observability

### Health Checks
- Liveness probes: Detect unhealthy containers
- Readiness probes: Route traffic only to ready pods

### Logging
- Container logs aggregated to cloud provider logging
- Structured logging for better observability

### Metrics
- Resource utilization (CPU, memory)
- Request rate and latency
- Error rates

## Extension Points

The architecture is designed for extensibility:

1. **Add new cloud providers**: Create new Terraform module in `iac/modules/`
2. **Add new policies**: Create Rego files in `policies/`
3. **Customize CI/CD**: Modify templates in `ci-cd/`
4. **Extend CLI**: Add new commands to `cli/deploy.py`

## Future Enhancements

- Automated rollback on health check failures
- Cost monitoring per environment
- Slack/Teams notifications for lifecycle events
- Advanced metrics and observability
- Multi-region deployments
