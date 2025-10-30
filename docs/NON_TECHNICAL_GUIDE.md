# Non-Technical User Guide

## Welcome! 👋

This guide is for **non-technical users** who need to use Scanlytic-ForensicAI but don't have a programming or technical background. We'll explain everything in plain English, using everyday analogies.

---

## What Does This Tool Do?

**In Simple Terms:**

Imagine you have a huge box of mixed items (files on a computer), and you need to find which ones might be dangerous or important. Going through each item by hand would take forever.

Scanlytic-ForensicAI is like a smart sorting machine that:
1. Looks at each item (file)
2. Identifies what it is
3. Checks for warning signs
4. Gives it a danger rating
5. Makes a list organized by danger level

**Real-World Analogy:**

Think of it like airport security scanning luggage:
- X-ray machine (Scanlytic) scans each bag (file)
- Identifies contents (file type identification)
- Flags suspicious items (malicious scoring)
- Security (you) focuses on flagged bags (high-risk files)

---

## Who Should Use This Tool?

This tool is designed for:

- **Corporate Security Teams** investigating incidents
- **IT Administrators** checking suspicious files
- **Legal Professionals** handling digital evidence
- **Law Enforcement** conducting digital investigations
- **Researchers** analyzing file collections
- **Anyone** who needs to quickly sort through many files

---

## How to Use Scanlytic-ForensicAI

### Option 1: Using Docker (Recommended for Non-Technical Users)

Docker is like a pre-packaged box that contains everything needed to run the software. You don't need to install Python or any dependencies.

#### Step 1: Install Docker

**Windows:**
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the on-screen instructions
4. Restart your computer if prompted

**Mac:**
1. Download Docker Desktop for Mac from [docker.com](https://www.docker.com/products/docker-desktop)
2. Open the downloaded file
3. Drag Docker to your Applications folder
4. Open Docker from Applications

**Verification:**
- Open Terminal (Mac) or Command Prompt (Windows)
- Type: `docker --version`
- You should see something like: `Docker version 20.10.x`

#### Step 2: Get Scanlytic-ForensicAI

**Option A: Download**
1. Go to [github.com/rohteemie/Scanlytic-ForensicAI](https://github.com/rohteemie/Scanlytic-ForensicAI)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to a folder (e.g., Desktop)

**Option B: Using Git** (if you have it installed)
1. Open Terminal/Command Prompt
2. Type: `git clone https://github.com/rohteemie/Scanlytic-ForensicAI.git`
3. Press Enter

#### Step 3: Build the Docker Image

1. Open Terminal/Command Prompt
2. Navigate to the Scanlytic folder:
   ```
   cd path/to/Scanlytic-ForensicAI
   ```
   (Replace `path/to/` with the actual location)

3. Build the image:
   ```
   docker build -t scanlytic .
   ```
   This takes a few minutes the first time.

#### Step 4: Analyze Files

**Analyze a Single File:**
```
docker run -v /path/to/files:/data scanlytic analyze /data/filename
```

**Example:**
```
docker run -v C:\Users\John\Documents:/data scanlytic analyze /data/suspicious.exe
```

**Analyze a Folder:**
```
docker run -v /path/to/folder:/data scanlytic analyze /data --recursive
```

**Save Results to a Report:**
```
docker run -v /path/to/files:/data -v /path/to/reports:/reports scanlytic analyze /data -o /reports/report.json
```

### Option 2: Using Python Directly

If you're comfortable with basic command-line usage:

#### Step 1: Install Python

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. Run installer
4. ✅ **Important:** Check "Add Python to PATH"
5. Click "Install Now"

**Mac:**
Python is usually pre-installed. To check:
1. Open Terminal
2. Type: `python3 --version`
3. If version is below 3.8, install from [python.org](https://www.python.org/downloads/)

#### Step 2: Install Scanlytic

1. Download Scanlytic-ForensicAI (see Option 1, Step 2 above)
2. Open Terminal/Command Prompt
3. Navigate to folder:
   ```
   cd path/to/Scanlytic-ForensicAI
   ```
4. Install:
   ```
   pip install -e .
   ```

#### Step 3: Verify Installation

Type:
```
scanlytic --version
```

You should see:
```
scanlytic 0.1.0
```

#### Step 4: Analyze Files

**Single File:**
```
scanlytic analyze /path/to/file.exe
```

**Folder:**
```
scanlytic analyze /path/to/folder --recursive
```

**With Report:**
```
scanlytic analyze /path/to/file.exe -o report.json
```

---

## Understanding the Results

### On-Screen Output

After analyzing a file, you'll see something like this:

```
=== Analysis Results ===

File: document.pdf
Category: PDF Document
Malicious Score: 25.0
Risk Level: medium

Summary:
- Standard PDF file
- Normal file size
- Created: 2024-10-15
- No suspicious patterns detected
- Overall: Medium caution advised
```

#### What Each Part Means

**File Name:**
- The name of the file you analyzed

**Category:**
- What type of file it is
- Examples: "Windows Executable", "PDF Document", "Image File"

**Malicious Score:**
- A number from 0 to 100
- **0-25**: Probably safe (green light)
- **25-50**: Be careful (yellow light)
- **50-75**: Likely dangerous (orange light)
- **75-100**: Very dangerous (red light)

**Risk Level:**
- Simple word: low, medium, high, or critical
- Based on the score

**Summary:**
- Plain-English explanation
- Lists specific concerns
- Gives overall recommendation

### Report Files

When you save a report, you get a file with detailed information:

#### JSON Reports (for computers)

**File:** `report.json`

**What is it?**
- Structured data file
- Can be imported into other tools
- Used for automated processing

**Example:**
```json
{
  "file_name": "suspicious.exe",
  "malicious_score": 75.0,
  "risk_level": "critical",
  "recommendation": "Investigate immediately"
}
```

**When to use:**
- You need to import into another security tool
- You're doing automated processing
- You want complete technical details

#### CSV Reports (for spreadsheets)

**File:** `report.csv`

**What is it?**
- Spreadsheet-compatible file
- Opens in Excel, Google Sheets, etc.
- Good for analyzing many files at once

**Example:**

| File Name | Category | Score | Risk Level | Recommendation |
|-----------|----------|-------|------------|----------------|
| file1.exe | Executable | 85.0 | critical | Quarantine immediately |
| file2.pdf | Document | 15.0 | low | Safe to open |
| file3.zip | Archive | 55.0 | high | Investigate contents |

**When to use:**
- You analyzed many files
- You want to sort/filter results
- You need to share with non-technical people
- You want to create charts/graphs

---

## Common Use Cases

### Use Case 1: Checking Downloaded Files

**Scenario:** You downloaded files from the internet and want to check if they're safe.

**Steps:**
1. Put all downloaded files in one folder (e.g., `Downloads/Check`)
2. Run analysis:
   ```
   scanlytic analyze Downloads/Check -o safety-check.csv
   ```
3. Open `safety-check.csv` in Excel
4. Sort by "Score" (highest to lowest)
5. Files with score >50: Don't open, delete or submit to IT
6. Files with score 25-50: Be cautious, scan with antivirus
7. Files with score <25: Probably safe

### Use Case 2: Investigating a Security Incident

**Scenario:** An employee's computer was compromised. You need to find suspicious files.

**Steps:**
1. Copy suspicious files to investigation folder
2. Run analysis:
   ```
   scanlytic analyze incident-files/ --recursive -o incident-report.json
   ```
3. Review files with "critical" or "high" risk first
4. Document findings for security team
5. Submit high-risk files for detailed analysis

### Use Case 3: Regular Security Checks

**Scenario:** Monthly security audit of file server.

**Steps:**
1. Set up scheduled task (Windows) or cron job (Mac/Linux)
2. Weekly scan:
   ```
   scanlytic analyze /file-server/ -o weekly-audit-$(date).csv
   ```
3. Review reports for new high-risk files
4. Compare with previous weeks to spot changes

### Use Case 4: Legal/Forensic Investigation

**Scenario:** Analyzing evidence for legal case.

**Steps:**
1. Create working copy of evidence (never modify originals!)
2. Run comprehensive analysis:
   ```
   scanlytic analyze evidence-copy/ --recursive -o evidence-analysis.json
   ```
3. Generate CSV for easy review:
   ```
   scanlytic analyze evidence-copy/ --recursive -o evidence-summary.csv
   ```
4. Document all high-risk findings
5. Maintain chain of custody records
6. Have technical expert review critical items

---

## Best Practices

### DO ✅

1. **Work on Copies**
   - Always analyze copies of files, not originals
   - Preserves evidence integrity

2. **Review High-Risk Items First**
   - Sort by score, highest first
   - Focus limited time on most dangerous files

3. **Keep Reports**
   - Save all analysis reports
   - Document when you ran analysis
   - Note any actions taken

4. **Update Regularly**
   - Check for Scanlytic updates
   - New versions have better detection

5. **Use with Other Tools**
   - Scanlytic is one tool in your toolbox
   - Combine with antivirus, sandboxing, etc.

### DON'T ❌

1. **Don't Execute Files**
   - NEVER run suspicious files
   - Analysis is safe, execution is not

2. **Don't Trust Score Alone**
   - Low score doesn't guarantee safety
   - Use human judgment

3. **Don't Modify Evidence**
   - Work on copies only
   - Preserve original timestamps and metadata

4. **Don't Ignore Context**
   - A file that's risky in one context may be safe in another
   - Example: Security tools may look suspicious

5. **Don't Skip Documentation**
   - Document what you analyzed
   - Keep records of findings
   - Important for legal cases

---

## Troubleshooting

### Problem: "Command not found" Error

**On Windows:**
```
'scanlytic' is not recognized as an internal or external command
```

**Solutions:**
1. Make sure you installed correctly: `pip install -e .`
2. Try: `python -m scanlytic` instead of `scanlytic`
3. Check Python is in PATH (reinstall Python with PATH option)

**On Mac/Linux:**
```
bash: scanlytic: command not found
```

**Solutions:**
1. Try: `python3 -m scanlytic`
2. Check installation: `pip3 install -e .`
3. Add to PATH: `export PATH=$PATH:~/.local/bin`

### Problem: "Permission Denied" Error

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
1. Make sure you have read access to the files
2. On Mac/Linux, use `sudo` if analyzing system files: `sudo scanlytic analyze ...`
3. On Windows, run Command Prompt as Administrator

### Problem: Analysis is Very Slow

**Causes & Solutions:**

1. **Analyzing Large Files**
   - Large files (>100MB) take longer
   - Consider setting max file size limit

2. **Too Many Files**
   - Analyzing thousands of files takes time
   - Let it run, or split into batches

3. **Slow Computer**
   - Close other programs
   - Run during off-peak hours

### Problem: Unexpected Results

**File Flagged as High-Risk but Seems Safe:**

**Possible Reasons:**
1. File is compressed/encrypted (high entropy)
2. File is a security tool (contains suspicious strings)
3. False positive

**What to Do:**
1. Check file with antivirus
2. Research the file online
3. Consult with IT/security expert
4. Report false positives on GitHub

**Safe File Flagged as Low-Risk:**

**Possible Reasons:**
1. Sophisticated malware (designed to evade detection)
2. New/unknown malware type
3. Legitimate file

**What to Do:**
1. Don't rely solely on Scanlytic
2. Use multiple analysis tools
3. When in doubt, treat as suspicious

---

## Security and Privacy

### What Scanlytic Does

✅ **Analyzes files locally** - Everything stays on your computer
✅ **Reads files only** - Never modifies or executes files
✅ **No internet required** - Works completely offline
✅ **No data collection** - Your files and data stay private
✅ **Open source** - Code is public and auditable

### What Scanlytic Does NOT Do

❌ **Does not send files anywhere** - No cloud uploads
❌ **Does not execute files** - Safe to analyze malware
❌ **Does not collect personal information** - Privacy-first design
❌ **Does not require registration** - Free and anonymous
❌ **Does not modify files** - Read-only analysis

### Privacy Considerations

**File Paths in Reports:**
- Reports include full file paths
- Be careful when sharing reports (may reveal sensitive folder names)
- Edit reports before sharing if privacy is a concern

**File Metadata:**
- Reports include file creation dates, sizes, etc.
- This is standard forensic information
- Don't share reports if this information is sensitive

---

## Getting Help

### When You're Stuck

1. **Check This Guide First**
   - Read the troubleshooting section
   - Review examples for your use case

2. **Check Documentation**
   - See `docs/BEGINNERS_GUIDE.md` for technical details
   - Read `README.md` for overview

3. **Search Existing Issues**
   - Go to GitHub: [github.com/rohteemie/Scanlytic-ForensicAI/issues](https://github.com/rohteemie/Scanlytic-ForensicAI/issues)
   - Search for your problem
   - Read solutions from others

4. **Ask for Help**
   - Open a new issue on GitHub
   - Describe your problem clearly
   - Include:
     - What you tried to do
     - What happened instead
     - Error messages (if any)
     - Your operating system

### Community Resources

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Documentation**: Comprehensive guides and references

---

## Frequently Asked Questions

### Q: Is this tool a replacement for antivirus software?

**A:** No. Scanlytic is a **triage** tool that helps you identify which files need closer inspection. It should be used **alongside** antivirus, not instead of it.

Think of it this way:
- **Antivirus**: Checks files against known malware signatures
- **Scanlytic**: Analyzes file characteristics and behavior patterns
- **Together**: Much more effective than either alone

### Q: Can Scanlytic detect all malware?

**A:** No tool can detect 100% of malware. Scanlytic is very good at:
- Identifying suspicious characteristics
- Flagging potentially dangerous files
- Prioritizing which files need manual review

But it may miss:
- Brand new, never-seen-before malware
- Extremely sophisticated attacks
- Files specifically designed to evade detection

### Q: Will analyzing malware infect my computer?

**A:** No. Scanlytic only **reads** files, it never **executes** them. Reading a file is safe, even if it's malicious.

However, good practices:
- Use a dedicated analysis computer
- Work in a virtual machine if possible
- Never double-click files you're analyzing

### Q: How accurate is the malicious score?

**A:** Current accuracy (rule-based scoring): ~70-80%

This means:
- 7-8 out of 10 high-risk files are actually malicious
- 2-3 out of 10 are false positives (safe files flagged as risky)

Future versions with machine learning will improve this to 90%+.

### Q: Can I use this for legal evidence?

**A:** Scanlytic can be part of a forensic investigation, but:

✅ **Good for:**
- Initial triage and prioritization
- Identifying files for deeper analysis
- Documenting file characteristics

❌ **Not sufficient alone for:**
- Legal proof of maliciousness
- Court admissible evidence (without expert testimony)
- Definitive malware identification

**Best practice:** Use Scanlytic to identify candidates, then have certified forensic experts conduct detailed analysis.

### Q: Is it free?

**A:** Yes! Scanlytic is completely free and open source (MIT License).

You can:
- Use it for any purpose (personal, commercial)
- Modify it
- Distribute it

The only requirement is to keep the license notice.

### Q: What if I find a bug?

**A:** Please report it! We can't fix bugs we don't know about.

To report:
1. Go to [GitHub Issues](https://github.com/rohteemie/Scanlytic-ForensicAI/issues)
2. Click "New Issue"
3. Describe:
   - What you were doing
   - What went wrong
   - Any error messages
4. Submit

---

## Glossary (Common Terms Explained)

**Analysis**
- The process of examining a file

**Archive**
- A file that contains other files (like ZIP or RAR)

**Binary File**
- A file in computer language (not human-readable text)

**Classification**
- Identifying what type of file something is

**CLI (Command-Line Interface)**
- Text-based way to interact with software

**CSV (Comma-Separated Values)**
- Spreadsheet file format

**Docker**
- Software that packages applications in containers

**Entropy**
- Measure of randomness in a file

**Executable**
- A program that can run on your computer (.exe on Windows)

**Feature Extraction**
- Collecting information about a file

**Forensics**
- Scientific investigation of digital evidence

**Hash**
- Unique "fingerprint" of a file

**JSON (JavaScript Object Notation)**
- Structured data format for computers

**Malware**
- Malicious software (viruses, trojans, etc.)

**Metadata**
- Information about a file (size, date, etc.)

**Risk Level**
- How dangerous a file appears to be

**Score**
- Numerical rating of suspiciousness (0-100)

**Triage**
- Quick initial sorting to prioritize work

---

## Quick Reference Card

**Common Commands:**

| Task | Command |
|------|---------|
| Check version | `scanlytic --version` |
| Get help | `scanlytic --help` |
| Analyze one file | `scanlytic analyze filename` |
| Analyze folder | `scanlytic analyze foldername` |
| Include subfolders | `scanlytic analyze folder -r` |
| Save JSON report | `scanlytic analyze file -o report.json` |
| Save CSV report | `scanlytic analyze file -o report.csv -f csv` |
| Adjust sensitivity | `scanlytic analyze file --threshold 60` |

**Risk Levels:**

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| 0-25 | Low | Probably safe | Normal caution |
| 25-50 | Medium | Some concerns | Extra caution |
| 50-75 | High | Likely risky | Investigate |
| 75-100 | Critical | Very dangerous | Immediate action |

---

## Conclusion

Scanlytic-ForensicAI is a powerful tool for quickly sorting through files and identifying potential threats. While it's designed to be user-friendly, remember:

- It's a **tool**, not a complete solution
- Use it as part of a broader security strategy
- When in doubt, consult experts
- Keep learning and improving your security practices

Stay safe! 🔒

---

**Need More Help?**
- 📚 Read the [Beginner's Guide](BEGINNERS_GUIDE.md) for technical details
- 🐛 Report issues on [GitHub](https://github.com/rohteemie/Scanlytic-ForensicAI/issues)
- 💬 Ask questions in [Discussions](https://github.com/rohteemie/Scanlytic-ForensicAI/discussions)
