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
    iwDob = '' 
    ethn = '' 
    sexStr = '' 
    intStr = '' 
    gd = ''
    spouseGend = ''
    wpDob = ''
    wikiSex = ''
    
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
        if gd == 'unknown' or gd == 'andy':
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

        while True:
            g = input() 
            if g == 'm' or g =='M':
                gend = 'M'
                break
            elif g == 'f' or g == 'F':
                gend = 'F'
                break
            elif g == '':
                gend = gd
                break
        
        if gend == 'M':
            for i in search(query3, tld="com", num=1, stop=1, pause=2):
                iw = i
            try:
                if iw.startswith('https://idolwiki.com/'):
                    iwDob, ethn, sexStr, intStr = IWscrape(iw)
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
            print(wp)
            

            twitt = input()
            if twitt!= "":
                tw = twitt 

            
            if wp.startswith('https://en.wikipedia.org/wiki/'):
                spouseGend, wpDob = WPscrape(wp)

            if spouseGend == 'bi':
                wikiSex = 'Bisexual'
            elif gend == spouseGend:
                wikiSex = 'Homosexual'
            elif gend != spouseGend and spouseGend != 'bi':
                wikiSex = 'Heterosexual'
            
            
            webdriver.get('https://www.google.com/search?q=' + name.replace(' ', '+') + '+age')
            #formato dd/mm/yyy
            try:
                if iwDob != '' and wpDob != '':
                    if iwDob == wpDob:
                        print('\nSuggestion: ' + iwDob + ' - Press enter to confirm')
                        print('Or enter date of birth manually DD/MM/YYYY\n')
                        bdate = input()
                        if bdate == '':
                            bdate = iwDob
                    else:
                        print('Wikipedia suggestion: ' + wpDob + '\nPress 1 to confirm\n')
                        print('Idolwiki suggestion: ' + iwDob + '\nPress 2 to confirm\n')
                        print('Or enter date of birth manually DD/MM/YYYY\n')
                        bdate = input()
                        if bdate == '1':
                            bdate = wpDob
                        elif bdate == '2':
                            bdate = iwDob
                        
                elif iwDob != '' and wpDob == '':
                    print('Suggestion: ' + iwDob + '\nPress enter to confirm')
                    print('Or enter date of birth manually DD/MM/YYYY\n')
                    bdate = input()
                    if bdate == '':
                        bdate = iwDob
                
                elif wpDob != '' and iwDob == '':
                    print('Suggestion: ' + wpDob + '\nPress enter to confirm')
                    print('Or enter date of birth manually DD/MM/YYYY\n')
                    bdate = input()
                    if bdate == '':
                        bdate = wpDob

                else:
                    bdate = input("Birthdate?")
                    
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
                    break
                elif ethnicity == "i":
                    ethnicity = "Indian"
                    break
                elif ethnicity == "as":
                    ethnicity = "Asian"
                    break
                
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
                if sexStr != '' and wikiSex == '':
                    print('\nSuggestion: ' + sexStr + ' - Press enter to confirm')
                elif wikiSex != '' and sexStr == '':
                    print('\nSuggestion: ' + wikiSex + ' - Press enter to confirm')
                elif wikiSex != '' and sexStr != '':
                    print('\nIdolwiki suggestion: ' + sexStr + ' - Press 1 to confirm')
                    print('\nWikipedia suggestion: ' + wikiSex + ' - Press 2 to confirm')
                
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
                    elif sex == '' and sexStr != '' and wikiSex == '':
                        sex = sexStr
                        break
                    elif sex == '' and wikiSex != '' and sexStr == '':
                        sex = wikiSex
                        break
                    elif wikiSex != '' and sexStr != '':
                        if sex == '1':
                            sex = sexStr
                        elif sex == '2':
                            sex = wikiSex

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

            print("City?")      
            city = input()
            

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