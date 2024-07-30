import sys
sys.path.append('../pinkpinapple')
from myTools.mySeleniumTools import Tools

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from extractTxtData import Data
import traceback

mainPage = "https://services.dasoertliche.de/services/schnupperpaket/sp/"
#All Paths
xpath_start = '//*[@id="packagetype1"]'
xpath_cookies = '//*[@id="cmpbntsavetxt"]'

#All Input fields first page
xpath_firmenname = '//*[@id="companyname"]'

xpath_straße = '//*[@id="companystreet"]'
xpath_hausnummer = '//*[@id="companyhnr"]'

xpath_plz = '//*[@id="companypc"]'
xpath_ort = '//*[@id="companycity"]'

xpath_vorwahl_telefon = '//*[@id="companytelpre"]'
xpath_telefon = '//*[@id="companytelnumber"]'

xpath_vorwahl_handy = '//*[@id="companymobtelpre"]'
xpath_handy = '//*[@id="companymobtelnumber"]'

xpath_vorwahl_fax = '//*[@id="companyfaxpre"]'
xpath_fax = '//*[@id="companyfaxnumber"]'

xpath_website = '//*[@id="companyurl"]'
xpath_email = '//*[@id="companyemail"]'
xpath_branche = '//*[@id="rubric"]'

xpath_next_page = '//*[@id="SubmitForward"]'


classname_submit = 'SubmitForward'

#All input fields last page
xpath_vorname = '//*[@id="contactfirstname"]'
xpath_nachname = '//*[@id="contactlastname"]'
xpath_vorwahl_last = '//*[@id="contactprefixnumber"]'
xpath_telefon_last = '//*[@id="contactcallnumber"]'
xpath_email_last = '//*[@id="contactemail"]'


class runDasOertliche():
    def firstPageLoad(self):
        self.driver.get(mainPage)
        wait = WebDriverWait(self.driver, 5)
        for i in range(1,4):
            try:
                element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_cookies)))
                element.click()
                break
            except Exception as e:
                print(f"No Cookies found! try_number{i}")
                print(f"Error: {e}")

        self.driver.find_element(By.XPATH, xpath_start).click()
        print("Cookies clicked!")

    def goToFirstPage(self):
        self.driver.get(mainPage)
        self.driver.find_element(By.XPATH, xpath_start).click()

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.getData = Data()
        self.Tools = Tools(self.driver)
        self.Email = Login(self.driver)
        self.firstPageLoad()

    def next_page(self):
        input_field = self.driver.find_element(By.XPATH, classname_submit)
        input_field.click()

    def clearAllInputs(self):
        self.enterFirmenname(text=(Keys.CONTROL, "a", Keys.BACKSPACE))
        time.sleep(0.1)

        self.enterStraße(text=(Keys.CONTROL, "a", Keys.BACKSPACE))
        time.sleep(0.1)
        
        self.enterHausnummer(text=(Keys.CONTROL, "a", Keys.BACKSPACE))
        time.sleep(0.1)

        self.enterOrt(text=(Keys.CONTROL, "a", Keys.BACKSPACE))
        time.sleep(0.1)

        self.enterPlz(text=(Keys.CONTROL, "a", Keys.BACKSPACE))
        time.sleep(0.1)

        self.enterOrt(text=(Keys.CONTROL, "a", Keys.BACKSPACE))
        time.sleep(0.1)

        print("All Cleared")

    def enterDataOfComp(self):
        ###################################
        #### input data for first page ####
        ###################################
        
        # Enter Firmenname
        self.Tools.inputFieldByXpath(self.firmenname, xpath_firmenname)
        time.sleep(0.1)

        # Enter Straße
        self.Tools.inputFieldByXpath(self.straße, xpath_straße)
        time.sleep(0.1)

        # Enter hausnummer
        self.Tools.inputFieldByXpath(self.hausnummer, xpath_hausnummer)
        time.sleep(0.1)
        
        # Enter plz
        self.Tools.inputFieldByXpath(self.plz, xpath_plz)
        time.sleep(0.1)

        # Enter Ort
        self.Tools.inputFieldByXpath(self.ort, xpath_ort)
        time.sleep(0.1)

        # Enter Email
        self.Tools.inputFieldByXpath(self.email, xpath_email)
        time.sleep(0.1)

        # Enter Vorwahl Handy
        self.Tools.inputFieldByXpath(self.vorwahl, xpath_vorwahl_handy)
        time.sleep(0.1)

        # Enter Handynummer
        self.Tools.inputFieldByXpath(self.phoneNumber, xpath_handy)
        time.sleep(0.1)

        # Enter Vorwahl Telefon
        self.Tools.inputFieldByXpath(self.vorwahl, xpath_vorwahl_telefon)
        time.sleep(0.1)

        # Enter Telfonnummer
        self.Tools.inputFieldByXpath(self.phoneNumber, xpath_telefon)
        time.sleep(0.1)

        # Enter Vorwahl Fax
        self.Tools.inputFieldByXpath(self.vorwahl, xpath_vorwahl_fax)
        time.sleep(0.1)

        # Enter Fax
        self.Tools.inputFieldByXpath(self.phoneNumber, xpath_fax)
        time.sleep(0.1)

        # Enter Website
        self.Tools.inputFieldByXpath(self.website, xpath_website)
        time.sleep(0.1)


        #### BRANCHE EVNTL ÄNDERN ####
        self.Tools.inputFieldByXpath("Autokauf", xpath_branche)
        time.sleep(0.1)

        # Skip first Input Page

        ### ERROR HERE ###

        self.Tools.clickElementByXpath(xpath_next_page)
        time.sleep(2)
        # Skip Time Page
        self.Tools.clickElementByXpath(xpath_next_page)
        time.sleep(2)
        # Skip Paymethods
        time.sleep(2)
        self.Tools.clickElementByXpath(xpath_next_page)
        
        ###############################
        #### Input data of last page #####
        ###############################

        # PRIMITIVE DONE 
        # MISSING NAME

    def loopData(self, source):
        
        # Make data to list were each element is a company
        with open(source, 'r') as file:
            self.content = file.read().strip().split('\n\n')
            
        # iterate over each company
        for idx, comp in enumerate(self.content):
            self.goToFirstPage()
            time.sleep(2)

            self.firmenname = self.getData.getFirmenname(comp)
            
            self.straße = self.getData.getStraße_n_number(comp)[0]
            self.hausnummer = self.getData.getStraße_n_number(comp)[1]
            
            self.plz = self.getData.getPlz_n_ort(comp)[0]
            self.ort = self.getData.getPlz_n_ort(comp)[1]

            self.vorwahl = self.getData.getVorwahl_n_nummer(comp)[0]
            self.phoneNumber = self.getData.getVorwahl_n_nummer(comp)[1]

            self.website = self.getData.getWebsite(comp)

            self.email = self.getData.getEmail(comp)
            self.pw = self.getData.getPw(comp)

            try:
                #### insert data for first input area ####
                self.enterDataOfComp()

                #### RUN EMAIL VERIFIKATION ####
                print(f"{self.firmenname}: Running Email Verifikation")

                # RUN()
                self.Email.login_to_email(email, pw)
                
                #### pop first element of txt and insert into new txt named Done append By email link 
                self.getData.popElementFromFile('remaining_companies.txt', elem=comp)
                print(f"{self.firmenname} DONEEEEEEE!")
                print()

            except Exception as e:
                print(f"Failed To Insert: {self.firmenname}")
                traceback.print_exc()
                print()
                print("##### STARTING By NEXT ####")
                continue

def main():
    scrapper = runDasOertliche()
    scrapper.loopData("remaining_companies.txt")


if __name__ == "__main__":
    main()