# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import hand_detector as hd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


class Controller(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("http://localhost:4200")

    def stepBackInBrowserForm(self):
        back_button = self.driver.find_element(By.ID, "back_button")
        if back_button:
            back_button.click()
        pass

    def submitFormInputs(self):
        submit_button = self.driver.find_element(By.ID, "submit_button")
        if submit_button:
            submit_button.click()
        pass

    def stepForwardInBrowserForm(self):
        back_button = self.driver.find_element(By.ID, "next_button")
        if back_button:
            back_button.click()
        pass

    def clearBrowserFormInputs(self):
        clear_button = self.driver.find_element(By.ID, "clear_button")
        if clear_button:
            clear_button.click()
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    controller = Controller()
    hd.startDetection(controller)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
