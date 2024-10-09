# Python Base template for projects

## Overview

This project is a base template for Python projects with a few basic features.
- Virtual environment setup with source.env
- Util files for sending Telegram messages
- Util files for sending emails
- Requirements.txt that installs pips for sending messages, interfacing with the OpenAI API, scraping websites, and provisioning SQL databases.

## Installation

1. Create a new Python virtual environment
2. Delete extraneous .gitignore files
3. git clone this repository
4. Change the git remote to your own repository
5. Run source.env to activate the virtual environment and set PYTHONPATH
6. pip install -r requirements.txt
7. Create .env file with API keys and other environment variables
8. Build the rest of the project
