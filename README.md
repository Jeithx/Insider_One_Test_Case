# Insider QA Automation Test Project

## Table of Contents
- [Project Overview](#project-overview)
- [Test Scenario](#test-scenario)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [How to Run Tests](#how-to-run-tests)
- [Test Execution Flow](#test-execution-flow)
- [Page Object Model (POM)](#page-object-model-pom)
- [Features](#features)
- [Expected Results](#expected-results)
- [Troubleshooting](#troubleshooting)
- [Requirements Compliance](#requirements-compliance)

---

## Project Overview

This is a **Selenium-based UI automation test project** designed to validate the career page functionality on the **Insider One** website. The test verifies the complete user journey from the homepage to the Lever application form, including filtering Quality Assurance positions in Istanbul, Turkiye.

### Key Objectives:
- Verify navigation from homepage to career pages
- Validate Lever filter functionality (Location & Team)
- Ensure all job listings match the applied filters
- Confirm successful redirection to the Lever application form

---

## Test Scenario

The automated test performs the following **10 steps**:

1. **Navigate to Homepage** - Visit `https://insiderone.com/` and verify it loads correctly
2. **Click "We're hiring"** - Click the footer link and verify navigation to the Careers page
3. **Check "Explore open roles"** - Verify the button is present on the Careers page
4. **Click "Explore open roles"** - Navigate to the teams/departments section
5. **Select Software Development** - Click the Software Development link, which navigates to the Lever job board
6. **Apply Filters** - Select Location: **"Istanbul, Turkiye"** and Team: **"Quality Assurance"** via Lever filter dropdowns
7. **Verify Job Listings** - Confirm at least one job posting is displayed
8. **Validate Job Details** - Verify all listings match the applied filters (location and department group header)
9. **Click Apply** - Click the Apply button on the first job listing
10. **Verify Lever Form** - Confirm redirection to a Lever application form (`lever.co` in URL)

---

## Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Programming Language |
| **Selenium** | >= 4.18.1 | Web Automation Framework |
| **Pytest** | >= 8.0.2 | Testing Framework |
| **WebDriver Manager** | >= 4.0.1 | Automatic ChromeDriver Management |
| **Chrome Browser** | Latest | Test Execution Browser |

---

## Project Structure

```
Insider_One_Test_Case/
|
+-- pages/                          # Page Object Model (POM) files
|   +-- __init__.py
|   +-- base_page.py               # Base page with reusable Selenium helpers
|   +-- home_page.py               # Homepage locators & methods
|   +-- careers_page.py            # Careers page + Lever job board locators & methods
|
+-- tests/                          # Test files
|   +-- __init__.py
|   +-- conftest.py                # Pytest fixtures & screenshot-on-failure hook
|   +-- test_insider.py            # Main test case (1 class, 1 test, 10 steps)
|
+-- screenshots/                    # Auto-generated on test failure
|   +-- FAIL_*.png                 # Failure screenshots (if any)
|
+-- requirements.txt                # Python dependencies
+-- .gitignore                      # Git ignore rules
+-- README.md                       # This file
```

---

## Installation & Setup

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Google Chrome Browser** (latest version)

3. **Git** (optional, for cloning)

### Install Dependencies

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## How to Run Tests

### Run All Tests (Recommended)
```bash
pytest tests/test_insider.py -v -s
```

> `-v` (verbose): Shows detailed test names and pass/fail status.
> `-s` (no capture): Shows `print()` output so you can follow the step-by-step execution in the terminal.

### Run without step output
```bash
pytest tests/test_insider.py -v
```

### Run with HTML Report (requires pytest-html)
```bash
pip install pytest-html
pytest tests/test_insider.py --html=report.html --self-contained-html
```

### Run in Headless Mode
Edit `tests/conftest.py` and uncomment these lines:
```python
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```

---

## Test Execution Flow

```
1. conftest.py initializes Chrome WebDriver
        |
2. test_insider.py creates HomePage + CareersPage objects
        |
3. HomePage.open() --> Navigate to insiderone.com, accept cookies
        |
4. HomePage.click_we_are_hiring() --> Click footer link
        |
5. CareersPage.is_careers_page_opened() --> Verify URL contains "careers"
        |
6. CareersPage.is_explore_open_roles_visible() --> Check button
        |
7. CareersPage.click_explore_open_roles() --> Scroll + JS click
        |
8. CareersPage.click_software_development_block() --> Navigate to Lever
        |
9. CareersPage.apply_filters() --> Select Location + Team via Lever dropdowns
        |
10. CareersPage.verify_all_jobs_match_filters() --> Validate all listings
        |
11. CareersPage.click_apply_on_first_job() --> Click Apply
        |
12. CareersPage.is_lever_application_form_opened() --> Verify lever.co URL
        |
13. Test PASSED (or FAILED with automatic screenshot)
```

---

## Page Object Model (POM)

### POM Implementation

#### 1. **BasePage** (`pages/base_page.py`)
Parent class with reusable Selenium helpers. Default timeout: 15 seconds.

```python
class BasePage:
    def find(locator)               # Wait for visibility, return element
    def find_clickable(locator)     # Wait for clickability
    def find_all(locator)           # Wait for all matching elements
    def find_present(locator)       # Wait for DOM presence
    def click(locator)              # Wait + click
    def js_click(element)           # JavaScript click (bypass overlays)
    def is_visible(locator)         # Boolean visibility check
    def is_clickable(locator)       # Boolean clickability check
    def is_present(locator)         # Boolean DOM presence check
    def scroll_to_element(element)  # Smooth scroll to center
    def scroll_to_bottom()          # Scroll to page bottom
    def hover(element)              # Mouse hover
    def switch_to_new_tab()         # Switch to last opened tab
    def wait_for_page_stable()      # Wait for document.readyState == "complete"
    def wait_for_url_contains(text) # URL validation
```

- Uses **Explicit Waits** throughout (no `time.sleep()`)
- All boolean checks return `True`/`False` without raising exceptions

#### 2. **HomePage** (`pages/home_page.py`)

```python
class HomePage(BasePage):
    URL = "https://insiderone.com/"

    COOKIE_ACCEPT_BTN   = (By.ID, "wt-cli-accept-all-btn")
    WE_ARE_HIRING_LINK  = (By.XPATH, "//footer//a[contains(text(), \"We're hiring\")]")

    def open()                  # Navigate to URL, accept cookies, wait for stable
    def is_home_page_opened()   # URL contains "insiderone.com" or title contains "Insider"
    def click_we_are_hiring()   # Scroll to footer, JS-click link, wait for "careers" in URL
```

#### 3. **CareersPage** (`pages/careers_page.py`)
Handles both the Insider careers page and the Lever job board.

```python
class CareersPage(BasePage):
    # Insider careers page
    EXPLORE_OPEN_ROLES_BTN = (By.XPATH, "//a[contains(@href, '#open-roles')]")
    SOFTWARE_DEV_LINK      = (By.XPATH, "//a[contains(@href,'Software%20Development')]")

    # Lever filter dropdowns
    FILTER_WRAPPER  = (By.CSS_SELECTOR, "div.filter-button-wrapper")
    FILTER_BUTTON   = (By.CSS_SELECTOR, "div.filter-button")
    FILTER_POPUP    = (By.CSS_SELECTOR, "div.filter-popup")

    # Lever job listing elements
    JOB_ITEM        = (By.CLASS_NAME, "posting")
    JOB_TITLE       = (By.CSS_SELECTOR, "h5[data-qa='posting-name']")
    JOB_LOCATION    = (By.CLASS_NAME, "sort-by-location")
    JOB_GROUP_TITLE = (By.CLASS_NAME, "posting-category-title")
    APPLY_BTN       = (By.CSS_SELECTOR, "a.posting-btn-submit")

    def is_careers_page_opened()             # URL contains "careers"
    def is_explore_open_roles_visible()      # Button present in DOM
    def click_explore_open_roles()           # Scroll + JS click
    def click_software_development_block()   # Navigate to Lever (30s timeout for async load)
    def apply_filters(location, department)  # Select Lever dropdowns (index 1=Location, 2=Team)
    def is_job_list_displayed()              # At least one .posting exists
    def get_all_jobs()                       # Return all .posting elements
    def get_job_count()                      # Number of postings
    def verify_all_jobs_match_filters(...)   # Check location per card + department via group header
    def click_apply_on_first_job()           # JS-click Apply on first posting
    def is_lever_application_form_opened()   # Switch tab if needed, check "lever.co" in URL
```

---

## Features

### 1. Automatic Screenshot on Failure
- Implemented via `pytest_runtest_makereport` hook in `tests/conftest.py`
- Screenshots saved to `screenshots/FAIL_{test_name}_{timestamp}.png`
- `screenshots/` directory is auto-created at startup via `pytest_configure`

### 2. Explicit Waits (No time.sleep)
All waits use Selenium's `WebDriverWait` with `expected_conditions`:

```python
WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located(locator)
)
```

### 3. Lever Filter Dropdown Handling
Custom handling for Lever's filter dropdowns using wrapper indices:

```
Index 0: Location Type
Index 1: Location        <-- used for "Istanbul, Turkiye"
Index 2: Team            <-- used for "Quality Assurance"
Index 3: Work Type
```

The `_select_lever_filter()` method opens the dropdown, performs exact match first then partial match fallback, and uses JS click to select the option.

### 4. Step-by-step Console Output
Test execution logs each step to the console (visible with `pytest -s`):

```
[Step 1] Opening homepage...
  OK - URL: https://insiderone.com/

[Step 2] Clicking 'We're hiring'...
  OK - URL: https://insiderone.com/careers

[Step 6] Applying filters...
  Location filter: Istanbul, Turkiye
  Team filter: Quality Assurance
  OK - Filters applied.

[Step 8] Verifying job details match filters...
  Scanning 5 job posting(s)...
  Job 1: QA Engineer | Location: Istanbul, Turkiye
  ...
```

### 5. Dynamic Job Validation
Validates every listed job against the applied filters:
- Location is checked per individual posting card
- Department is verified via group header elements (`posting-category-title`)

---

## Expected Results

### Successful Test Run

```
tests/test_insider.py::TestInsiderCareers::test_insider_qa_jobs_istanbul

[Step 1] Opening homepage...
  OK - URL: https://insiderone.com/

[Step 2] Clicking 'We're hiring'...
  OK - URL: https://insiderone.com/careers

[Step 3] Checking 'Explore open roles' button...
  OK - Button is present.

[Step 4] Clicking 'Explore open roles'...
  OK - Button clicked.

[Step 5] Clicking Software Development block...
  OK - Software Development selected.

[Step 6] Applying filters...
  OK - Filters applied.

[Step 7] Checking job listings...
  OK - N job(s) listed.

[Step 8] Verifying job details match filters...

[Step 9] Clicking Apply on first job...
  OK - Apply button clicked.

[Step 10] Verifying Lever redirect...
  OK - Lever application form opened.

==================================================
ALL 10 STEPS PASSED
==================================================

PASSED
```

### Test Failure
If any step fails:
1. Test stops at the failing assertion
2. Screenshot is automatically saved to `screenshots/`
3. Error message with assertion details is displayed

---

## Troubleshooting

### Common Issues

| Issue | Error | Solution |
|-------|-------|----------|
| ChromeDriver mismatch | `SessionNotCreatedException` | `pip install --upgrade webdriver-manager` |
| Element not found | `TimeoutException` | Check locators in `pages/` files; website may have changed |
| Slow connection | Page load timeout | Increase timeout values or use headless mode |
| Cookie popup not found | (handled gracefully) | No action needed, test continues |
| Lever filters not loading | Dropdown options missing | Verify Lever page loaded; check filter wrapper indices |
| Import errors | `ModuleNotFoundError` | Activate virtual environment and reinstall dependencies |
| Browser not opening | Headless mode enabled | Comment out `--headless` in `tests/conftest.py` |

---

## Requirements Compliance

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Python + Selenium | Done | Python 3.8+ with Selenium >= 4.18.1 |
| No BDD Frameworks | Done | Pure Python with Pytest (no Cucumber, etc.) |
| Screenshot on Failure | Done | `pytest_runtest_makereport` hook in `conftest.py` |
| Page Object Model | Done | `BasePage`, `HomePage`, `CareersPage` with inheritance |
| All Test Steps | Done | 10 steps covering homepage to Lever application form |

---

**Last Updated:** February 2026
**Version:** 1.0.0
