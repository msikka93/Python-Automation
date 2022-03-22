from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Confidential import odhusername,odhpassword
import sys
import time
class Bot():
    def __init__(self):
        self.driver=webdriver.Chrome()

    def get_input(self):
        while True:
            try:
                try:
                    jobName = input("Please enter job name: ")
                    if not jobName:
                        raise ValueError('Job name is not defined')
                    if jobName.isdigit():
                        print("Sorry, job name must be a string.")
                        continue
                except ValueError as e:
                    print("Sorry, I didn't understand that.", e)
                    continue

                self.driver.find_element(By.XPATH, '//*[@id="nodesearcher"]/input').send_keys(jobName)
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="nodesearcher"]/input'))
                )
                time.sleep(2.0)

                containers = self.driver.find_elements(By.XPATH, '//*[@id="nodesearcher"]/div[2]')
                for item in containers:
                    searchedItem = item.find_element(By.CLASS_NAME, 'item').text

                if searchedItem == 'No results found.':
                    print('Searched item not found')
                    self.driver.find_element(By.XPATH, '//*[@id="nodesearcher"]/input').clear()
                    continue

                elif searchedItem == 'Error: Failed to retrieve data.':
                    print('Error while retrieving data')
                    self.driver.find_element(By.XPATH, '//*[@id="nodesearcher"]/input').clear()
                    continue
                else:
                    self.driver.find_element(By.CLASS_NAME, 'highlighted').click()

            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

            else:
                print("Output is achieved")
                break


    def login(self):
        print(f"{'#' * 50} Python Script To Access Marathon {'#' * 50}")
        # odhusername = input("Enter the user name")
        # odhpassword = input("Enter the password")
        #self.driver.maximize_window()
        url = "http://"+odhusername+":"+odhpassword+"@odh.lgi.io/oats"
        self.driver.get(url)
        try:
            self.get_input()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

bot = Bot()
bot.login()
sys.exit()