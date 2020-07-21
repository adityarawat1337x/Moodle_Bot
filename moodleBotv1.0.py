from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expCon
import warnings
from bs4 import BeautifulSoup
from os import system

loginPage = "http://45.116.207.203/moodle/login/index.php"  # put your moodle link

loginData = ["username", "password"]  # put username and password

subjects = []

options = Options()
options.add_argument('--headless')

# waits 100 sec before throwing error


def driverWait(driver, timeout, element, elementValue, login=0):
    try:
        WebDriverWait(driver, timeout).until(
            expCon.presence_of_all_elements_located((element, elementValue)))
    except:
        if login:
            print("\n\x1b[1;30;41m #LOGIN FAILED \x1b[0m")
            print("\x1b[1;30;41m #WRONG CREDENTIALS \x1b[0m")
        else:
            print(f"\n\x1b[1;30;41m #TIME-OUT \x1b[0m")
        driver.quit()
        exit(0)


if __name__ == "__main__":
    # initializing driver
    driver = webdriver.Firefox(
        executable_path="D:\\NAPSTER_LABS\\PROJECTS\\PYTHON\\geckodriver.exe", options=options)  # path of geckodriver
    # For browser tab visible
    # driver = webdriver.Firefox(
    #     executable_path="D:\\NAPSTER_LABS\\PROJECTS\\PYTHON\\geckodriver.exe")
    # For chrome users
    # driver = webdriver.Chrome(
    #     executable_path="D:\\NAPSTER_LABS\\PROJECTS\\PYTHON\\chromedriver.exe, options=options")

    system('cls||clear')
    print(
        "\n\t\t\t\t\t\x1b[1;36;40m SCRIPT BY Napster/taurus@KEVIN \x1b[0m\n")
    print(
        "\t\t\t\t\t\t\x1b[1;30;47m Moodle_Bot v1.0 \x1b[0m\n\n")

    # dont touch this
    # dont touch this
    # dont touch this

    try:
        driver.get(
            "https://docs.google.com/document/d/e/2PACX-1vQxoob071VXFMBUUM_9N3FpnfNwp_rFiYcgNJHt_x8ad8ySV17TdoFZWfuMiOC8NNcYkrekgQOeA21s/pub")

        for each in driver.find_elements_by_tag_name('span'):
            each = str(each.get_attribute("innerHTML")).replace("&nbsp;", "")
            if "Published" not in each and "Updated automatically" not in each:
                print(f"\x1b[1;32;40m{each}\x1b[0m")
    # dont touch this
    # dont touch this
    # dont touch this

    except:
        pass
    try:
        driver.get(loginPage)
        print("\n\n\x1b[1;30;46m #LOGGING IN \x1b[0m")
    except TimeoutException as e:
        print("\n\x1b[1;30;41m #LOGIN FAILED \x1b[0m")
    except:
        print("\n\x1b[1;30;41m #TIME-OUT \x1b[0m")
        driver.quit()
        exit(0)

    driver.find_element_by_id("username").send_keys(loginData[0])
    driver.find_element_by_id("password").send_keys(loginData[1])
    driver.find_element_by_id("loginbtn").click()

    driverWait(driver, 100, By.CLASS_NAME, "progress-bar", 1)
    print("\n\x1b[1;30;42m #LOGIN SUCCESSFUL \x1b[0m")

    # dashboard
    for each in driver.find_elements_by_class_name("dashboard-card"):
        links, name, progress, subId = '', '', '', ''
        try:
            links = str(each.find_element_by_tag_name(
                "a").get_attribute("href"))
            name = str(each.find_element_by_class_name(
                "multiline").get_attribute("innerHTML")).replace("\n", "").replace("  ", "")
            progress = str(each.find_element_by_tag_name(
                "strong").get_attribute("innerHTML"))
            subId = re.search('id=(.*)', links).group(1)
        except:
            pass
        if name and [links, name, progress] not in subjects:
            subjects.append([links, name, progress, subId])

    # printing attendance
    print(f"\n\x1b[1;30;44m #SUBJECTS \x1b[0m")
    print(f"\x1b[2;34;40m {'_'*60} \x1b[0m\n")
    for each in subjects:
        print(
            f"\x1b[1;34;40m{each[1]}  \x1b[0m \x1b[1;32;40m{each[2]}%\x1b[0m")
    print(f"\x1b[2;34;40m {'_'*60} \x1b[0m\n")

    # upcoming events
    print(f"\n\x1b[1;30;44m #UPCOMING EVENTS \x1b[0m\n")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for each in soup.findAll('div', class_="event"):
        event = ''
        Id = re.search('course=(.*?)&', str(each.find('a')["href"])).group(1)
        for every in subjects:
            if every[3] == Id:
                event = every[1] + ': '
                break
        event += str(each.find('a').text)
        event += each.find('div').text
        print(f'\x1b[1;33;40m{event}\x1b[0m')

    # attendance maker
    trigger = 0
    for each in subjects:
        driver.get(each[0])
        driverWait(driver, 100, By.CLASS_NAME, "btn-link")
        # finding unchecked assignment
        print(f'\n\x1b[1;34;47m{subjects[trigger][1]}\x1b[0m\n')
        # loop for all checkbox
        for each in driver.find_elements_by_class_name("btn-link"):
            driverWait(driver, 100, By.CLASS_NAME, "btn-link")
            task = str(each.find_element_by_class_name(
                "icon").get_attribute("title"))
            if "Completed" in task:
                print(f"  \x1b[0;36;40m>>{task} \x1b[0m")
            elif "Not completed" in task:
                # clicking checkboxes
                print(f"  \x1b[1;31;40m>>{task} \x1b[0m")
                each.find_element_by_class_name("icon").click()
                time.sleep(3)
                print(f"\x1b[1;32;40m    >>Completed \x1b[0m")
        trigger += 1

    print(
        "\n\x1b[1;30;47m Feedback form: https://forms.gle/bFq1ncrs4k5LiXFi6 \x1b[0m")
    print(
        "\n\x1b[1;30;47m Announcements: https://docs.google.com/document/d/e/2PACX-1vQxoob071VXFMBUUM_9N3FpnfNwp_rFiYcgNJHt_x8ad8ySV17TdoFZWfuMiOC8NNcYkrekgQOeA21s/pub\x1b[0m")

    driver.quit()
