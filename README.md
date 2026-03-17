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

## Batch Download (Any Module)

The connector includes a **generic batch downloader** that works with any Moodle module. No hardcoding needed!

### Setup

1. **Copy the example config:**
```bash
cp downloads.example.json downloads.json
```

2. **Edit `downloads.json`** to add your modules and file URLs:
```json
{
  "downloads": [
    {
      "module": "Your Course Name",
      "course_id": 12345,
      "files": [
        {
          "name": "Lecture1.pdf",
          "url": "https://mytimes.taylors.edu.my/webservice/pluginfile.php/..."
        },
        {
          "name": "Lecture2.pdf",
          "url": "https://mytimes.taylors.edu.my/webservice/pluginfile.php/..."
        }
      ]
    }
  ]
}
```

3. **Run the downloader:**
```bash
# Uses downloads.json by default
python batch_downloader.py

# Or specify custom config/output
python batch_downloader.py --config my_courses.json --output /path/to/downloads
```

### File Structure Created
```
downloads/
├── Your_Course_Name/
│   ├── Lecture1.pdf
│   └── Lecture2.pdf
├── Another_Course/
│   ├── Chapter1.pdf
│   └── Chapter2.pdf
```

**No modification needed!** Just edit the JSON, run the script, and files are organized by module.

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
├── batch_downloader.py              # Generic batch downloader
├── downloads.example.json           # Example download config
├── downloads.json                   # Your config (gitignored, copy from example)
├── config.json                      # Your Moodle config (gitignored)
├── config.template.json             # Template Moodle config
├── requirements.txt                 # Python dependencies
├── cache/                           # API cache + files (auto-created)
├── downloads/                       # Downloaded materials (auto-created)
│   ├── Module_Name_1/
│   ├── Module_Name_2/
│   └── ...
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

March 17, 2026 — Generic batch downloader + JSON config for plug-and-play usage
