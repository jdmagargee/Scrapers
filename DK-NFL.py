#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3


#There is a folder with the whole project. accidental backup somewhere, idk where though
#real weird move by DK to keep every single line for the season up, I guess they expect favorable movement if any

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager
pd.set_option("display.max_rows", None, "display.max_columns", None)



driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome(executable_path= '/Users/johnmagargee/Downloads/chromedriver')

driver.get('https://sportsbook.draftkings.com/leagues/football/3?category=game-lines&subcategory=game')



content = driver.page_source
soup = BeautifulSoup(content, features = "html.parser")
driver.quit()

##https://oxylabs.io/blog/python-web-scraping##
results = []
for elem in soup.findAll(attrs='event-cell__team-info'):
    name = elem.find('span')
    if name not in results:
        results.append(name.text)

results2 = []

o = 0
while o < len(results):
    if o == 0 or o%2 == 0:
        results2.append(results[o+1])
    elif o %2 != 0:
        results2.append(results[o-1])
    o+=1

dfname = pd.DataFrame({'Names': results,
                       'Opponents':results2})

l = 0
dates = []
today = date.today()
while l < len(dfname):
    dates.append(today)
    l += 1
dfDate = pd.DataFrame({'Date': dates})

results = []
for elem in soup.findAll(attrs='sportsbook-outcome-cell__label-line-container'):
    line = elem.find('span')
    results.append(line.text)

results2 = []
for i in results:
    try:
        k = float(i)
        results2.append(i)
    except:
        pass

results3 = []

o = 0
while o < len(results2):
    if o == 0 or o%2 == 0:
        results3.append(results2[o+1])
    elif o %2 != 0:
        results3.append(results2[o-1])
    o+=1

dfline = pd.DataFrame({'DKLine': results2,
                       'DKOppLine': results3})


results = []
for elem in soup.findAll(attrs='sportsbook-outcome-cell__element'):
    odds = elem.find('span')
    results.append(odds)


results2 = []
for i in results:
    try:
        k = (str(i).index('color">'))
        #print('k is ',k)
        l = (str(i).index('span>'))
        #print('l is',l)
        try:
            j = float(str(i)[k + 7:l - 2])
            results2.append(j)
            # print(j)
        except:
            # print(i[k+4,l-3])
            pass
    except:
        # print('skipping')
        pass

#print('lres2', len(results2))
results3 = []

o = 0
while o < len(results2):
    if o == 0 or o%2 == 0:
        results3.append(results2[o+1])
    elif o %2 != 0:
        results3.append(results2[o-1])
    o+=1



dfodds = pd.DataFrame({'DKOdds': results2,
                       'DKOppOdds': results3})
dfodds = dfodds.dropna(how = 'all')

dfTotalDK = pd.merge(dfname,dfline,left_index=True, right_index=True)
#print(dfTotalDK)
dfodds.reset_index(inplace=True)
dfTotalDK = pd.merge(dfTotalDK,dfodds,left_index=True, right_index=True)
dfodds.reset_index(inplace=True)
dfTotalDK = pd.merge(dfTotalDK,dfDate,left_index=True, right_index=True)

print(dfTotalDK)
