"""
Command-line interface for Scanlytic-ForensicAI.

Provides a user-friendly CLI for forensic file analysis with argument
parsing and output formatting.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from scanlytic import __version__
from scanlytic.core.analyzer import ForensicAnalyzer
from scanlytic.reporting.generator import ReportGenerator
from scanlytic.utils.config import Config
from scanlytic.utils.logger import get_logger

logger = get_logger()


def create_parser() -> argparse.ArgumentParser:
    """
    Create argument parser for CLI.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog='scanlytic',
        description='Scanlytic-ForensicAI: Automated File Classification '
                    'and Malicious Intent Scoring',
        epilog='For more information, visit: '
               'https://github.com/rohteemie/Scanlytic-ForensicAI'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze files for malicious intent'
    )

    analyze_parser.add_argument(
        'path',
        type=str,
        help='Path to file or directory to analyze'
    )

    analyze_parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively analyze directory'
    )

    analyze_parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file path for report'
    )

    analyze_parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['json', 'csv'],
        default='json',
        help='Report output format (default: json)'
    )

    analyze_parser.add_argument(
        '-c', '--config',
        type=str,
        help='Path to configuration file'
    )

    analyze_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    analyze_parser.add_argument(
        '--no-features',
        action='store_true',
        help='Exclude detailed features from report'
    )

    analyze_parser.add_argument(
        '--threshold',
        type=int,
        default=50,
        help='Malicious score threshold (default: 50)'
    )

    return parser


def analyze_command(args: argparse.Namespace) -> int:
    """
    Execute analyze command.

    Args:
        args: Parsed command-line arguments

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        # Load configuration
        config = None
        if args.config:
            config = Config(Path(args.config))
        else:
            config = Config()

        # Override config with CLI arguments
        if hasattr(args, 'threshold'):
            config.config['scoring']['malicious_threshold'] = args.threshold

        # Initialize analyzer
        analyzer = ForensicAnalyzer(config)

        # Determine if path is file or directory
        path = Path(args.path)

        if not path.exists():
            logger.error(f"Path does not exist: {args.path}")
            print(f"Error: Path does not exist: {args.path}")
            return 1

        # Perform analysis
        if path.is_file():
            logger.info(f"Analyzing file: {args.path}")
            results = analyzer.analyze_file(args.path)
        elif path.is_dir():
            logger.info(f"Analyzing directory: {args.path}")
            results = analyzer.analyze_directory(
                args.path,
                recursive=args.recursive
            )
        else:
            logger.error(f"Invalid path type: {args.path}")
            print(f"Error: Invalid path type: {args.path}")
            return 1

        # Generate report
        report_gen = ReportGenerator(
            include_features=not args.no_features,
            verbose=args.verbose
        )

        # Print summary to console
        report_gen.print_summary(results)

        # Save report if output specified
        if args.output:
            report_gen.generate_report(
                results,
                args.output,
                format=args.format
            )
            print(f"\nReport saved to: {args.output}")

        return 0

    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        return 130
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        print(f"\nError: {str(e)}")
        return 1


def main() -> int:
    """
    Main entry point for CLI.

    Returns:
        int: Exit code
    """
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == 'analyze':
        return analyze_command(args)

    return 0


if __name__ == '__main__':
    sys.exit(main())
