#!/usr/bin/env python3
"""Interactive installer for CloudLens.
Prompts the user for cloud provider and credentials and saves them to
cloudlens_config.json at the repository root.
"""
import json
import os

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    boto3 = None

try:
    from azure.identity import ClientSecretCredential
    from azure.core.exceptions import ClientAuthenticationError
except ImportError:
    ClientSecretCredential = None  # type: ignore

try:
    from google.oauth2 import service_account
except ImportError:
    service_account = None  # type: ignore

CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'cloudlens_config.json')

PROVIDERS = ['aws', 'azure', 'gcp']

def prompt_provider():
    print("Select your cloud provider:")
    for idx, name in enumerate(PROVIDERS, 1):
        print(f" {idx}) {name}")
    choice = input("Enter number: ").strip()
    try:
        idx = int(choice) - 1
        return PROVIDERS[idx]
    except (ValueError, IndexError):
        print("Invalid selection")
        return prompt_provider()

def prompt_credentials(provider):
    creds = {}
    if provider == 'aws':
        creds['aws_access_key_id'] = input('AWS Access Key ID: ').strip()
        creds['aws_secret_access_key'] = input('AWS Secret Access Key: ').strip()
        if boto3:
            try:
                boto3.client('sts',
                             aws_access_key_id=creds['aws_access_key_id'],
                             aws_secret_access_key=creds['aws_secret_access_key']).get_caller_identity()
            except (BotoCoreError, ClientError) as exc:
                print(f'Invalid AWS credentials: {exc}')
                return prompt_credentials(provider)
    elif provider == 'azure':
        creds['azure_client_id'] = input('Azure Client ID: ').strip()
        creds['azure_secret'] = input('Azure Secret: ').strip()
        creds['azure_tenant_id'] = input('Azure Tenant ID: ').strip()
        if ClientSecretCredential:
            try:
                cred = ClientSecretCredential(
                    tenant_id=creds['azure_tenant_id'],
                    client_id=creds['azure_client_id'],
                    client_secret=creds['azure_secret'],
                )
                cred.get_token('https://management.azure.com/.default')
            except ClientAuthenticationError as exc:
                print(f'Invalid Azure credentials: {exc}')
                return prompt_credentials(provider)
    elif provider == 'gcp':
        creds['gcp_service_account'] = input('Path to GCP service account JSON: ').strip()
        if service_account:
            try:
                service_account.Credentials.from_service_account_file(
                    creds['gcp_service_account']
                )
            except Exception as exc:
                print(f'Invalid GCP credentials: {exc}')
                return prompt_credentials(provider)
    return creds

def main():
    print('=== CloudLens Interactive Installer ===')
    provider = prompt_provider()
    creds = prompt_credentials(provider)
    config = {'provider': provider, **creds}
    with open(CONFIG_FILE, 'w') as fh:
        json.dump(config, fh, indent=2)
    print(f'Configuration written to {CONFIG_FILE}')
    print('Run "python cloudlens.py" to start cost checks.')

if __name__ == '__main__':
    main()
