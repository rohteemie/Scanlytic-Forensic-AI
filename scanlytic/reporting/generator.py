"""
Report generator for Scanlytic-ForensicAI.

Generates analysis reports in various formats (JSON, CSV)
with comprehensive details and statistics.
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from scanlytic.utils.exceptions import ReportGenerationError
from scanlytic.utils.logger import get_logger

logger = get_logger()


class ReportGenerator:
    """
    Generates forensic analysis reports in multiple formats.

    Supports JSON and CSV output formats with customizable detail levels
    and privacy-compliant reporting.
    """

    def __init__(self, include_features: bool = True,
                 verbose: bool = True):
        """
        Initialize report generator.

        Args:
            include_features: Whether to include detailed features in report
            verbose: Whether to include verbose information
        """
        self.include_features = include_features
        self.verbose = verbose

    def generate_report(self, results: Dict[str, Any],
                        output_path: str,
                        format: str = 'json') -> None:
        """
        Generate analysis report in specified format.

        Args:
            results: Analysis results
            output_path: Path to output file
            format: Report format ('json' or 'csv')

        Raises:
            ReportGenerationError: If report generation fails
        """
        try:
            logger.info(f"Generating {format.upper()} report: {output_path}")

            if format.lower() == 'json':
                self._generate_json_report(results, output_path)
            elif format.lower() == 'csv':
                self._generate_csv_report(results, output_path)
            else:
                raise ReportGenerationError(
                    f"Unsupported report format: {format}"
                )

            logger.info(f"Report generated successfully: {output_path}")

        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            raise ReportGenerationError(
                f"Failed to generate report: {str(e)}"
            )

    def _generate_json_report(self, results: Dict[str, Any],
                              output_path: str) -> None:
        """
        Generate JSON format report.

        Args:
            results: Analysis results
            output_path: Path to output file
        """
        # Prepare report data
        report_data = self._prepare_report_data(results)

        # Write JSON file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

    def _generate_csv_report(self, results: Dict[str, Any],
                             output_path: str) -> None:
        """
        Generate CSV format report.

        Args:
            results: Analysis results
            output_path: Path to output file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Extract results list
        if 'results' in results:
            # Directory analysis
            results_list = results['results']
        else:
            # Single file analysis
            results_list = [results]

        if not results_list:
            logger.warning("No results to write to CSV")
            return

        # Define CSV columns
        fieldnames = [
            'file_name',
            'file_path',
            'file_size',
            'category',
            'file_type',
            'mime_type',
            'extension',
            'md5',
            'sha1',
            'sha256',
            'entropy',
            'suspicious_strings_count',
            'malicious_score',
            'risk_level',
            'is_malicious',
            'is_high_risk'
        ]

        # Write CSV file
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in results_list:
                row = self._extract_csv_row(result)
                writer.writerow(row)

    def _prepare_report_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare report data with proper structure.

        Args:
            results: Raw analysis results

        Returns:
            Dict[str, Any]: Formatted report data
        """
        # Check if single file or directory analysis
        if 'results' in results:
            # Directory analysis
            report = {
                'report_type': 'directory_analysis',
                'directory': results.get('directory'),
                'recursive': results.get('recursive', False),
                'summary': results.get('summary', {}),
                'total_files': results.get('total_files', 0),
                'errors': results.get('errors', 0),
                'files': []
            }

            for file_result in results.get('results', []):
                report['files'].append(
                    self._format_file_result(file_result)
                )

            if self.verbose and results.get('error_details'):
                report['error_details'] = results['error_details']

        else:
            # Single file analysis
            report = {
                'report_type': 'file_analysis',
                'file': self._format_file_result(results)
            }

        # Add metadata
        report['analysis_version'] = results.get('analysis_version', '0.1.0')
        report['generated_by'] = 'Scanlytic-ForensicAI'

        return report

    def _format_file_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single file result for reporting.

        Args:
            result: File analysis result

        Returns:
            Dict[str, Any]: Formatted file result
        """
        formatted = {
            'file_name': result.get('file_name'),
            'file_path': result.get('file_path'),
            'classification': result.get('classification', {}),
            'scoring': result.get('scoring', {})
        }

        if self.include_features:
            features = result.get('features', {})
            # Include selected features, exclude raw data
            formatted['features'] = {
                'file_size': features.get('file_size'),
                'extension': features.get('extension'),
                'entropy': features.get('entropy'),
                'hashes': {
                    'md5': features.get('md5'),
                    'sha1': features.get('sha1'),
                    'sha256': features.get('sha256')
                },
                'strings': {
                    'count': features.get('strings', {}).get('count', 0),
                    'suspicious_count': features.get(
                        'strings', {}
                    ).get('suspicious_count', 0)
                }
            }

            if self.verbose:
                # Include string samples in verbose mode
                formatted['features']['strings']['suspicious_patterns'] = \
                    features.get('strings', {}).get('suspicious_patterns', [])

        return formatted

    def _extract_csv_row(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract data for CSV row from result.

        Args:
            result: File analysis result

        Returns:
            Dict[str, Any]: CSV row data
        """
        features = result.get('features', {})
        classification = result.get('classification', {})
        scoring = result.get('scoring', {})

        return {
            'file_name': result.get('file_name', ''),
            'file_path': result.get('file_path', ''),
            'file_size': features.get('file_size', 0),
            'category': classification.get('category', ''),
            'file_type': classification.get('file_type', ''),
            'mime_type': classification.get('mime_type', ''),
            'extension': classification.get('extension', ''),
            'md5': features.get('md5', ''),
            'sha1': features.get('sha1', ''),
            'sha256': features.get('sha256', ''),
            'entropy': features.get('entropy', 0),
            'suspicious_strings_count': features.get(
                'strings', {}
            ).get('suspicious_count', 0),
            'malicious_score': scoring.get('score', 0),
            'risk_level': scoring.get('risk_level', ''),
            'is_malicious': scoring.get('is_malicious', False),
            'is_high_risk': scoring.get('is_high_risk', False)
        }

    def print_summary(self, results: Dict[str, Any]) -> None:
        """
        Print human-readable summary to console.

        Args:
            results: Analysis results
        """
        print("\n" + "=" * 70)
        print("SCANLYTIC-FORENSICAI ANALYSIS REPORT")
        print("=" * 70 + "\n")

        if 'results' in results:
            # Directory analysis summary
            summary = results.get('summary', {})
            print(f"Directory: {results.get('directory')}")
            print(f"Total Files Analyzed: {summary.get('total_files', 0)}")
            print(
                f"Average Malicious Score: "
                f"{summary.get('average_score', 0):.2f}"
            )
            print(
                f"High-Risk Files: "
                f"{summary.get('high_risk_files', 0)}"
            )
            print(f"\nRisk Distribution:")
            for level, count in summary.get(
                'risk_distribution', {}
            ).items():
                print(f"  {level.capitalize()}: {count}")

            print(f"\nCategory Distribution:")
            for category, count in summary.get(
                'category_distribution', {}
            ).items():
                print(f"  {category.capitalize()}: {count}")

        else:
            # Single file analysis
            print(f"File: {results.get('file_name')}")
            classification = results.get('classification', {})
            scoring = results.get('scoring', {})

            print(f"Category: {classification.get('category')}")
            print(f"File Type: {classification.get('file_type')}")
            print(
                f"Malicious Score: {scoring.get('score', 0):.2f}/100"
            )
            print(f"Risk Level: {scoring.get('risk_level', '').upper()}")
            print(
                f"Is Malicious: "
                f"{'YES' if scoring.get('is_malicious') else 'NO'}"
            )

        print("\n" + "=" * 70 + "\n")
