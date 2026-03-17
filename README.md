# Moodle Connector for Taylor's University (mytimes.taylors.edu.my)

A robust Python connector for the Taylor's University Moodle LMS with:
- Microsoft MFA/OAuth2 authentication
- Encrypted credential storage
- Full Moodle REST API coverage
- Markdown output for AI agents
- Aggressive caching for token efficiency
- CLI and batch download modes

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
# For browser-based MFA (recommended):
playwright install chromium
```

### 2. Create your config

```bash
cp config.template.json config.json
# Edit config.json if needed (mostly auto-configured)
```

### 3. Run connector

```bash
# Get courses
python moodle_connector.py courses

# Get grades
python moodle_connector.py grades

# List assignments with deadlines
python moodle_connector.py assignments

# Get course materials
python moodle_connector.py materials --course-id 44864

# Download a file
python moodle_connector.py download "https://mytimes.taylors.edu.my/..." --output myfile.pdf

# Full summary (all data)
python moodle_connector.py summary
```

---

## Batch Download Materials

### Using the batch downloader

```bash
python batch_downloader_connector.py
```

This downloads **21 key files** (133 MB) from your courses:

**File Structure Created:**

```
downloads_via_connector/
├── Machine_Learning/
│   ├── Week1_Python_Basics.zip              (66 MB)
│   ├── Week2_ML_Intro.zip                   (1 MB)
│   ├── Week3_Preprocessing_Regression.zip   (1.2 MB)
│   ├── Week4_Classification.zip             (1.2 MB)
│   ├── Week5_Advanced_Classification.zip    (0.9 MB)
│   ├── Week6_SVM_Probability.zip            (0.6 MB)
│   └── Week7_Applications_Ethics.zip        (2 MB)
│
└── Big_Data/
    ├── Chapter1_BigData_Introduction.pdf     (4.4 MB)
    ├── Chapter2_Hadoop_HBase.pdf             (3.8 MB)
    ├── Chapter3_MapReduce.pdf                (3 MB)
    ├── Chapter4_Part1_BigData_Tech.pdf       (3.3 MB)
    ├── Chapter4_Part2_BigData_Tech.pdf       (3.8 MB)
    ├── Chapter5_ML_BigData_Integration.pdf   (3 MB)
    ├── Chapter6_BigData_Analytics.pdf        (2.6 MB)
    ├── Practical3_HDFS_Operations.pdf        (4 MB)
    ├── Practical5_MapReduce.pdf              (0.4 MB)
    ├── Practical6_HIVE_PIG.pdf               (0.4 MB)
    ├── Practical7_Apache_Impala.pdf          (0.7 MB)
    ├── Practical8_Apache_Spark.pdf           (0.5 MB)
    ├── EXAM_Revision_Summary.pdf             (4.6 MB)
    └── EXAM_Sample_Questions.pdf             (0.5 MB)
```

**All files are downloaded to:** `./downloads_via_connector/`

---

## Authentication

### Automatic (Recommended)
1. Run any command — connector will open a browser
2. Sign in with your Microsoft account (MFA will trigger if enabled)
3. Token is captured automatically and saved encrypted

### Manual Token Retrieval (Fallback)
If browser auth fails:
1. Log in to https://mytimes.taylors.edu.my
2. Go to: **User menu → Preferences → Security keys**
   - OR navigate to: `/user/managetoken.php`
3. Find the **"Moodle mobile web service"** token
4. Copy the token value (32 hex characters)
5. Run: `python moodle_connector.py login`
6. Paste token when prompted

---

## Configuration

Edit `config.json` for:
- **Moodle URL:** `moodle.base_url` (default: `https://mytimes.taylors.edu.my`)
- **Token:** `moodle.web_service_token` (auto-filled or paste manually)
- **Cache TTL:** `cache.api_ttl_seconds` (default: 300 = 5 min)
- **Output format:** `output.format` (markdown is default)

Example:
```json
{
  "moodle": {
    "base_url": "https://mytimes.taylors.edu.my",
    "web_service_token": "YOUR_TOKEN_HERE"
  },
  "cache": {
    "api_ttl_seconds": 300
  }
}
```

---

## Features

### Supported Commands

| Command | Output | Use Case |
|---------|--------|----------|
| `courses` | All enrolled courses + progress | Course overview |
| `grades` | Grade summary or per-course details | Check grades |
| `assignments` | All assignments with deadlines | Track work due |
| `materials` | Course materials, links, files | Access course content |
| `deadlines` | Calendar events (assignments, exams) | Stay on schedule |
| `announcements` | Course announcements | Latest news |
| `download <url>` | Downloaded file (cached) | Get resources |
| `summary` | Full markdown dump | AI consumption |

### Caching

- **API responses:** 5 minutes (configurable)
- **Files:** Cached indefinitely (redownloading returns cached copy)
- **Cache location:** `./cache/`

Clear cache:
```bash
rm -r cache/
```

---

## Python API

Use the connector in your own code:

```python
from moodle_connector import MoodleConnector
from pathlib import Path

# Initialize
connector = MoodleConnector(
    config_path=Path('config.json'),
    password='your-encryption-password'
)

# Get data
print(connector.courses())
print(connector.grades())
print(connector.assignments())
print(connector.materials(course_id=44864))

# Download a file
connector.download("https://mytimes.taylors.edu.my/...", "output.pdf")
```

---

## Troubleshooting

### "Invalid parameter value detected" for calendar API
- Known Moodle API limitation (some endpoints return this)
- **Workaround:** Use `assignments()` to get deadlines instead

### "Token expired" error
- Re-run: `python moodle_connector.py login`
- Or paste a fresh token into `config.json`

### File downloads stuck
- Check network connection
- Increase timeout in code: `download_file(..., timeout=120)`
- Files already downloaded are cached — rerun will skip

### Encryption password issues
- Password is used to encrypt stored credentials
- Set `MOODLE_CRED_PASSWORD` environment variable to auto-provide password

---

## Security Notes

- **Tokens never stored in git** (in `.gitignore`)
- **Credentials encrypted** with PBKDF2 + Fernet (480K iterations)
- **Never commit `config.json`** with real tokens
- **Use template:** Copy `config.template.json` for new setups

---

## Development

### Project Structure

```
moodle_connector/
├── moodle_connector.py              # Main connector class
├── batch_downloader_connector.py    # Batch file downloader
├── config.json                      # Your config (gitignored)
├── config.template.json             # Template config
├── requirements.txt                 # Python dependencies
├── cache/                           # API cache + files (auto-created)
├── downloads_via_connector/         # Downloaded materials (auto-created)
│   ├── Machine_Learning/
│   └── Big_Data/
└── README.md                        # This file
```

### Requirements

- Python 3.10+
- `requests` — HTTP library
- `cryptography` — Credential encryption
- `playwright` — Browser automation (optional, for MFA)

Install:
```bash
pip install -r requirements.txt
```

---

## License

Private use. Not for distribution.

---

## Author

Jabir (Jsi0503@taylors.edu.my)  
Taylor's University, Kuala Lumpur, Malaysia

---

## Last Updated

March 17, 2026 — Grades API fix + batch downloader with organized file structure
