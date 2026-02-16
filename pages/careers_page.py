"""
Careers Page - handles the Insider One careers page and Lever job board interactions.
Covers navigation, filtering, job listing verification, and application.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CareersPage(BasePage):

    # --- Careers page locators ---
    EXPLORE_OPEN_ROLES_BTN = (By.XPATH, "//a[contains(@href, '#open-roles')]")
    SOFTWARE_DEV_LINK = (By.XPATH, "//a[contains(@href,'Software%20Development')]")

    # --- Lever filter locators ---
    # Lever has 4 filter wrappers in order: [0] Location Type, [1] Location, [2] Team, [3] Work Type
    FILTER_WRAPPER = (By.CSS_SELECTOR, "div.filter-button-wrapper")
    FILTER_BUTTON = (By.CSS_SELECTOR, "div.filter-button")
    FILTER_POPUP = (By.CSS_SELECTOR, "div.filter-popup")

    # --- Lever job listing locators ---
    JOB_ITEM = (By.CLASS_NAME, "posting")
    JOB_TITLE = (By.CSS_SELECTOR, "h5[data-qa='posting-name']")
    JOB_LOCATION = (By.CLASS_NAME, "sort-by-location")
    JOB_GROUP_TITLE = (By.CLASS_NAME, "posting-category-title")
    APPLY_BTN = (By.CSS_SELECTOR, "a.posting-btn-submit")

    def __init__(self, driver):
        super().__init__(driver)

    # --- Careers page verification ---

    def is_careers_page_opened(self):
        """Check if URL contains 'careers'."""
        return "careers" in self.get_url().lower()

    def is_explore_open_roles_visible(self):
        """Check if 'Explore open roles' button exists in the DOM."""
        return self.is_present(self.EXPLORE_OPEN_ROLES_BTN, timeout=15)

    def click_explore_open_roles(self):
        """Scroll to and click the 'Explore open roles' button."""
        btn = self.find(self.EXPLORE_OPEN_ROLES_BTN)
        self.scroll_to_element(btn)
        self.js_click(btn)
        self.wait_for_page_stable()

    # --- Software Development block ---

    def click_software_development_block(self):
        """Click the Software Development link that navigates to Lever."""
        # Team blocks load via AJAX after readyState is already "complete",
        # so we use a longer timeout to account for the async rendering.
        link = self.find_present(self.SOFTWARE_DEV_LINK, timeout=30)

        # Verify href is populated (content loads dynamically)
        WebDriverWait(self.driver, 20).until(
            lambda d: link.get_attribute("href") is not None
            and "Software%20Development" in link.get_attribute("href")
        )

        print(f"  Found: {link.text}")
        print(f"  Href: {link.get_attribute('href')}")

        self.scroll_to_element(link)
        self.js_click(link)

        # Wait for navigation to Lever
        WebDriverWait(self.driver, 20).until(EC.url_contains("lever.co"))
        print("  Navigated to Lever page.")

    # --- Lever filters ---

    def _select_lever_filter(self, wrapper_index, option_text):
        """
        Select an option from a Lever filter dropdown by wrapper index.
        Indices: 0=Location Type, 1=Location, 2=Team, 3=Work Type
        """
        wrappers = self.find_all(self.FILTER_WRAPPER, timeout=15)
        wrapper = wrappers[wrapper_index]

        btn = wrapper.find_element(*self.FILTER_BUTTON)
        current_text = btn.text.strip()

        # Skip if already selected
        if option_text.lower() in current_text.lower():
            print(f"  Filter [{wrapper_index}]: '{option_text}' already selected, skipping.")
            return

        # Open dropdown
        self.scroll_to_element(btn)
        self.js_click(btn)

        # Wait for popup to appear
        popup = WebDriverWait(wrapper, 10).until(
            EC.visibility_of_element_located(self.FILTER_POPUP)
        )

        # Find the matching option inside the popup
        options = popup.find_elements(By.XPATH, ".//*[not(*)]")
        target = None

        for opt in options:
            opt_text = opt.text.strip()
            if opt_text and option_text.lower() == opt_text.lower():
                target = opt
                break

        # Fallback: partial match
        if target is None:
            for opt in options:
                opt_text = opt.text.strip()
                if opt_text and option_text.lower() in opt_text.lower():
                    target = opt
                    break

        if target:
            print(f"  Filter [{wrapper_index}]: selecting '{target.text.strip()}'")
            self.js_click(target)
        else:
            print(f"  Filter [{wrapper_index}]: '{option_text}' not found, closing popup.")
            self.js_click(btn)

        self.wait_for_page_stable()

    def apply_filters(self, location="Istanbul, Turkiye", department="Quality Assurance"):
        """Apply location and department filters on the Lever page."""
        print(f"  Location filter: {location}")
        self._select_lever_filter(1, location)

        print(f"  Team filter: {department}")
        self._select_lever_filter(2, department)

    # --- Job listing verification ---

    def is_job_list_displayed(self):
        """Return True if at least one job posting is visible."""
        return self.is_present(self.JOB_ITEM, timeout=15)

    def get_all_jobs(self):
        """Return all job posting elements."""
        return self.find_all(self.JOB_ITEM, timeout=10)

    def get_job_count(self):
        return len(self.get_all_jobs())

    def verify_all_jobs_match_filters(self, expected_location="Istanbul, Turkiye",
                                       expected_department="Quality Assurance"):
        """
        Verify every listed job matches the applied filters.
        Checks location per posting card and department via group headers.
        """
        jobs = self.get_all_jobs()

        if not jobs:
            print("  ERROR: No job postings found on the Lever page.")
            return False

        print(f"  Scanning {len(jobs)} job posting(s)...")
        all_match = True

        for index, job in enumerate(jobs, 1):
            try:
                self.scroll_to_element(job)

                title = job.find_element(*self.JOB_TITLE).text
                location = job.find_element(*self.JOB_LOCATION).text

                print(f"  Job {index}: {title} | Location: {location}")

                if expected_location.lower() not in location.lower():
                    print(f"    FAIL: expected location '{expected_location}'")
                    all_match = False

            except Exception as e:
                print(f"  WARNING: Could not inspect job {index} - {e}")
                continue

        # Department check via group headers
        try:
            group_titles = self.find_all(self.JOB_GROUP_TITLE, timeout=5)
            group_names = [g.text for g in group_titles]
            print(f"  Group headers: {group_names}")

            if not any(expected_department.lower() in name.lower() for name in group_names):
                print(f"  FAIL: '{expected_department}' group header not found.")
                all_match = False
            else:
                print(f"  '{expected_department}' group header verified.")
        except Exception:
            print("  WARNING: Could not verify group headers.")

        return all_match

    # --- Application ---

    def click_apply_on_first_job(self):
        """Click the Apply button on the first job posting."""
        jobs = self.get_all_jobs()

        if not jobs:
            raise Exception("No job postings found to apply to.")

        first_job = jobs[0]
        self.scroll_to_element(first_job)

        apply_btn = first_job.find_element(*self.APPLY_BTN)
        print(f"  Apply URL: {apply_btn.get_attribute('href')}")
        self.js_click(apply_btn)

    def is_lever_application_form_opened(self):
        """Verify the browser navigated to a Lever application form."""
        if len(self.driver.window_handles) > 1:
            self.switch_to_new_tab()

        self.wait_for_page_stable()
        current_url = self.get_url()
        print(f"  Redirected to: {current_url}")
        return "lever.co" in current_url
