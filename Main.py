import pyinputplus as pyip
from bot import InstagramBot
from bot import print_list

#TODO add checks for broken links/ elements not found


newBot = InstagramBot(input('Please enter your username: '), input('Please enter your password: '))
newBot.login()
choice = ''
while choice != 'Logout':
    choice = pyip.inputMenu(['Follow user', 'Unfollow user', 'Get followers', 'Get following', 'Get ratio', 'Like recent posts' , 'Logout'])
    if choice == 'Follow user':
        newBot.follow_user(input('Please enter a valid username to follow: '))
    if choice == 'Unfollow user':
        newBot.unfollow_user(input('Please enter a valid username to unfollow: '))
    if choice == 'Get followers':
        user = pyip.inputYesNo('Would you like to get your own followers?')
        if user == 'yes':
            print_list(newBot.followers)
        else:
            print_list(newBot.get_followers(input('Enter a valid username: ')))
    if choice == 'Get following':
        user = pyip.inputYesNo('Would you like to get the accounts you are following?')
        if user == 'yes':
            print_list(newBot.following)
        else:
            print_list(newBot.get_following(input('Enter a valid username: ')))
    if choice == 'Get ratio':
        newBot.get_self_ratio()
    if choice == 'Like recent posts':
        newBot.like_recent_post()

newBot.logout()

