import time

import pyinputplus as pyip
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# TODO what should bot do/goal. is this a manager bot or trying to gain followers bot? Leaning towards manager/automate
# TODO Goal cont.^ bot should automate tasks like liking posts, listing followers/following, ratio, follow/unfollow user
# TODO Goal cont.^

# TODO put in checks for broken pages everytime you redirect.

def print_list(list):
    print('------FOLLOWING------')
    for element in list:
        print('--> @' + element)

class InstagramBot:
    base_url = 'https://instagram.com'

    def __init__(self, username, password):
        self.browser = webdriver.Firefox()
        self.username = username
        self.password = password
        self.followers = []
        self.following = []
        self.numFollowers = 0
        self.numFollowing = 0

    def login(self):
        """redirects browser to Instagram sign in page and logs in user and calls function to get basic account info"""
        self.browser.get(self.base_url)
        time.sleep(3)
        username_field = self.browser.find_element_by_css_selector(
            '#react-root > section > main > article > div.rgFsT > div:nth-child(1) > div > form > div:nth-child(2) > '
            'div > label > input')
        password_field = self.browser.find_element_by_css_selector(
            '#react-root > section > main > article > div.rgFsT > div:nth-child(1) > div > form > div:nth-child(3) > '
            'div > label > input')
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.submit()
        time.sleep(3)
        try:
            while self.browser.find_element_by_css_selector('#slfErrorAlert').is_enabled():
                self.password = input('Your password was in correct, please re-enter: ')
                self.login()
        except selenium.common.exceptions.NoSuchElementException:
            pass
        self.get_info()

    def get_info(self):
        list_followers = self.get_followers(self.username)
        for elements in list_followers:  # instantiates list of followers
            account = elements.text.split('\n')[0]
            self.followers.append(account)

        list_following = self.get_following(self.username)
        for elements in list_following:  # instantiates list of following
            account = elements.text.split('\n')[0]
            self.following.append(account)

    def logout(self):
        """redirects to profile page and logs user out"""
        time.sleep(2)
        self.browser.get(str(self.base_url) + '/' + str(self.username))  # change to profile page
        self.browser.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > div.nZSzR > div > button').click()
        time.sleep(2)
        self.browser.find_element_by_css_selector(
            'body > div.RnEpo.Yx5HN > div > div > div > button:nth-child(9)').click()
        time.sleep(1)
        self.browser.quit()

    def redirect_home(self):
        self.browser.get(self.base_url)

    def check_user_validity(self, user):
        """Checks to see if user exists, calls returns to home function."""
        self.browser.get(self.base_url + '/' + user)
        if 'Page Not Found' in self.browser.title:
            print("Error, could not find user.. redirecting home.")
            return False
        else:
            return True

    def follow_user(self, user):
        """Checks if user exists, and follows if you are not already following."""
        if not self.check_user_validity(user):
            self.redirect_home()
        else:
            self.browser.get(self.base_url + '/' + user)
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
        """checks validity of username and unfollows if account was following them."""
        if not self.check_user_validity(user):
            self.redirect_home()
        else:
            self.browser.get(self.base_url + '/' + user)  # redirect to user page
            self.browser.find_element_by_css_selector(
                '#react-root > section > main > div > header > section > div.nZSzR > div.Igw0E.IwRSH.eGOV_._4EzTm > span > span.vBF20._1OSdk > button').click()
            unfollow_dialog = self.browser.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div')
            if not unfollow_dialog.is_displayed():
                print('You don\'t follow this user...')
            elif unfollow_dialog.is_displayed():
                self.browser.find_element_by_css_selector(
                    'body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.-Cab_').click()
                print('You unfollowed @' + str(user) + '....')

    def like_recent_posts(self):  # have to wait for elements to load or obscure error will occur.
        """likes posts on home page until it reaches a post you haven't liked."""
        # TODO make the function lol, figure out HOW KEYCHAIN WORKs and how to scroll down.
        self.browser.get(self.base_url)  # navigate to the home page

    def get_followers(self, username):
        '''Returns a list of followers'''
        self.browser.get(self.base_url + '/' + username)  # redirect to users page
        time.sleep(3)
        self.numFollowers = int(self.browser.find_element_by_css_selector(
            'li.Y8-fY:nth-child(3) > a:nth-child(1) > span:nth-child(1)').text)
        followersLink = self.browser.find_element_by_css_selector(
            'li.Y8-fY:nth-child(2) > a:nth-child(1) > span:nth-child(1)')
        followersLink.click()
        time.sleep(2)
        bodyFollowers = self.browser.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        while scroll < self.numFollowers:  # scroll through number of followers
            self.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                        bodyFollowers)
            time.sleep(2)
            scroll += 1
        followersList = self.browser.find_elements_by_xpath("//div[@class='isgrP']//li")
        return followersList

    def get_following(self, username):
        '''Returns a list of following users'''
        self.browser.get(self.base_url + '/' + username)  # redirect to users page
        time.sleep(3)
        self.numFollowing = int(self.browser.find_element_by_css_selector(
            'li.Y8-fY:nth-child(2) > a:nth-child(1) > span:nth-child(1)').text)
        followingLink = self.browser.find_element_by_css_selector(
            '#react-root > section > main > div > header > section > ul > li:nth-child(3)')
        followingLink.click()
        time.sleep(2)
        bodyFollowing = self.browser.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        while scroll < self.numFollowing:  # scroll until you reach num of followerd
            self.browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;',
                                        bodyFollowing)
            time.sleep(2)
            scroll += 1
        followingList = self.browser.find_elements_by_xpath("//div[@class='isgrP']//li")
        return followingList

    def get_self_ratio(self):
        ''' Ratio = NumFollowers/NumFollowing
            if you are following someone and they aren't following you back, add them to the list'''
        notFollowingBack = []
        ratio = float(len(self.followers) / len(self.following))
        for account in self.following:
            if account not in self.followers:
                notFollowingBack.append(account)
        print('Your ratio is: ' + "{:.2f}".format(ratio) + '. Here are the accounts not following you back:')
        print_list(notFollowingBack)


newBot = InstagramBot(input('Enter your username: '), input('Enter your password: '))
time.sleep(2)
newBot.login()
time.sleep(2)
newBot.get_self_ratio()
print_list(newBot.followers)
print_list(newBot.following)

