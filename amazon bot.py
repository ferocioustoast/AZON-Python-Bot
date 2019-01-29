from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
browser = webdriver.Firefox()
entered = 0 #amount of giveaways entered
wins = 0 #times won
giveaway_number = 0 #giveaway we are on
times = input('How many Giveaways do you want to enter?') #get number of giveaways to enter
times = int(times)

def get_giveaway():
	global giveaway
	global giveaway_number
	time.sleep(.5)
	giveaway_number += 1
	print('Found giveaway '+str(giveaway_number))
	if giveaway_number == 25 : #reset giveaway_number because there is only 24 giveaways per page
		giveaway_number = 1
		time.sleep(1)
		browser.find_element_by_partial_link_text('Next').click()
	if check_page == 'old' :
		giveaway = browser.find_element_by_id('giveaway-item-'+str(giveaway_number))
		return
	else :
		giveaway = browser.find_elements_by_class_name('a-link-normal.item-link')
		return

def click_giveaway():
	print('Clicking giveaway '+str(giveaway_number))
	if check_page == "old" :
		giveaway.click()
		return
	else :
		giveaway[(giveaway_number)].click()
		return
		
def login():
	print ("\n" * 100) #"clear" screen
	browser.get('https://www.amazon.com/gp/sign-in.html')
	password = browser.find_elements_by_id("ap_password")
	try:
		if password != []: #single page login
			print('single page login')
			user = browser.find_element_by_id("ap_email")
			file = open("login.txt", "r")
			file.readline()#ignore line one
			print('entering user')
			user.send_keys(file.readline())
			file.readline()#ignore line two
			password = browser.find_element_by_id("ap_password")
			print('entering password')
			password.send_keys(file.readline())
			browser.find_element_by_id("signInSubmit").click()
			print('signing in')
			file.close()
			return
	except:
		print("")
	try: #look for login.txt and use info login
		print('Multipage login')
		user = browser.find_element_by_id("ap_email")
		file = open("login.txt", "r")
		file.readline()#ignore line one
		print('Entering user')
		user.send_keys(file.readline())
		browser.find_element_by_id("continue").click()
		file.readline()#ignore line two
		password = browser.find_element_by_id("ap_password")
		print('Entering password')
		password.send_keys(file.readline())
		print('signing in')
		browser.find_element_by_id("signInSubmit").click()
		file.close()
	except: #cant find login.txt or entered wrong wait for them to enter it
		print ("No login.txt found please enter info manually")
	while browser.title == "Amazon Sign In" :
		time.sleep(1)
		if browser.title != "Amazon Sign In" :
			break
			
def get_giveaway_type():
	while browser.title == "Amazon Giveaways" :
		#look for add to cart button to skip ones already done
		giveaway_type = browser.find_elements_by_name('addToCart')
		if giveaway_type != [] :
			print('Looks like we already did this one.')
			browser.back()
			break
		#check for youtube video if so wait 15 seconds then click
		giveaway_type = browser.find_elements_by_id('enter-youtube-video-button-announce')
		if giveaway_type != [] :
			print('Looks like a YouTube video waiting 15 seconds')
			time.sleep(15)
			giveaway_type = browser.find_element_by_id('videoSubmitForm')
			giveaway_type.click()
			check_box_target()
			check_loss()
			check_win()
			browser.back()
			break
		#check for instant enter button, click it
		giveaway_type = browser.find_elements_by_name('enter')
		if giveaway_type != [] :
			print('instant enter')
			giveaway_type = browser.find_element_by_name('enter')
			giveaway_type.click()
			check_win()
			browser.back()
			break
		#check for box, click it
		giveaway_type = browser.find_elements_by_id('box_click_target')
		if giveaway_type != [] :
			print('box target, clicking')
			giveaway_type = browser.find_element_by_id('box_click_target')
			giveaway_type.click()
			check_win()
			browser.back()
			break
		#check for amazon video, click it. cant seem to mute
		giveaway_type = browser.find_elements_by_id('airy-container')
		if giveaway_type != [] :
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
		#nothing found go back
		else:
			print('might have ended, or asking for captcha')
			browser.back()
			break
			
def check_win():
	global wins
	while browser.title == "Amazon Giveaways" :
		giveaway_type = browser.find_elements_by_name('addToCart')
		if giveaway_type != [] :
			browser.back()
			break
		time.sleep(7) #wait for box to see if won
		did_win = browser.find_elements_by_name('ClaimMyPrize')
		if did_win != [] : #claim prize
			did_win = browser.find_element_by_name('ClaimMyPrize')
			wins += 1
			did_win.click()
			break
		else :
			break
			
def check_box_target():
	time.sleep(2)#wait for box to land
	while browser.title == "Amazon Giveaways" :
		giveaway_type = browser.find_elements_by_id('box_click_target')
		if giveaway_type != [] :#click box
			giveaway_type = browser.find_element_by_id('box_click_target')
			giveaway_type.click()
			time.sleep(2)
			break
		else :
			break

def check_loss():
	while browser.title == "Amazon Giveaways" : #look for add to cart button to see if lose
		did_lose = browser.find_elements_by_id('giveaway-addToCart-btn')
		if did_lose != [] :
			break
		else :
			time.sleep(2)
			break
			
# For some reason there is two different types of giveaway pages, lets see which one we get
def check_giveaway_page():
	global check_page
	time.sleep(.5)
	if browser.title == "Giveaways" :
		print('Looks like we got an old page')
		check_page = "old"
		return
	else :
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
	print("Entered " + str(entered) + " giveaways | " + str(times) + " giveaways remaining")

print("Tried to enter " + str(entered) + " giveaways")
print("You won " + str(wins) + " times")
browser.close()
quit = input('Press Enter to close')