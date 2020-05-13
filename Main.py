from selenium import webdriver
import sys
import time


class InstagramBot:
    def __init__(self, username, password):
        self.browser = webdriver.Firefox()
        self.username = username
        self.password = password
        self.login()

    def login(self):
        self.browser.get('https://instagram.com')
        time.sleep(3)
        username_field = self.browser.find_element_by_css_selector(
            '#react-root > section > main > article > div.rgFsT > div:nth-child(1) > div > form > div:nth-child(2) > div > label > input')
        password_field = self.browser.find_element_by_css_selector(
            '#react-root > section > main > article > div.rgFsT > div:nth-child(1) > div > form > div:nth-child(3) > div > label > input')
        username_field.send_keys(self.username)
        time.sleep(3)
        password_field.send_keys(self.password)
        time.sleep(3)
        password_field.submit()

    def logout(self):
        time.sleep(3)
        self.browser.get(str(self.browser.current_url) + str(self.username))  # change to profile page
        self.browser.find_element_by_css_selector('#react-root > section > main > div > header > section > div.nZSzR > div > button').click()
        time.sleep(3)
        self.browser.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > button:nth-child(9)').click()
        self.browser.quit()


newBot = InstagramBot(input('Enter username: '), input('Enter password: '))
time.sleep(3)
newBot.logout()