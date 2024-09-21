from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from faker import Faker
import os
from login import login  # Importing the login function


# Function to invite teammates
def invite_teammates(page, num_members=100):
    try:
        fake = Faker()
        emails = ", ".join([fake.email() for _ in range(num_members)])

        # Navigate through the UI to invite teammates
        page.get_by_role("button", name="Settings", exact=True).click()
        page.get_by_role("button", name="People").nth(1).click()
        page.get_by_role("button", name="Add members").nth(1).click()

        # Fill in the email field
        page.get_by_placeholder("Search name or emails").click()
        page.get_by_placeholder("Search name or emails").fill(emails)

        # Wait for a moment (3 seconds)
        page.wait_for_timeout(3000)

        # Click the Invite button
        page.get_by_role("button", name="Invite", exact=True).click()

        # Wait for the "Updating" text to appear and disappear
        page.get_by_text("Updating").wait_for(timeout=10000)
        page.get_by_text("Updating").wait_for(state="detached", timeout=30000)

        page.close()
        print(f"Invited {num_members} teammates!")
    except PlaywrightTimeoutError:
        print("Error: Timeout while trying to invite teammates.")
    except Exception as e:
        print(f"An error occurred while inviting teammates: {e}")


# Main function
def main():
    try:
        with sync_playwright() as playwright_instance:
            browser = playwright_instance.chromium.launch(headless=False)
            page = browser.new_page()

            # Step 1: Log in using the login function
            if login(page):
                print("Login successful, proceeding with inviting teammates...")

                # Step 2: Invite teammates
                invite_teammates(page, num_members=100)
            else:
                print("Login failed. Cannot proceed with inviting teammates.")
            browser.close()
    except Exception as e:
        print(f"Error launching browser or during script execution: {e}")


if __name__ == "__main__":
    main()
