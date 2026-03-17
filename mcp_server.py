#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for Moodle Connector
Exposes Moodle connector as MCP tools for Claude Code, OpenCode, and other MCP clients.

Usage:
    python mcp_server.py
"""

import sys
import io
import json
from pathlib import Path
from typing import Any

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult
from moodle_connector import MoodleConnector

# Initialize MCP server
server = Server("moodle-connector")

# Global connector instance
_connector = None


def get_connector() -> MoodleConnector:
    """Get or create the connector instance"""
    global _connector
    if _connector is None:
        _connector = MoodleConnector(
            config_path=Path('config.json'),
            password='test-pass'  # Can be overridden via env var MOODLE_CRED_PASSWORD
        )
    return _connector


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="courses",
            description="Get list of enrolled courses",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="grades",
            description="Get grades overview or per-course grades",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "Optional: specific course ID to get detailed grades"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="assignments",
            description="Get all assignments with deadlines",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "Optional: filter by course ID"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="materials",
            description="Get course materials and resources",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "Optional: specific course ID"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="deadlines",
            description="Get upcoming deadlines and calendar events",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "Optional: filter by course ID"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="announcements",
            description="Get course announcements",
            inputSchema={
                "type": "object",
                "properties": {
                    "course_id": {
                        "type": "integer",
                        "description": "Optional: filter by course ID"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="download",
            description="Download a file from Moodle",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "File URL to download"
                    },
                    "output": {
                        "type": "string",
                        "description": "Optional: output file path (defaults to cache)"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="summary",
            description="Get full summary of all course data (courses, grades, assignments, deadlines, announcements)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> ToolResult:
    """Handle tool calls from MCP clients"""
    try:
        connector = get_connector()
        
        if name == "courses":
            result = connector.courses()
        elif name == "grades":
            course_id = arguments.get("course_id")
            result = connector.grades(course_id=course_id)
        elif name == "assignments":
            course_id = arguments.get("course_id")
            result = connector.assignments(course_id=course_id)
        elif name == "materials":
            course_id = arguments.get("course_id")
            result = connector.materials(course_id=course_id)
        elif name == "deadlines":
            course_id = arguments.get("course_id")
            result = connector.deadlines(course_id=course_id)
        elif name == "announcements":
            course_id = arguments.get("course_id")
            result = connector.announcements(course_id=course_id)
        elif name == "download":
            url = arguments.get("url")
            output = arguments.get("output")
            result = connector.download(url, output)
        elif name == "summary":
            result = connector.summary()
        else:
            return ToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                isError=True
            )
        
        return ToolResult(
            content=[TextContent(type="text", text=result)],
            isError=False
        )
    
    except Exception as e:
        return ToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )


def main():
    """Run the MCP server"""
    import asyncio
    asyncio.run(server.run(sys.stdin.buffer, sys.stdout.buffer))


if __name__ == "__main__":
    main()
