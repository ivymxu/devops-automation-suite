# DevOps Automation Suite - Usage Guide

## Quick Start

### Prerequisites
- Python 3.11+
- Terraform 1.0+
- kubectl
- Helm 3.x
- Cloud provider credentials (AWS/GCP/Azure)
- OPA/Conftest (optional, for policy validation)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ivymxu/devops-automation-suite.git
cd devops-automation-suite
```

2. Install Python dependencies (if using YAML configs):
```bash
pip install pyyaml
```

## Using the CLI

### Deploy an Ephemeral Environment

```bash
python cli/deploy.py deploy --env-name pr-123 --provider aws
```

Options:
- `--env-name`: Name of the environment (required)
- `--provider`: Cloud provider (aws/gcp/azure, default: aws)
- `--namespace`: Kubernetes namespace (default: same as env-name)
- `--config`: Path to configuration file

### Teardown an Environment

```bash
python cli/deploy.py teardown --env-name pr-123
```

### Validate Policies

```bash
python cli/deploy.py validate --manifest demo-app/kubernetes/deployment.yaml
```

### List Active Environments

```bash
python cli/deploy.py list
```

## Infrastructure as Code (Terraform)

### AWS EKS

```bash
cd iac/modules/aws
terraform init
terraform plan -var="cluster_name=my-cluster"
terraform apply -var="cluster_name=my-cluster"
```

### GCP GKE

```bash
cd iac/modules/gcp
terraform init
terraform plan -var="cluster_name=my-cluster" -var="project_id=my-project"
terraform apply -var="cluster_name=my-cluster" -var="project_id=my-project"
```

### Azure AKS

```bash
cd iac/modules/azure
terraform init
terraform plan -var="cluster_name=my-cluster" -var="resource_group_name=my-rg"
terraform apply -var="cluster_name=my-cluster" -var="resource_group_name=my-rg"
```

## Policy as Code

### Running Policy Checks with Conftest

Install Conftest:
```bash
# macOS
brew install conftest

# Linux
wget https://github.com/open-policy-agent/conftest/releases/download/v0.47.0/conftest_0.47.0_Linux_x86_64.tar.gz
tar xzf conftest_0.47.0_Linux_x86_64.tar.gz
sudo mv conftest /usr/local/bin/
```

Run policy checks:
```bash
conftest test demo-app/kubernetes/*.yaml -p policies/
```

## Demo Application

### Building the Demo App

```bash
cd demo-app/app
docker build -t demo-app:latest .
```

### Running Locally

```bash
cd demo-app/app
pip install -r requirements.txt
python app.py
```

Access at: http://localhost:8080

### Deploying to Kubernetes

Using kubectl:
```bash
kubectl apply -f demo-app/kubernetes/
```

Using Helm:
```bash
helm install demo-app demo-app/helm/
```

## CI/CD Integration

### GitHub Actions

Copy the workflow files to your `.github/workflows/` directory:
```bash
mkdir -p .github/workflows
cp ci-cd/github-actions/*.yml .github/workflows/
```

### GitLab CI

Copy the GitLab CI configuration to your repository root:
```bash
cp ci-cd/gitlab/.gitlab-ci.yml .
```

### Jenkins

Import the Jenkinsfile to your Jenkins pipeline:
```bash
cp ci-cd/jenkins/Jenkinsfile .
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Pull Request Event                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   CI/CD Pipeline (GH Actions)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Policy Check  │→ │  Build App   │→ │  Deploy Env  │      │
│  │   (OPA)      │  │   (Docker)   │  │ (Terraform+  │      │
│  └──────────────┘  └──────────────┘  │   Helm)      │      │
│                                       └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Ephemeral Environment (K8s)                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Namespace: pr-123                                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │     │
│  │  │   App    │  │   DB     │  │  Secrets │         │     │
│  │  │   Pod    │  │   Pod    │  │          │         │     │
│  │  └──────────┘  └──────────┘  └──────────┘         │     │
│  │                                                     │     │
│  │  Preview URL: https://pr-123.preview.example.com   │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           Auto-Teardown on PR Merge/Close                    │
└─────────────────────────────────────────────────────────────┘
```

## Policy Enforcement

The suite includes three main policy categories:

1. **No Root Containers**: Ensures containers run as non-root users
2. **Resource Requirements**: Enforces CPU/memory requests and limits
3. **No Hardcoded Secrets**: Detects hardcoded secrets in manifests

All policies are enforced pre-deployment and will block the pipeline on violations.

## Troubleshooting

### CLI Issues
- Ensure Python 3.11+ is installed
- Install PyYAML if using YAML configs: `pip install pyyaml`

### Terraform Issues
- Verify cloud provider credentials are configured
- Check that required Terraform providers are installed: `terraform init`

### Policy Violations
- Review the policy output for specific violations
- Update manifests to comply with security requirements
- Test locally with: `conftest test <manifest> -p policies/`

## Support

For issues or questions:
- Check existing documentation in the `docs/` directory
- Review the demo application for examples
- Open an issue on GitHub
