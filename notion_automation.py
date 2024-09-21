from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
from datetime import datetime
import json
from login import login  # Importing the login function


# Function to convert timestamp to a readable date format
def convert_timestamp_to_date(timestamp):
    try:
        return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error converting timestamp {timestamp}: {e}")
        return "Invalid Timestamp"


# Function to capture and store results from the first API (getVisibleUsers)
def fetch_visible_users(page):
    try:
        users_data = []
        with page.expect_response("https://www.notion.so/api/v3/getVisibleUsers") as response_info:
            page.reload()  # Reloading the page to trigger the API call
            response = response_info.value
            json_data = response.json()
            for user in json_data.get("users", []):
                users_data.append({
                    "role": user.get("role"),
                    "Date": convert_timestamp_to_date(user.get("firstJoinedSpaceTime")),
                    "id": user.get("userId")
                })
        return users_data
    except PlaywrightTimeoutError:
        print("Error: Timeout while fetching visible users.")
        return []
    except Exception as e:
        print(f"An error occurred while fetching visible users: {e}")
        return []


# Function to capture user emails and names from syncRecordValues
def capture_sync_record_values(page, users_data):
    try:
        with page.expect_response("https://www.notion.so/api/v3/syncRecordValues") as response_info:
            response = response_info.value
            json_data = response.json()

            for user in users_data:
                user_id = user["id"]
                user_details = json_data.get("recordMap", {}).get("notion_user", {}).get(user_id, {})
                value = user_details.get("value", {}).get("value", {})
                email = value.get("email")
                name = value.get("name", email)

                user["email"] = email
                user["name"] = name
        return users_data
    except PlaywrightTimeoutError:
        print("Error: Timeout while capturing sync record values.")
        return users_data
    except Exception as e:
        print(f"An error occurred while capturing sync record values: {e}")
        return users_data


# Main function
def main():
    try:
        with sync_playwright() as playwright_instance:
            browser = playwright_instance.chromium.launch()
            page = browser.new_page()

            # Step 1: Log in using the login function
            if login(page):
                print("Login successful, proceeding with data fetching...")

                # Step 2: Capture users from the first API (getVisibleUsers)
                users_data = fetch_visible_users(page)
                if users_data:
                    print("Fetched data from getVisibleUsers API.")

                    # Step 3: Capture emails and names from syncRecordValues
                    final_users_data = capture_sync_record_values(page, users_data)

                    time.sleep(10)  # Wait before saving the data

                    # Save the final combined data
                    try:
                        with open('final_user_data.json', 'w') as f:
                            json.dump(final_users_data, f, indent=4)
                        print("Final data saved to 'final_user_data.json'.")
                    except Exception as e:
                        print(f"Error saving data to file: {e}")
                else:
                    print("No data fetched from getVisibleUsers API.")
            else:
                print("Login failed, cannot proceed with data fetching.")
            browser.close()
    except Exception as e:
        print(f"Error launching browser or during script execution: {e}")


if __name__ == "__main__":
    main()
