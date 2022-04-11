import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from config import UPLOAD_DIR, BASE_DIR


class WebDriver:

    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')

        self.driver = webdriver.Firefox(options=options, executable_path=f'{BASE_DIR}/geckodriver')
        self.driver.maximize_window()

    def make_screen(self, url, filename):
        self.driver.get(url)
        self.driver.save_screenshot(os.path.join(UPLOAD_DIR, filename))

    def close(self):
        self.driver.close()

