#used packages
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np
import pandas as pd

#used functions
def get_html(browser):
    form = browser.find_elements_by_css_selector('#main > div > div:nth-child(3n)')
    html = form[0].get_attribute('innerHTML')
    bs = BeautifulSoup(html, 'html.parser')
    cups = bs("table")[0].findAll("tbody")
    return cups
def parse_the_table(cups):
    #create an empty table
    rows = cups[0].findAll('tr')
    cols0 = rows[0].findAll('th')
    colnames = [cols0[i].string for i in range(1, len(cols0))]
    t_names = ['time', 'cup', 'players', 'set', 'Score0', 'Score1', '01', '02', 'Hcap.0']
    for i in range(3, len(colnames)):
        t_names.append(str(colnames[i]))
    table = pd.DataFrame(columns = t_names)
    #fill in the table
    cnt = 0
    for b in range(len(cups)):
        rows = cups[b].findAll('tr')
        cols0 = rows[0].findAll('th')
        colnames = ['01', '02', 'Hcap.0']
        for n in range(4, len(cols0)):
            colnames.append(cols0[n].string)
        cup_name = cols0[0].findAll('span')[2].string
        for r in range(1, len(rows)):
            l = len(rows[r].findAll('td')[1].findAll('a'))
            table.loc[cnt, 'time'] = int_time
            table.loc[cnt, 'cup'] = cup_name
            if l != 0:
                cols1 = rows[r].findAll('td')
                players = cols1[1].findAll('div')[0]('a')[0].string 
                table.loc[cnt, 'players'] = players
                table.loc[cnt, 'set'] = None
                score_list = cols1[1].findAll('div')[1].findAll('div',{"class":"table__score"})[0].findAll("span")
                table.loc[cnt, 'Score0'] = score_list[0].string
                table.loc[cnt, 'Score1'] = score_list[1].string
                for c in range(2, len(cols1)):
                    table.loc[cnt, colnames[c-2]] = cols1[c].string
            else:
                table.loc[cnt, 'players'] = None
                cols2 = rows[r].findAll('td')
                set_num = cols2[1].findAll('div')[0].contents[2]  
                table.loc[cnt, 'set'] = set_num
                set_score = cols2[1].findAll('div')[1].span.string 
                table.loc[cnt, 'Score0'] = set_score
                table.loc[cnt, 'Score1'] = None
                for c in range(2, len(cols2)):
                    table.loc[cnt, colnames[c-2]] = cols2[c].string
            cnt += 1
    return table

#run this block and wait until it finishes ~ 10 seconds
browser = webdriver.Chrome('***path/to/chrome_driver***')
ref = '***link***'
browser.get(ref)

#now you can run this chunk of code: usually takes less than 0.2 seconds to run
x0 = time.time()
int_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
cups = get_html(browser)
table = parse_the_table(cups)
