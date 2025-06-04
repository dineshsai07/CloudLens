#!/usr/bin/env python3
"""Entry point for CloudLens cost checker.
Reads configuration from cloudlens_config.json (created by interactive installer)
and prompts for missing information. Displays a simple cost summary and savings
suggestions. This is a stub implementation without real cloud API calls.
"""
import json
import os

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

def show_cost_summary(provider):
    print(f'Fetching current costs for {provider}...')
    # In a real implementation this would query the provider APIs.
    print('Total monthly cost: $123.45')
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
    elif provider == 'azure':
        prompt_for_missing(config, 'azure_client_id', 'Azure Client ID: ')
        prompt_for_missing(config, 'azure_secret', 'Azure Secret: ')
    elif provider == 'gcp':
        prompt_for_missing(config, 'gcp_service_account', 'Path to GCP service account JSON: ')

    show_cost_summary(provider)

if __name__ == '__main__':
    main()
