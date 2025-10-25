#!/usr/bin/env python3
"""
Example usage of Scanlytic-ForensicAI Python API.

This script demonstrates how to use the ForensicAnalyzer programmatically.
"""

import sys
from pathlib import Path

from scanlytic.core.analyzer import ForensicAnalyzer
from scanlytic.reporting.generator import ReportGenerator
from scanlytic.utils.config import Config


def main():
    """Main example function."""
    print("Scanlytic-ForensicAI API Example\n")
    print("=" * 70)

    # Basic Analysis Example
    print("\n1. Basic File Analysis")
    print("-" * 70)

    # Create analyzer with default configuration
    analyzer = ForensicAnalyzer()

    # For demonstration, create a test file
    test_file = Path('example_test.txt')
    test_file.write_text('Example content for analysis')

    try:
        result = analyzer.analyze_file(str(test_file))

        print(f"File: {result['file_name']}")
        print(f"Category: {result['classification']['category']}")
        print(f"Risk Score: {result['scoring']['score']:.2f}/100")
        print(f"Risk Level: {result['scoring']['risk_level'].upper()}")

    finally:
        if test_file.exists():
            test_file.unlink()

    print("\n" + "=" * 70)
    print("Example completed successfully!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
