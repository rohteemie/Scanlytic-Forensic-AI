# Sample Data for Scanlytic-ForensicAI

This directory contains sample files for testing and demonstration purposes.

## Structure

- `benign/`: Safe, benign files for testing
- `suspicious/`: Files with suspicious characteristics (simulated, not actual malware)

## Usage

These samples can be used to test Scanlytic-ForensicAI's analysis capabilities:

```bash
# Analyze benign samples
scanlytic analyze examples/sample_data/benign/ -r

# Analyze suspicious samples
scanlytic analyze examples/sample_data/suspicious/ -r

# Analyze all samples
scanlytic analyze examples/sample_data/ -r -o results.json
```

## Safety Note

All files in the `suspicious/` directory are **safe simulations** created for testing purposes. They contain patterns that Scanlytic looks for but are not actual malware.

Never use real malware samples in development or testing environments without proper isolation and security measures.

## Adding More Samples

You can add your own test files following this structure:
- Keep benign files clearly separated
- Document the expected behavior
- Never commit actual malicious files to the repository
