import json
from re import X
import pandas as pd
import pyperclip
from datetime import date
import time
from IPython.display import clear_output
from googlesearch import search
from script import *

#calculate age based on date of birth
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
    
    #reset variables to avoid raising a NameError exception on first iteration or
    #using the wrong value in the next iterations
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

        #asks for name
        temp_name = input()
        if temp_name == "":
            name = c
        else:
            name = temp_name
        
        query1 = name + " facebook"
        query2 = name + " twitter"
        query3 = name + ' idolwiki'
        query4 = name + ' wikipedia'
        
        #predicts gender based on first name
        gd = getGender(name)
        #asks for confirmation if name is not in database (e.g. the name is a brand)
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

        #asks for gender
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
        
        #if the celerity being analyzed is not a male the program skips to the next iteration
        if gend == 'M':

            #start query to find Idolwiki page
            for i in search(query3, tld="com", num=1, stop=1, pause=2):
                iw = i


            #scrapes date of birth, ethnicity, sexual orientation, interests from Idolwiki
            try:
                if iw.startswith('https://idolwiki.com/'):
                    iwDob, ethn, sexStr, intStr = IWscrape(iw)
            except NameError:
                pass
            
        
            #shows suggestion for Facebook profile
            if fb != '':
                print('\nSuggestion: ' + fb + ' - Press enter to confirm')
            print("Facebook?")
            webdriver.get(fb)

            #asks for Facebook profile link
            face = input()
            if face != "":
                fb = face

            #shows suggestion for Twitter profile
            if tw != '':
                print('\nSuggestion: ' + tw + ' - Press enter to confirm')
            print("Twitter?")
            webdriver.get(tw)
            
            #start query to find english Wikipedia page
            for i in search(query4, tld="com", lang='en', num=1, stop=1, pause=2):
                wp = i

            #asks for Twitter profile link
            twitt = input()
            if twitt!= "":
                tw = twitt 


            #scrapes spouse gender, date of birth from Wikipedia
            try:
                if wp.startswith('https://en.wikipedia.org/wiki/'):
                    spouseGend, wpDob = WPscrape(wp)
            except NameError:
                pass

            #determines sexual orientation based on gender and spouse(s) gender
            if spouseGend in ['male', 'female', 'bi']:
                if spouseGend == 'bi':
                    wikiSex = 'Bisexual'
                elif gend == spouseGend:
                    wikiSex = 'Homosexual'
                elif gend != spouseGend and spouseGend != 'bi':
                    wikiSex = 'Heterosexual'
            
            #shows google results to help in case of manual input for date of birth
            webdriver.get('https://www.google.com/search?q=' + name.replace(' ', '+') + '+age')
            #formato dd/mm/yyy
            try:
                #date of birth was found on Idolwiki AND Wikipedia
                if iwDob != '' and wpDob != '':
                    #they are the same
                    if iwDob == wpDob:
                        print('\nSuggestion: ' + iwDob + ' - Press enter to confirm')
                        print('Or enter date of birth manually DD/MM/YYYY\n')
                        bdate = input()
                        if bdate == '':
                            bdate = iwDob

                    #theres a conflict between the data found
                    else:
                        print('Wikipedia suggestion: ' + wpDob + '\nPress 1 to confirm\n')
                        print('Idolwiki suggestion: ' + iwDob + '\nPress 2 to confirm\n')
                        print('Or enter date of birth manually DD/MM/YYYY\n')
                        bdate = input()
                        if bdate == '1':
                            bdate = wpDob
                        elif bdate == '2':
                            bdate = iwDob

                #only Idolwiki's date of birth was found
                elif iwDob != '' and wpDob == '':
                    print('Suggestion: ' + iwDob + '\nPress enter to confirm')
                    print('Or enter date of birth manually DD/MM/YYYY\n')
                    bdate = input()
                    if bdate == '':
                        bdate = iwDob

                #only Wikipedia's date of birth was found
                elif wpDob != '' and iwDob == '':
                    print('Suggestion: ' + wpDob + '\nPress enter to confirm')
                    print('Or enter date of birth manually DD/MM/YYYY\n')
                    bdate = input()
                    if bdate == '':
                        bdate = wpDob
                #no date of birth was found automatically
                else:
                    bdate = input("Birthdate?")
                    
            except NameError:
                bdate = input("Birthdate?")
                pass
            
            age = calculate_age(bdate)

            #shows ethnicity's suggestion
            try:
                if ethn != '':
                    print('\nSuggestion: ' + ethn)
            except NameError:
                pass
            
            #asks for ethnicity
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
                
            #shows interests' suggestion(s)
            try:
                if intStr != '':
                    print('\nSuggestions: ' + intStr + ' - Press enter to confirm')
                #asks for interests
                interest = input("Interest?")
                if interest == '':
                    interest = intStr
            except NameError:
                interest = input("Interest?")
                pass

            #shows sexual orientation suggestion(s)
            try:
                #only Idolwiki's suggestion was found
                if sexStr != '' and wikiSex == '':
                    print('\nSuggestion: ' + sexStr + ' (Idolwiki) - Press enter to confirm')
                #only Wikipedia's suggestion was found
                elif wikiSex != '' and sexStr == '':
                    print('\nSuggestion: ' + wikiSex + ' (Wikipedia) - Press enter to confirm')
                #both Idolwiki's and Wikipedia's suggestions were found
                elif wikiSex != '' and sexStr != '':
                    #they are equal
                    if wikiSex == sexStr:
                        print('Suggestion: ' + wikiSex + ' - Press enter to confirm')
                    #they are conflicting
                    else: 
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

                    elif sexStr != '' and wikiSex == '' and sex == '':
                        sex = sexStr
                        break
                    elif wikiSex != '' and sexStr == '' and sex == '':
                        sex = wikiSex
                        break
                    elif wikiSex != '' and sexStr != '' and sex in ['1', '2', '']:
                        if wikiSex == sexStr and sex == '':
                            sex = wikiSex
                            break
                        else:
                            if sex == '1':
                                sex = sexStr
                                break
                            elif sex == '2':
                                sex = wikiSex
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

            #shows search result to help in case of manual input for current city
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