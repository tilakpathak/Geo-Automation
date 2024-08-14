import re
import imaplib
import email
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Signin:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

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

        time.sleep(5)

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
        try:
            for i, digit in enumerate(verification_code):
                verification_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[class] [type='text']:nth-of-type({i + 1})"))
                )
                verification_field.send_keys(digit)
        except TimeoutException:
            print(f"Failed to find the verification code input field for digit {digit}")

    # Method to test empty email field
    def test_empty_email(self):
        self.driver.get(self.url)
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        print("Tested empty email field")

    # Method to test email field with whitespace
    def test_whitespace_email(self):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys("   ")
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        print("Tested whitespace email field")

    # Method to test invalid email format
    def test_invalid_email(self):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys("abc@")
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()
        print("Tested invalid email format")

    # Method to test correct email but incorrect verification code
    def test_incorrect_verification_code(self, email_address):
        self.driver.get(self.url)
        email_field = self.driver.find_element(By.CSS_SELECTOR, "#email")
        email_field.send_keys(email_address)
        lets_go_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Let')]")
        lets_go_button.click()

        # Simulate entering a random verification code
        random_code = "467811"
        self.enter_verification_code(random_code)
        time.sleep(1)
        print("Tested incorrect verification code")

    # Method to perform the valid login
    def test_valid_login(self, email_address, email_username, email_password):
        self.test_signup(email_address, email_username, email_password)
        print("Tested valid login")


if __name__ == "__main__":

    tester = Signin("https://staging.geonadir.com/myprojects?login=sign-in")

    # Perform invalid logins
    tester.test_empty_email()
    time.sleep(2)
    tester.test_whitespace_email()
    time.sleep(2)
    tester.test_invalid_email()
    time.sleep(2)
    tester.test_incorrect_verification_code("tilak.naxa@gmail.com")
    time.sleep(2)

    # Perform valid login
    tester.test_valid_login("tilak.naxa@gmail.com", "tilak.naxa@gmail.com", "grqn anvl awnf lnwc")

    tester.close_browser()
