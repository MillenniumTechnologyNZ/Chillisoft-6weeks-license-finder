# This is a sample Python script.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import secrets
import pyautogui
import numpy

myUrl = "https://miltech.repairshopr.com/invoices"
path = "C:\\Users\tree_\\Downloads\\chromedriver_win32\\chromedriver.exe"


def pyrun():
    number = pyautogui.prompt("Click OK if you have copied the number to clipboard")
    setup(number)


def setup(number):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome('chromedriver.exe', options=option)
    type(browser)
    browser.get(myUrl)
    login(browser)
    search_num(browser, number)
    get_info(browser)


def search_num(browser, number):
    search_box = browser.find_element_by_id("search_common")
    search_box.click()
    print(number)
    search_box.send_keys(number)
    search_box.submit()
    my_elem = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
        (By.XPATH, "//*[text()=\'" + number + "\']")))
    my_elem.click()
    pyautogui.alert("Open invoice")


def get_info(browser):
    mobile = browser.find_element_by_xpath(
        "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[6]/td/a")
    print(mobile.get_attribute('text'))
    name = browser.find_element_by_xpath(
        "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/span/a")
    print(name.get_attribute('text'))

def login(browser):
    if browser.find_element_by_id("user_email"):
        item = browser.find_element_by_id("user_email")
        item.click()
        item.send_keys(secrets.username)

    if browser.find_element_by_id("user_password"):
        item = browser.find_element_by_id("user_password")
        item.click()
        item.send_keys(secrets.password)
        submit_btn = browser.find_element_by_name("commit")
        submit_btn.click()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pyrun()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
