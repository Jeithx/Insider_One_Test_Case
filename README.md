# Insider QA Automation Test Project

## 📋 Table of Contents
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
- [Contact](#contact)

---

## 🎯 Project Overview

This is a **Selenium-based UI automation test project** designed to validate the career page functionality on the **Insider One** website. The test verifies the complete user journey from the homepage to the Lever application form, including filtering Quality Assurance positions in Istanbul, Turkey.

### Key Objectives:
- ✅ Verify navigation from homepage to career pages
- ✅ Validate filter functionality (Location & Department)
- ✅ Ensure all job listings match the applied filters
- ✅ Confirm successful redirection to the Lever application form

---

## 📝 Test Scenario

The automated test performs the following steps:

1. **Navigate to Homepage**
   - Visit `https://insiderone.com/`
   - Verify the Insider One homepage is loaded

2. **Access Career Page**
   - Click on "We're hiring" link in the footer
   - Verify navigation to the Career page
   - Confirm "Explore open roles" button is present

3. **Navigate to Job Listings**
   - Click "Explore open roles" button
   - Navigate to the teams/departments page

4. **Select Software Development**
   - Click on "Software Development" block
   - Navigate to the "Open Positions" link

5. **Apply Filters**
   - Select Location filter: **"Istanbul, Turkiye"**
   - Select Team/Department filter: **"Quality Assurance"**

6. **Validate Job Listings**
   - Verify job list is displayed
   - Confirm all listings contain:
     - Position: "Quality Assurance"
     - Location: "Istanbul, Turkiye"

7. **Apply to a Position**
   - Click "Apply" / "View Role" button on the first job listing

8. **Verify Lever Form**
   - Confirm redirection to Lever Application Form
   - Verify URL contains `lever.co`

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.8+ | Programming Language |
| **Selenium** | 4.18.1 | Web Automation Framework |
| **Pytest** | 8.0.2 | Testing Framework |
| **WebDriver Manager** | 4.0.1 | Automatic WebDriver Management |
| **Chrome Browser** | Latest | Test Execution Browser |

### Why These Technologies?

- **Selenium**: Industry-standard for web automation
- **Pytest**: Clean syntax, powerful fixtures, detailed reporting
- **WebDriver Manager**: Eliminates manual ChromeDriver setup
- **No BDD Framework**: Pure Python/Pytest as per requirements

---

## 📁 Project Structure

```
Insider_Selenium_Task/
│
├── pages/                          # Page Object Model (POM) files
│   ├── __init__.py
│   ├── base_page.py               # Base page with reusable methods
│   ├── home_page.py               # Homepage locators & methods
│   └── careers_page.py            # Career page locators & methods
│
├── tests/                          # Test files
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures & hooks
│   └── test_insider.py            # Main test case
│
├── screenshots/                    # Auto-generated on test failure
│   ├── .gitkeep
│   └── FAIL_*.png                 # Failure screenshots (if any)
│
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **Google Chrome Browser** (latest version)
   - Download from: https://www.google.com/chrome/

3. **Git** (optional, for cloning)
   ```bash
   git --version
   ```

### Step-by-Step Installation

#### Option 1: Clone the Repository
```bash
git clone <repository-url>
cd Insider_Selenium_Task
```

#### Option 2: Download ZIP
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the project folder

### Install Dependencies

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
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
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
pip list
```

**Expected output:**
```
selenium            4.18.1
pytest              8.0.2
webdriver-manager   4.0.1
```

---

## ▶️ How to Run Tests

### Run All Tests (Recommended)
```bash
pytest tests/test_insider.py -v -s
```

> **Why `-v -s`?**
> - `-v` (verbose): Shows detailed test names and pass/fail status instead of just dots.
> - `-s` (no capture): By default, pytest captures and hides `print()` output. Since this test uses `print()` statements to log each step's progress, `-s` is **required** to see the step-by-step execution output in the terminal.

### Run without step output (minimal)
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

Then run:
```bash
pytest tests/test_insider.py -v
```

---

## 🔄 Test Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    TEST EXECUTION FLOW                       │
└─────────────────────────────────────────────────────────────┘

1. conftest.py initializes Chrome WebDriver
        ↓
2. test_insider.py creates Page Objects
        ↓
3. HomePage.open() → Navigate to insiderone.com
        ↓
4. HomePage.click_we_are_hiring() → Click footer link
        ↓
5. CareersPage.is_careers_page_opened() → Verify URL
        ↓
6. CareersPage.is_explore_open_roles_visible() → Check button
        ↓
7. CareersPage.click_explore_open_roles() → Navigate to teams
        ↓
8. CareersPage.click_software_development_block() → Select dept
        ↓
9. CareersPage.apply_filters() → Set Istanbul + QA filters
        ↓
10. CareersPage.verify_all_jobs_match_filters() → Validate
        ↓
11. CareersPage.click_view_role_on_first_job() → Apply
        ↓
12. CareersPage.is_lever_application_form_opened() → Verify
        ↓
13. Test PASSED ✅ (or FAILED ❌ with screenshot)
```

---

## 🏗️ Page Object Model (POM)

### What is POM?

**Page Object Model** is a design pattern that:
- Separates test logic from page-specific code
- Improves code maintainability and reusability
- Makes tests more readable and easier to update

### POM Implementation in This Project

#### 1. **BasePage** (`pages/base_page.py`)
Contains reusable methods used by all page objects:

```python
class BasePage:
    def find(locator)           # Wait and find element
    def click(locator)          # Click element
    def is_visible(locator)     # Check visibility
    def scroll_to_element()     # Scroll to element
    def wait_for_url_contains() # URL validation
    # ... and more
```

**Key Features:**
- ✅ Uses **Explicit Waits** (no `time.sleep()`)
- ✅ Exception handling
- ✅ Scroll management
- ✅ Tab/window switching

#### 2. **HomePage** (`pages/home_page.py`)
Handles homepage-specific operations:

```python
class HomePage(BasePage):
    # Locators
    COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")
    WE_ARE_HIRING_LINK = (By.XPATH, "//footer//a[...]")

    # Methods
    def open()
    def is_home_page_opened()
    def click_we_are_hiring()
```

#### 3. **CareersPage** (`pages/careers_page.py`)
Handles career page operations:

```python
class CareersPage(BasePage):
    # Locators
    EXPLORE_OPEN_ROLES_BTN = (By.XPATH, "//a[...]")
    FILTER_BY_LOCATION = (By.ID, "select2-filter-by-location-container")
    JOB_ITEM = (By.CLASS_NAME, "position-list-item")

    # Methods
    def is_careers_page_opened()
    def click_explore_open_roles()
    def apply_filters(location, department)
    def verify_all_jobs_match_filters()
```

#### 4. **Test File** (`tests/test_insider.py`)
Contains only test logic:

```python
def test_insider_qa_jobs_istanbul(driver):
    home_page = HomePage(driver)
    careers_page = CareersPage(driver)

    # Step 1: Open homepage
    home_page.open()
    assert home_page.is_home_page_opened()

    # Step 2: Navigate to careers
    home_page.click_we_are_hiring()
    # ... and so on
```

### POM Benefits in This Project

✅ **Separation of Concerns**: Locators are separate from test logic
✅ **Reusability**: Methods can be used in multiple tests
✅ **Maintainability**: If UI changes, update only the page object
✅ **Readability**: Tests read like plain English

---

## ✨ Features

### 1. **Automatic Screenshot on Failure**
- Implemented in `tests/conftest.py`
- Uses `pytest_runtest_makereport` hook
- Screenshots saved to `screenshots/` folder
- Filename format: `FAIL_{test_name}_{timestamp}.png`

**Example:**
```
screenshots/
  └── FAIL_test_insider_qa_jobs_istanbul_2024-02-16_14-30-45.png
```

### 2. **Explicit Waits (No time.sleep)**
All waits use Selenium's `WebDriverWait`:

```python
# ❌ BAD (not used in this project)
time.sleep(5)

# ✅ GOOD (used throughout)
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(locator)
)
```

### 3. **Select2 Dropdown Handling**
Special handling for Select2 JavaScript dropdowns:

```python
def select_filter_option(dropdown_locator, option_text):
    # 1. Click dropdown to open
    # 2. Wait for options to load
    # 3. Click desired option
    # 4. Wait for page update
```

### 4. **Detailed Console Output**
Test execution includes step-by-step logging:

```
═══════════════════════════════════════════
📌 STEP 1: Navigating to homepage...
═══════════════════════════════════════════
✅ Homepage successfully opened.
   URL: https://insiderone.com/

═══════════════════════════════════════════
📌 STEP 2: Clicking 'We're hiring' link...
═══════════════════════════════════════════
✅ Career page successfully opened.
   URL: https://insiderone.com/careers
```

### 5. **Dynamic Job Validation**
Validates all job listings match filters:

```python
for job in jobs:
    department = job.find_element(...).text
    location = job.find_element(...).text

    assert "Quality Assurance" in department
    assert "Istanbul, Turkiye" in location
```

---

## 📊 Expected Results

### Successful Test Run Output

```
tests/test_insider.py::TestInsiderCareers::test_insider_qa_jobs_istanbul

═══════════════════════════════════════════
📌 STEP 1: Navigating to homepage...
═══════════════════════════════════════════
✅ Homepage successfully opened.

═══════════════════════════════════════════
📌 STEP 2: Clicking 'We're hiring' link...
═══════════════════════════════════════════
✅ Career page successfully opened.

... (more steps) ...

═══════════════════════════════════════════
🎉 TEST SUCCESSFULLY COMPLETED! 🎉
═══════════════════════════════════════════
   ✓ Homepage verified
   ✓ Career page verified
   ✓ Explore open roles button verified
   ✓ Software Development block selected
   ✓ Filters applied (Istanbul, Turkiye + QA)
   ✓ 12 job listings verified
   ✓ Lever application form verified
═══════════════════════════════════════════

PASSED                                    [100%]
```

### Test Failure with Screenshot

If any step fails:
1. Test stops immediately
2. Screenshot is automatically saved
3. Detailed error message is displayed
4. Screenshot path is printed

```
❌ FAILED: AssertionError: Location filter mismatch!
   Expected: Istanbul, Turkiye
   Found: Ankara, Turkey

📸 Screenshot saved: screenshots/FAIL_test_insider_qa_jobs_istanbul_2024-02-16_14-30-45.png
```

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **ChromeDriver Version Mismatch**
**Error:** `SessionNotCreatedException: session not created`

**Solution:**
```bash
# WebDriver Manager should auto-update, but if it fails:
pip install --upgrade webdriver-manager
```

#### 2. **Element Not Found**
**Error:** `NoSuchElementException` or `TimeoutException`

**Solution:**
- Website structure may have changed
- Check locators in `pages/` files
- Use browser DevTools (F12) to verify selectors
- Increase timeout in `base_page.py`:
  ```python
  def __init__(self, driver, timeout=30):  # Increase from 15
  ```

#### 3. **Slow Internet Connection**
**Error:** Page loads timeout

**Solution:**
- Increase timeout values
- Use headless mode for faster execution
- Check your internet connection

#### 4. **Cookie Popup Not Appearing**
**Error:** Test passes but cookie button not found

**Solution:**
- This is handled gracefully in `home_page.py`
- If popup doesn't appear, test continues
- No action needed

#### 5. **Filters Not Working**
**Error:** Dropdown options not appearing

**Solution:**
- Ensure JavaScript is enabled
- Check if Select2 library is loaded
- Verify dropdown IDs in DevTools
- Update locators if website changed

#### 6. **Import Errors**
**Error:** `ModuleNotFoundError: No module named 'selenium'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 7. **Tests Run But Browser Doesn't Open**
**Error:** Headless mode is enabled

**Solution:**
Edit `tests/conftest.py` and comment out:
```python
# chrome_options.add_argument("--headless")
```

---

## ✅ Requirements Compliance

This project fully meets all specified requirements:

### 1. ✅ Programming Language & Framework
- **Requirement:** Python or Java + Selenium (preferred)
- **Implementation:** Python 3.8+ with Selenium 4.18.1
- **Framework:** Pytest 8.0.2

### 2. ✅ No BDD Frameworks
- **Requirement:** Do not use Cucumber, Quantum, Codeception, etc.
- **Implementation:** Pure Python with Pytest (no BDD)

### 3. ✅ Screenshot on Failure
- **Requirement:** Take screenshot if any test step fails
- **Implementation:**
  - `tests/conftest.py` lines 52-82
  - Automatic screenshot using `pytest_runtest_makereport` hook
  - Saved to `screenshots/FAIL_{test_name}_{timestamp}.png`

### 4. ✅ Page Object Model (POM)
- **Requirement:** Code must fully comply with POM requirements
- **Implementation:**
  - ✅ Separate page classes (`BasePage`, `HomePage`, `CareersPage`)
  - ✅ Locators defined in page classes (not in tests)
  - ✅ Page-specific methods in respective classes
  - ✅ Test file contains only test logic
  - ✅ Inheritance structure (pages inherit from `BasePage`)
  - ✅ Reusable methods in base class
  - ✅ No hardcoded waits (`time.sleep`)

### 5. ✅ Test Scenario Coverage
All PDF requirements are implemented:
- ✅ Step 1: Visit homepage and verify
- ✅ Step 2: Click "We're hiring" and verify Career page
- ✅ Step 3: Check "Explore open roles" button presence
- ✅ Step 4: Click "Explore open roles"
- ✅ Step 5: Click Software Development "Open Positions"
- ✅ Step 6: Apply filters (Istanbul, Turkiye + Quality Assurance)
- ✅ Step 7: Verify job list is displayed
- ✅ Step 8: Verify all jobs match filters
- ✅ Step 9: Click "Apply" button
- ✅ Step 10: Verify Lever Application Form page

---

## 📚 Additional Resources

### Selenium Documentation
- Official Docs: https://www.selenium.dev/documentation/
- Python Bindings: https://selenium-python.readthedocs.io/

### Pytest Documentation
- Official Docs: https://docs.pytest.org/
- Fixtures: https://docs.pytest.org/en/stable/fixture.html

### WebDriver Manager
- GitHub: https://github.com/SergeyPirogov/webdriver_manager

### Page Object Model
- Selenium Guide: https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/

---


## 📄 License

This project is created for QA automation testing purposes.

---

## 🙏 Acknowledgments

- **Insider:** For providing the test website
- **Selenium Community:** For the excellent automation framework
- **Pytest Contributors:** For the powerful testing framework

---

**Last Updated:** February 2026
**Version:** 1.0.0
**Status:** ✅ Production Ready

---

Made with ❤️ for Insider One
