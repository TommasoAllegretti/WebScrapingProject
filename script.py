from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import instaloader
import gender_guesser.detector as gender
import pandas as pd
from googlesearch import search
import os
import re


#specifying chromedriver's path
chromedriver_path = 'chromedriver.exe'
#adding "headless" option to not show the window and the "log-level=3" option to not print selenium warnings 
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
webdriver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        


#function used to download Facebook's profile picture given the account url
def FBscrape(fbLink, folder, fbName):
    #opening Facebook account
    webdriver.get(fbLink)
    
    #wait for element to load in the web page
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'image'))
        WebDriverWait(webdriver, timeout).until(element_present)
    except TimeoutException:
        pass

    
    try:
        filePath = folder + '/' + fbName.replace(' ', '')
        if os.path.exists(filePath):
            print('\nFacebook profile picture already downloaded')

        #getting all images from the page 
        fbImgs = webdriver.find_elements(By.TAG_NAME, 'image')

        #checks if directory exists, if not => creates directory
        if not os.path.exists(folder):
            os.mkdir(folder)
    
        #downloading 1st image from the page (profile picture)
        fbImg = fbImgs[0].get_attribute('xlink:href')
        response = requests.get(fbImg)
        file = open(folder + '/' + fbName.replace(' ', '') + 'FBpicture.png', 'wb')
        file.write(response.content)
        file.close()    
        print('\nFacebook profile picture downloaded')
    
    except (NoSuchElementException,IndexError) as e:
        pass


def TWscrape(twLink, folder, twName):
    #opening Twitter account
    webdriver.get(twLink)

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div/div[2]/div/a'))
        WebDriverWait(webdriver, timeout).until(element_present)
    except TimeoutException:
        pass

    try:
        #getting profile picture
        twImg = webdriver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div/div/div[1]/div[1]/div[2]/div/div[2]/div/a').get_attribute('href')
    
        filePath = folder + '/' + twName.replace(' ', '')
        if os.path.exists(filePath):
            print('\nTwitter profile picture already downloaded')
            return

        #checks if directory exists, if not => creates directory
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        #downloading profile picture
        response = requests.get(twImg)
        file = open(filePath + 'TWpicture.png', 'wb')
        file.write(response.content)
        file.close()   
        print('\nTwitter profile picture downloaded')

    except (NoSuchElementException,IndexError) as e:
        pass

#checks if the current IG post is already been logged in "postsLog.txt"
#returns True if the post hasn't been downloaded yet, then the list is updated
def updateIGPostList(igName, filename):
    with open(igName + '/postsLog.txt', 'r') as r:
        if filename in r.read():
            print('\nImage already downloaded')
            return False
    
    with open(igName + '/postsLog.txt', 'a') as a:
        a.write(filename + '\n')
        print('\nNew image - Updating list')
        return True

def IGscrape(igName, IL):
    if not igName:
        print('\nURL not valid')
        return

    #getting account to scrape
    profile = instaloader.Profile.from_username(IL.context, igName)

    #download profile picture
    IL.download_profilepic(profile)

    #checks if posts "postsLog.txt" exists, else it creates it
    try:
        open(igName + '/postsLog.txt', 'r')
    except FileNotFoundError:
        open(igName + '/postsLog.txt', 'w')

    #download latest 30 posts
    posts = profile.get_posts()
    counter = 0
    for post in posts:
        counter += 1
        filename = IL.format_filename(post)
        if(updateIGPostList(igName, filename)):
            IL.download_post(post, igName)
            print('Downloaded post n. ' + str(counter) + '\n')
        if counter == 30:
            break

def IWscrape(iw):
    try:
        webdriver.get(iw)
    except UnboundLocalError:
        return
    
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="movie-left"]/div[3]/div[5]/div'))
        WebDriverWait(webdriver, timeout).until(element_present)
    except TimeoutException:
        pass

    #find date of birth
    try:        #CAN BE OPTIMIZED !!!
        dobStr = webdriver.find_element(By.XPATH, '//*[@id="movie-left"]/div[3]/div[5]/div')
        dayFlag = False
        yearFlag = False
        for word in dobStr.text.split():
            if yearFlag:
                dobYear = word
                yearFlag = False
            if dayFlag:
                dobDay = word.replace(',', '')
                dayFlag = False
                yearFlag = True
            if word in months.upper():
                dobMonth = str(months.upper().index(word) + 1)
                dayFlag = True
        
        if len(dobDay) < 2:
            dobDay = '0' + dobDay
        if len(dobMonth) < 2:
            dobMonth = '0' + dobMonth

        dob = dobDay + '/' + dobMonth + '/' + dobYear


    except (NoSuchElementException,IndexError) as e:
        pass

    #find ethnicity
    try:
        ethnStr = webdriver.find_element(By.XPATH, ('//*[@id="movie-left"]/div[3]/div[11]/div')).text
        if 'RACE / ETHNICITY' in ethnStr:
            ethn = ethnStr.split(':')[-1].replace(' ','').capitalize()
        else:
            raise NoSuchElementException
    except (NoSuchElementException,IndexError) as e:
        pass

    #find sexual orientation
    try:
        sexStr = webdriver.find_element(By.XPATH, '//*[@id="movie-right"]/div[7]/div/p[1]').text
        if 'SEXUAL ORIENTATION' in sexStr.upper():
            sexStr = sexStr.split(':')[-1].replace(' ', '').replace('.', '').upper()
            if sexStr == 'STRAIGHT':
                sex = 'Heterosexual'
            elif sexStr == 'BISEXUAL':
                sex = 'Bisexual'
            elif sexStr == 'GAY':
                sex = 'Homosexual'
            else:
                raise NoSuchElementException
        else:
            raise NoSuchElementException
    except (NoSuchElementException,IndexError) as e:
        pass

        
    #find interests
    try:
        intStr = webdriver.find_element(By.XPATH, '//*[@id="movie-left"]/div[3]/div[2]/div').text
        if 'OCCUPATION' in intStr.upper():
            intStr = intStr.split(': ')[-1].title()
        else:
            raise NoSuchElementException

    except (NoSuchElementException,IndexError) as e:
        pass
    
    return dob, ethn, sex, intStr
    
#edits the celebrity first name in order to be analyzed by gender_guesser
#this is because the module requires for names to be in this specific format
def cleanGString(name):
    name = name.split()[0]
    name = name.capitalize()
    return name

def getGender(name):
    d = gender.Detector()
    gend = d.get_gender(cleanGString(name))

    if gend == 'mostly_male' or gend == 'male':
        gend = 'M'
    elif gend == 'mostly_female' or gend == 'female':
        gend = 'F'
    
    return gend


#find wikipedia page to search for the current city 
def WPscrape(wp):
    spGend = ''
    webdriver.get(wp)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[3]'))
        WebDriverWait(webdriver, timeout).until(element_present)
    except TimeoutException:
        pass

    #find date of birth
    try:
        wikiDob = webdriver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[contains(., "Born")]')
        strings = wikiDob.text.split()

        for string in strings:
            if string.isdecimal and len(string) < 3:
                dobDay = string.replace(',', '')
            elif string.lower() in months:
                dobMonth = str(months.index(string.lower()) + 1)
            elif string.isdecimal() and len(string) == 4:
                dobYear = string
                
        if len(dobDay) < 2:
            dobDay = '0' + dobDay
        if len(dobMonth) < 2:
            dobMonth = '0' + dobMonth

        dob = dobDay + '/' + dobMonth + '/' + dobYear
        dob = dob.replace(' ', '')

    except (NoSuchElementException,IndexError) as e:
        pass

    try:
        wikiSpouse = webdriver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[contains(., "Spouse(s)")]').text
        wikiSpouse = wikiSpouse.replace('Spouse(s)', '').split()
        delFlag = False
        spNames = []
        i = 0
        spNames.append('')
        for sp in wikiSpouse:
            if sp.startswith('('):
                delFlag = True
            if not delFlag:
                spNames[i] = spNames[i] + ' ' + sp
            if sp.endswith(')'):
                delFlag = False
                spNames.append('')
                i += 1
        
        for x in spNames:
            tmp = getGender(x.split()[0].replace(' ', ''))
            if x != '':
                try:
                    if spGend != tmp:
                        spGend = 'bi'
                except UnboundLocalError:
                    spGend = tmp

    except (NoSuchElementException,IndexError) as e:
        pass

    return spGend, dob




def downloadSocials(igLink, IL, fbLink, twLink, name):
    if igLink.startswith('https://www.instagram.com/'):
        igName = igLink.replace('https://www.instagram.com/', '')
        if igLink:
                IGscrape(igName, IL)
    else:
        print('\nInstagram URL not valid')

    if fbLink.startswith('https://www.facebook.com/'):
        FBscrape(fbLink, igName, name)
    else:
        print('\nFacebook URL not valid')

    if twLink.startswith('https://twitter.com/') or twLink.startswith('https://mobile.twitter.com/'):
        TWscrape(twLink, igName, name)
    else:
        print('\nTwitter URL not valid')


#WPscrape('https://en.wikipedia.org/wiki/Dwayne_Johnson')