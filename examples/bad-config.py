"""
Example file with secrets - DO NOT USE IN PRODUCTION
This file is for testing GuardKey detection capabilities
"""

# ❌ BAD: Hardcoded AWS keys
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ❌ BAD: Hardcoded Stripe keys
# GuardKey detects patterns like: sk_live_*, pk_live_*, sk_test_*, pk_test_*
# Example pattern (DO NOT USE): STRIPE_SECRET_KEY = "sk_live_..."

# ❌ BAD: Hardcoded GitHub token
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz123456"

# ❌ BAD: Generic API key
API_KEY = "api_key_1234567890abcdefghijklmnopqrstuvwxyz"

# ❌ BAD: Private key in code
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAz1z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z
8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8
8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8
8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8
8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8
8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8z8
-----END RSA PRIVATE KEY-----"""

# ❌ BAD: Database credentials
DB_PASSWORD = "SuperSecretPassword123!"
DB_HOST = "db.example.com"
DB_USER = "admin"
