"""Amazon Giveaway bot."""
from selenium import webdriver
import time

try:
    browser = webdriver.Firefox()
except Exception:
    browser = webdriver.Edge()
entered = 0
wins = 0
giveaway_number = 0
times = input('How many Giveaways do you want to enter?')
times = int(times)


def get_giveaway():
    """Find the giveaways."""
    global giveaway
    global giveaway_number
    time.sleep(.5)
    print('Found giveaway '+str(giveaway_number))
    giveaway_number += 1
    if giveaway_number == 25:  # Only 24 giveaways per page.
        giveaway_number = 1
        time.sleep(1)
        browser.find_element_by_partial_link_text('Next').click()
    if check_page == 'old':
        giveaway = browser.find_element_by_id, \
         ('giveaway-item-'+str(giveaway_number))
        return
    else:
        giveaway = []
        giveaway.insert((giveaway_number),
                        browser.find_elements_by_class_name
                        ('a-link-normal.item-link'))
        return


def click_giveaway():
    """Click giveaway."""
    print('Clicking giveaway '+str(giveaway_number))
    if check_page == "old":
        giveaway.click()
        return
    else:
        giveaway[(giveaway_number)].click()
        return


def login():
    """Login to Bing."""
    print("\n" * 100)
    browser.get('https://www.amazon.com/gp/sign-in.html')
    password = browser.find_elements_by_id("ap_password")
    try:
        if password != []:
            print('single page login')
            user = browser.find_element_by_id("ap_email")
            file = open("login.txt", "r")
            file.readline()
            print('entering user')
            user.send_keys(file.readline())
            file.readline()
            password = browser.find_element_by_id("ap_password")
            print('entering password')
            password.send_keys(file.readline())
            browser.find_element_by_id("signInSubmit").click()
            print('signing in')
            file.close()
            return
    except Exception:
        pass
    try:
        print('Multipage login')
        user = browser.find_element_by_id("ap_email")
        file = open("login.txt", "r")
        file.readline()
        print('Entering user')
        user.send_keys(file.readline())
        browser.find_element_by_id("continue").click()
        file.readline()
        password = browser.find_element_by_id("ap_password")
        print('Entering password')
        password.send_keys(file.readline())
        print('signing in')
        browser.find_element_by_id("signInSubmit").click()
        file.close()
    except Exception:
        print("No login.txt found please enter info manually")
    while browser.title == "Amazon Sign In":
        time.sleep(1)
        if browser.title != "Amazon Sign In":
            break


def get_giveaway_type():
    """Find the giveaway type."""
    while browser.title == "Amazon Giveaways":
        # look for add to cart button to skip ones already done
        giveaway_type = browser.find_elements_by_name('addToCart')
        if giveaway_type != []:
            print('Looks like we already did this one.')
            browser.back()
            break
        # Check for youtube video if so wait 15 seconds then click
        giveaway_type = browser.find_elements_by_id, \
            ('enter-youtube-video-button-announce')
        if giveaway_type != []:
            print('Looks like a YouTube video waiting 15 seconds')
            time.sleep(15)
            giveaway_type = browser.find_element_by_id('videoSubmitForm')
            giveaway_type.click()
            check_box_target()
            check_loss()
            check_win()
            browser.back()
            break
        # Check for instant enter button, click it
        giveaway_type = browser.find_elements_by_name('enter')
        if giveaway_type != []:
            print('instant enter')
            giveaway_type = browser.find_element_by_name('enter')
            giveaway_type.click()
            check_win()
            browser.back()
            break
        # Check for box, click it
        giveaway_type = browser.find_elements_by_id('box_click_target')
        if giveaway_type != []:
            print('box target, clicking')
            giveaway_type = browser.find_element_by_id('box_click_target')
            giveaway_type.click()
            check_win()
            browser.back()
            break
        # Check for amazon video, click it. cant seem to mute
        giveaway_type = browser.find_elements_by_id('airy-container')
        if giveaway_type != []:
            print('Amazon video waiting 15 seconds')
            giveaway_type = browser.find_element_by_id('airy-container')
            giveaway_type.click()
            # browser.find_element_by_class_name('airy-audio-elements').click()
            time.sleep(15)
            giveaway_type = browser.find_element_by_id('videoSubmitForm')
            giveaway_type.click()
            check_box_target()
            check_loss()
            check_win()
            browser.back()
            break
        # Nothing found go back
        else:
            print('might have ended, or asking for captcha')
            browser.back()
            break


def check_win():
    """See if we won, claim prize."""
    global wins
    while browser.title == "Amazon Giveaways":
        giveaway_type = browser.find_elements_by_name('addToCart')
        if giveaway_type != []:
            browser.back()
            break
        time.sleep(7)
        did_win = browser.find_elements_by_name('ClaimMyPrize')
        if did_win != []:
            did_win = browser.find_element_by_name('ClaimMyPrize')
            wins += 1
            did_win.click()
            break
        else:
            break


def check_box_target():
    """Look for a box target, click it."""
    time.sleep(2)
    while browser.title == "Amazon Giveaways":
        giveaway_type = browser.find_elements_by_id('box_click_target')
        if giveaway_type != []:  # Click box
            giveaway_type = browser.find_element_by_id('box_click_target')
            giveaway_type.click()
            time.sleep(2)
            break
        else:
            break


def check_loss():
    """Check to see if we lost."""
    while browser.title == "Amazon Giveaways":
        did_lose = browser.find_elements_by_id('giveaway-addToCart-btn')
        if did_lose != []:
            break
        else:
            time.sleep(2)
            break


def check_giveaway_page():
    """See if we got an old page or a new one."""
    global check_page
    time.sleep(.5)
    if browser.title == "Giveaways":
        print('Looks like we got an old page')
        check_page = "old"
        return
    else:
        print('Looks like we got a new page')
        check_page = "new"
        return


login()
browser.get('https://www.amazon.com/ga/giveaways')
while times > 0:
    times = times - 1
    entered += 1
    check_giveaway_page()
    get_giveaway()
    click_giveaway()
    get_giveaway_type()
    print("Entered " + str(entered) +
          " giveaways | " + str(times) + " giveaways remaining")

print("Tried to enter " + str(entered) + " giveaways")
print("You won " + str(wins) + " times")
browser.close()
quit = input('Press Enter to close')
