import re
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class SignIn:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def generate_random_email(self):
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{random_string}@maildrop.cc"

    def test_signup(self, email_address):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys(email_address)
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        time.sleep(5)

        verification_code = self.fetch_verification_code_from_maildrop(email_address)
        if verification_code:
            self.enter_verification_code(verification_code)
        else:
            print("Verification code not found.")
            return

    def close_browser(self):
        self.driver.quit()

    def fetch_verification_code_from_maildrop(self, email_address):
        try:
            email_prefix = email_address.split('@')[0]
            inbox_url = f"https://maildrop.cc/inbox/?mailbox={email_prefix}"

            # Open Maildrop in a new tab
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(inbox_url)
            time.sleep(5)  # Wait for the page to load

            for attempt in range(2):  # Search for email up to 2 times
                try:
                    self.driver.refresh()  # Refresh the Maildrop page
                    time.sleep(5)  # Wait for the page to reload

                    email_list = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".message"))
                    )
                    if email_list:
                        latest_email = email_list[0]
                        latest_email.click()
                        time.sleep(5)  # Wait for the email content to load

                        try:
                            otp_element = WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[class] div:nth-of-type(1) .truncate:nth-of-type(3)"))
                            )
                            otp_text = otp_element.text
                            print(f"OTP text found: {otp_text}")
                            verification_code = self.extract_verification_code(otp_text)
                            if verification_code:
                                return verification_code
                            else:
                                print(f"No OTP found in email content: {otp_text}")
                        except NoSuchElementException:
                            print("OTP element not found in the email.")
                        except Exception as e:
                            print(f"Error locating OTP element: {e}")

                    print(f"No verification email found, retrying... (Attempt {attempt + 1})")
                except Exception as e:
                    print(f"Error while fetching email: {e}")
                    time.sleep(5)
        except Exception as e:
            print(f"Error fetching verification code: {e}")
        finally:
            # Close Maildrop tab and switch back to the GeoNadir tab
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        return None

    def extract_verification_code(self, text):
        print(f"Email content: {text}")
        verification_code = re.search(r'\b\d{6}\b', text)
        if verification_code:
            print(f"Verification code found: {verification_code.group()}")
            return verification_code.group()
        return None

    def enter_verification_code(self, verification_code):
        print(f"Entering verification code: {verification_code}")
        for i, digit in enumerate(verification_code):
            try:
                verification_field = self.driver.find_element(By.CSS_SELECTOR,
                                                              f"[class] [type='text']:nth-of-type({i + 1})")
                verification_field.send_keys(digit)
                print(f"Entered digit '{digit}' into field {i + 1}")
                time.sleep(1)  # Add delay between entering each digit
            except Exception as e:
                print(f"Error entering digit '{digit}' into field {i + 1}: {e}")
        print("Verification code entered successfully.")

    def test_empty_email(self):
        self.driver.get(self.url)
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        print("Tested empty email field")

    def test_whitespace_email(self):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys("   ")
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        print("Tested whitespace email field")

    def test_invalid_email(self):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys("abc@")
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        print("Tested invalid email format")

    def test_incorrect_verification_code(self, email_address):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys(email_address)
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        time.sleep(5)  # Wait for the page to load and email to be sent

        # Simulate entering a random verification code
        random_code = "467811"
        self.enter_verification_code(random_code)
        time.sleep(1)
        print("Tested incorrect verification code")

    def run_test(self):
        try:
            self.test_empty_email()
            self.test_whitespace_email()
            self.test_invalid_email()

            email_address = self.generate_random_email()
            print(f"Generated email address: {email_address}")
            self.test_incorrect_verification_code(email_address)
            self.test_signup(email_address)
            time.sleep(5)
        finally:
            self.close_browser()


if __name__ == "__main__":
    url = "https://staging.geonadir.com/myprojects?login=sign-in"
    tester = SignIn(url)
    tester.run_test()
