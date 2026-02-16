"""
Base Page - parent class for all page objects.
Provides reusable helpers built on Selenium explicit waits.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base class that all page objects inherit from."""

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.actions = ActionChains(driver)

    # --- Element lookup ---

    def find(self, locator, timeout=None):
        """Wait for element to be visible and return it."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator, timeout=None):
        """Wait for element to be clickable and return it."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator, timeout=None):
        """Wait for all matching elements to be present and return them."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def find_present(self, locator, timeout=None):
        """Wait for element to exist in DOM (doesn't need to be visible)."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    # --- Element actions ---

    def click(self, locator, timeout=None):
        """Wait for element to be clickable, then click."""
        element = self.find_clickable(locator, timeout)
        element.click()

    def js_click(self, element):
        """Click element via JavaScript (bypasses overlay issues)."""
        self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text, timeout=None):
        """Clear field and type text."""
        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=None):
        """Return the visible text of an element."""
        return self.find(locator, timeout).text

    # --- Visibility checks ---

    def is_visible(self, locator, timeout=5):
        """Return True if element is visible within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_clickable(self, locator, timeout=5):
        """Return True if element is clickable within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, locator, timeout=5):
        """Return True if element exists in the DOM within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # --- Page info ---

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def wait_for_url_contains(self, text, timeout=None):
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.url_contains(text))

    def wait_for_title_contains(self, text, timeout=None):
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.title_contains(text))

    # --- Scrolling ---

    def scroll_to_element(self, element):
        """Scroll element into the center of the viewport."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
            element
        )
        self.wait_for_page_stable()

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait_for_page_stable()

    def scroll_down(self, pixels=500):
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        self.wait_for_page_stable()

    # --- Mouse actions ---

    def hover(self, element):
        self.actions.move_to_element(element).perform()

    def hover_by_locator(self, locator, timeout=None):
        element = self.find(locator, timeout)
        self.hover(element)

    # --- Tab handling ---

    def switch_to_new_tab(self):
        """Switch to the most recently opened tab."""
        self.wait.until(lambda d: len(d.window_handles) > 1)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_to_main_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_tab_count(self):
        return len(self.driver.window_handles)

    # --- Utilities ---

    def wait_for_page_stable(self, timeout=2):
        """Wait until document.readyState is 'complete'."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            pass

    def wait_for_element_staleness(self, element, timeout=10):
        """Wait until element is removed from the DOM (e.g. after page reload)."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.staleness_of(element))
