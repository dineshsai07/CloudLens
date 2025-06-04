#!/usr/bin/env python3
"""Common functionality for CloudLens scripts."""
import json
import os
import datetime
from typing import Optional

try:
    from azure.identity import ClientSecretCredential
    from azure.core.exceptions import ClientAuthenticationError
except ImportError:  # pragma: no cover - optional dependency
    ClientSecretCredential = None  # type: ignore
    ClientAuthenticationError = Exception  # type: ignore

try:
    from google.oauth2 import service_account
except ImportError:  # pragma: no cover - optional dependency
    service_account = None  # type: ignore

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:  # pragma: no cover - dependency might not be installed yet
    boto3 = None  # type: ignore

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'cloudlens_config.json')

SUGGESTIONS = {
    'aws': [
        'Right-size EC2 instances',
        'Delete unused EBS volumes',
        'Consider Reserved Instances or Savings Plans'
    ],
    'azure': [
        'Use Azure Advisor recommendations',
        'Remove idle disks',
        'Leverage Azure Hybrid Benefit'
    ],
    'gcp': [
        'Delete unattached persistent disks',
        'Utilize committed use discounts',
        'Scale down overprovisioned services'
    ]
}

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as fh:
            return json.load(fh)
    return {}


def save_config(config: dict) -> None:
    with open(CONFIG_FILE, 'w') as fh:
        json.dump(config, fh, indent=2)


def validate_aws_credentials(config: dict) -> Optional['boto3.Session']:
    """Return a boto3 session if credentials work, otherwise None."""
    if boto3 is None:
        print('boto3 is not installed; cannot validate AWS credentials.')
        return None
    try:
        session = boto3.Session(
            aws_access_key_id=config.get('aws_access_key_id'),
            aws_secret_access_key=config.get('aws_secret_access_key')
        )
        sts = session.client('sts')
        sts.get_caller_identity()
        return session
    except (BotoCoreError, ClientError) as exc:
        print(f'Invalid AWS credentials: {exc}')
        return None


def fetch_aws_monthly_cost(session: 'boto3.Session') -> float:
    """Return the current month's total cost using AWS Cost Explorer."""
    ce = session.client('ce', region_name='us-east-1')
    today = datetime.date.today()
    start = today.replace(day=1)
    end = today + datetime.timedelta(days=1)
    resp = ce.get_cost_and_usage(
        TimePeriod={'Start': start.strftime('%Y-%m-%d'), 'End': end.strftime('%Y-%m-%d')},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )
    amount = resp['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
    return float(amount)


def fetch_azure_monthly_cost(_credential: 'ClientSecretCredential') -> float:
    """Stub for fetching Azure monthly cost (returns 0.0)."""
    # Production code would query Azure Cost Management APIs here
    return 0.0


def fetch_gcp_monthly_cost(_creds: 'service_account.Credentials') -> float:
    """Stub for fetching GCP monthly cost (returns 0.0)."""
    # Production code would query GCP Billing APIs here
    return 0.0


def validate_azure_credentials(config: dict) -> Optional['ClientSecretCredential']:
    """Return Azure credential if valid, otherwise None."""
    if ClientSecretCredential is None:
        print('azure-identity is not installed; cannot validate Azure credentials.')
        return None
    try:
        credential = ClientSecretCredential(
            tenant_id=config.get('azure_tenant_id', 'common'),
            client_id=config.get('azure_client_id'),
            client_secret=config.get('azure_secret'),
        )
        # Attempt to obtain a token for ARM
        credential.get_token('https://management.azure.com/.default')
        return credential
    except ClientAuthenticationError as exc:  # pragma: no cover - network
        print(f'Invalid Azure credentials: {exc}')
        return None


def validate_gcp_credentials(config: dict) -> Optional['service_account.Credentials']:
    """Return service account credentials if valid, otherwise None."""
    if service_account is None:
        print('google-auth is not installed; cannot validate GCP credentials.')
        return None
    try:
        creds = service_account.Credentials.from_service_account_file(
            config.get('gcp_service_account')
        )
        return creds
    except Exception as exc:  # pragma: no cover - filesystem/network
        print(f'Invalid GCP credentials: {exc}')
        return None
