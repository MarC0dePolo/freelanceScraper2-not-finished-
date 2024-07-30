import traceback
from dasOertliche import *
from extractTxtData import Data
from myTools.mySeleniumTools import Tools
from extractTxtData import Data
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

main_page = 'https://s298.goserver.host/webmail/'

# xpaths login
xpath_username = '//*[@id="rcmloginuser"]'
xpath_pw = '//*[@id="rcmloginpwd"]'
xpath_submit = '//*[@id="rcmloginsubmit"]'

# xpaths account

xpath_refresh = '//*[@id="rcmbtn112"]'
xpath_last_email = '//*[@id="rcmrowNTk"]'
xpath_email_body = '/html/body/div[1]/div[3]/div[4]/table[2]/tbody'

#messagelist > tbody:nth-child(2)
# css selector
css_sel_message_body = '#messagelist > tbody:nth-child(2)'
css_sel_last_email = '#rcmrowNTk'
css_path_last_email = ''

class Login():
    def __init__(self, driver):
        self.driver = driver
        self.Tools = Tools(self.driver)

    def login_to_email(self, email : str, pw : str) -> None:
        self.driver.execute_script("window.open('about:blank','email_tab')")
        self.driver.switch_to.window('email_tab')
        self.driver.get(main_page)
        self.Tools.inputFieldByXpath(text=email, xpath=xpath_username)
        self.Tools.inputFieldByXpath(text=pw, xpath=xpath_pw)
        self.Tools.clickElementByXpath(xpath=xpath_submit)

    def get_last_email(self) -> str:
        message_element = self.driver.find_element(By.XPATH, xpath_email_body)
        message_body = message_element.get_attribute('innerHTML')

        message_body = BeautifulSoup(message_body, 'html.parser')

        first_tr = message_body.find('tr') 
        return first_tr

    def get_date_of_email(self, email_html):
        date = self.get_last_email()
        date = date.select('span[class*="date]')[0].text
        return date

    def is_correct_email(self, date) -> bool:
        current_time = datetime.time.now()
        email_time = date.strip().split(' ')
        
        week_day_of_email = email_time[0].strip()
        time_of_email = email_time[1].strip()

        time_of_email = datetime.strptime(time_of_email, "%H:%M").time()

        if lower(week_day_of_email) == 'heute':
            if time_of_email >= current_time - timedelta(minutes=1) and time_of_email <= current_time:
                return True
        
        return False

    def verify_email(self, email, pw):
        self.login_to_email(email, pw)
        time.sleep(1)

        last_email_html = self.get_last_email()
        date_of_email = self.get_date_of_email(last_email_html)

        #last_email_html.get_attribute()

        # Get Last email (first email visable)
        message_body = self.driver.find_element(By.CSS_SELECTOR, css_sel_message_body)
        last_email_element = message_body.find_element(By.TAG_NAME, 'tr')

        # click email


        if self.is_correct_email('Heute 09:54'):
            last_email_element.click()
        
        else:
            print("Correct Email not found yet!")
            time.sleep(10)
            self.dirver.find_element(By.XPATH, xpath_refresh).click()

def main():
    driver = webdriver.Firefox()

    myTest = Login(driver)

    content = Data.getContentAsList("test_one_comp.txt")
    
    getData = Data()

    email = getData.getEmail(content[0])
    pw = getData.getPw(content[0])

    time.sleep(2)
    myTest.verify_email(email, pw)



if __name__ == '__main__':
    main()