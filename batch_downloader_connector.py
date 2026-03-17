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

# Define files to download
downloads = [
    # ML Course materials
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1833173/mod_resource/content/5/First%20week.zip", ml_dir / "Week1_Python_Basics.zip"),
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1833168/mod_resource/content/3/Second%20Week.zip", ml_dir / "Week2_ML_Intro.zip"),
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1819731/mod_resource/content/6/Third%20Week.zip", ml_dir / "Week3_Preprocessing_Regression.zip"),
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1819761/mod_resource/content/3/Week%204.zip", ml_dir / "Week4_Classification.zip"),
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1819791/mod_resource/content/2/Week%205.zip", ml_dir / "Week5_Advanced_Classification.zip"),
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1820333/mod_resource/content/3/week%206%20..zip", ml_dir / "Week6_SVM_Probability.zip"),
    ("Machine Learning", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1820342/mod_resource/content/2/Week%207-1.zip", ml_dir / "Week7_Applications_Ethics.zip"),
    
    # Big Data Chapters
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1823290/mod_resource/content/5/bigDataIntroduction.pdf", bd_dir / "Chapter1_BigData_Introduction.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1835956/mod_resource/content/7/Chapter%202%20Hadoop%20Ecosystem%20and%20HBase.pdf", bd_dir / "Chapter2_Hadoop_HBase.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1838378/mod_resource/content/2/Chapter%203-Hadoop%20MapReduce.pdf", bd_dir / "Chapter3_MapReduce.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1839973/mod_resource/content/2/Chapter%204-Big%20Data%20Technologies%20%28Part%201%29.pdf", bd_dir / "Chapter4_Part1_BigData_Tech.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1840329/mod_resource/content/1/Chapter%204-%20Big%20Data%20Technologies%20%28Part%202%29.pdf", bd_dir / "Chapter4_Part2_BigData_Tech.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1841891/mod_resource/content/1/C5-MLBD.pdf", bd_dir / "Chapter5_ML_BigData_Integration.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1842395/mod_resource/content/1/%20Chapter%206%20Big%20Data%20Analytics.pdf", bd_dir / "Chapter6_BigData_Analytics.pdf"),
    
    # Big Data Practicals (Most Important)
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1816451/mod_resource/content/3/Prac3.pdf", bd_dir / "Practical3_HDFS_Operations.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1818939/mod_resource/content/6/MapReduce.pdf", bd_dir / "Practical5_MapReduce.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1838225/mod_resource/content/1/Practical6ApacheHIVE%20and%20PIG.pdf", bd_dir / "Practical6_HIVE_PIG.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1841662/mod_resource/content/2/Prac7.pdf", bd_dir / "Practical7_Apache_Impala.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1842092/mod_resource/content/1/Prac8.pdf", bd_dir / "Practical8_Apache_Spark.pdf"),
    
    # Exam Preparation (CRITICAL)
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1843716/mod_resource/content/2/BDT%20Summary.pdf", bd_dir / "EXAM_Revision_Summary.pdf"),
    ("Big Data", "https://mytimes.taylors.edu.my/webservice/pluginfile.php/1843755/mod_resource/content/5/samples.pdf", bd_dir / "EXAM_Sample_Questions.pdf"),
]

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
