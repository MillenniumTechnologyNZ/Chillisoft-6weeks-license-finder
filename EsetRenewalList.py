# This is a sample Python script.
import bs4
import pyautogui
from openpyxl import Workbook
from selenium import webdriver

import secrets
file_location = "Esetcustomers.xlsx"
chillisoft_prefix = "https://secure.chillisoft.net"
login_url = "https://secure.chillisoft.net/login/"
postVerifiedUrl = "https://secure.chillisoft.net/ssl/extranet/index.cfm/licence-filter/1/due-to-expire-in-next-6-weeks/"


def run():
    operation()


def operation():
    browser = setup()
    pyautogui.confirm("Click OK to proceed")
    persons = get_profiles(browser)
    wb = Workbook()
    # Sets up the Excel spreadsheet
    sheets = wb.sheetnames
    sheet = wb[sheets[0]]
    sheet.title = "Nod32"
    wb.create_sheet("IntSec&Smart")
    wb.create_sheet("Multi")
    wb.create_sheet("CyberSecMac")
    wb.create_sheet("Other")
    # ----
    get_info(browser, wb, persons)
    wb.save(file_location)


def setup():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # , options=option
    browser = webdriver.Chrome('chromedriver.exe', options=option)
    return browser


def get_profiles(browser):
    browser.get(login_url)
    is_logged_in(browser)
    browser.get(postVerifiedUrl)
    soup = bs4.BeautifulSoup(browser.page_source, 'lxml')
    persons = []
    for links in soup.select("#jax > div.uk-hidden-small > table > tbody > tr > td:nth-child(7) > a"):
        persons.append(links.get('href'))
    return persons
    # Search
    # return get_info(browser)


def is_logged_in(browser):
    try:
        browser.find_element_by_id("LoginName")
        login(browser)
    finally:
        return


def get_info(browser, wb, persons):
    print("Getting info")
    nod32_count, int_sec_count, multi_count, mac_count, other_count = 0, 0, 0, 0, 0
    for index, person in enumerate(persons):
        browser.get(chillisoft_prefix + person)
        profile_html_parse = bs4.BeautifulSoup(browser.page_source, 'lxml')
        license_type = profile_html_parse.select("div > div.uk-width-7-10")[0].get_text()
        if license_type == "ESET NOD32 Antivirus":
            add_to_sheet(wb["Nod32"], index, profile_html_parse, nod32_count)
            nod32_count += 1
        elif license_type == "ESET Internet Security" \
                or license_type == "ESET Smart Security":
            add_to_sheet(wb["IntSec&Smart"], index, profile_html_parse, int_sec_count)
            int_sec_count += 1
        elif license_type == "ESET Multi-Device Security 5-Pack":
            add_to_sheet(wb["Multi"], index, profile_html_parse, multi_count)
            multi_count += 1
        elif license_type == "ESET Cyber Security for Mac":
            add_to_sheet(wb["CyberSecMac"], index, profile_html_parse, mac_count)
            mac_count += 1
        else:
            add_to_sheet(wb["Other"], index, profile_html_parse, other_count)
            other_count += 1


def add_to_sheet(sheet, index, soup, offset):
    sheet['A' + str(1 + offset)] = soup.select("#licenceeTab > div > div:nth-child(3)")[0].get_text()
    sheet['B' + str(1 + offset)] = soup.select("#licenceeTab > div > div:nth-child(5)")[0].get_text()
    print("Added customer: " + str(index) + " | " + str(sheet['A' + str(1 + offset)].value) + " " +
          str(sheet['B' + str(1 + offset)].value))


def login(browser):
    login_id = "LoginName"
    password_id = "Password"
    submit_id = "sendbutton2"
    if browser.find_element_by_id(login_id):
        item = browser.find_element_by_id(login_id)
        item.click()
        item.clear()
        item.send_keys(secrets.username)

    if browser.find_element_by_id(password_id):
        item = browser.find_element_by_id(password_id)
        item.click()
        item.clear()
        item.send_keys(secrets.password)
        submit_btn = browser.find_element_by_name(submit_id)
        submit_btn.click()
    print("Signed in")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
