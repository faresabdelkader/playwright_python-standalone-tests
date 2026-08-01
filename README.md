# Playwright Python Test Suite

This repository contains automated web tests built using **Python**, **pytest**, and **Playwright**. The test suite targets practice pages on [QA Playground](https://qaplayground.com/practice), covering various UI components like buttons, input fields, and other interactive elements.


## Installation

Follow these steps to set up the project locally:

### 1. Prerequisites
Ensure you have **Python 3.8 or higher** installed on your system.

### 2. Create a Virtual Environment
Create a virtual environment (`.venv`) to isolate the project dependencies:

**On Windows (PowerShell/CMD):**
```powershell
python -m venv .venv
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment
Activate the created virtual environment:

**On Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```

### 5. Install Playwright Browsers
Install the browser binaries needed by Playwright to run the tests:
```bash
playwright install
```

---

## Configuration

You can customize the test runner behavior by editing [config/settings.py](file:///c:/Users/Lenovo/Desktop/Standlone_tests/playwright_python-standalone-tests/config/settings.py). Key settings include:

- `BASE_URL`: The target URL for the test suite (default: `https://qaplayground.com/practice`).
- `BROWSER_TYPE`: The browser to use (e.g., `"firefox"`, `"chromium"`, `"webkit"`).
- `HEADLESS`: Set to `True` to run tests headlessly, or `False` to view the browser during test execution.
- `SLOW_MO`: Introduces a delay (in milliseconds) between actions to make execution visual.

---

## Running Tests

Ensure your virtual environment is activated before running tests.

### Run All Tests
To run all test cases:
```bash
pytest
```

### Run a Specific Test Suite
To run a specific test suite (e.g., Buttons or Input Fields):
```bash
pytest tests/Buttons/
# or
pytest tests/Input_Field/
```

### View Test Reports
After running the tests, an HTML report is generated automatically at:
`results/report.html`

You can open this file in any web browser to see detailed results, timings, and logs.
