#!/usr/bin/env python3
"""
GuardKey Pre-Commit Hook
Written by IBM Bob for the 48-hour hackathon sprint
Intercepts commits, detects secrets, and provides educational feedback
"""

import subprocess
import sys
import json
import os
from pathlib import Path

# ANSI color codes for terminal output
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
BOLD = '\033[1m'
RESET = '\033[0m'


def print_education_message(finding):
    """Print educational message for a finding"""
    check_id = finding.get('check_id', 'unknown')
    path = finding.get('path', 'unknown')
    line = finding.get('start', {}).get('line', 'unknown')
    message = finding.get('extra', {}).get('message', 'Secret detected')
    
    print(f"\n{RED}{BOLD}🚨 SECRET DETECTED{RESET}")
    print(f"{YELLOW}Location:{RESET} {path}:{line}")
    print(f"{YELLOW}Type:{RESET} {check_id}")
    print(f"{YELLOW}Why this matters:{RESET}")
    print(f"  {message}")
    
    # Print remediation if available
    metadata = finding.get('extra', {}).get('metadata', {})
    remediation = metadata.get('remediation', '')
    if remediation:
        print(f"{GREEN}✅ How to fix:{RESET}")
        for line in remediation.strip().split('\n'):
            print(f"  {line}")
    print()


def main():
    """Main pre-commit hook logic"""
    # Get the repository root
    result = subprocess.run(
        ['git', 'rev-parse', '--show-toplevel'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"{RED}[GuardKey] Error: Not in a git repository{RESET}")
        sys.exit(1)
    
    repo_root = result.stdout.strip()
    rules_dir = Path(repo_root) / '.guardkey' / 'rules'
    
    if not rules_dir.exists():
        print(f"{YELLOW}[GuardKey] Rules directory not found at {rules_dir}{RESET}")
        print(f"{YELLOW}[GuardKey] Skipping secret scan{RESET}")
        sys.exit(0)
    
    # Run semgrep on staged files
    print(f"{BLUE}[GuardKey] Scanning for secrets...{RESET}")
    
    result = subprocess.run(
        [
            'semgrep',
            '--config', str(rules_dir),
            '--json',
            '--error',
            '.'
        ],
        capture_output=True,
        text=True,
        cwd=repo_root
    )
    
    if result.returncode == 0:
        print(f"{GREEN}[GuardKey] ✓ No secrets detected{RESET}")
        sys.exit(0)
    
    # Parse findings
    try:
        findings = json.loads(result.stdout).get('results', [])
    except json.JSONDecodeError:
        print(f"{RED}[GuardKey] Error parsing semgrep output{RESET}")
        sys.exit(1)
    
    if not findings:
        print(f"{GREEN}[GuardKey] ✓ No secrets detected{RESET}")
        sys.exit(0)
    
    # Separate high severity from warnings
    high_severity = [f for f in findings if f.get('extra', {}).get('severity') == 'ERROR']
    warnings = [f for f in findings if f.get('extra', {}).get('severity') == 'WARNING']
    
    # Print summary
    print(f"\n{RED}{BOLD}═══════════════════════════════════════{RESET}")
    print(f"{RED}{BOLD}[GuardKey] {len(high_severity)} secret(s) detected. Commit blocked.{RESET}")
    print(f"{RED}{BOLD}═══════════════════════════════════════{RESET}\n")
    
    # Print educational messages for high severity findings
    for finding in high_severity:
        print_education_message(finding)
    
    # Print warnings if any
    if warnings:
        print(f"{YELLOW}{BOLD}⚠️  Additional warnings ({len(warnings)}):{RESET}")
        for finding in warnings:
            path = finding.get('path', 'unknown')
            line = finding.get('start', {}).get('line', 'unknown')
            check_id = finding.get('check_id', 'unknown')
            print(f"  {YELLOW}→{RESET} {path}:{line} — {check_id}")
        print()
    
    print(f"{BLUE}💡 Learn more about secrets management: https://owasp.org/www-project-top-ten/{RESET}\n")
    
    # Block commit if high severity findings exist
    if high_severity:
        sys.exit(1)
    else:
        print(f"{YELLOW}[GuardKey] Only warnings found. Commit allowed but review recommended.{RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
