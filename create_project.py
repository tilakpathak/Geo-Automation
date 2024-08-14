import os
import re
import imaplib
import email
import string
import time
import random
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from first_signin import SignIn


class WebsiteTester:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # self.final_signIn = SignIn(self.url)
        print("----website tester instance----")  

    def login(self):
        self.final_signIn.run_test()

    def test_signup(self, email_address, email_username, email_password):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys(email_address)
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()

        verification_code = self.fetch_verification_code(email_username, email_password)
        if verification_code:
            self.enter_verification_code(verification_code)
        else:
            print("Verification code not found.")
            return

        time.sleep(10)

    def close_browser(self):
        self.driver.quit()

    def fetch_verification_code(self, username, password):
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(username, password)
            time.sleep(15)
            mail.select("inbox")
            print("Logged into email successfully")

            for _ in range(20):  # Check up to 20 times (e.g., up to 100 seconds)
                result, data = mail.search(None, 'ALL')
                if result != 'OK':
                    print(f"Failed to search emails: {result}")
                    return None

                email_ids = data[0].split()
                print(f"Email IDs found: {email_ids}")

                if email_ids:
                    # Check the latest email first and move backwards
                    for email_id in reversed(email_ids):
                        result, data = mail.fetch(email_id, "(RFC822)")
                        if result != 'OK':
                            print(f"Failed to fetch email: {result}")
                            continue

                        raw_email = data[0][1]
                        msg = email.message_from_bytes(raw_email)
                        print("Fetched email content successfully")

                        verification_code = self.extract_verification_code(msg)
                        if verification_code:
                            return verification_code
                        else:
                            print(f"No OTP found in email ID: {email_id}")

                print("No verification email found, retrying...")
                time.sleep(5)
        except Exception as e:
            print("Error fetching verification code:", e)
        finally:
            mail.logout()
            print("Logged out of email")
        return None

    def extract_verification_code(self, msg):
        subject = msg["subject"]
        print(f"Email subject: {subject}")
        verification_code = re.search(r'\b\d{6}\b', subject)
        if verification_code:
            print(f"Verification code found: {verification_code.group()}")
            return verification_code.group()
        return None

    def enter_verification_code(self, verification_code):
        for i, digit in enumerate(verification_code):
            verification_field = self.driver.find_element(By.CSS_SELECTOR,
                                                          f"[class] [type='text']:nth-of-type({i + 1})")
            verification_field.send_keys(digit)

    def select_workspace(self, workspace):
        # Locate and click on the workspace element in the sidebar
        workspace_element = self.driver.find_element(By.CSS_SELECTOR, "[class*='naxatw-text-[#FAFAFB]']")
        workspace_element.click()
        print(f"Workspace '{workspace}' selected.")

    def select_project(self):
        project_element = self.driver.find_element(By.CSS_SELECTOR,
                                                   "a:nth-of-type(1) .naxatw-font-semibold:first-of-type")
        project_element.click()
        time.sleep(10)

    def select_management(self, invited_email):
        try:
            # Click on the management section link
            management_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "a:nth-of-type(3) > .naxatw-box-border.naxatw-flex.naxatw-h-\[39px\].naxatw-items-center.naxatw-justify-center.naxatw-rounded.naxatw-w-full"))
            )
            management_element.click()
            time.sleep(3)

            # Click on the search bar and enter the invited email
            search_bar = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     "[class='naxatw-w-\[17\.125rem\] naxatw-h-\[2\.5rem\] naxatw-rounded naxatw-flex naxatw-gap-2 naxatw-border border-\[\#DADEE3\] naxatw-items-center naxatw-px-\[0\.84rem\] naxatw-py-\[0\.5rem\]']"))
            )
            search_bar.click()
            time.sleep(1)
            search_bar.send_keys(invited_email)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(3)

            # Highlight the email if found in the search results
            highlighted_element = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  ".naxatw-font-normal.naxatw-h-12.naxatw-text-\[\#262626\].naxatw-text-sm > tr:nth-of-type(1)"))
            )
            self.highlight_element(highlighted_element)
        except Exception as e:
            print(f"An error occurred while selecting the management section: {e}")

    def highlight_element(self, element):
        try:
            # Highlight the element by adding a red border
            self.driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", element)
            time.sleep(2)  # Keep the highlight for 2 seconds
            self.driver.execute_script("arguments[0].setAttribute('style', 'border: 0px');", element)

        except Exception as e:
            print(f"Error highlighting element: {e}")

    # def select_card(self):
    #     card_element = self.driver.find_element(By.CSS_SELECTOR, "div.projects > a:first-of-type")
    #     card_element.click()
    #     time.sleep(10)

    def select_card(self):
        try:
            # Try to locate and click on the first project card
            card_element = self.driver.find_element(By.CSS_SELECTOR, "div.projects > a:first-of-type")
            card_element.click()
            print("Project card selected.")
            time.sleep(10)

        except:
            # If no project card is found, click on the New Project button
            print("No project card found, clicking on 'New Project' button.")
            new_project_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='button'] > div")
            new_project_button.click()
            time.sleep(10)

        # Perform the earlier tasks that need to be done after clicking on the project card
        # self.edit_project_name()
        self.zoomtoLayer()
        self.select_polygon()
        self.draw_point()
        self.draw_line()
        self.upload_existing_data()
        time.sleep(8)
        self.share_project()

    def select_polygon(self):
        polygon_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".darwing-icons.naxatw-pr-0\\.5"))
        )
        polygon_element.click()
        time.sleep(5)

        map_section = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#imageMap"))
        )

        map_width = map_section.size['width']
        map_height = map_section.size['height']

        center_x = random.randint(50, map_width - 50)
        center_y = random.randint(50, map_height - 50)

        print(f"Map width: {map_width}, Map height: {map_height}")
        print(f"Random map center: ({center_x}, {center_y})")

        if random.choice(['triangle', 'rectangle']) == 'triangle':
            self.draw_triangle(map_section, center_x, center_y, map_width, map_height)
        else:
            self.draw_rectangle(map_section, center_x, center_y, map_width, map_height)

        # Add a comment at the center of the drawn shape
        self.add_comment(map_section, center_x, center_y)

    def draw_point(self):
        # Click on the point drawing icon
        point_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-of-type(3) > img[alt='icons']"))
        )
        point_element.click()
        time.sleep(5)

        # Assuming you need to click on the map section with specific coordinates
        map_section = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#imageMap"))
        )

        # Get the dimensions of the map section
        map_width = map_section.size['width']
        map_height = map_section.size['height']

        for _ in range(2):  # Draw at least 2 points
            point_x = random.randint(50, map_width - 50)
            point_y = random.randint(50, map_height - 50)
            print(f"Drawing point at: ({point_x}, {point_y})")
            ActionChains(self.driver).move_to_element_with_offset(map_section, point_x - map_width / 2,
                                                                  point_y - map_height / 2).click().perform()
            time.sleep(1)  # Add a short delay between clicks

        print("Points drawn on the map.")

    def draw_line(self):
        # Click on the line drawing icon
        line_element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-of-type(4) > img[alt='icons']"))
        )
        line_element.click()
        time.sleep(5)

        # Assuming you need to click on the map section with specific coordinates
        map_section = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div#imageMap"))
        )

        # Get the dimensions of the map section
        map_width = map_section.size['width']
        map_height = map_section.size['height']

        # Generate two random points within the map bounds
        start_x = random.randint(50, map_width - 50)
        start_y = random.randint(50, map_height - 50)
        end_x = random.randint(50, map_width - 50)
        end_y = random.randint(50, map_height - 50)

        print(f"Drawing line from ({start_x}, {start_y}) to ({end_x}, {end_y})")

        # Create an action chain to perform the clicks
        action_chain = ActionChains(self.driver)
        action_chain.move_to_element_with_offset(map_section, start_x - map_width / 2,
                                                 start_y - map_height / 2).click().perform()
        time.sleep(1)  # Add a short delay between clicks
        action_chain.move_to_element_with_offset(map_section, end_x - map_width / 2,
                                                 end_y - map_height / 2).click().perform()
        time.sleep(1)  # Add a short delay between clicks

        # Double click at the end point to finalize the line
        action_chain.move_to_element_with_offset(map_section, end_x - map_width / 2,
                                                 end_y - map_height / 2).double_click().perform()

        print("Line drawn on the map.")

    def add_comment(self, map_section, x, y):
        random_comment = self.generate_random_comment()

        # Click on the comment icon to enable comment mode
        comment_icon = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-of-type(8) > img[alt='icons']"))
        )
        comment_icon.click()
        time.sleep(5)

        # Click on the map at the specified coordinates to place the comment
        ActionChains(self.driver).move_to_element_with_offset(
            map_section, x - map_section.size['width'] / 2, y - map_section.size['height'] / 2
        ).click().perform()
        time.sleep(1)

        # After clicking on the map to place the comment, input the comment text
        ActionChains(self.driver).send_keys(random_comment).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.RETURN).perform()
        time.sleep(2)

        print(f"Comment added at ({x}, {y}): {random_comment}")

    def generate_random_comment(self):
        # Generate a random meaningful comment
        words = ["Map", "annotation", "feature", "example", "comment"]
        comment = ' '.join(random.choice(words) for _ in range(5))
        return comment

    def draw_triangle(self, map_section, center_x, center_y, map_width, map_height):
        # Define the positions for each vertex of the triangle around the center
        positions = [
            (0, -50),  # Top vertex relative to the center
            (-43, 25),  # Bottom-left vertex relative to the center
            (43, 25),  # Bottom-right vertex relative to the center
            (0, -50)  # Top vertex relative to the center (same as starting point to close the polygon)
        ]

        print(f"Triangle vertices relative to center: {positions}")

        # Create an action chain to perform the clicks
        action_chain = ActionChains(self.driver)

        for position in positions:
            target_x = center_x + position[0]
            target_y = center_y + position[1]
            if 0 <= target_x <= map_width and 0 <= target_y <= map_height:
                action_chain.move_to_element_with_offset(map_section, target_x - map_width / 2,
                                                         target_y - map_height / 2).click().perform()
                print(f"Clicked at: ({target_x}, {target_y})")
            else:
                print(f"Skipping out-of-bounds click at: ({target_x}, {target_y})")
            time.sleep(1)  # Add a short delay between clicks

        print("Triangle drawn on the map.")

    def draw_rectangle(self, map_section, center_x, center_y, map_width, map_height):
        # Define the positions for each vertex of the rectangle around the center
        positions = [
            (-50, -25),  # Top-left vertex relative to the center
            (50, -25),  # Top-right vertex relative to the center
            (50, 25),  # Bottom-right vertex relative to the center
            (-50, 25),  # Bottom-left vertex relative to the center
            (-50, -25)  # Top-left vertex relative to the center (same as starting point to close the polygon)
        ]

        print(f"Rectangle vertices relative to center: {positions}")

        # Create an action chain to perform the clicks
        action_chain = ActionChains(self.driver)

        for position in positions:
            target_x = center_x + position[0]
            target_y = center_y + position[1]
            if 0 <= target_x <= map_width and 0 <= target_y <= map_height:
                action_chain.move_to_element_with_offset(map_section, target_x - map_width / 2,
                                                         target_y - map_height / 2).click().perform()
                print(f"Clicked at: ({target_x}, {target_y})")
            else:
                print(f"Skipping out-of-bounds click at: ({target_x}, {target_y})")
            time.sleep(1)  # Add a short delay between clicks

        print("Rectangle drawn on the map.")

    # def upload_files(self, file_paths):
    #     try:
    #         print("Waiting for upload file button to be clickable")
    #         add_drone_data = WebDriverWait(self.driver, 20).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, "div:nth-of-type(7) > img[alt='icons']"))
    #         )
    #         add_drone_data.click()
    #
    #         upload_drone_data = WebDriverWait(self.driver, 20).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='menu'] > div:nth-of-type(1)"))
    #         )
    #         upload_drone_data.click()
    #
    #         browse_files = WebDriverWait(self.driver, 20).until(
    #             EC.element_to_be_clickable(
    #                 (By.CSS_SELECTOR, ".\!naxatw-font-medium.naxatw-mt-\[0\.44rem\].naxatw-text-sm > a:nth-of-type(1)"))
    #         )
    #         browse_files.send_keys(file_paths)
    #
    #         print("Files uploaded successfully")
    #
    #     except TimeoutException:
    #         print("Timeout: Upload button not clickable.")
    #     except NoSuchElementException:
    #         print("Element not found: Upload button.")
    #     except Exception as e:
    #         print("Error uploading files:", e)

    def upload_existing_data(self):
        try:
            add_drone_data = self.driver.find_element(By.CSS_SELECTOR, "div:nth-of-type(7) > img[alt='icons']")
            add_drone_data.click()
            time.sleep(5)

            upload_existing_data = self.driver.find_element(By.CSS_SELECTOR, "div[role='menu'] > div:nth-of-type(2)")
            upload_existing_data.click()
            time.sleep(10)

            select_data = self.driver.find_element(By.CSS_SELECTOR,
                                                   ".naxatw-pr-\[0\.4375rem\].projects > div:nth-of-type(1)")
            select_data.click()
            time.sleep(5)

            add_to_project = self.driver.find_element(By.CSS_SELECTOR,
                                                      "[class='\!naxatw-w-\[8\.313rem\] naxatw-bg-primary naxatw-text-white naxatw-flex naxatw-w-full md\:naxatw-w-\[17\.25rem\] naxatw-h-\[2\.25rem\] naxatw-rounded-\[2rem\] naxatw-justify-center naxatw-items-center naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-font-semibold naxatw-text-sm']")
            add_to_project.click()
            time.sleep(5)

        except Exception as e:
            print("Error uploading files:", e)

    # def edit_project_name(self):
    #     try:
    #         # Locate the default project name field
    #         select_edit_name = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ellipsis")))
    #
    #         action_chain = ActionChains(self.driver)
    #         action_chain.double_click(select_edit_name).perform()  # Double click to select all text
    #         # select_edit_name.clear()
    #         self.driver.execute_script("arguments[0].innerHTML = '';", select_edit_name)
    #         # Generate and input the new project name
    #         new_project_name = self.generate_random_project_name()
    #         select_edit_name.send_keys(new_project_name)
    #         select_edit_name.send_keys(Keys.RETURN)
    #
    #         print(f"Project name changed to: {new_project_name}")
    #
    #     except Exception as e:
    #         print(f"Failed to edit project name: {e}")
    #
    # def generate_random_project_name(self):
    #     # Generate a random project name starting with "test_"
    #     adjectives = ["Dynamic", "Innovative", "Creative", "Strategic", "Efficient"]
    #     nouns = ["Mapping", "Project", "Initiative", "Exploration", "Plan"]
    #     project_name = f"test_{random.choice(adjectives)}_{random.choice(nouns)}"
    #     return project_name

    def zoomIn(self):
        zoomIn_Icon = self.driver.find_element(By.CSS_SELECTOR,
                                               "[tooltip='Zoom in    \+'] [width]")
        zoomIn_Icon.click()
        time.sleep(10)

    def zoomOut(self):
        zoomOut_Icon = self.driver.find_element(By.CSS_SELECTOR,
                                                "[tooltip='Zoom out    -'] [width]")
        # zoomOut_Icon.click()
        action_chain = ActionChains(self.driver)
        action_chain.double_click(zoomOut_Icon).perform()
        time.sleep(10)

    def zoomtoLayer(self):
        zoomtoLayer_Icon = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[tooltip='Zoom to all layers    Z'] [width]")
        zoomtoLayer_Icon.click()
        time.sleep(10)

    def zoomMyLocation(self):
        zoomMyLocation_Icon = self.driver.find_element(By.CSS_SELECTOR,
                                                       "[tooltip = 'Zoom to my location'] [width]")
        zoomMyLocation_Icon.click()
        time.sleep(10)

    def select_layer(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[tooltip='Choose map layer'] [width]"))
            ).click()
            time.sleep(5)
        except Exception as e:
            print("Error selecting layer:", e)

    def select_satellite_view(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "img[alt='orthomosaic']"))
            ).click()
        except Exception as e:
            print("Error selecting satellite view:", e)

    def select_map_view(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "img[alt='dsm']"))
            ).click()
        except Exception as e:
            print("Error selecting map view:", e)

    def share_project(self, role="can view"):
        try:
            receiver_email = self.generate_random_email()
            share_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            ".\\!naxatw-h-9.\\!naxatw-w-fit.naxatw-bg-primary.naxatw-rounded-\\[2rem\\] > .naxatw-font-\\[600\\].naxatw-font-archivo.naxatw-px-\\[1\\.6rem\\].naxatw-py-\\[0\\.25rem\\].naxatw-text-\\[0\\.875rem\\].naxatw-text-white"))
            )
            share_btn.click()
            time.sleep(5)

            invitee_email = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".edit-email-wrapper > input"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", invitee_email)
            time.sleep(1)  # Short delay to ensure the element is in view

            invitee_email.click()
            time.sleep(3)
            invitee_email.send_keys(receiver_email)
            invitee_email.send_keys(Keys.ENTER)
            time.sleep(3)

            invite_in_project = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".invite-button-container [type]"))
            )
            invite_in_project.click()
            time.sleep(5)

            # Close the modal
            close_icon = self.driver.find_element(By.CSS_SELECTOR, ".filter-close-icon > svg")
            # Scroll to the close icon
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_icon)
            time.sleep(1)  # Short delay to ensure the element is in view

            # Click on the close icon
            self.click_element_with_retry(close_icon)

            print("------------------")

            # Select management section and verify the invited email
            self.select_management(receiver_email)

        except Exception as e:
            print("Error sharing project:", e)

    def click_element_with_retry(self, element):
        try:
            # Attempt to click on the element
            element.click()
        except Exception:
            # If click fails, try scrolling into view again and clicking
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)
            element.click()

    # def generate_random_email(self, domain="maildrop.cc"):
    #     names = ["ram", "john", "mike", "sara", "lisa", "peter", "jane"]
    #     random_name = random.choice(names)
    #     return f"{random_name}@{domain}"

    def generate_random_email(self, domain="maildrop.cc"):
        name_length = random.randint(3, 7)  # Random length for the name part
        letters = string.ascii_lowercase
        random_name = ''.join(random.choice(letters) for i in range(name_length))
        return f"{random_name}@{domain}"


# Replace the following with your actual credentials
tester = WebsiteTester("https://staging.geonadir.com/myprojects?login=sign-in")
tester.test_signup("kishankc949@gmail.com", "kishankc949@gmail.com", "gvbk tlcy sbtb zzrj")
tester.select_workspace("KI")  # Replace with the actual workspace name or identifier

tester.select_project()
tester.select_card()
tester.zoomIn()
tester.zoomOut()
tester.zoomtoLayer()
tester.zoomMyLocation()
tester.select_layer()
tester.select_satellite_view()
tester.zoomIn()  # Call zoomIn after selecting satellite view
time.sleep(15)
tester.select_layer()
tester.select_map_view()
tester.zoomOut()

time.sleep(10)
tester.close_browser()
