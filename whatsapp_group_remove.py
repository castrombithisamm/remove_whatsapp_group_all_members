from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Use ChromeDriverManager to automatically manage the ChromeDriver installation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open WhatsApp Web (you will need to scan the QR code only on the first run)
driver.get('https://web.whatsapp.com')

# Allow time for WhatsApp Web to load
time.sleep(40)  # Adjust this time based on your connection speed

# Function to find and open the group chat
def open_group(group_name):
    try:
        # Locate the search box
        search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
        search_box.click()
        search_box.send_keys(group_name)
        time.sleep(5)
        search_box.send_keys(Keys.ENTER)
        print(f"Opened group: {group_name}")
    except Exception as e:
        print(f"Failed to open group: {e}")

# Function to remove all members from the group except admins
def remove_all_members():
    try:
        # Open group info by clicking on the group header
        group_header = driver.find_element(By.XPATH, "//header[@class='_amid']")
        group_header.click()
        time.sleep(2)

        # Wait for the element to be present and clickable
        members_locate = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'x1xhoq4m') and contains(text(), '149 members')]"))
        )
        # Scroll and click the element
        driver.execute_script("arguments[0].scrollIntoView();", members_locate)
        members_locate.click()
        time.sleep(15)

        # Re-locate the member list dynamically in each iteration to avoid stale elements
        while True:
            try:
                # Refresh the members list after each removal
                members = driver.find_elements(By.XPATH, "//span[contains(@class, 'x1iyjqo2')]")
                
                if not members:
                    print("No more members found to remove.")
                    break

                for member in members:
                    try:
                        member_name = member.get_attribute("title")  # Get the member's name

                        # Skip if the member is 'You' (the admin)
                        if member_name == "You":
                            print(f"Skipping admin: {member_name}")
                            continue  # Skip clicking on 'You'

                        # Print the member's name for debugging/logging purposes
                        print(f"Processing member: {member_name}")
                        
                        # Click on the member to open their options
                        member.click()
                        time.sleep(1)

                        # Click on the "Remove" button
                        remove_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[text()='Remove']"))
                        )
                        remove_button.click()
                        time.sleep(1)

                        print(f"Removed member: {member_name}")
                        time.sleep(2)

                        # Re-open the group header to refresh members after each removal
                        group_header.click()
                        time.sleep(2)
                        break  # After removal, refresh the member list and continue

                    except Exception as e:
                        print(f"Failed to remove member {member_name}: {e}")

            except Exception as e:
                print(f"Error iterating over members: {e}")
                break

    except Exception as e:
        print(f"Failed to remove members: {e}")

# Example usage:
group_name = "RAMSEY & ESTHER DOWRY CEREMONY (NTHEO + NGAASYA) TO BE HELD ON 19/10/2024"  # Replace with your actual group name

# Open the group and remove all members
open_group(group_name)
time.sleep(5)  # Wait for group details to load
remove_all_members()

# Close the browser when done
driver.quit()
