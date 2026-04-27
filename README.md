# GuardKey

AI-Powered Secrets Leak Prevention - Built with IBM Bob

> Every 11 minutes, a leaked API key scraped from a public repo is used to compromise a system. GuardKey stops this at the source.

## What is GuardKey?

GuardKey is a pre-commit hook and CI gate that detects secrets (API keys, passwords, tokens) leaking into codebases. Unlike traditional tools that just block commits, GuardKey **educates** developers on why it matters and how to fix it properly.

## How It Works

1. **Pre-Commit Hook**: Automatically scans code before it leaves your machine
2. **Secret Detection**: Uses Semgrep rules to identify 50+ secret patterns
3. **Educational Feedback**: Provides plain-English explanations and remediation guidance
4. **CI Gate**: Blocks PRs with critical secrets in GitHub Actions
5. **Team Dashboard**: Shows security knowledge gaps across your team

## Quick Start

### Prerequisites

- Python 3.7+
- Semgrep (`pip install semgrep`)
- Git

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/guardkey.git
cd guardkey
```

2. Install dependencies:
```bash
pip install semgrep
```

3. Install the pre-commit hook:
```bash
cp guardkey/pre-commit.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

4. Test it:
```bash
# Try to commit a file with a secret
echo 'API_KEY = "sk_live_1234567890"' > test.py
git add test.py
git commit -m "test"
```

## Features

### 🔍 Secret Detection Rules

GuardKey detects:
- AWS Access Keys (`AKIA*`)
- Stripe Keys (`sk_live_*`, `pk_live_*`)
- GitHub Tokens (`ghp_*`, `gho_*`)
- Private Keys (`-----BEGIN PRIVATE KEY-----`)
- Generic API keys
- And 50+ more patterns

### 📚 Educational Feedback

When a secret is detected, GuardKey provides:
- **What was found**: Exact secret type and location
- **Why it matters**: Security risk explanation
- **How to fix**: Code examples showing the correct pattern

Example output:
```
🚨 SECRET DETECTED
Location: config.py:12
Type: guardkey-stripe-secret-key
Why this matters:
  Stripe live secret key found in config.py. This key can charge cards 
  and access sensitive payment data. Rotate immediately and use 
  environment variables.

✅ How to fix:
  ❌ DON'T: hardcode Stripe keys
  ✅ DO: Use environment variables
  Example: os.environ.get('STRIPE_SECRET_KEY')
```

### 🚀 CI Integration

GuardKey integrates with GitHub Actions to:
- Scan every pull request
- Comment on PRs with educational reports
- Block PRs with critical secrets
- Track security trends over time

## Architecture

```
┌─────────────┐
│  Developer  │
│   commits   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Pre-Commit Hook │ ◄── Semgrep Rules
│  (Python)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Secret Found?  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   Yes        No
    │         │
    ▼         ▼
┌─────────┐  ┌──────────┐
│ Block + │  │  Allow   │
│ Educate │  │  Commit  │
└─────────┘  └──────────┘
```

## IBM Bob Integration

GuardKey was built in 48 hours using IBM Bob as the development partner. Bob contributed:

1. **Semgrep Rules**: Generated detection patterns for 50+ secret types
2. **Educational Content**: Wrote plain-English explanations for each rule
3. **CI Pipeline**: Scaffoled GitHub Actions workflow
4. **Security Review**: Performed OWASP A02 compliance check
5. **Code Review**: Caught bugs in the hook implementation

This demonstrates how Bob enables builders at any skill level to deliver high-quality, secure software with greater speed and confidence.

## Configuration

### Custom Rules

Add custom Semgrep rules to `.guardkey/rules/`:

```yaml
rules:
  - id: my-custom-rule
    patterns:
      - pattern-regex: 'MY_SECRET_[A-Z0-9]+'
    message: Custom secret detected
    languages: [python]
    severity: ERROR
```

### Ignore Patterns

Create `.guardkey/ignore` to exclude false positives:

```
# Test files
tests/fixtures/secrets.py
# Documentation
docs/examples/bad-pattern.py
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

GuardKey will automatically scan your PR for secrets! 🔒

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built for the IBM Bob Hackathon (May 15-17, 2026)

**GuardKey: Secrets don't leak. Developers learn.**
