#!/usr/bin/env python3
"""CLI entry point for CloudLens cost checks."""
from typing import Optional

from cloudlens_core import (
    SUGGESTIONS,
    load_config,
    save_config,
    validate_aws_credentials,
    validate_azure_credentials,
    validate_gcp_credentials,
    fetch_aws_monthly_cost,
    fetch_azure_monthly_cost,
    fetch_gcp_monthly_cost,
)


def prompt_for_missing(config: dict, key: str, prompt_text: str) -> str:
    if key not in config:
        config[key] = input(prompt_text).strip()
    return config[key]


def show_cost_summary(provider: str, session: Optional[object] = None) -> None:
    print(f'Fetching current costs for {provider}...')
    total = None
    if provider == 'aws' and session:
        try:
            total = fetch_aws_monthly_cost(session)
        except Exception as exc:  # pragma: no cover - network
            print(f'Failed to query AWS costs: {exc}')
    elif provider == 'azure' and session:
        try:
            total = fetch_azure_monthly_cost(session)
        except Exception as exc:  # pragma: no cover - network
            print(f'Failed to query Azure costs: {exc}')
    elif provider == 'gcp' and session:
        try:
            total = fetch_gcp_monthly_cost(session)
        except Exception as exc:  # pragma: no cover - network
            print(f'Failed to query GCP costs: {exc}')

    if total is not None:
        print(f'Total monthly cost: ${total:.2f}')
    else:
        print('Total monthly cost: N/A')

    print('Potential savings:')
    for line in SUGGESTIONS.get(provider, []):
        print(f' - {line}')
    print('Alerts would be configured here to notify you about anomalies.')


def main() -> None:
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
        prompt_for_missing(config, 'azure_tenant_id', 'Azure Tenant ID: ')
        session = validate_azure_credentials(config)
        if not session:
            return
    elif provider == 'gcp':
        prompt_for_missing(config, 'gcp_service_account', 'Path to GCP service account JSON: ')
        session = validate_gcp_credentials(config)
        if not session:
            return
    else:
        session = None

    save_config({'provider': provider, **config})
    show_cost_summary(provider, session)


if __name__ == '__main__':
    main()
