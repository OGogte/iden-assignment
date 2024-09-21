from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import json
import os
import time

# File to store session info
SESSION_FILE = 'session.json'


# Function to save session cookies to a file
def save_session_cookies(page):
    try:
        cookies = page.context.cookies()
        with open(SESSION_FILE, 'w') as f:
            json.dump(cookies, f)
        print("Session saved to", SESSION_FILE)
    except Exception as e:
        print(f"Error saving session cookies: {e}")


# Function to load session cookies from the file
def load_session_cookies(page):
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r') as f:
                cookies = json.load(f)
                page.context.add_cookies(cookies)
            print("Session loaded from", SESSION_FILE)
            return True
        else:
            print(f"Session file {SESSION_FILE} not found.")
            return False
    except Exception as e:
        print(f"Error loading session cookies: {e}")
        return False


# Function to check if the login is successful
def is_logged_in(page):
    try:
        # Replace with a suitable page that requires login
        page.goto("https://www.notion.so", timeout=10000)  # 10-second timeout
        time.sleep(3)  # Wait for a few seconds to ensure the page has loaded
        # Assuming the page title doesn't have "Login" when logged in
        return "Login" not in page.title()
    except PlaywrightTimeoutError:
        print("Error: Timeout while trying to access the Notion homepage.")
        return False
    except Exception as e:
        print(f"Error during login check: {e}")
        return False


# Main login function
def login(page):
    try:
        # Try loading session cookies first
        if load_session_cookies(page):
            print("Attempting to log in using stored session...")
            if is_logged_in(page):
                print("Logged in using saved session!")
                return True
            else:
                print("Stored session failed, manual login required.")

        # If session login failed or no session, perform manual login
        print("Please log in manually...")
        page.goto("https://www.notion.so/login", timeout=10000)  # 10-second timeout
        input("Press Enter after manually logging in...")

        # After manual login, save the new session
        if is_logged_in(page):
            save_session_cookies(page)
            return True
        else:
            print("Login failed. Please try again.")
            return False
    except PlaywrightTimeoutError:
        print("Error: Timeout while trying to access the login page.")
        return False
    except Exception as e:
        print(f"Error during login process: {e}")
        return False


# Example usage
if __name__ == "__main__":
    try:
        with sync_playwright() as playwright_instance:
            browser = playwright_instance.chromium.launch(headless=False)
            page = browser.new_page()

            # Call the login function
            if login(page):
                print("Login successful!")
            else:
                print("Login failed.")
            browser.close()
    except Exception as e:
        print(f"Error launching browser or during script execution: {e}")
