from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from Confidential import username,password

import time

class Bot():
    def __init__(self):
        self.driver=webdriver.Chrome()

    def login(self):
        self.driver.get('https://dashboard.horizon.tv/')

        user=self.driver.find_element_by_xpath('//*[@id="login-view"]/form/div[1]/input')
        user.click()
        user.send_keys(username)

        pwd = self.driver.find_element_by_xpath('//*[@id="inputPassword"]')
        pwd.click()
        pwd.send_keys(password)

        btn = self.driver.find_element_by_xpath('//*[@id="login-view"]/form/div[3]/button')
        btn.click()
        time.sleep(5)
        home =  self.driver.find_element_by_xpath('/html/body/grafana-app/div/div/div/react-container/div/div[1]/div[1]/a/i[2]')
        home.click()

        dashboardName = input("Enter the dashboard name")
        inp = self.driver.find_element_by_xpath('/html/body/grafana-app/dashboard-search/div[2]/div[1]/input')
        inp.click()
        inp.send_keys(dashboardName)
        time.sleep(2)
        searchedDashboard = self.driver.find_element_by_xpath('/html/body/grafana-app/dashboard-search/div[2]/div[2]/div[1]/div/div[1]/dashboard-search-results/div/div[3]')
        searchedDashboard.click()


bot = Bot()
bot.login()