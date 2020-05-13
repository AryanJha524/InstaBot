import selenium
from selenium import webdriver
import time
import pyinputplus as pyip


class InstagramBot:
    base_url = 'https://instagram.com'

    def __init__(self, username, password):
        self.browser = webdriver.Firefox()
        self.username = username
        self.password = password
        self.followers = []

    def login(self):
        self.browser.get(self.base_url)
        time.sleep(3)
        username_field = self.browser.find_element_by_css_selector(
            '#react-root > section > main > article > div.rgFsT > div:nth-child(1) > div > form > div:nth-child(2) > div > label > input')
        password_field = self.browser.find_element_by_css_selector(
            '#react-root > section > main > article > div.rgFsT > div:nth-child(1) > div > form > div:nth-child(3) > div > label > input')
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.submit()

    def logout(self):
        time.sleep(3)
        self.browser.get(str(self.base_url) + '/' + str(self.username))  # change to profile page
        self.browser.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > div.nZSzR > div > button').click()
        time.sleep(3)
        self.browser.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div > button:nth-child(9)').click()
        time.sleep(1)
        self.browser.quit()

    def redirect_home(self):
        self.browser.get(self.base_url)

    def follow_user(self, user):
        try:
            self.browser.get(self.base_url + '/' + user)
        except:  # need to except a 404 error, page not found, probably have to import something else 
            print("Error, could not find user.. redirecting home.")
            self.redirect_home()
        self.browser.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_._4EzTm > span > span.vBF20._1OSdk > button').click()
        try:
            if self.browser.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div').is_enabled():
                response = pyip.inputYesNo(prompt='You already follow this user, would you like to unfollow? ')
                if response == 'yes':
                    self.unfollow_user(user)
                self.redirect_home()
        except selenium.common.exceptions.NoSuchElementException:
            print('You are now following @' + str(user))

    def unfollow_user(self, user):
        self.browser.get(self.base_url + '/' + user)  # redirect to user page
        self.browser.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_._4EzTm > span > span.vBF20._1OSdk > button').click()

        # prob have to try the box below and see if it is found or not.
        unfollow_dialog = self.browser.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div')
        if not unfollow_dialog.is_displayed():
            print('You don\'t follow this user...')
        elif unfollow_dialog.is_displayed():
            self.browser.find_element_by_css_selector(
                'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.-Cab_').click()
            print('You unfollowed @' + str(user) + '....')

    def like_recent_posts(self):  # have to wait for elements to load or obscure error will occur.
        self.browser.get(self.base_url)  # navigate to the home page


    def check_follower_ratio(self, username):
        time.sleep(3)
        self.browser.get(self.base_url + '/' + username)  # redirect to users page
        time.sleep(2)
        followersLink = self.browser.find_element_by_css_selector('li.Y8-fY:nth-child(2) > a:nth-child(1) > span:nth-child(1)')
        followersLink.click()
        time.sleep(3)
        listOfFollowers = self.browser.find_element_by_css_selector("div[role=\'dialog\'] ul")
        numberOfFollowersInList = len(listOfFollowers.find_elements_by_css_selector('li'))
        print(numberOfFollowersInList)
        following_list = []
        for elements in list(listOfFollowers.find_elements_by_css_selector('li')):
            account = elements.text.split('\n')[0]
            name = elements.text.split('\n')[1]
            following_list.append(name)
        return following_list


newBot = InstagramBot(input('Enter your username: '), input('Enter your password: '))
time.sleep(3)
newBot.login()
time.sleep(3)
listFollowers = newBot.check_follower_ratio(newBot.username)
print("Here are your followers")
for name in listFollowers:
    print(name)




