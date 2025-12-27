# DevOps Automation Suite

A production-inspired DevOps framework that automates CI/CD, enforces policy-as-code, provisions ephemeral environments, and supports multi-cloud deployments (AWS, GCP, Azure) using reusable Terraform modules.

This project is designed to mimic real-world DevOps challenges and solutions, making it easy to bootstrap secure, scalable, and cloud-agnostic pipelines for modern applications.

## Key Features
## 1. Ephemeral Environments (per Pull Request)
- Spin up full Kubernetes namespaces for each PR (with DB + secrets).
- Auto-deploy app via Helm, generate preview URLs for reviewers.
- Auto-teardown on merge/close → saves costs, keeps infra clean.

## 2. Policy-as-Code Enforcement
- Pre-deployment checks using Open Policy Agent (OPA).
- Enforces:
  - No containers running as root.
  - All pods must define resource requests/limits.
  - No hardcoded secrets in manifests.
- Blocks pipeline on violations → security & compliance baked in.

## 3. Multi-Cloud Deployment (AWS, GCP, Azure)
- Reusable Terraform modules for EKS, GKE, and AKS clusters.
- Unified pipeline config (config.yaml) lets you select provider.
- Deploy the same app across providers seamlessly.

## Architecture

```
DevOps-Automation-Suite/
├── cli/               # CLI for deployment & teardown
├── iac/               # Terraform modules for AWS/GCP/Azure
├── policies/          # OPA policies (security, compliance)
├── ci-cd/             # Pipeline templates (GitHub Actions, GitLab, Jenkins)
├── docs/              # Architecture diagrams, usage docs
├── demo-app/
└── README.md
```

## Demo Application

This repository includes a sample microservice (`/demo-app`) used to showcase the DevOps Automation Suite in action.
Features:
- Simple Flask API with Dockerfile and Helm chart.
- Kubernetes manifests for deployment.
- Integrated into CI/CD workflows for:
  - Ephemeral environment provisioning.
  - Policy-as-code enforcement.
  - Multi-cloud Terraform deployments.

### Demo:
https://github.com/user-attachments/assets/445b68b8-c14e-4693-b1fd-c8cb247220c7

## Why
- Demonstrates enterprise-grade DevOps practices (policy enforcement, GitOps, IaC)
- Helps developers preview features safely with ephemeral environments
- Provides cloud-agnostic deployments for teams avoiding vendor lock-in

## Tech Stack
- Infrastructure: Terraform, Kubernetes, Helm
- CI/CD: GitHub Actions, GitLab CI, Jenkins
- Policy-as-Code: Open Policy Agent (OPA), Conftest
- Cloud Providers: AWS EKS, GCP GKE, Azure AKS

## Roadmap
- Add rollback automation on failed health checks
- Integrate cost monitoring per environment
- Build CLI in Go for performance & portability
- Add Slack notifications for environment lifecycle events
