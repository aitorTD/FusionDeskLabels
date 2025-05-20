# FusionDeskLabels

## Project Overview
This project merges two files provided by Cambridge University that are used in official exams. By combining these files, we reduce paper usage, contributing to environmental sustainability.

The application is built using Python and PyInstaller for distribution, with components for creating standalone applications on macOS.

## Installation
1. Clone this repository
2. Ensure Python 3.9+ is installed
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To build the application:
```bash
pyinstaller cards.spec
```

The built application will be available in the `dist` directory.

## Dependencies
Main dependencies include:
- PyInstaller
- setuptools
- Other Python standard libraries

For development, you may need additional tools listed in the `bin` directory.