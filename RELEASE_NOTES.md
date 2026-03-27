🚀 Production-ready Moodle connector for Taylor's University

## Features

✅ **Full Moodle REST API Support**
- List courses, grades, assignments, materials
- Get deadlines, announcements, summaries
- Download files with caching

✅ **Multiple Interfaces**
- CLI tool: python moodle_connector.py courses
- Python library: from moodle_connector import MoodleConnector
- MCP protocol: Use with Claude Code, OpenCode, and compatible AI agents

✅ **Batch Downloading**
- Generic, JSON-driven downloader
- Works with any Moodle course modules
- Organizes files by course name
- Zero code modification needed

✅ **Security & Privacy**
- Encrypted credential storage (PBKDF2 + Fernet)
- Token management built-in
- No secrets in git history
- GPLv3 licensed

## Quick Start

git clone https://github.com/Jabir-Srj/moodle-connector.git
cd moodle-connector
pip install -r requirements.txt

# Setup
cp config.template.json config.json
# Add your Moodle token

# Use
python moodle_connector.py courses
python moodle_connector.py grades
python batch_downloader.py

## Integration with Claude Code / OpenCode

Add to your MCP config (claude_desktop_config.json):

{
  "mcpServers": {
    "moodle-connector": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"]
    }
  }
}

All 8 Moodle tools will be available as native MCP functions.

## Requirements
- Python 3.10+
- requests, cryptography, playwright, mcp
- Moodle web service token from your Moodle instance

See README.md for full documentation.
