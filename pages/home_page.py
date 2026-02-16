"""
Home Page - Insider One homepage actions.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    URL = "https://insiderone.com/"

    # Locators
    COOKIE_ACCEPT_BTN = (By.ID, "wt-cli-accept-all-btn")
    WE_ARE_HIRING_LINK = (By.XPATH, "//footer//a[contains(text(), \"We're hiring\")]")

    def __init__(self, driver):
        super().__init__(driver)

    def open(self):
        """Navigate to the homepage and dismiss the cookie banner if present."""
        self.driver.get(self.URL)
        self._accept_cookies()
        self.wait_for_page_stable()

    def _accept_cookies(self):
        """Click the cookie accept button if it appears."""
        try:
            if self.is_visible(self.COOKIE_ACCEPT_BTN, timeout=5):
                self.click(self.COOKIE_ACCEPT_BTN)
        except Exception:
            pass

    def is_home_page_opened(self):
        """Verify the homepage loaded by checking URL and title."""
        current_url = self.get_url()
        title = self.get_title()
        return ("insiderone.com" in current_url or
                "Insider" in title or
                "insider" in current_url.lower())

    def click_we_are_hiring(self):
        """Scroll to footer, click 'We're hiring' link via JS to avoid overlay issues."""
        self.scroll_to_bottom()
        element = self.find(self.WE_ARE_HIRING_LINK, timeout=10)
        self.scroll_to_element(element)
        self.js_click(element)
        self.wait_for_url_contains("careers")
