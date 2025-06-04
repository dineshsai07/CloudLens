#!/usr/bin/env python3
"""Flask-based web UI for CloudLens installer and cost summary."""
from flask import Flask, render_template, request, redirect, url_for, flash

from cloudlens_core import (
    SUGGESTIONS,
    save_config,
    validate_aws_credentials,
    fetch_aws_monthly_cost,
)

app = Flask(__name__)
app.secret_key = 'cloudlens'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        provider = request.form.get('provider', '').lower()
        if provider not in SUGGESTIONS:
            flash('Unsupported provider', 'danger')
            return redirect(url_for('index'))

        config = {'provider': provider}
        session = None
        cost = None

        if provider == 'aws':
            config['aws_access_key_id'] = request.form.get('aws_access_key_id', '')
            config['aws_secret_access_key'] = request.form.get('aws_secret_access_key', '')
            session = validate_aws_credentials(config)
            if not session:
                flash('Invalid AWS credentials', 'danger')
                return redirect(url_for('index'))
            try:
                cost = fetch_aws_monthly_cost(session)
            except Exception as exc:  # pragma: no cover - network
                flash(f'Failed to fetch AWS cost: {exc}', 'warning')
        elif provider == 'azure':
            config['azure_client_id'] = request.form.get('azure_client_id', '')
            config['azure_secret'] = request.form.get('azure_secret', '')
        elif provider == 'gcp':
            config['gcp_service_account'] = request.form.get('gcp_service_account', '')

        save_config(config)
        return render_template('result.html', provider=provider, cost=cost, suggestions=SUGGESTIONS.get(provider, []))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
