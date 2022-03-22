from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from Confidential import odhusername,odhpassword
import win32com.client
import sys
import time
class Bot():
    def __init__(self):
        self.driver=webdriver.Chrome()

    def get_input(self, prompt):
        while True:
            try:
                value = input(prompt)
                if not value:
                    raise ValueError('Jobname is not defined')
            except ValueError as e:
                print("Sorry, I didn't understand that.", e)
                continue

            if value.isdigit():
                print("Sorry, job name must be a string.")
                continue
            else:
                break
        return value

    def login(self):
        # Switch the control to the Alert window
        print(f"{'#' * 50} Python Script To Access Marathon {'#' * 50}")
        # odhusername = input("Enter the user name")
        # odhpassword = input("Enter the password")
        self.driver.maximize_window()
        url = url = "http://"+odhusername+":"+odhpassword+"@connectivity.odh.lgi.io/marathon/"
        self.driver.get(url)
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.Sendkeys("^l")
            time.sleep(2.0)
            shell.Sendkeys("{ENTER}")
            time.sleep(2.0)
        except NoAlertPresentException as e:
            print("no alert",e)

        #jobName = input("Enter the job name")
        try:
            jobName = self.get_input("Please enter job name: ")
            self.driver.find_element(By.XPATH,'//*[@id="marathon"]/div/nav/div/div[2]/div[1]/input').send_keys(jobName)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="marathon"]/div/nav/div/div[2]/div[1]/input'))
            ).send_keys(Keys.ENTER)

            try:
                self.driver.find_element(By.XPATH,'//*[@id="marathon"]/div/div/div/div/main/div[2]/table/tbody/tr[4]').click()
                time.sleep(2.0)
                jobStatus = self.driver.find_element(By.XPATH, '//*[@id="marathon"]/div/div/div/div[1]/span/span[1]').text
                if (jobStatus == 'Suspended'):
                    print("The job is already in suspended state")
                    pass
                else:
                    #suspend the marathon
                    print(f"{'#' * 50} Suspending the Job... {'#' * 50}")
                    self.driver.find_element(By.XPATH,'//*[@id="marathon"]/div/div/div/div[1]/div[2]/div/button').click()
                    time.sleep(1.0)
                    self.driver.find_element(By.XPATH,'//*[@id="marathon"]/div/div/div/div[1]/div[2]/div/ul/li[1]/a').click()
                # Switch the control to the Alert window
                try:
                    time.sleep(2.0)
                    shell.Sendkeys("{ENTER}")

                    # WebDriverWait(self.driver, 3).until(EC.alert_is_present()),
                    #                                     'Timed out waiting for PA creation ' +
                    #                                     'confirmation popup to appear.')
                    #
                    # alert = self.driver.switch_to.alert
                    # alert.accept()
                    # print("alert accepted")
                except:
                    print("no alert")
                #get the hdfs path
                time.sleep(10.0)
                self.driver.find_element(By.XPATH,'//*[@id="marathon"]/div/div/div/div[2]/ul/li[2]/a').click()
                time.sleep(1.0)
                command = self.driver.find_element(By.XPATH,'//*[@id="marathon"]/div/div/div/div[2]/div/div/div[1]/dl/dd[2]/span[1]').text
                hdfsPath=command.rsplit(' ', 1)[1]
                print('HDFS PATH',hdfsPath)
            except NoSuchElementException as e:
                print("Element not found:", e)
            except WebDriverException as e:
                print("Site is not reachable")
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
if __name__ == "__main__":
    bot = Bot()
    bot.login()
    sys.exit()