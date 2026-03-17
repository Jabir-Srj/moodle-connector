#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch downloader using MoodleConnector.download() method.
Uses the connector's built-in file download with caching.
"""

import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from moodle_connector import MoodleConnector
from pathlib import Path

# Initialize connector
connector = MoodleConnector(
    config_path=Path('config.json'),
    password='test-pass'
)

# Create download directories
download_base = Path(__file__).parent / "downloads_via_connector"
ml_dir = download_base / "Machine_Learning"
bd_dir = download_base / "Big_Data"
ml_dir.mkdir(parents=True, exist_ok=True)
bd_dir.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("BATCH DOWNLOADER — Using MoodleConnector.download() Method")
print("=" * 80)

# Download each file using connector.download()
downloaded = 0
failed = 0

for course, url, target in downloads:
    try:
        print(f"\n[{course}] Downloading: {target.name}...")
        # Use the connector's download() method
        result = connector.download(url, str(target))
        print(f"  {result.strip()}")
        downloaded += 1
    except Exception as e:
        print(f"  ERROR: {e}")
        failed += 1

print("\n" + "=" * 80)
print(f"DOWNLOAD COMPLETE: {downloaded} files downloaded, {failed} failed")
print(f"Files saved to: {download_base}")
print("=" * 80)
