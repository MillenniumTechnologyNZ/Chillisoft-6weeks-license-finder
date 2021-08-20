# This is a sample Python script.
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import secrets

myUrl = "https://miltech.repairshopr.com/invoices"


def run():
    test()


def test():
    browser = setup()
    number = pyautogui.prompt("Click OK if you have copied the number to clipboard")
    while number is not None or number != "":
        values = main_run(browser, number)
        number = enter_values(values)


def enter_values(values):
    pyautogui.click()
    val1 = values[0]
    val2 = values[1]
    pyautogui.typewrite(val2)
    pyautogui.press('enter')
    pyautogui.move(150, 0)
    pyautogui.click()
    pyautogui.typewrite(val1)
    pyautogui.move(-225, 20)
    pyautogui.doubleClick()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.press('enter')
    pyautogui.move(75, 0)
    pyautogui.sleep(0.5)
    return pyperclip.paste()


def setup():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    #
    browser = webdriver.Chrome('chromedriver.exe', options=option)
    return browser


def main_run(browser, number):
    browser.get(myUrl)
    is_logged_in(browser)
    try:
        search_num(browser, number)
    except:
        return ["N/A", "N/A"]
    return get_info(browser)


def is_logged_in(browser):
    try:
        browser.find_element_by_id("user_email")
        login(browser)
    except:
        return


def search_num(browser, number):
    search_box = browser.find_element_by_id("search_common")
    search_box.click()
    print(number)
    search_box.send_keys(number)
    search_box.submit()
    my_elem = WebDriverWait(browser, 3).until(EC.presence_of_element_located(
        (By.XPATH, "//*[text()=\'" + number + "\']")))
    my_elem.click()
    print("Opening invoice")


def get_info(browser):
    try:
        mobile = browser.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[6]/td/a").get_attribute('text')
        print(mobile)
    except:
        try:
            mobile = browser.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div/div/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[6]/td/a").get_attribute(
                'text')
            print(mobile)
        except:
            mobile = "N/A"
    try:
        name = browser.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/span/a")\
            .get_attribute('text')

        print(name)
        if name == "(empty)":
            name = browser.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td/span")\
                .get_attribute('innerHTML').strip()
            print(name)
            print("Name is (empty)")
            # get business name if name is empty
    except:
        try:
            name = browser.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div/div/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/span/a") \
                .get_attribute('text')

            print(name)
            if name == "(empty)":
                name = browser.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/div/div/div[4]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td/span") \
                    .get_attribute('innerHTML').strip()
                print(name)
                print("Name is (empty)")
        except:
            try:
                mobile = browser.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[5]/td/a")\
                    .get_attribute('innerHTML').strip()
                print(mobile)
                name = browser.find_element_by_xpath(
                    "/html/body/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td/span/a")\
                    .get_attribute('text')
                print(name)
            except:
                name = "N/A"

    print("sending info")
    return [mobile, name]


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
    print("Signed in")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
