"""Train a minimal baseline AI model for Scanlytic-ForensicAI."""

import argparse

from scanlytic.ai.training import train_baseline_model


def main():
    parser = argparse.ArgumentParser(
        description='Train baseline AI model for Scanlytic.'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='models/ai_baseline.joblib',
        help='Output path for the model file'
    )
    args = parser.parse_args()

    output_path = train_baseline_model(args.output)
    print(f"Saved baseline model to {output_path}")


if __name__ == '__main__':
    main()
