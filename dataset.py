import os
import re
import time
import pyautogui
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from signin import Signin


class DatasetUpload:

    def __init__(self, url):
        self.url = url
        self.signin = Signin(self.url)

    def login(self):
        self.signin.test_valid_login("tilak.naxa@gmail.com", "tilak.naxa@gmail.com", "grqn anvl awnf lnwc")
        self.driver = self.signin.driver  # Use the same driver instance
        time.sleep(2)  # Wait for the page to fully load

    def select_workspace(self, workspace):
        workspace_element = self.driver.find_element(By.CSS_SELECTOR, "[class*='naxatw-text-[#FAFAFB]']")
        workspace_element.click()
        print(f"Workspace '{workspace}' selected.")

    def select_dataset(self):
        dataset_element = self.driver.find_element(By.CSS_SELECTOR,
                                                   "a:nth-of-type(2) .naxatw-font-semibold:first-of-type")
        dataset_element.click()
        time.sleep(5)

    def explore_fair_geo(self):
        try:
            explore_fairGeo = self.driver.find_element(By.CSS_SELECTOR,
                                                       "[class='sidebar-btn clear-btn naxatw-z-10'] [type]")
            explore_fairGeo.click()
            time.sleep(5)

            select_data = self.driver.find_element(By.CSS_SELECTOR, "[href='\/image-collection-details\/4541']")
            select_data.click()
            time.sleep(5)

            add_to_project = self.driver.find_element(By.CSS_SELECTOR,
                                                      ".add-to-project-button")
            add_to_project.click()
            time.sleep(4)
            click_checkbox = self.driver.find_element(By.CSS_SELECTOR, ".input__search__on__map__move")
            click_checkbox.click()
            time.sleep(5)
            add_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-primary.naxatw-bg-primary")
            add_button.click()
            time.sleep(5)

        except Exception as e:
            print("Error uploading files:", e)

    def upload_dataset(self, folder_path):

        try:
            # Back to the dataset page'
            # self.driver.back()
            # time.sleep(2)
            # self.driver.back()
            # time.sleep(5)
            # Locate the file input element
            file_input = self.driver.find_element(By.CSS_SELECTOR,
                                                  ".header button > div")
            file_input.click()
            time.sleep(8)

            print(f"Typing the full path: {folder_path}")
            pyautogui.write(folder_path, interval=0.08)  # Slow down typing to ensure the full path is written
            time.sleep(10)

            pyautogui.press('enter')
            time.sleep(5)

            pyautogui.hotkey('command', 'a')
            time.sleep(4)

            pyautogui.press('enter')
            time.sleep(5)

            #alert box handled
            pyautogui.press('enter')
            time.sleep(5)

            continue_upload = self.driver.find_element(By.CSS_SELECTOR,
                                                       "[class='naxatw-bg-\[\#00ACBB\] naxatw-text-\[\#FFF\] naxatw-flex naxatw-w-full md\:naxatw-w-\[17\.25rem\] naxatw-h-\[2\.25rem\] naxatw-rounded-\[2rem\] naxatw-justify-center naxatw-items-center naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-font-semibold naxatw-text-sm']")
            continue_upload.click()
            time.sleep(5)

            checkbox_for_fairGeo_share = self.driver.find_element(By.CSS_SELECTOR,
                                                                  "[class='naxatw-cursor-pointer naxatw-flex-1 naxatw-mt-\[0\.5rem\] md\:naxatw-w-full naxatw-flex naxatw-items-center naxatw-gap-\[0\.5rem\]'] svg")
            checkbox_for_fairGeo_share.click()
            time.sleep(2)

            final_upload = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[class='naxatw-w-\[8\.3125rem\] naxatw-h-\[2\.25rem\] naxatw-items-center naxatw-justify-center naxatw-rounded-\[2rem\] naxatw-flex naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-bg-\[\#00ACBB\] naxatw-text-\[\#FFFFFF\] naxatw-text-\[0\.875rem\] naxatw-font-semibold']")
            final_upload.click()
            time.sleep(100)

            done_button = self.driver.find_element(By.CSS_SELECTOR,
                                                   "[class='naxatw-w-\[8\.3125rem\] naxatw-h-\[2\.25rem\] naxatw-items-center naxatw-justify-center naxatw-rounded-\[2rem\] naxatw-flex naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-border naxatw-border-primary naxatw-text-\[0\.875rem\] naxatw-text-white naxatw-bg-primary naxatw-font-semibold']")
            done_button.click()

            self.driver.execute_script("location.reload(true);")
            time.sleep(5)

            print("Dataset uploaded successfully.")

        except Exception as e:
            print(f"Error uploading dataset: {e}")

    def perform_upload(self, image_path):
        pyautogui.write(image_path, interval=0.05)  # Slow down typing to ensure the full path is written
        time.sleep(10)

        pyautogui.press('enter')
        time.sleep(5)

        pyautogui.press('enter')
        time.sleep(5)

        checkbox_for_fairGeo_share = self.driver.find_element(By.CSS_SELECTOR,
                                                              "[class='naxatw-cursor-pointer naxatw-flex-1 naxatw-mt-\[0\.5rem\] md\:naxatw-w-full naxatw-flex naxatw-items-center naxatw-gap-\[0\.5rem\]'] svg")
        checkbox_for_fairGeo_share.click()
        time.sleep(2)

        final_upload = self.driver.find_element(By.CSS_SELECTOR,
                                                "[class='naxatw-w-\[8\.3125rem\] naxatw-h-\[2\.25rem\] naxatw-items-center naxatw-justify-center naxatw-rounded-\[2rem\] naxatw-flex naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-bg-\[\#00ACBB\] naxatw-text-\[\#FFFFFF\] naxatw-text-\[0\.875rem\] naxatw-font-semibold']")
        final_upload.click()
        time.sleep(50)

        done_button = self.driver.find_element(By.CSS_SELECTOR,
                                               "[class='naxatw-w-\[8\.3125rem\] naxatw-h-\[2\.25rem\] naxatw-items-center naxatw-justify-center naxatw-rounded-\[2rem\] naxatw-flex naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-border naxatw-border-primary naxatw-text-\[0\.875rem\] naxatw-text-white naxatw-bg-primary naxatw-font-semibold']")
        done_button.click()

        self.driver.execute_script("location.reload(true);")
        time.sleep(5)

        print("Dataset uploaded successfully.")

    def upload_dataset_photos(self, image_path):
        try:
            # Check if the dataset_card is present
            dataset_card = self.driver.find_element(By.CSS_SELECTOR, "[href='\/image-collection-details\/4573']")
            time.sleep(3)

            if dataset_card:
                time.sleep(3)
                try:
                    # Proceed to find the browse_file element if dataset_card is found
                    browse_file = self.driver.find_element(By.CSS_SELECTOR,
                                                           ".sidebar-text .naxatw-text-center [class='\!naxatw-underline \!naxatw-decoration-1 naxatw-underline-offset-\[0\.175rem\]']:nth-of-type(1)")
                    browse_file.click()
                    time.sleep(5)

                    # Call the perform_upload method to upload the image
                    self.perform_upload(image_path)

                except NoSuchElementException:
                    print("browse_file element not found.")
            else:
                # If dataset_card is not found, proceed with an alternate path
                upload_photos = self.driver.find_element(By.CSS_SELECTOR, ".sidebar-text a")
                upload_photos.click()
                time.sleep(5)

                self.perform_upload(image_path)

        except NoSuchElementException:
            print("browse_file element not found.")

    def merge_dataset(self, folders_path):
        try:
            file_input = self.driver.find_element(By.CSS_SELECTOR,
                                                  ".header button > div")
            file_input.click()
            time.sleep(3)

            print(f"Typing the full path: {folders_path}")
            pyautogui.write(folders_path, interval=0.08)  # Slow down typing to ensure the full path is written
            time.sleep(5)

            pyautogui.press('enter')
            time.sleep(5)

            pyautogui.hotkey('command', 'a')
            time.sleep(4)

            pyautogui.press('enter')
            time.sleep(5)

            # alert box handled
            pyautogui.press('enter')
            time.sleep(5)

            merge_into_single_set = self.driver.find_element(By.CSS_SELECTOR, ".go-to-datasets.upload-clear-btn > img[alt='single-dataset']")
            merge_into_single_set.click()
            time.sleep(3)

            continue_upload = self.driver.find_element(By.CSS_SELECTOR,
                                                       "[class] .naxatw-w-full.naxatw-justify-center:nth-of-type(2)")
            continue_upload.click()
            time.sleep(5)

            checkbox_for_fairGeo_share = self.driver.find_element(By.CSS_SELECTOR,
                                                                  "[class='naxatw-cursor-pointer naxatw-flex-1 naxatw-mt-\[0\.5rem\] md\:naxatw-w-full naxatw-flex naxatw-items-center naxatw-gap-\[0\.5rem\]'] svg")
            checkbox_for_fairGeo_share.click()
            time.sleep(2)

            final_upload = self.driver.find_element(By.CSS_SELECTOR,
                                                    "[class='naxatw-w-\[8\.3125rem\] naxatw-h-\[2\.25rem\] naxatw-items-center naxatw-justify-center naxatw-rounded-\[2rem\] naxatw-flex naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-bg-\[\#00ACBB\] naxatw-text-\[\#FFFFFF\] naxatw-text-\[0\.875rem\] naxatw-font-semibold']")
            final_upload.click()
            time.sleep(10)

            done_button = self.driver.find_element(By.CSS_SELECTOR,
                                                   "[class='naxatw-w-\[8\.3125rem\] naxatw-h-\[2\.25rem\] naxatw-items-center naxatw-justify-center naxatw-rounded-\[2rem\] naxatw-flex naxatw-gap-\[4\.375rem\] naxatw-py-\[0\.5rem\] naxatw-px-\[1\.25rem\] naxatw-border naxatw-border-primary naxatw-text-\[0\.875rem\] naxatw-text-white naxatw-bg-primary naxatw-font-semibold']")
            done_button.click()

            self.driver.execute_script("location.reload(true);")
            time.sleep(5)

            print("Dataset uploaded successfully.")

        except Exception as e:
            print(f"Error uploading dataset: {e}")


if __name__ == "__main__":
    datasetUpload = DatasetUpload("https://staging.geonadir.com/myprojects?login=sign-in")
    datasetUpload.login()
    time.sleep(2)
    datasetUpload.select_workspace("TI")
    time.sleep(5)

    datasetUpload.select_dataset()
    time.sleep(5)
    # datasetUpload.explore_fair_geo()
    time.sleep(3)

    dataset_path = "/home/tilak/Office_Work/Selenium/Geo-Automation/upload_data/"
    dataset_image_path = "/home/tilak/Office_Work/Selenium/Geo-Automation/upload_data/shivapuri/DJI_0555.JPG"
    # datasetUpload.upload_dataset(dataset_path)
    # datasetUpload.upload_dataset_photos(dataset_image_path)
    time.sleep(5)

