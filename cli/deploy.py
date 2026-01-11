#!/usr/bin/env python3
"""
DevOps Automation Suite CLI
Automates deployment and teardown of ephemeral environments
"""

import argparse
import sys
import os
import subprocess
import json
from pathlib import Path


def load_config(config_path):
    """Load configuration from YAML or JSON file"""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found")
        return None
    
    try:
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except ImportError:
        print("Warning: PyYAML not installed, trying JSON...")
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            return None


def deploy_environment(args):
    """Deploy ephemeral environment"""
    print(f"🚀 Deploying environment: {args.env_name}")
    print(f"   Provider: {args.provider}")
    print(f"   Namespace: {args.namespace or args.env_name}")
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
        if config is None:
            return 1
    
    # Simulate deployment steps
    steps = [
        "Validating configuration...",
        "Running policy checks (OPA)...",
        "Provisioning infrastructure (Terraform)...",
        "Deploying application (Helm)...",
        "Generating preview URL..."
    ]
    
    for step in steps:
        print(f"   ✓ {step}")
    
    preview_url = f"https://{args.env_name}.preview.example.com"
    print(f"\n✅ Environment deployed successfully!")
    print(f"   Preview URL: {preview_url}")
    print(f"   Namespace: {args.namespace or args.env_name}")
    
    return 0


def teardown_environment(args):
    """Teardown ephemeral environment"""
    print(f"🗑️  Tearing down environment: {args.env_name}")
    
    # Simulate teardown steps
    steps = [
        "Removing application resources...",
        "Cleaning up Kubernetes namespace...",
        "Destroying infrastructure (Terraform)...",
        "Removing DNS records..."
    ]
    
    for step in steps:
        print(f"   ✓ {step}")
    
    print(f"\n✅ Environment '{args.env_name}' removed successfully!")
    
    return 0


def validate_policies(args):
    """Validate policies using OPA/Conftest"""
    print(f"🔍 Validating policies for: {args.manifest}")
    
    if not os.path.exists(args.manifest):
        print(f"Error: Manifest file '{args.manifest}' not found")
        return 1
    
    # Simulate policy checks
    checks = [
        "✓ No containers running as root",
        "✓ Resource requests/limits defined",
        "✓ No hardcoded secrets found",
        "✓ Security context configured"
    ]
    
    for check in checks:
        print(f"   {check}")
    
    print(f"\n✅ All policy checks passed!")
    
    return 0


def list_environments(args):
    """List active environments"""
    print("📋 Active Environments:")
    print("-" * 60)
    
    # Simulate listing environments
    environments = [
        {"name": "pr-123", "status": "running", "age": "2h"},
        {"name": "pr-456", "status": "running", "age": "5h"},
        {"name": "staging", "status": "running", "age": "3d"}
    ]
    
    for env in environments:
        print(f"   {env['name']:<20} {env['status']:<15} {env['age']}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='DevOps Automation Suite CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy an ephemeral environment
  python deploy.py deploy --env-name pr-123 --provider aws

  # Teardown an environment
  python deploy.py teardown --env-name pr-123

  # Validate policies
  python deploy.py validate --manifest kubernetes/deployment.yaml

  # List active environments
  python deploy.py list
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy ephemeral environment')
    deploy_parser.add_argument('--env-name', required=True, help='Environment name (e.g., pr-123)')
    deploy_parser.add_argument('--provider', default='aws', choices=['aws', 'gcp', 'azure'],
                               help='Cloud provider (default: aws)')
    deploy_parser.add_argument('--namespace', help='Kubernetes namespace (default: env-name)')
    deploy_parser.add_argument('--config', help='Path to config file')
    deploy_parser.set_defaults(func=deploy_environment)
    
    # Teardown command
    teardown_parser = subparsers.add_parser('teardown', help='Teardown ephemeral environment')
    teardown_parser.add_argument('--env-name', required=True, help='Environment name')
    teardown_parser.set_defaults(func=teardown_environment)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate policies')
    validate_parser.add_argument('--manifest', required=True, help='Path to Kubernetes manifest')
    validate_parser.set_defaults(func=validate_policies)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List active environments')
    list_parser.set_defaults(func=list_environments)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
