# Scanlytic Forensic AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Automated File Classification and Malicious Intent Scoring using Python and Machine Learning for Digital Forensic Triage

## 📋 Table of Contents

- [Overview](🔍-overview)
- [Key Features](#key-features)
- [Problem Statement](#problem-statement)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Research Background](#research-background)
- [Roadmap](#roadmap)
- [Liscense](#-license)
- [Contact](#contact)

## 🔍 Overview

**Scanlytic-ForensicAI** is an AI-driven forensic triage system designed to revolutionize digital forensic analysis. This innovative tool automatically classifies files and assigns malicious intent scores based on extracted features, significantly enhancing the speed and accuracy of digital forensic investigations.

> **Note:** This project is currently under active development. The documentation below describes the planned architecture, features, and functionality that are being built based on applied research in digital forensics.

Built from applied research in the security perspective of digital forensics, Scanlytic-ForensicAI empowers security personnel, forensic analysts, and incident responders to quickly identify and prioritize potentially malicious files in large datasets, streamlining the investigative process.

### Why Scanlytic-ForensicAI?

In modern digital forensics, analysts face the challenge of examining massive volumes of data within tight timeframes. Manual analysis is time-consuming and prone to human error. Scanlytic-ForensicAI addresses these challenges by:

- **Automating** the initial triage process
- **Prioritizing** files based on malicious intent scores
- **Reducing** analysis time from hours to minutes
- **Improving** detection accuracy through machine learning
- **Enabling** forensic teams to focus on high-priority threats

## ✨ Key Features

### Core Capabilities

- **🤖 Intelligent File Classification**
  - Automatic categorization of files based on type, content, and behavior
  - Support for multiple file formats (executables, documents, archives, scripts, etc.)
  - Binary and multi-class classification models

- **🎯 Malicious Intent Scoring**
  - Advanced scoring algorithm that assigns risk levels (0-100)
  - Real-time threat assessment based on extracted features
  - Configurable threshold settings for different security policies

- **📊 Feature Extraction Engine**
  - Static analysis of file properties (size, entropy, headers, metadata)
  - PE header analysis for executables
  - String extraction and pattern matching
  - Hash computation (MD5, SHA1, SHA256)
  - File signature detection

- **⚡ High-Performance Processing**
  - Batch processing capabilities for large datasets
  - Parallel processing support
  - Optimized for speed without compromising accuracy

- **📈 Reporting & Visualization**
  - Detailed analysis reports in multiple formats (JSON, CSV, HTML)
  - Visual dashboards for threat distribution
  - Timeline analysis of suspicious activities
  - Export capabilities for integration with SIEM systems

- **🔄 Continuous Learning**
  - Model retraining capabilities
  - Integration with threat intelligence feeds
  - Adaptive learning from analyst feedback

## 🎯 Problem Statement

Digital forensic investigations are increasingly challenging due to:

1. **Volume**: Massive amounts of data requiring analysis
2. **Velocity**: Time-sensitive nature of incident response
3. **Variety**: Diverse file types and attack vectors
4. **Complexity**: Sophisticated evasion techniques used by malware

Traditional manual triage methods cannot keep pace with these challenges. Security personnel need intelligent tools that can:

- Quickly identify suspicious files in large datasets
- Accurately assess threat levels
- Provide actionable intelligence
- Scale with growing data volumes

Scanlytic-ForensicAI solves these problems through machine learning-powered automation, enabling faster and more accurate forensic triage.

## 📦 Installation

### Prerequisites

Before installing Scanlytic-ForensicAI, ensure you have:

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (recommended: venv or conda)
- Git
- At least 4GB RAM (8GB recommended)
- 2GB free disk space

### Installation Steps

1. **Clone the Repository**

```bash
git clone https://github.com/rohteemie/Scanlytic-ForensicAI.git
cd Scanlytic-ForensicAI
```

2. **Create Virtual Environment**

```bash
# Using venv
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

3. **Install Dependencies**

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

4. **Download Pre-trained Models** (if available)

```bash
python scripts/download_models.py
```

5. **Verify Installation**

```bash
python -m scanlytic --version
python -m scanlytic --health-check
```

### Docker Installation (Recommended for Easy Setup)

Docker provides the easiest way to get started with Scanlytic-ForensicAI:

```bash
# Build Docker image
docker build -t scanlytic-forensicai .

# Run analysis on a file
docker run -v /path/to/files:/data scanlytic-forensicai analyze /data/file.exe

# Run analysis on a directory with report output
docker run -v /path/to/files:/data -v /path/to/reports:/reports \
  scanlytic-forensicai analyze /data -o /reports/report.json
```

**For detailed Docker usage**, see the [Docker Guide](docs/DOCKER_GUIDE.md)

**New to Docker or digital forensics?** Check out our comprehensive guides:

- 📚 [Beginner's Guide](docs/BEGINNERS_GUIDE.md) - For students and new programmers
- 👤 [Non-Technical User Guide](docs/NON_TECHNICAL_GUIDE.md) - For non-technical users
- 🏗️ [Architecture Guide](docs/ARCHITECTURE.md) - Understanding the system design
- 💡 [Development Process Guide](docs/DEVELOPMENT_PROCESS.md) - How we built this

## 🚀 Usage

### Basic Usage

#### Command Line Interface

**Analyze a Single File**

```bash
python -m scanlytic analyze /path/to/suspicious_file.exe
```

**Analyze a Directory**

```bash
python -m scanlytic analyze /path/to/directory --recursive
```

**Batch Processing with Custom Output**

```bash
python -m scanlytic analyze /path/to/files \
    --output report.json \
    --format json \
    --threshold 50 \
    --verbose
```

### Advanced Usage

#### Custom Configuration

```bash
python -m scanlytic analyze /path/to/files \
    --config custom_config.yaml \
    --model custom_model.pkl \
    --workers 4
```

#### Generate Detailed Report

```bash
python -m scanlytic analyze /path/to/files \
    --report-type detailed \
    --output-format html \
    --include-visuals
```

### Python API

```python
from scanlytic import ForensicAnalyzer

# Initialize analyzer
analyzer = ForensicAnalyzer(
    model_path='models/classifier.pkl',
    config='config.yaml'
)

# Analyze single file
result = analyzer.analyze_file('/path/to/file.exe')
print(f"Classification: {result.classification}")
print(f"Malicious Score: {result.score}")
print(f"Features: {result.features}")

# Analyze directory
results = analyzer.analyze_directory(
    '/path/to/directory',
    recursive=True,
    threshold=50
)

# Generate report
analyzer.generate_report(
    results,
    output_path='report.html',
    format='html'
)
```

### Example Output

```json
{
  "file": "suspicious.exe",
  "classification": "malicious",
  "malicious_score": 87.3,
  "confidence": 0.94,
  "features": {
    "file_size": 245760,
    "entropy": 7.2,
    "file_type": "PE32 executable",
    "sections": 5,
    "imports": ["kernel32.dll", "advapi32.dll"],
    "suspicious_strings": ["cmd.exe", "powershell", "download"]
  },
  "threat_indicators": [
    "High entropy suggests packing/encryption",
    "Suspicious API calls detected",
    "Contains obfuscated strings"
  ],
  "recommendation": "Quarantine and investigate further"
}
```

## 🔬 How It Works

### Workflow Overview

```bash
┌─────────────────┐
│  Input Files    │
│  (Any Format)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   File Intake   │
│   & Validation  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Feature      │
│   Extraction    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   ML Model      │
│  Classification │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Malicious Intent│
│     Scoring     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Report       │
│   Generation    │
└─────────────────┘
```

### Processing Pipeline

1. **File Ingestion**: System accepts individual files or directories for analysis
2. **Preprocessing**: File validation, format detection, and metadata extraction
3. **Feature Engineering**: Extraction of relevant features including:
   - Static properties (size, type, timestamps)
   - Content-based features (entropy, byte distribution)
   - Structural features (PE headers, file signatures)
   - Behavioral indicators (strings, imports, exports)
4. **ML Classification**: Trained models classify files into categories:
   - Benign
   - Suspicious
   - Malicious
   - Unknown
5. **Scoring Algorithm**: Assigns a malicious intent score (0-100) based on:
   - Classification confidence
   - Feature weights
   - Known threat patterns
   - Historical data
6. **Result Aggregation**: Compiles findings into comprehensive reports with:
   - File classifications
   - Risk scores
   - Detailed analysis
   - Recommendations

## 🛠️ Technology Stack

### Core Technologies

- **Language**: Python 3.8+
- **Machine Learning**:
  - scikit-learn (Classification algorithms)
  - TensorFlow/Keras (Deep learning models)
  - XGBoost (Gradient boosting)
  - pandas (Data manipulation)
  - NumPy (Numerical computing)

### Analysis & Processing

- **Static Analysis**:
  - pefile (PE file analysis)
  - python-magic (File type detection)
  - yara-python (Pattern matching)

- **Feature Extraction**:
  - ssdeep (Fuzzy hashing)
  - entropy calculation libraries
  - regex patterns for string analysis

### Data & Storage

- **Database**: SQLite/PostgreSQL (Analysis results storage)
- **Caching**: Redis (Performance optimization)
- **Serialization**: pickle/joblib (Model persistence)

### Reporting & Visualization

- **Visualization**:
  - Matplotlib
  - Seaborn
  - Plotly (Interactive dashboards)
- **Reporting**:
  - Jinja2 (HTML reports)
  - ReportLab (PDF generation)

### Development & Testing

- **Testing**: pytest, unittest
- **Code Quality**: pylint, black, flake8
- **Documentation**: Sphinx
- **Version Control**: Git

## 🏗️ Project Architecture

### Directory Structure

```bash
Scanlytic-ForensicAI/
│
├── scanlytic/                 # Main package
│   ├── __init__.py
│   ├── analyzer.py           # Core analysis engine
│   ├── classifier.py         # ML classification models
│   ├── feature_extractor.py  # Feature extraction logic
│   ├── scorer.py             # Malicious intent scoring
│   ├── preprocessor.py       # Data preprocessing
│   └── utils/                # Utility functions
│       ├── file_handler.py
│       ├── hash_utils.py
│       └── logger.py
│
├── models/                    # Pre-trained ML models
│   ├── classifier_v1.pkl
│   └── feature_scaler.pkl
│
├── config/                    # Configuration files
│   ├── default_config.yaml
│   └── logging_config.yaml
│
├── scripts/                   # Utility scripts
│   ├── train_model.py
│   ├── download_models.py
│   └── benchmark.py
│
├── tests/                     # Test suite
│   ├── test_analyzer.py
│   ├── test_classifier.py
│   └── test_features.py
│
├── docs/                      # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── TRAINING.md
│
├── examples/                  # Example usage scripts
│   └── basic_analysis.py
│
├── data/                      # Sample data (not in repo)
│   ├── benign/
│   └── malicious/
│
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Development dependencies
├── setup.py                   # Package setup
├── .gitignore
├── LICENSE
└── README.md
```

### Component Overview

#### Analyzer Module

Central orchestrator that coordinates the analysis pipeline, managing data flow between components.

#### Feature Extractor

Implements various feature extraction techniques:

- Static file properties
- PE header analysis
- String extraction
- Entropy calculation
- Hash generation

#### Classifier

Machine learning models for file classification:

- Random Forest
- Gradient Boosting
- Neural Networks
- Ensemble methods

#### Scorer

Sophisticated scoring algorithm that combines:

- Model predictions
- Feature weights
- Threat intelligence
- Historical patterns

## ⚙️ Configuration

### Configuration File Structure

Create a `config.yaml` file to customize behavior:

```yaml
# Analysis Configuration
analysis:
  max_file_size: 104857600  # 100MB
  timeout: 300              # seconds
  parallel_workers: 4

# Feature Extraction
features:
  extract_strings: true
  string_min_length: 4
  calculate_entropy: true
  extract_pe_headers: true
  compute_hashes: ["md5", "sha1", "sha256"]

# Classification
classification:
  model_path: "models/classifier_v1.pkl"
  confidence_threshold: 0.7
  enable_ensemble: true

# Scoring
scoring:
  malicious_threshold: 50
  high_risk_threshold: 75
  weight_features: true

# Output
output:
  format: "json"  # json, csv, html
  verbose: true
  include_features: true
  save_samples: false

# Logging
logging:
  level: "INFO"
  file: "scanlytic.log"
  console: true
```

### Environment Variables

```bash
export SCANLYTIC_CONFIG=/path/to/config.yaml
export SCANLYTIC_MODEL_PATH=/path/to/models
export SCANLYTIC_LOG_LEVEL=DEBUG
export SCANLYTIC_WORKERS=8
```

## 🤝 Contributing

We welcome contributions from the community! Whether it's bug reports, feature requests, documentation improvements, or code contributions, your help is appreciated.

### How to Contribute

1. **Fork the Repository**

   ```bash
   git clone https://github.com/rohteemie/Scanlytic-ForensicAI.git
   cd Scanlytic-ForensicAI
   ```

2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines
   - Add tests for new features
   - Update documentation as needed

4. **Test Your Changes**

   ```bash
   pytest tests/
   pylint scanlytic/
   ```

5. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push and Create Pull Request**

   ```bash
   git push origin feature/your-feature-name
   ```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v --cov=scanlytic

# Check code quality
pylint scanlytic/
black scanlytic/
flake8 scanlytic/
```

### Contribution Guidelines

- Follow Python PEP 8 style guide
- Write comprehensive tests for new features
- Document all public APIs
- Keep commits atomic and well-described
- Update README if adding new features
- Ensure all tests pass before submitting PR

### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a welcoming and inclusive community.

## 🔬 Research Background

Scanlytic-ForensicAI is the product of applied research in digital forensics and cybersecurity. This project emerged from investigating:

### Research Focus Areas

1. **Machine Learning in Forensics**
   - Application of supervised learning to malware detection
   - Feature engineering for file classification
   - Model interpretability in security contexts

2. **Automated Triage Systems**
   - Reducing manual analysis overhead
   - Prioritization algorithms for forensic investigations
   - Real-time threat assessment methodologies

3. **Security Perspective**
   - Threat modeling and risk assessment
   - Attack vector analysis
   - Evasion technique detection

### Research Methodology

The system was developed using:

- Analysis of real-world forensic datasets
- Collaboration with security professionals
- Iterative testing and validation
- Benchmarking against existing tools

### Academic Foundation

This work builds upon research in:

- Machine learning for malware detection
- Static and dynamic analysis techniques
- Digital forensic triage methodologies
- Automated threat intelligence

### Publications & Citations

If you use Scanlytic-ForensicAI in your research, please cite:

```bash
@software{scanlytic_forensicai,
  author = {Owolabi, Rotimi},
  title = {Scanlytic-ForensicAI: AI-Driven Forensic Triage System},
  year = {2025},
  url = {https://github.com/rohteemie/Scanlytic-Forensic-AI}
}
```

## 🗺️ Roadmap

### Current Version (v0.1.0)

- [x] Core file classification engine
- [x] Basic feature extraction
- [x] Malicious intent scoring
- [x] Command-line interface
- [x] JSON/CSV report generation

### Planned Features

#### Version 0.2.0 (Short-term)

- [ ] Web-based dashboard
- [ ] Enhanced PE analysis
- [ ] Support for archive files
- [ ] Integration with VirusTotal API
- [ ] Real-time monitoring capabilities

#### Version 0.3.0 (Mid-term)

- [ ] Dynamic analysis integration
- [ ] Memory forensics support
- [ ] Network traffic analysis
- [ ] Behavioral analysis engine
- [ ] Custom YARA rule support

#### Version 1.0.0 (Long-term)

- [ ] Enterprise features
- [ ] Multi-user support
- [ ] REST API
- [ ] Plugin architecture
- [ ] Cloud deployment options
- [ ] Advanced reporting and analytics

### Long-term Vision

- Distributed processing for large-scale investigations
- Integration with major SIEM platforms
- Mobile application for field analysis
- Automated threat hunting capabilities
- Community-driven threat intelligence sharing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```bash
MIT License

Copyright (c) 2025 Rotimi Owolabi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 📧 Contact

**Author**: Rotimi Owolabi

- GitHub: [@rohteemie](https://github.com/rohteemie)
- Project Link: [https://github.com/rohteemie/Scanlytic-ForensicAI](https://github.com/rohteemie/Scanlytic-ForensicAI)
- Email: [Contact via GitHub](https://github.com/rohteemie)

### Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/rohteemie/Scanlytic-ForensicAI/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/rohteemie/Scanlytic-ForensicAI/discussions)
- **Security**: Report security vulnerabilities privately via GitHub Security Advisories

### Inspiration

This project was inspired by my love for security systems and the need for accessible, efficient forensic tools that can keep pace with modern cyber threats, and the ease of investigations for security professionals at all levels.

---

>
> **If you find this project useful, please consider giving it a star! ⭐**
>
> Made with ❤️ for the digital forensics and cybersecurity community
