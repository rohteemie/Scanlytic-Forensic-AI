"""Setup script for Scanlytic-Forensic-AI."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().splitlines()
    requirements = [r.strip() for r in requirements if r.strip()
                    and not r.startswith('#')]

setup(
    name="scanlytic-forensic-ai",
    version="0.1.0",
    author="Rotimi Owolabi",
    author_email="",
    description="Automated File Classification and Malicious Intent Scoring "
               "for Digital Forensic Triage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohteemie/Scanlytic-Forensic-AI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'scanlytic=scanlytic.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'scanlytic': ['config/*.yaml'],
    },
)
