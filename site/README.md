# GitHub Pages Site

This folder hosts the standalone GitHub Pages landing site for Scanlytic Forensic AI.

## Why separate

- Keeps marketing and docs content isolated from core package code.
- Avoids build-time coupling with the Python project.
- Makes it safe to deploy without touching runtime dependencies.

## How to publish

This project uses a GitHub Actions workflow that builds Sphinx docs and deploys the
/site folder as the GitHub Pages artifact.

1. In GitHub, open Settings -> Pages.
2. Set Source to "GitHub Actions".
3. Save. GitHub will publish the content under the Pages URL.

## Linking docs

The landing site links to docs/ and docs/api/ (relative to the Pages root). The
workflow builds Sphinx HTML and copies it to site/docs/api/ so those links stay in
sync while the hand-authored pages under site/docs/ are preserved.
