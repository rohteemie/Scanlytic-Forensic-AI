# Quick Start Guide for Contributors

This guide helps new contributors get started quickly with the Scanlytic-ForensicAI project.

## 🚀 For Developers

### 1. Initial Setup (5 minutes)

We recommend using the repository-local virtual environment named `.venv` so it's obvious to scripts and CI what environment to use.

Quick one-line setup (recommended):

```bash
# Clone the repository
git clone https://github.com/rohteemie/Scanlytic-Forensic-AI.git
cd Scanlytic-Forensic-AI

# Run the helper script which creates and populates `.venv`
./scripts/setup-dev.sh

# Activate the environment (Linux/macOS)
source .venv/bin/activate

# Verify python/pip
python -V && which python && pip -V
```

If you prefer manual steps use these commands:

```bash
# Create virtual environment in the repo (named .venv)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Upgrade pip and install dependencies
pip install -U pip
pip install -r requirements.txt
pip install -r requirements-dev.txt || true  # requirements-dev is optional
```

### 2. Understanding the Project

- **Read**: [README.md](../README.md) for project overview
- **Check**: [ROADMAP.md](../ROADMAP.md) for development timeline

### 3. Development Workflow

```bash
# Create a feature branch
git checkout -b feature/issue-number-description

# Make your changes
# ...write code...

# Run tests (when available)
pytest tests/

# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/

# Commit changes
git add .
git commit -m "feat(module): brief description

Detailed description of changes.

Closes #issue-number"

# Push and create PR
git push origin feature/issue-number-description
```

### 4. Code Quality Checklist

Before submitting a PR:

- [ ] Code follows PEP 8 style guide
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow conventions
- [ ] No merge conflicts

## 📊 For Project Managers

### Setting Up GitHub Issues

Use the [ISSUES_BREAKDOWN.md](../ISSUES_BREAKDOWN.md) to create issues:

```markdown
Title: [From breakdown]
Labels: priority/P0, type/feature, effort/M
Milestone: Phase 1: Foundation & Infrastructure

[Copy description from breakdown]

**Tasks:**
[Copy task checklist]

**Acceptance Criteria:**
[Copy acceptance criteria]

**Dependencies:** #1, #2
```

## 📞 Getting Help

- **Questions**: Open a [GitHub Discussion](https://github.com/rohteemie/Scanlytic-Forensic-AI/discussions) (if enabled) or create an issue with the `question` label
- **Bugs**: Create an issue with the `type/bug` label
- **Features**: Create an issue with the `type/feature` label-
- **Chat**: Discord/Slack to be added in the future

## 🎓 Learning Resources

### Digital Forensics

- [SANS Digital Forensics Blog](https://www.sans.org/blog/)
- [ForensicFocus](https://www.forensicfocus.com/)

### Machine Learning

- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Machine Learning Mastery](https://machinelearningmastery.com/)

### Python Best Practices

- [Real Python](https://realpython.com/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

Thank you for contributing to Scanlytic-ForensicAI! 🚀
