#!/usr/bin/env python3
"""Entry point for CloudLens cost checker.
Reads configuration from cloudlens_config.json (created by interactive installer)
and prompts for missing information. Displays a simple cost summary and savings
suggestions. This is a stub implementation without real cloud API calls.
"""
import json
import os
import datetime
from typing import Optional

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:  # pragma: no cover - dependency might not be installed yet
    boto3 = None

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

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as fh:
            return json.load(fh)
    return {}

def prompt_for_missing(config, key, prompt_text):
    if key not in config:
        config[key] = input(prompt_text).strip()
    return config[key]


def validate_aws_credentials(config) -> Optional['boto3.Session']:
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

def show_cost_summary(provider, session=None):
    print(f'Fetching current costs for {provider}...')
    total = None
    if provider == 'aws' and session:
        try:
            total = fetch_aws_monthly_cost(session)
        except (BotoCoreError, ClientError) as exc:
            print(f'Failed to query AWS costs: {exc}')

    if total is not None:
        print(f'Total monthly cost: ${total:.2f}')
    else:
        print('Total monthly cost: N/A')

    print('Potential savings:')
    for line in SUGGESTIONS.get(provider, []):
        print(f' - {line}')
    print('Alerts would be configured here to notify you about anomalies.')

def main():
    config = load_config()
    provider = config.get('provider') or input('Cloud provider [aws/azure/gcp]: ').strip().lower()
    if provider not in SUGGESTIONS:
        print('Unsupported provider.')
        return
    if provider == 'aws':
        prompt_for_missing(config, 'aws_access_key_id', 'AWS Access Key ID: ')
        prompt_for_missing(config, 'aws_secret_access_key', 'AWS Secret Access Key: ')
        session = validate_aws_credentials(config)
        if not session:
            return
    elif provider == 'azure':
        prompt_for_missing(config, 'azure_client_id', 'Azure Client ID: ')
        prompt_for_missing(config, 'azure_secret', 'Azure Secret: ')
        session = None
    elif provider == 'gcp':
        prompt_for_missing(config, 'gcp_service_account', 'Path to GCP service account JSON: ')
        session = None

    show_cost_summary(provider, session)

if __name__ == '__main__':
    main()
