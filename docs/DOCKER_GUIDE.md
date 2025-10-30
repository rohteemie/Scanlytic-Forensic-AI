# Docker Usage Guide for Scanlytic-ForensicAI

## Table of Contents

1. [Introduction](#introduction)
2. [Why Use Docker?](#why-use-docker)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Building the Image](#building-the-image)
6. [Running Analyses](#running-analyses)
7. [Advanced Usage](#advanced-usage)
8. [Docker Compose](#docker-compose)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Introduction

This guide explains how to use Scanlytic-ForensicAI with Docker, which provides:

- **Easy setup**: No need to install Python or dependencies
- **Consistency**: Works the same on any platform
- **Isolation**: Doesn't affect your system
- **Portability**: Easy to share and deploy

---

## Why Use Docker?

### Traditional Installation Challenges

When installing Python applications, you might face:

- Version conflicts with other Python programs
- Missing system dependencies
- Platform-specific issues
- Complex setup procedures

### Docker Solution

Docker packages everything needed into a "container":

- ✅ Python runtime
- ✅ All dependencies
- ✅ System libraries
- ✅ Application code

**One command** gets you running, regardless of your operating system.

---

## Prerequisites

### Install Docker

**Windows:**

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the setup wizard
4. Restart your computer
5. Launch Docker Desktop

**macOS:**

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Open the downloaded `.dmg` file
3. Drag Docker to Applications
4. Launch Docker from Applications
5. Grant necessary permissions

**Linux:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional, avoids using sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

### Verify Installation

```bash
docker --version
# Output: Docker version 20.10.x or higher

docker run hello-world
# Should download and run a test container
```

---

## Quick Start

### 5-Minute Setup

1. **Get the code:**

   ```bash
   git clone https://github.com/rohteemie/Scanlytic-Forensic-AI.git
   cd Scanlytic-Forensic-AI
   ```

2. **Build the image:**

   ```bash
   docker build -t scanlytic .
   ```

   *This takes 2-3 minutes the first time*

3. **Test it:**

   ```bash
   docker run scanlytic --version
   ```

   *Should display: scanlytic 0.1.0*

4. **Analyze a file:**

   ```bash
   # Create a test file
   echo "print('Hello')" > test.py

   # Analyze it
   docker run -v $(pwd):/data scanlytic analyze /data/test.py
   ```

✅ **Done!** You're ready to analyze files.

---

## Building the Image

### Basic Build

```bash
docker build -t scanlytic-forensicai .
```

**What this does:**

- `-t scanlytic-forensicai`: Tags the image with a name
- `.`: Uses Dockerfile in current directory

### Build with Custom Tag

```bash
docker build -t scanlytic:v0.1.0 .
```

### Build with No Cache

If you made changes and want a clean build:

```bash
docker build --no-cache -t scanlytic-forensicai .
```

### View Built Images

```bash
docker images | grep scanlytic
```

**Output:**

```bash
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
scanlytic-forensicai latest    abc123def456   5 minutes ago   450MB
```

---

## Running Analyses

### Basic Usage Pattern

```bash
docker run -v /host/path:/container/path scanlytic-forensicai analyze /container/path
```

**Components:**

- `docker run`: Execute a container
- `-v /host/path:/container/path`: Mount a directory
- `scanlytic-forensicai`: Image name
- `analyze /container/path`: Command to run

### Example 1: Analyze a Single File

**Windows:**

```powershell
docker run -v C:\Users\John\Documents:/data scanlytic-forensicai analyze /data/file.exe
```

**macOS/Linux:**

```bash
docker run -v /Users/john/documents:/data scanlytic-forensicai analyze /data/file.exe
```

**Using Current Directory:**

```bash
# Linux/Mac
docker run -v $(pwd):/data scanlytic-forensicai analyze /data/file.exe

# Windows PowerShell
docker run -v ${PWD}:/data scanlytic-forensicai analyze /data/file.exe
```

### Example 2: Analyze a Directory

```bash
docker run -v /path/to/files:/data scanlytic-forensicai analyze /data
```

**Recursive (include subdirectories):**

```bash
docker run -v /path/to/files:/data scanlytic-forensicai analyze /data --recursive
```

### Example 3: Save Report to File

```bash
docker run \
  -v /path/to/files:/data \
  -v /path/to/reports:/reports \
  scanlytic-forensicai analyze /data -o /reports/report.json
```

**Breakdown:**

- First `-v`: Mount files to analyze
- Second `-v`: Mount directory for saving reports
- `-o /reports/report.json`: Save output to report file

### Example 4: Generate CSV Report

```bash
docker run \
  -v /path/to/files:/data \
  -v /path/to/reports:/reports \
  scanlytic-forensicai analyze /data -o /reports/report.csv -f csv
```

### Example 5: Custom Threshold

```bash
docker run -v /path/to/files:/data scanlytic-forensicai analyze /data --threshold 60
```

**Threshold values:**

- `30`: More sensitive (flags more files)
- `50`: Default balance
- `70`: Less sensitive (only flags very suspicious files)

---

## Advanced Usage

### Interactive Mode

Run container interactively to execute multiple commands:

```bash
docker run -it -v $(pwd):/data scanlytic-forensicai /bin/bash
```

**Now you're inside the container:**

```bash
# Run multiple analyses
scanlytic analyze /data/file1.exe
scanlytic analyze /data/file2.pdf
scanlytic analyze /data/directory --recursive

# Exit when done
exit
```

### Environment Variables

Set configuration through environment variables:

```bash
docker run \
  -e SCANLYTIC_LOGGING_LEVEL=DEBUG \
  -e SCANLYTIC_WORKERS=4 \
  -v $(pwd):/data \
  scanlytic-forensicai analyze /data
```

**Available variables:**

- `SCANLYTIC_LOGGING_LEVEL`: DEBUG, INFO, WARNING, ERROR
- `SCANLYTIC_WORKERS`: Number of parallel workers
- `SCANLYTIC_OUTPUT_FORMAT`: json, csv

### Custom Configuration File

```bash
docker run \
  -v $(pwd)/files:/data \
  -v $(pwd)/config:/config \
  scanlytic-forensicai analyze /data --config /config/custom.yaml
```

### Resource Limits

Limit CPU and memory usage:

```bash
docker run \
  --cpus="2.0" \
  --memory="2g" \
  -v $(pwd):/data \
  scanlytic-forensicai analyze /data
```

### Run in Background

For long-running analyses:

```bash
docker run -d \
  --name scanlytic-analysis \
  -v $(pwd):/data \
  -v $(pwd)/reports:/reports \
  scanlytic-forensicai analyze /data -o /reports/report.json
```

**Check status:**

```bash
docker ps -a | grep scanlytic-analysis
```

**View logs:**

```bash
docker logs scanlytic-analysis
```

**View live output:**

```bash
docker logs -f scanlytic-analysis
```

### Read-Only Mode (Security)

Mount files as read-only for extra security:

```bash
docker run -v /path/to/files:/data:ro scanlytic-forensicai analyze /data
```

The `:ro` flag ensures the container cannot modify your files.

---

## Docker Compose

### Using Docker Compose

Docker Compose simplifies running containers with configuration files.

### Basic Usage

**File: `docker-compose.yml`** (already provided)

**Start:**

```bash
docker-compose up
```

**Run analysis:**

```bash
docker-compose run scanlytic analyze /data
```

**Stop:**

```bash
docker-compose down
```

### Custom Compose Configuration

Create `docker-compose.override.yml` for local customization:

```yaml
version: '3.8'

services:
  scanlytic:
    volumes:
      # Your custom file locations
      - /my/files:/data:ro
      - /my/reports:/reports

    environment:
      # Your custom settings
      - SCANLYTIC_LOGGING_LEVEL=DEBUG
      - SCANLYTIC_WORKERS=8
```

**Use it:**

```bash
docker-compose up
```

*Automatically merges with docker-compose.yml*

### Development Mode

For developers working on the code:

```bash
docker-compose run scanlytic-dev
```

**Features:**

- Source code mounted (changes reflect immediately)
- Debug logging enabled
- Interactive terminal

---

## Troubleshooting

### Problem: "Cannot connect to Docker daemon"

**Error:**

```bash
Cannot connect to the Docker daemon. Is the docker daemon running?
```

**Solutions:**

**Windows/Mac:**

1. Open Docker Desktop
2. Wait for it to start (whale icon in system tray)
3. Try command again

**Linux:**

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Problem: Permission Denied

**Error:**

```bash
Permission denied while trying to connect to the Docker daemon socket
```

**Solutions:**

**Linux:**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or:
newgrp docker

# Try again
docker run scanlytic-forensicai --version
```

**Windows/Mac:**

- Run Docker Desktop as administrator
- Grant requested permissions in settings

### Problem: Volume Mount Not Working

**Error:**
Files not found or "no such file or directory"

**Solutions:**

1. **Check path format:**
   - Windows: Use forward slashes or escape backslashes

     ```bash
     # Good
     -v C:/Users/John:/data

     # Good
     -v C:\\Users\\John:/data

     # Bad
     -v C:\Users\John:/data
     ```

2. **Use absolute paths:**

   ```bash
   # Good
   -v /full/path/to/files:/data

   # Bad (may not work)
   -v ./files:/data
   ```

3. **Enable file sharing (Docker Desktop):**
   - Settings → Resources → File Sharing
   - Add your drive/folder
   - Apply & Restart

### Problem: Container Runs Out of Memory

**Error:**

```bash
Killed
```

or container stops unexpectedly

**Solution:**

Increase memory limit:

**Docker Desktop:**

1. Settings → Resources
2. Increase Memory slider to 4GB or more
3. Apply & Restart

**Command-line:**

```bash
docker run --memory="4g" -v $(pwd):/data scanlytic-forensicai analyze /data
```

### Problem: Slow Performance

**Causes & Solutions:**

1. **First run (image building):**
   - Normal, takes time to download and build
   - Subsequent runs are faster

2. **Large dataset:**
   - Analyzing many files takes time
   - Use `--threshold` to filter
   - Consider splitting into batches

3. **Resource limits too low:**
   - Increase CPU/memory allocation
   - Check Docker Desktop resource settings

### Problem: Image Build Fails

**Error:**

```bash
Error building image
```

**Solutions:**

```bash
1. **Check internet connection:**
   - Building requires downloading packages

2. **Clear Docker cache:**

   ```bash
   docker system prune -a
   docker build --no-cache -t scanlytic-forensicai .
   ```

3. **Check Dockerfile:**

   - Ensure it hasn't been modified
   - Re-download from GitHub if needed

---

## Best Practices

### Security

1. **Use read-only mounts for analysis:**

   ```bash
   -v /path/to/files:/data:ro
   ```

2. **Don't run as root (advanced):**

   ```bash
   docker run --user 1000:1000 -v $(pwd):/data scanlytic-forensicai analyze /data
   ```

3. **Use security options:**

   ```bash
   docker run --security-opt=no-new-privileges -v $(pwd):/data scanlytic-forensicai
   ```

### Performance

1. **Allocate adequate resources:**
   - At least 2GB RAM
   - 2 CPU cores for large datasets

2. **Use volumes efficiently:**
   - Only mount directories you need
   - Avoid mounting entire drives

3. **Clean up regularly:**

   ```bash
   # Remove stopped containers
   docker container prune

   # Remove unused images
   docker image prune

   # Remove everything unused
   docker system prune -a
   ```

### Organization

1. **Use descriptive tags:**

   ```bash
   docker build -t scanlytic:v0.1.0-$(date +%Y%m%d) .
   ```

2. **Organize reports:**

   ```bash
   mkdir -p reports/$(date +%Y-%m-%d)
   docker run \
     -v $(pwd):/data \
     -v $(pwd)/reports:/reports \
     scanlytic-forensicai analyze /data -o /reports/$(date +%Y-%m-%d)/report.json
   ```

3. **Version control configurations:**
   - Keep custom `docker-compose.override.yml` in version control
   - Document any custom settings

---

## Useful Commands Reference

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi scanlytic-forensicai

# Remove all unused images
docker image prune -a
```

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop container-name

# Remove container
docker rm container-name

# Remove all stopped containers
docker container prune
```

### Logs and Debugging

```bash
# View container logs
docker logs container-name

# Follow logs (live)
docker logs -f container-name

# Execute command in running container
docker exec -it container-name /bin/bash
```

### System Information

```bash
# Disk usage
docker system df

# Detailed info about images
docker inspect scanlytic-forensicai

# Container resource usage
docker stats
```

---

## Examples for Common Scenarios

### Scenario 1: Weekly Security Scan

**Script: `weekly-scan.sh`**

```bash
#!/bin/bash

DATE=$(date +%Y-%m-%d)
REPORT_DIR="reports/$DATE"

mkdir -p "$REPORT_DIR"

docker run \
  -v /server/files:/data:ro \
  -v $(pwd)/reports:/reports \
  scanlytic-forensicai analyze /data \
  --recursive \
  -o "/reports/$DATE/scan-report.json"

echo "Scan complete. Report saved to $REPORT_DIR"
```

**Use with cron:**

```bash
# Edit crontab
crontab -e

# Add line (runs every Monday at 2 AM)
0 2 * * 1 /path/to/weekly-scan.sh
```

### Scenario 2: Batch Processing Multiple Directories

**Script: `batch-analyze.sh`**

```bash
#!/bin/bash

DIRS=(
  "/path/to/dir1"
  "/path/to/dir2"
  "/path/to/dir3"
)

for DIR in "${DIRS[@]}"; do
  DIRNAME=$(basename "$DIR")
  echo "Analyzing $DIRNAME..."

  docker run \
    -v "$DIR:/data:ro" \
    -v $(pwd)/reports:/reports \
    scanlytic-forensicai analyze /data \
    -o "/reports/$DIRNAME-report.csv" \
    -f csv
done

echo "All analyses complete!"
```

### Scenario 3: CI/CD Integration

**GitHub Actions example:**

```yaml
name: Security Scan

on:
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build Scanlytic
        run: docker build -t scanlytic .

      - name: Scan files
        run: |
          docker run \
            -v ${{ github.workspace }}:/data:ro \
            scanlytic analyze /data \
            -o scan-report.json

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: security-scan
          path: scan-report.json
```

---

## Summary

Docker makes running Scanlytic-ForensicAI easy and consistent across all platforms. Key takeaways:

- ✅ **One-time setup**: Build the image once, use anywhere
- ✅ **No conflicts**: Isolated from your system
- ✅ **Portable**: Same commands on Windows, Mac, Linux
- ✅ **Secure**: Read-only mounts, resource limits
- ✅ **Reproducible**: Same results every time

**Next steps:**

1. Build the image
2. Try the quick start examples
3. Adapt to your use case
4. Automate with scripts or compose

For more information:

- [Docker Documentation](https://docs.docker.com/)
- [Scanlytic Documentation](../README.md)
- [GitHub Issues](https://github.com/rohteemie/Scanlytic-ForensicAI/issues)

Happy analyzing! 🐳🔍
