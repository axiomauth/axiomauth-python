# axiomauth-python

Official Python SDK for the [AxiomAuth](https://axiomauth.com) identity platform.

[![PyPI version](https://img.shields.io/pypi/v/axiomauth.svg)](https://pypi.org/project/axiomauth/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## Installation

```bash
pip install axiomauth
```

## Quick Start

```python
from axiomauth import AxiomAuth

client = AxiomAuth(api_key=os.environ["AXIOMAUTH_API_KEY"])

# List users
result = client.users.list()
for user in result["data"]:
    print(user["email"], user["role"])

# Get org configuration
config = client.config.get()
print(config["saml_metadata_url"])

# Query audit log
events = client.audit.list(action="login.success", limit=50)
```

## Authentication

```python
client = AxiomAuth(api_key="axm_live_your_key_here")
```

Generate keys from your [dashboard](https://axiomauth.com/dashboard).

## API Reference

### Users

```python
# List (paginated)
result = client.users.list(page=1, per_page=20)

# Single user
user = client.users.get("usr_abc123")

# Deprovision
client.users.deprovision("usr_abc123")
```

### Sessions

```python
sessions = client.sessions.list()
client.sessions.revoke("sess_abc123")
```

### Config

```python
config = client.config.get()
# { org_id, org_name, sso_enabled, saml_metadata_url,
#   scim_endpoint, mfa_required, session_duration_hours, ... }

client.config.update({"session_duration_hours": 12})
```

### Audit

```python
events = client.audit.list(
    from_dt="2025-01-01T00:00:00Z",
    action="login.failure",
    limit=100
)
```

## Async Support

```python
from axiomauth import AsyncAxiomAuth

async with AsyncAxiomAuth(api_key=os.environ["AXIOMAUTH_API_KEY"]) as client:
    users = await client.users.list()
```

## Support

- Docs: [axiomauth.com/docs](https://axiomauth.com/docs)
- Email: support@axiomauth.com

## License

[MIT](LICENSE) — © Axiom Identity Services Ltd.
