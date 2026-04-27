"""
Example file with proper secret management - USE THIS PATTERN
This file demonstrates the correct way to handle secrets
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (not committed to git)
load_dotenv()

# ✅ GOOD: Use environment variables
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# ✅ GOOD: Use environment variables
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

# ✅ GOOD: Use environment variables or GitHub Secrets
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

# ✅ GOOD: Use environment variables
API_KEY = os.environ.get('API_KEY')

# ✅ GOOD: Load private key from secure file or secret manager
def get_private_key():
    key_path = os.environ.get('PRIVATE_KEY_PATH')
    if key_path and os.path.exists(key_path):
        with open(key_path, 'r') as f:
            return f.read()
    return None

# ✅ GOOD: Use environment variables for database credentials
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'user')

# Validate required environment variables
required_vars = ['AWS_ACCESS_KEY_ID', 'STRIPE_SECRET_KEY']
missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
