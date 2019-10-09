from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import json

class portfolioManager(object):
    def __init__(self):
        self.stockElement = None
        self.timeout = 10
        self.loadLoginDetails()
        self.launchDriver()

    def getXpathElement(self, xpath):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def getAllXpathElements(self, xpath):
        firstMatch = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        allElements = self.driver.find_elements_by_xpath(xpath)
        return allElements

    def loadLoginDetails(self):
        with open("loginDetails.json") as loginFile:
            credentials = json.load(loginFile)
            self.userID = credentials['userID']
            self.password = credentials['password']
            self.twoFactorPIN = credentials['twoFactorPIN']

    def launchDriver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")        
        self.driver = webdriver.Chrome(chrome_options=options)
        self.pageURL = "https://kite.zerodha.com"
        self.driver.get(self.pageURL)

    def executeLogin(self):
        try:
            xpathUserID = '//*[@id="container"]/div/div/div/form/div[2]/input'
            xpathPassword = '//*[@id="container"]/div/div/div/form/div[3]/input'
            # xpathLoginButton = '//*[@id="container"]/div/div/div/form/div[4]/button'
            inputUserID = self.getXpathElement(xpathUserID)
            inputUserID.send_keys(self.userID)
            inputPassword = self.getXpathElement(xpathPassword)
            inputPassword.send_keys(self.password)
            inputPassword.send_keys(Keys.ENTER)
            # loginButton = self.getXpathElement(xpathLoginButton)
            # loginButton.click()

            #Two Factor Authentication:
            xpathTwoFactorPIN ='//*[@id="container"]/div/div/div/form/div[2]/div/input'
            inputTwoFactorPIN = self.getXpathElement(xpathTwoFactorPIN)
            inputTwoFactorPIN.send_keys(self.twoFactorPIN)
            inputTwoFactorPIN.send_keys(Keys.ENTER)
            # while True:
            #     a = 5
        except TimeoutException:
            print("Login Failue.")
    
    def executeOrder(self, stockName='YESBANK', orderType='BUY', numUnits=2):
        # try:
        if (self.stockElement==None):
            xpathMarketWatchNames = '//*[@id="app"]/div[2]/div[1]/div/div[2]/div/div/div/div/span[1]/span/span'
            allMarketWatchStockElements = self.getAllXpathElements(xpathMarketWatchNames)
            for stockElement_ in allMarketWatchStockElements:
                if (stockElement_.text==stockName):
                    self.stockElement = stockElement_
                    break
        hover = ActionChains(self.driver).move_to_element(self.stockElement)
        hover.perform()
        if (orderType=='BUY'):
            xpathStockElementBuyButton = '//*[@id="app"]/div[2]/div[1]/div/div[2]/div/div/div/span/button[1]'
            StockElementBuyButton = self.getXpathElement(xpathStockElementBuyButton)
            StockElementBuyButton.click()
            misRadioButton = self.getXpathElement('//*[@value="MIS"]')
            # ActionChains(self.driver).move_to_element(misRadioButton).perform()
            misRadioButton.send_keys(Keys.SPACE)
            # misRadioButton.click()
            self.getXpathElement('//*[@value="MARKET"]').send_keys(Keys.SPACE)
            self.getXpathElement('//*[@label="Qty."]').send_keys(numUnits)
            xpathBuyButton = '//*[@id="app"]/div[3]/div/form/div[3]/div[3]/div[2]/button[1]'
            # ActionChains(self.driver).move_to_element(self.getXpathElement(xpathBuyButton))
            # self.getXpathElement(xpathBuyButton).send_keys("\n")
            xpathCancelButton = '//*[@id="app"]/div[3]/div/form/div[3]/div[3]/div[2]/button[2]'
            # self.getXpathElement(xpathCancelButton).send_keys("\n")
        else:
            xpathStockElementSellButton = '//*[@id="app"]/div[2]/div[1]/div/div[2]/div/div/div/span/button[2]'
        # if (orderType=='BUY'):

            # else:
        # except TimeoutException:
        #     print("Timeout Exception in Placing Order")
            

if __name__=="__main__":
    obj = portfolioManager()
    obj.executeLogin()
    obj.executeOrder()
    # while True:
    #     a = 5

