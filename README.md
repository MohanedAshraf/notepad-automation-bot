# TJM Labs Technical Assessment - Notepad Automation Bot

## Project Overview

This project is a Python-based automation bot that fetches posts from a JSON API and creates text files using Windows Notepad. It was developed as part of the TJM Labs software developer position technical assessment.

## Features

- Fetches posts from JSONPlaceholder API
- Automates Notepad operations using PyAutoGUI
- Creates formatted text files for each post
- Includes error handling and logging
- Saves files to a dedicated desktop folder

## Requirements

- Python 3.x
- Required packages:
  - requests
  - pyautogui
  - botcity.core
  - logging

## Installation

```bash
pip install requests pyautogui botcity-core
```

## Usage

1. Run the script:

```bash
python notepad_automation.py
```

2. The bot will:
   - Create output directory on desktop
   - Fetch 10 posts from the API
   - Process each post in Notepad
   - Save formatted text files

## Output Format

Each text file contains:

- Post title (uppercase)
- Post ID
- User ID
- Post body
- End of post marker

## Error Handling

- Comprehensive logging system
- Graceful failure handling
- Automatic cleanup on errors

## Author

Mohaned (Technical Assessment Submission)
