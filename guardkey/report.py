#!/usr/bin/env python3
"""
GuardKey Educational Report Generator
Generates detailed reports with remediation guidance
"""

import json
import sys
import argparse
from pathlib import Path


def generate_report(findings):
    """Generate educational report from findings"""
    report = []
    
    report.append("# GuardKey Security Report\n")
    report.append(f"## Summary\n")
    report.append(f"- **Total Findings:** {len(findings)}\n")
    
    high_severity = [f for f in findings if f.get('extra', {}).get('severity') == 'ERROR']
    warnings = [f for f in findings if f.get('extra', {}).get('severity') == 'WARNING']
    
    report.append(f"- **Critical:** {len(high_severity)}")
    report.append(f"- **Warnings:** {len(warnings)}\n")
    
    # Group by secret type
    secret_types = {}
    for finding in findings:
        check_id = finding.get('check_id', 'unknown')
        if check_id not in secret_types:
            secret_types[check_id] = []
        secret_types[check_id].append(finding)
    
    report.append("## Findings by Type\n")
    for secret_type, type_findings in secret_types.items():
        report.append(f"### {secret_type}")
        report.append(f"**Count:** {len(type_findings)}\n")
        
        for finding in type_findings[:3]:  # Show first 3 examples
            path = finding.get('path', 'unknown')
            line = finding.get('start', {}).get('line', 'unknown')
            message = finding.get('extra', {}).get('message', 'Secret detected')
            report.append(f"- **{path}:{line}** - {message}")
        
        if len(type_findings) > 3:
            report.append(f"- ... and {len(type_findings) - 3} more")
        report.append("")
    
    # Add remediation guide
    report.append("## Remediation Guide\n")
    report.append("### Best Practices for Secret Management\n")
    report.append("1. **Never hardcode secrets** in source code")
    report.append("2. **Use environment variables** for configuration")
    report.append("3. **Rotate compromised keys immediately**")
    report.append("4. **Use secret management services** (AWS Secrets Manager, HashiCorp Vault)")
    report.append("5. **Implement least privilege access** for all keys\n")
    
    report.append("### Example: Using Environment Variables\n")
    report.append("```python")
    report.append("# ❌ DON'T")
    report.append('API_KEY = "sk_live_1234567890"')
    report.append("")
    report.append("# ✅ DO")
    report.append("import os")
    report.append('API_KEY = os.environ.get("STRIPE_SECRET_KEY")')
    report.append("```\n")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='Generate GuardKey security report')
    parser.add_argument('--findings-file', help='JSON file with semgrep findings')
    parser.add_argument('--post-to-pr', action='store_true', help='Post report to PR (requires GitHub context')
    args = parser.parse_args()
    
    if args.findings_file:
        with open(args.findings_file, 'r') as f:
            findings = json.load(f).get('results', [])
    else:
        # Read from stdin
        findings = json.load(sys.stdin).get('results', [])
    
    report = generate_report(findings)
    print(report)
    
    if args.post_to_pr:
        print("\n[GuardKey] Report generated for PR comment")
        print("[GuardKey] In CI environment, this would post as a PR comment")


if __name__ == '__main__':
    main()
