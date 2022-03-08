import json
from re import X
import pandas as pd
import pyperclip
from datetime import date
import time
from IPython.display import clear_output
from googlesearch import search
from script import *

def calculate_age(born):
    day = born.split("/")[0]
    month = born.split("/")[1]
    year = born.split("/")[2]
    today = date.today()
    return today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))

celeb = json.load(open("celebrities.json","r"))
df = pd.read_csv("dataset.csv")
last = df.iloc[-1]
print(last["IG profile"])
print(len(df.index))

ready_to_start = False
for c in celeb:
    #reach last done
    if ready_to_start == False and celeb[c] != last["IG profile"]:
        continue
    elif celeb[c] == last["IG profile"]:
        ready_to_start = True
        continue
    
    #reset variables
    wp = '' 
    iw = '' 
    fb = '' 
    tw = '' 
    dob = '' 
    ethn = '' 
    sexStr = '' 
    intStr = '' 
    gd = ''
    
    print(c, celeb[c])
    print("https://www.google.com/search?q="+c.replace(" ","+"))
    webdriver.get('https://www.google.com/search?q='+c.replace(" ","+"))
    pyperclip.copy(c)
    if(input("skip?")==""):
        print("ok next")

    else: #analyze the guy
        print('Name?')

        temp_name = input()
        if temp_name == "":
            name = c
        else:
            name = temp_name
        
        query1 = name + " facebook"
        query2 = name + " twitter"
        query3 = name + ' idolwiki'
        query4 = name + ' wikipedia'
        
        
        gd = getGender(name)
        if gd == 'unknown':
            x = input('\nThis name is not in the database\nIs this a real person? [Y]/n ')
            if x == 'n' or x == 'N':
                break
        else:
            if gd != '':
                print('\nSuggestion: ' + gd + ' - Press enter to confirm')
        
        print('Gender? m/f')
        

        #start query for finding facebook profile
        for j in search(query1, tld="com", num=1, stop=1, pause=2):
            fb = j
        

        #start query for finding twitter profile
        for k in search(query2, tld="com", num=1, stop=1, pause=2):
            tw = k.split("?")[0]

        g = input() 

        if g == 'm' or g =='M':
            gend = 'M'
        elif g == 'f' or g == 'F':
            gend = 'F'
        elif g == '':
            gend = gd
        
        if gend == 'M':
            

            for i in search(query3, tld="com", num=1, stop=1, pause=2):
                iw = i
            try:
                if iw.startswith('https://idolwiki.com/'):
                    dob, ethn, sexStr, intStr = IWscrape(iw)
            except NameError:
                pass
        
            if fb != '':
                print('\nSuggestion: ' + fb + ' - Press enter to confirm')
            print("Facebook?")
            webdriver.get(fb)
    

            

            face = input()
            if face != "":
                fb = face

            if tw != '':
                print('\nSuggestion: ' + tw + ' - Press enter to confirm')
            print("Twitter?")
            webdriver.get(tw)
            
            for i in search(query4, tld="com", lang='en', num=1, stop=1, pause=2):
                wp = i

            try:
                if wp.startswith('https://en.wikipedia.org/wiki/'):
                    locStr = WPscrape(wp)
            except NameError:
                pass

            twitt = input()
            if twitt!= "":
                tw = twitt
            
            webdriver.get('https://www.google.com/search?q=' + name.replace(' ', '+') + '+age')
            #formato gg/mm/anno
            try:
                if dob != '':
                    print('\nSuggestion: ' + dob + ' - Press enter to confirm')
                bdate = input("Birthdate?")
                if bdate == '':
                    bdate = dob
            except NameError:
                bdate = input("Birthdate?")
                pass
            age = calculate_age(bdate)


            try:
                if ethn != '':
                    print('\nSuggestion: ' + ethn)
            except NameError:
                pass

            print("Ethnicity? c/af/i/as")
                
            ethnicity = input()

            while True:
                if ethnicity == "c":
                    ethnicity = "Caucasian"
                    break
                elif ethnicity == "af":
                    ethnicity = "African American"
                elif ethnicity == "i":
                    ethnicity = "Indian"
                elif ethnicity == "as":
                    ethnicity = "Asian"
                
            try:
                if intStr != '':
                    print('\nSuggestions: ' + intStr + ' - Press enter to confirm')
                interest = input("Interest?")
                if interest == '':
                    interest = intStr
            except NameError:
                interest = input("Interest?")
                pass

            
            try:
                if sexStr != '':
                    print('\nSuggestion: ' + sexStr + ' - Press enter to confirm')
                while True:
                    sex = input("Sexual? H/O/B")
                    if sex == "H" or sex == "h":
                        sex = "Heterosexual"
                        break
                    elif sex == "O" or sex == "o":
                        sex ="Homosexual"
                        break
                    elif sex == "B" or sex == "b":
                        sex ="Bisexual"
                        break
                    elif sex == '' and sexStr:
                        sex = sexStr
                        break
            except NameError:
                
                while True:
                    sex = input("Sexual? H/O/B")
                    if sex == "H" or sex == "h":
                        sex = "Heterosexual"
                        break
                    elif sex == "O" or sex == "o":
                        sex ="Homosexual"
                        break
                    elif sex == "B" or sex == "b":
                        sex ="Bisexual"
                        break

            webdriver.get('https://www.google.com/search?q=where+does+' + name.replace(' ', '+') + '+live')        
            try:
                if locStr != '':
                    print('\nSuggestion: ' + locStr + ' - Press enter to confirm')
                print("City?")      
                city = input()
                if city == '':
                    city = locStr
            except NameError:
                print("City?")      
                city = input()
                pass
            

            newCeleb = {'Celebrity name':name, 'IG profile':celeb[c], 'fb profile':fb, 'Twitter profile':tw,
            'Gender':gend, 'Age':age, 'DOB':bdate, 'Ethnicity':ethnicity, 'Interest':interest, 'Sexual orientation':sex,
            'Current city':city}
            df = df.append(newCeleb,ignore_index=True)
            print("Total Done: ",len(df.index))
            df.to_csv("dataset.csv",index=False)

            if(input("\nContinue?[Y]/n") == 'n'):
                break
            
        else:
            print('Not a male\n')
        #for i in range(10):
        #    clear_output(wait=True)
        #time.sleep(1)