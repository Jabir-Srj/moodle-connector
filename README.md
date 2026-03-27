---
name: moodle-connector
description: "Moodle REST API client, batch downloader, and MCP server for Claude Code integration"
metadata: { "author": "Jabir Iliyas Suraj-Deen, Sebastian Guevara M.", "license": "MIT", "homepage": "https://github.com/Jabir-Srj/moodle-connector", "repository": "https://github.com/Jabir-Srj/moodle-connector.git", "tags": ["moodle", "education", "lms", "api", "batch-download", "mcp", "claude-code"] }
---

> **English** | [Español](README.es.md)

# Moodle Connector

**Full-featured Moodle REST API client with batch downloading and MCP protocol support for Claude Code and OpenCode.**

## Features

**Complete Moodle API Access**
- List courses, check grades, track assignments
- Fetch materials, deadlines, announcements
- Download files with aggressive caching

**Microsoft SSO / MFA Support**
- Automated Mobile Launch Flow (same as the official Moodle app)
- Works with any SSO provider: Microsoft Azure AD, Google, SAML, etc.
- Browser opens for interactive login - closes automatically once token is captured

**Multiple Integration Modes**
- **CLI:** `python moodle_connector.py courses`
- **Python Library:** `from moodle_connector import MoodleConnector`
- **MCP Protocol:** Native integration with Claude Code, OpenCode, and OpenClaw

**Generic Batch Downloader**
- JSON-driven configuration (zero code modification)
- Works with any Moodle module
- Auto-organized by course name

**Security**
- Encrypted credentials (PBKDF2 + Fernet)
- Token management built-in
- No secrets in git history
- MIT licensed

## Installation

Once installed via `clawhub install moodle-connector`:

```bash
cd ./skills/moodle-connector
pip install -r requirements.txt
python -m playwright install chromium
```

## Quick Start

### 1. Configure

```bash
cp config.template.json config.json
# Edit config.json: set base_url to your Moodle instance
```

### 2. Login (SSO / MFA)

```bash
MOODLE_CRED_PASSWORD=any-password python moodle_connector.py login
```

A browser window will open. Complete your Microsoft (or other SSO) login and MFA normally - the window closes automatically once the token is captured. You should see:

```
# ✅ Authentication Successful
- User: Your Name
- Site: Your Moodle Site
- Moodle version: 4.x.x
```

> If your instance allows direct username/password login (no SSO), you can also run:
> `python moodle_connector.py login --username you@email.com --user-password yourpassword`

### 3. Use CLI

```bash
python moodle_connector.py courses        # List all courses
python moodle_connector.py grades         # Check grades
python moodle_connector.py assignments    # View assignments with deadlines
python moodle_connector.py announcements  # Course announcements
python moodle_connector.py materials --course-id 12345
python moodle_connector.py deadlines      # Upcoming calendar events
python moodle_connector.py download "https://your-moodle-site.example.com/..." --output myfile.pdf
python moodle_connector.py summary        # Full markdown export (all data)
```

### 4. Use Python Library

```python
from moodle_connector import MoodleConnector
from pathlib import Path

connector = MoodleConnector(
    config_path=Path('config.json'),
    password='encryption-password'
)

courses = connector.courses()
grades = connector.grades()
assignments = connector.assignments()
materials = connector.materials()
deadlines = connector.deadlines()
announcements = connector.announcements()
content = connector.summary()

# Download with caching
file_content = connector.download("https://...")
```

### 5. Batch Download (Any Module)

```bash
cp downloads.example.json downloads.json
# Edit downloads.json to add modules and file URLs
python batch_downloader.py
```

**Output Structure:**
```
downloads/
├── Your_Module_Name_1/
│   ├── file1.pdf
│   ├── file2.zip
│   └── ...
└── Your_Module_Name_2/
    ├── lecture.pdf
    └── ...
```

## Tampermonkey Token Helper

If the connector is running on a headless server (no display), get the token from a PC or Mac with a browser and copy it over. Install the included userscript on that machine:

1. Install [Tampermonkey](https://www.tampermonkey.net/) in your browser
2. Open Tampermonkey - Create new script - paste the contents of [`moodle_token_helper.user.js`](moodle_token_helper.user.js)
3. Navigate to your Moodle site while logged in
4. Click the **"Get Token"** button (bottom right corner)
5. Copy the token and paste it into `config.json` under `web_service_token`

The script uses `GM_xmlhttpRequest` to call the Mobile Launch endpoint with your active session cookies and intercepts the `moodlemobile://` redirect without leaving the page.

To support additional Moodle instances, add `@match` and `@connect` lines to the script header.

## How Authentication Works

This connector uses Moodle's **Mobile Launch Flow** - the same mechanism used by the official Moodle mobile app. It works with any SSO provider without needing API credentials or special server configuration.

**Flow:**
1. Browser navigates to `/admin/tool/mobile/launch.php`
2. If no session exists, Moodle redirects to the SSO provider (e.g. Microsoft)
3. User completes login + MFA interactively
4. SSO redirects back to Moodle, which issues a `moodlemobile://token=<base64>` redirect
5. The connector intercepts this redirect, decodes the token, and closes the browser

The token is cached in an encrypted file (`credentials.enc`) and reused until it expires.

## MCP Integration (Claude Code / OpenCode / OpenClaw)

**REQUIRED:** Set `MOODLE_CRED_PASSWORD` environment variable before starting Claude Code.

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "moodle-connector": {
      "command": "python",
      "args": ["./skills/moodle-connector/mcp_server.py"],
      "env": {
        "MOODLE_CRED_PASSWORD": "your-encryption-password"
      }
    }
  }
}
```

**Important:** Replace `your-encryption-password` with the actual password used when running `login`.

Restart Claude Code. All 8 Moodle functions are now available as native MCP tools:
- `courses()` - List enrolled courses
- `grades()` - Get grades
- `assignments()` - Get assignments
- `materials()` - Get course materials
- `deadlines()` - Get upcoming deadlines
- `announcements()` - Get course news
- `download(url, output?)` - Download files
- `summary()` - Get complete data export

## Configuration

### Moodle Token (`config.json`)
```json
{
  "moodle": {
    "base_url": "https://your-moodle-site.example.com",
    "web_service_token": ""
  },
  "cache": {
    "api_ttl_seconds": 300
  }
}
```

Leave `web_service_token` empty to use the automated SSO login flow. Set it manually if you already have a token.

### Batch Downloader (`downloads.json`)
```json
{
  "downloads": [
    {
      "module": "Machine Learning",
      "course_id": 44864,
      "files": [
        {
          "name": "Week1.zip",
          "url": "https://your-moodle-site.example.com/webservice/pluginfile.php/..."
        }
      ]
    }
  ]
}
```

## Requirements

- Python 3.10+
- requests ≥2.31.0
- cryptography ≥41.0.0
- playwright ≥1.40.0
- mcp ≥0.1.0 (for MCP server)

## Supported Moodle Instances

Tested with:
- Taylor's University (mytimes.taylors.edu.my)
- Universidad Técnica Federico Santa María (aula.usm.cl) - Microsoft Azure AD SSO
- Should work with any Moodle 3.x+ instance

## Security Notes

- **Environment-enforced:** `MOODLE_CRED_PASSWORD` is **required** - no hardcoded defaults
- **Error sanitization:** MCP server sanitizes errors, no internal details leaked to clients
- **Encrypted credentials:** PBKDF2 (480K iterations) + Fernet encryption
- **Safe for headless:** Use `MOODLE_CRED_PASSWORD` env var for automation
- **Git-safe:** Never commit `config.json` with real tokens
- **No telemetry:** No external data transmission or logging

## Troubleshooting

### Browser opens but never closes
The token redirect was not captured. Check if your University allows the usage of Moodle App.

### "Invalid parameter value detected" for calendar API
Use `assignments()` instead - gets same deadline info.

### Token expired / login required again
Delete `credentials.enc` and run `python moodle_connector.py login` again.

### File download stuck
Check network. Increase timeout in code or clear cache: `rm -rf cache/`

## License

MIT - See LICENSE file for details. You are free to use, modify, and distribute this software.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Agree to license your work under GPLv3

## Authors

**Jabir Iliyas Suraj-Deen** - original author
- GitHub: https://github.com/Jabir-Srj
- Email: jabirsrj8@protonmail.com
- Taylor's University, Kuala Lumpur, Malaysia

**Sebastian Guevara M.** - SSO Mobile Launch Flow, multi-instance support
- GitHub: https://github.com/SebaG20xx
- Email: contacto@sebag20xx.cl
- Universidad Técnica Federico Santa María, Viña del Mar, Chile

---

**GitHub:** https://github.com/Jabir-Srj/moodle-connector
**Release:** v1.1.0 (March 26, 2026)
