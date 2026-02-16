"""
Test suite for Insider One QA job listings.
Validates the full user journey from homepage to Lever application form.
"""

import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage


class TestInsiderCareers:

    def test_insider_qa_jobs_istanbul(self, driver):
        """
        End-to-end test: verify QA positions in Istanbul, Turkiye
        are listed correctly and the Apply flow reaches Lever.
        """

        home_page = HomePage(driver)
        careers_page = CareersPage(driver)

        # Step 1 - Open homepage
        print("\n[Step 1] Opening homepage...")
        home_page.open()
        assert home_page.is_home_page_opened(), \
            "Homepage did not load correctly."
        print(f"  OK - URL: {home_page.get_url()}")

        # Step 2 - Click "We're hiring" and verify careers page
        print("\n[Step 2] Clicking 'We're hiring'...")
        home_page.click_we_are_hiring()
        assert careers_page.is_careers_page_opened(), \
            "Careers page did not open. URL does not contain 'careers'."
        print(f"  OK - URL: {careers_page.get_url()}")

        # Step 3 - Verify "Explore open roles" button exists
        print("\n[Step 3] Checking 'Explore open roles' button...")
        assert careers_page.is_explore_open_roles_visible(), \
            "'Explore open roles' button not found."
        print("  OK - Button is present.")

        # Step 4 - Click "Explore open roles"
        print("\n[Step 4] Clicking 'Explore open roles'...")
        careers_page.click_explore_open_roles()
        print("  OK - Button clicked.")

        # Step 5 - Click Software Development block
        print("\n[Step 5] Clicking Software Development block...")
        careers_page.click_software_development_block()
        print("  OK - Software Development selected.")

        # Step 6 - Apply filters (Istanbul, Turkiye + Quality Assurance)
        print("\n[Step 6] Applying filters...")
        careers_page.apply_filters(
            location="Istanbul, Turkiye",
            department="Quality Assurance"
        )
        print("  OK - Filters applied.")

        # Step 7 - Verify job listings are displayed
        print("\n[Step 7] Checking job listings...")
        assert careers_page.is_job_list_displayed(), \
            "No job listings are displayed."
        job_count = careers_page.get_job_count()
        print(f"  OK - {job_count} job(s) listed.")

        # Step 8 - Verify all jobs match the filters
        print("\n[Step 8] Verifying job details match filters...")
        assert careers_page.verify_all_jobs_match_filters(
            expected_location="Istanbul, Turkiye",
            expected_department="Quality Assurance"
        ), "Some job listings do not match the applied filters."

        # Step 9 - Click Apply on first job
        print("\n[Step 9] Clicking Apply on first job...")
        careers_page.click_apply_on_first_job()
        print("  OK - Apply button clicked.")

        # Step 10 - Verify redirect to Lever application form
        print("\n[Step 10] Verifying Lever redirect...")
        assert careers_page.is_lever_application_form_opened(), \
            "Did not redirect to Lever application form."
        print("  OK - Lever application form opened.")

        print("\n" + "=" * 50)
        print("ALL 10 STEPS PASSED")
        print("=" * 50)
