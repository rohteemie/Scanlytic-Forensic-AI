# Beginner's Guide to Scanlytic-ForensicAI

## Welcome! 🎓

This guide is designed for **students**, **new Python programmers**, and **anyone learning about digital forensics**. We'll explain everything from the ground up, assuming no prior knowledge of forensic analysis or advanced programming concepts.

## Table of Contents

1. [What is Scanlytic-ForensicAI?](#what-is-scanlytic-forensicai)
2. [Why Does This Project Exist?](#why-does-this-project-exist)
3. [How Does It Work? (Simple Explanation)](#how-does-it-work)
4. [Project Structure Explained](#project-structure-explained)
5. [Core Concepts](#core-concepts)
6. [How Components Work Together](#how-components-work-together)
7. [Getting Started](#getting-started)
8. [Your First Analysis](#your-first-analysis)
9. [Understanding the Results](#understanding-the-results)
10. [For Developers: Contributing](#for-developers-contributing)

---

## What is Scanlytic-ForensicAI?

Imagine you're a detective investigating a computer. You find thousands of files - documents, programs, images, and more. Which ones are important? Which ones might be dangerous? Going through them one by one would take forever!

**Scanlytic-ForensicAI** is like a smart assistant that:

- Looks at each file
- Figures out what type of file it is
- Checks for suspicious characteristics
- Gives each file a "danger score" from 0 to 100
- Creates a report showing which files need investigation

Think of it as a "file sorting robot" for digital forensics.

### Real-World Example

**Scenario**: A company's computer was hacked. There are 10,000 files on the hard drive.

**Without Scanlytic**:

- Manual review: 10-20 seconds per file
- Total time: ~55 hours of work
- Risk of missing important files due to fatigue

**With Scanlytic**:

- Automatic analysis: <1 second per file
- Total time: ~3 hours (including setup and review)
- Files ranked by suspiciousness
- Investigators focus only on high-risk files

---

## Why Does This Project Exist?

### The Problem

Digital forensic investigators face several challenges:

1. **Too Much Data**: Modern storage devices hold millions of files
2. **Time Pressure**: Investigations often have strict deadlines
3. **Hidden Threats**: Malicious files can disguise themselves
4. **Human Error**: Manual review is prone to mistakes when tired

### The Solution

Scanlytic-ForensicAI automates the initial sorting ("triage") process using:
- **File analysis**: Examining file properties and contents
- **Pattern recognition**: Identifying suspicious characteristics
- **Scoring system**: Ranking files by potential danger
- **Machine Learning** (future): Learning from known malicious files

---

## How Does It Work? (Simple Explanation)

Let's break down the analysis process into simple steps:

### Step 1: File Identification

**What it does**: Figures out what type of file it is

**How it works**:

```bash
You give it: mystery_file.doc
It checks: First few bytes of the file (called "magic numbers")
It determines: "This is a Microsoft Word document"
```

**Why this matters**: Attackers often rename malicious programs to look harmless (e.g., `vacation_photo.jpg` that's actually a virus)

### Step 2: Feature Extraction

**What it does**: Collects information about the file

**Information collected**:

- **Basic stuff**: Size, creation date, file permissions
- **Hashes**: Unique "fingerprint" of the file (like DNA for files)
- **Entropy**: How random/compressed the file is
- **Strings**: Text found inside the file

**Example**:

```bash
File: suspicious.exe
Size: 245,760 bytes
Created: 2024-10-15 03:45:22
Hash (SHA-256): 3a5f6b8c9d...
Entropy: 7.2/8.0 (high - possibly compressed)
Strings found: "cmd.exe", "password", "download"
```

### Step 3: Malicious Scoring

**What it does**: Calculates a danger score (0-100)

**Factors considered**:

- High entropy (7.2/8.0) → Suspicious (+20 points)
- Contains "cmd.exe" string → Suspicious (+15 points)
- Contains "password" → Suspicious (+10 points)
- Is an executable (.exe) → Risky by nature (+20 points)
- **Total Score**: 65/100 → **HIGH RISK**

### Step 4: Reporting

**What it does**: Creates an easy-to-read report

**Report includes**:

- List of all analyzed files
- Risk score for each file
- Explanation of why each file is risky
- Summary statistics

---

## Project Structure Explained

Let's tour the codebase and explain each part:

```bash
Scanlytic-ForensicAI/
│
├── scanlytic/              # Main application code
│   ├── cli.py              # Command-line interface (how users interact)
│   ├── core/               # Core functionality
│   │   ├── analyzer.py     # Orchestrates the analysis process
│   │   └── classifier.py   # Identifies file types
│   ├── features/           # Feature extraction
│   │   └── extractor.py    # Extracts file information
│   ├── scoring/            # Scoring system
│   │   └── scorer.py       # Calculates danger scores
│   ├── reporting/          # Report generation
│   │   └── generator.py    # Creates JSON/CSV reports
│   └── utils/              # Helper functions
│       ├── config.py       # Configuration management
│       ├── file_utils.py   # File handling utilities
│       ├── logger.py       # Logging system
│       └── exceptions.py   # Error definitions
│
├── tests/                  # Automated tests
│   ├── unit/               # Test individual components
│   └── integration/        # Test components working together
│
├── docs/                   # Documentation
│   └── (this file!)
│
├── config/                 # Configuration files
│   └── default_config.yaml # Default settings
│
├── examples/               # Example usage scripts
│
├── requirements.txt        # Python packages needed
├── setup.py                # Installation script
└── README.md               # Project overview
```

### What Each Directory Does

#### `scanlytic/` - The Brain

This is where all the magic happens. It's organized by function:

- **cli.py**: The "front door" - where you type commands
- **core/**: The "thinking" components - analysis and classification
- **features/**: The "eyes" - examining files
- **scoring/**: The "judge" - deciding if files are dangerous
- **reporting/**: The "secretary" - writing reports
- **utils/**: The "toolbox" - helper functions used everywhere

#### `tests/` - Quality Control

Contains automated tests that ensure everything works correctly. Think of it as a robot that checks the code thousands of times to catch bugs.

#### `docs/` - The Manual

Documentation explaining how everything works (including this guide!).

---

## Core Concepts

### Concept 1: File Classification

**What is it?**
Determining what type of file you're looking at.

**Why it matters?**

Different file types have different risk levels:
- Executables (.exe, .app) → Can run code (higher risk)
- Documents (.pdf, .doc) → Usually safe, but can have macros
- Images (.jpg, .png) → Generally safe
- Scripts (.py, .sh) → Can execute commands (higher risk)

**How we do it:**

```python
# Simplified example
def classify_file(file_path):
    # Read first few bytes (magic numbers)
    with open(file_path, 'rb') as f:
        header = f.read(4)

    # Check against known signatures
    if header == b'MZ':  # DOS/Windows executable
        return "Windows Executable"
    elif header[:2] == b'\xff\xd8':  # JPEG image
        return "JPEG Image"
    # ... many more checks ...
```

### Concept 2: Entropy

**What is it?**
A measure of randomness in data (scale: 0-8).

**What it tells us:**

- **Low entropy (0-3)**: Repetitive data (text files, simple images)
- **Medium entropy (3-6)**: Normal files
- **High entropy (6-8)**: Compressed or encrypted data

**Why it matters:**
Malware often uses encryption/compression to hide from detection.

**Visual example:**

```bash
Low Entropy (2.3):
"AAAAAABBBBBBCCCCCC"  # Very repetitive

Medium Entropy (4.5):
"Hello, this is normal text with variety."

High Entropy (7.8):
"9x$mK@#pqL&zR^vF%wN"  # Looks random (encrypted?)
```

### Concept 3: Hash Functions

**What is it?**
A mathematical function that creates a unique "fingerprint" for a file.

**Analogy:**
Like a fingerprint or DNA - no two files have the same hash (practically speaking).

**Example:**

```bash
File: document.pdf (1 MB)
MD5 Hash: 5d41402abc4b2a76b9719d911017c592

File: document_modified.pdf (1 MB + 1 byte changed)
MD5 Hash: 7f5d2b89f1e0c24d3a8e9c6b4f1a0d2e
         ↑ Completely different!
```

**Why we use it:**

1. Identify known malicious files (hash matching)
2. Detect if file has been modified
3. Remove duplicate files

### Concept 4: String Extraction

**What is it?**
Finding readable text inside binary files.

**Why it matters:**

Malware often contains revealing strings:
- Command-line tools it uses ("cmd.exe", "powershell")
- Network addresses (URLs, IPs)
- Suspicious keywords ("keylog", "backdoor", "steal")

**Example:**

```bash
Binary file: malware.exe
Strings found:
- "http://malicious-site.com"
- "password"
- "C:\\Windows\\System32\\cmd.exe"
- "keylogger_data.txt"

→ Very suspicious!
```

---

## How Components Work Together

Let's trace a file through the entire system:

### The Journey of a File

```bash
┌─────────────────────────────────────────────────────────┐
│ Step 1: User Input                                      │
│ User runs: scanlytic analyze suspicious.exe             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: CLI (cli.py)                                    │
│ - Parses command-line arguments                         │
│ - Validates input file exists                           │
│ - Creates ForensicAnalyzer instance                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Analyzer (core/analyzer.py)                     │
│ - Orchestrates the analysis pipeline                    │
│ - Calls classifier, feature extractor, scorer           │
└────────────────────┬────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
┌──────────┐  ┌────────────┐  ┌──────────┐
│Classifier│  │  Feature   │  │ Scorer   │
│          │  │ Extractor  │  │          │
│Identifies│  │Examines    │  │Calculates│
│file type │  │properties  │  │risk score│
└──────────┘  └────────────┘  └──────────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Result Compilation                              │
│ {                                                       │
│   "file_name": "suspicious.exe",                        │
│   "classification": "Windows Executable",               │
│   "features": {...},                                    │
│   "scoring": {"score": 75, "risk_level": "critical"}    │
│ }                                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Report Generation (reporting/generator.py)      │
│ - Formats results as JSON/CSV                           │
│ - Displays summary on screen                            │
│ - Saves to file if requested                            │
└─────────────────────────────────────────────────────────┘
```

### Code Flow Example

Here's simplified code showing how components interact:

```python
# cli.py - Entry point
def main():
    args = parse_arguments()  # Get user input
    analyzer = ForensicAnalyzer()  # Create analyzer
    results = analyzer.analyze_file(args.file)  # Analyze
    reporter = ReportGenerator()
    reporter.generate_report(results)  # Generate report

# core/analyzer.py - Orchestrator
class ForensicAnalyzer:
    def analyze_file(self, file_path):
        # Step 1: Classify the file
        classification = self.classifier.classify(file_path)

        # Step 2: Extract features
        features = self.extractor.extract(file_path)

        # Step 3: Calculate score
        score = self.scorer.score(features, classification)

        # Step 4: Return combined results
        return {
            'classification': classification,
            'features': features,
            'scoring': score
        }
```

---

## Getting Started

### Prerequisites

You'll need:

1. **Python 3.8 or higher** - The programming language
2. **pip** - Python's package installer (comes with Python)
3. **Basic command-line skills** - Opening a terminal/command prompt

### Installation (Step-by-Step)

#### Option 1: Regular Installation

**Step 1: Install Python**

- Windows: Download from [python.org](https://www.python.org/downloads/)
- macOS: `brew install python3` (if you have Homebrew)
- Linux: Usually pre-installed, or `sudo apt install python3 python3-pip`

**Step 2: Verify Installation**

```bash
python --version  # Should show Python 3.8 or higher
pip --version     # Should show pip version
```

**Step 3: Clone the Repository**

```bash
git clone https://github.com/rohteemie/Scanlytic-ForensicAI.git
cd Scanlytic-ForensicAI
```

**Step 4: Create Virtual Environment** (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**Step 5: Install the Package**

```bash
pip install -e .
```

**Step 6: Verify Installation**

```bash
scanlytic --version
# Should display: scanlytic 0.1.0
```

#### Option 2: Docker Installation (Easiest!)

If you have Docker installed:

```bash
# Build the Docker image
docker build -t scanlytic-forensicai .

# Run analysis
docker run -v /path/to/your/files:/data scanlytic-forensicai analyze /data
```

---

## Your First Analysis

Let's analyze a file step by step!

### Example 1: Analyze a Single File

```bash
# Create a test file (a simple Python script)
echo "print('Hello, World!')" > test_script.py

# Analyze it
scanlytic analyze test_script.py
```

**Output you'll see:**

```bash
=== Analysis Results ===

File: test_script.py
Category: Python Script
Malicious Score: 15.0
Risk Level: low

Summary:
- File is a Python script
- Low entropy (2.3) - normal text file
- Contains common programming keywords
- No suspicious patterns detected
- Overall: Low risk
```

### Example 2: Analyze Multiple Files

```bash
# Analyze all files in a directory
scanlytic analyze /path/to/directory

# Analyze recursively (including subdirectories)
scanlytic analyze /path/to/directory --recursive
```

### Example 3: Generate a Report

```bash
# Generate JSON report
scanlytic analyze myfile.exe -o report.json -f json

# Generate CSV report
scanlytic analyze /path/to/directory -o report.csv -f csv

# The report will be saved to the specified file
```

### Example 4: Adjust Sensitivity

```bash
# Use stricter threshold (flag more files as suspicious)
scanlytic analyze file.exe --threshold 30

# Use looser threshold (only flag very suspicious files)
scanlytic analyze file.exe --threshold 70
```

---

## Understanding the Results

### Reading the Console Output

When you analyze a file, you'll see output like this:

```bash
=== Analysis Results ===

File: suspicious.exe
Category: Windows Executable
Malicious Score: 78.5
Risk Level: critical

Features:
├─ File Size: 1.2 MB
├─ Entropy: 7.4/8.0 (HIGH)
├─ MD5: 5d41402abc4b2a76b9719d911017c592
├─ SHA-256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
└─ Suspicious Strings: 6 found

Risk Factors:
✗ High entropy (suggests encryption/packing)
✗ Suspicious strings detected:
  - "cmd.exe"
  - "powershell"
  - "password"
✗ Executable file type (higher inherent risk)
✗ Contains network indicators

Recommendation: INVESTIGATE IMMEDIATELY
```

### What Each Field Means

**Category**:

- The type of file (e.g., "Windows Executable", "PDF Document")
- Determined by examining the file's structure

**Malicious Score**:

- A number from 0 to 100
- 0-25: Low risk (probably safe)
- 25-50: Medium risk (be cautious)
- 50-75: High risk (likely malicious)
- 75-100: Critical risk (almost certainly malicious)

**Risk Level**:

- Simple categorization: low, medium, high, critical
- Based on the malicious score

**Features**:

- Technical details about the file
- Used to calculate the malicious score

**Risk Factors**:

- Specific reasons why the file is considered risky
- Helps you understand the score

### Understanding the JSON Report

If you generate a JSON report, it looks like this:

```json
{
  "file_name": "suspicious.exe",
  "file_path": "/path/to/suspicious.exe",
  "classification": {
    "category": "Windows Executable",
    "mime_type": "application/x-dosexec",
    "extension": ".exe"
  },
  "features": {
    "file_size": 1234567,
    "entropy": 7.4,
    "md5": "5d41402abc4b2a76b9719d911017c592",
    "sha256": "e3b0c442...",
    "suspicious_strings": [
      "cmd.exe",
      "powershell"
    ]
  },
  "scoring": {
    "score": 78.5,
    "risk_level": "critical",
    "is_high_risk": true,
    "risk_factors": [
      "High entropy (7.4)",
      "Suspicious strings detected",
      "Executable file type"
    ]
  }
}
```

**How to use this:**

- Import into other tools for further analysis
- Create custom reports or visualizations
- Integrate with security systems

---

## For Developers: Contributing

Want to help improve Scanlytic-ForensicAI? Here's how!

### Understanding the Code

#### Key Files to Know

1. **scanlytic/core/analyzer.py**
   - The "main controller"
   - Coordinates all other components
   - Good starting point for understanding the flow

2. **scanlytic/features/extractor.py**
   - Examines files and extracts information
   - Great for adding new feature extraction methods

3. **scanlytic/scoring/scorer.py**
   - Calculates risk scores
   - Good for tuning the scoring algorithm

### Making Your First Contribution

**Step 1: Find an Issue**

- Look for issues labeled "good first issue" on GitHub
- Or find something you want to improve

**Step 2: Fork and Clone**

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Scanlytic-ForensicAI.git
cd Scanlytic-ForensicAI
```

**Step 3: Create a Branch**

```bash
git checkout -b my-new-feature
```

**Step 4: Make Changes**

- Write your code
- Follow the existing code style
- Add tests for new features

**Step 5: Test Your Changes**

```bash
# Run tests
pytest tests/

# Check code style
pycodestyle scanlytic/
```

**Step 6: Submit Pull Request**

- Push your changes to your fork
- Open a Pull Request on GitHub
- Describe what you changed and why

### Code Style Guidelines

We follow PEP 8 style guidelines:

```python
# Good: Clear variable names, proper spacing
def calculate_entropy(file_path):
    """
    Calculate Shannon entropy of a file.

    Args:
        file_path: Path to the file

    Returns:
        float: Entropy value (0-8)
    """
    data = read_file(file_path)
    return compute_shannon_entropy(data)

# Bad: Unclear names, poor formatting
def calc(fp):
    d=read(fp)
    return cse(d)
```

### Testing Best Practices

Always add tests for new features:

```python
# tests/unit/test_new_feature.py
import pytest
from scanlytic.features.extractor import FeatureExtractor

def test_entropy_calculation():
    """Test that entropy is calculated correctly."""
    extractor = FeatureExtractor()

    # Create test file
    test_file = create_test_file("AAAA")  # Low entropy

    # Extract features
    features = extractor.extract(test_file)

    # Assert entropy is low
    assert features['entropy'] < 2.0
```

---

## Learning Resources

### Digital Forensics Basics

- [NIST Digital Forensics Resources](https://www.nist.gov/topics/forensic-science/digital-evidence)
- [Digital Forensics Basics (YouTube)](https://www.youtube.com/results?search_query=digital+forensics+basics)

### Python Programming

- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python - Beginner Tutorials](https://realpython.com/start-here/)
- [Python for Beginners (YouTube)](https://www.youtube.com/results?search_query=python+for+beginners)

### File Formats and Analysis

- [File Signatures Database](https://en.wikipedia.org/wiki/List_of_file_signatures)
- [PE File Format](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)

### Machine Learning (for future features)

- [Machine Learning Crash Course (Google)](https://developers.google.com/machine-learning/crash-course)
- [scikit-learn Tutorial](https://scikit-learn.org/stable/tutorial/index.html)

---

## Frequently Asked Questions

### Q: Is this tool safe to use on real malware?

**A:** Yes! Scanlytic only *reads* files, it never executes them. However:
- Always work in a isolated/sandboxed environment
- Use a virtual machine for analyzing unknown files
- Never run suspicious files directly

### Q: Can this replace human forensic analysts?

**A:** No. Scanlytic is a *triage* tool that helps analysts prioritize their work. Human expertise is still essential for:
- Final determination of maliciousness
- Understanding context
- Legal requirements
- Complex cases

### Q: How accurate is the malicious scoring?

**A:** The current version uses rule-based scoring, which is about 70-80% accurate. Future versions will use machine learning to improve accuracy to 90%+.

### Q: Can I use this for commercial purposes?

**A:** Yes! The project is MIT licensed, which allows commercial use. However, please:
- Give appropriate credit
- Consider contributing improvements back
- Understand this is provided "as-is" without warranty

### Q: How can I improve the detection accuracy?

**A:** Several ways:
1. Adjust the scoring weights in `scanlytic/scoring/scorer.py`
2. Add new feature extraction methods
3. Contribute training data for machine learning models
4. Report false positives/negatives as GitHub issues

### Q: What if I find a bug?

**A:** Please report it! Open an issue on GitHub with:

- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

---

## Next Steps

Now that you understand how Scanlytic-ForensicAI works:

1. **Try it out**: Analyze some files on your computer
2. **Read the code**: Start with `scanlytic/core/analyzer.py`
3. **Run the tests**: `pytest tests/ -v`
4. **Experiment**: Modify the scoring weights and see how it changes results
5. **Contribute**: Find an issue and submit your first pull request!

---

## Summary

You've learned:

- ✅ What Scanlytic-ForensicAI does and why it exists
- ✅ How the file analysis process works
- ✅ The project structure and organization
- ✅ Core concepts (classification, entropy, hashing, strings)
- ✅ How components work together
- ✅ How to install and use the tool
- ✅ How to understand the results
- ✅ How to contribute to the project

**Remember**: Digital forensics is a complex field, but everyone starts as a beginner. Don't be afraid to ask questions, experiment, and learn!

---

## Get Help

- **Questions?** Open a discussion on GitHub
- **Bugs?** Open an issue on GitHub
- **Want to chat?** Contact the maintainer

Happy analyzing! 🔍🔬
