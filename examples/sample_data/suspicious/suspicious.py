#!/usr/bin/env python3
"""
SIMULATION ONLY - NOT ACTUAL MALWARE
This file contains suspicious patterns for testing Scanlytic-ForensicAI
"""

import base64

# Simulated suspicious keywords (for detection testing)
# keylogger
# password
# credential
# backdoor
# reverse_shell

# Simulated obfuscation
obfuscated = "cGFzc3dvcmQ="  # "password" in base64
decoded = base64.b64decode(obfuscated)

# Simulated network references
malicious_url = "http://command-and-control.example/download"
attacker_ip = "192.0.2.123"

# This script does nothing malicious - it's just for testing detection
print("This is a safe test file with suspicious patterns")
