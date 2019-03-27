import re
import requests
from time import mktime
import os
import datetime
import pandas as pd
import json

''' 
	This script will be used for downloading csv files from yahoofinance.com.
	So, it must be executed at the begining, except you have downloaded csv files by yourself.
	Select two dates at first in order to get the interval for csv files.
	Before that, download from https://www.nasdaq.com/screening/company-list.aspx 	
	a csv file of companies you want get their data at "finance.yahoo.com".
	Save it with "companylist.csv" name in the same folder of this file.
	Execute this using "python download_csv.py" in a terminal.
'''

# Change this two varibles
print('Select two dates for the time interval separated by forward slash. For example:')
print('30/03/2010')

start_date_ = input('Start date:')
end_date_ = input('End date:')

start_date = str(int(mktime(datetime.datetime.strptime(start_date_,'%d/%m/%Y').timetuple())))
end_date = str(int(mktime(datetime.datetime.strptime(end_date_, '%d/%m/%Y').timetuple())))


work_dir = os.getcwd()

try: 
    os.mkdir('csv')
except:
    pass

df = pd.read_csv('companylist.csv')

stock_list = list(df.Symbol)
stock_name = list(df.Name)
full_dict_symbol_name = dict()

for key, value in zip(stock_list,stock_name):
    full_dict_symbol_name[key] = value
    
crumble_link = 'https://finance.yahoo.com/quote/{}/history?p={}'
crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
cookie_regex = r'set-cookie: (.*?);'
quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}'
counting_rows = dict()

#for ii in range(0,10):
#    symbol = stock_list[ii] #  Uncomment this two lines if you want to check how this script works with fewer iterations.

for symbol in stock_list:
    link = 'https://finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d'.format(symbol, start_date, end_date)
    session = requests.Session()
    response = session.get(link)
    text = str(response.content)
    match = re.search(crumble_regex, text)
    crumbs = match.group(1)
    cookie = session.cookies.get_dict()
    # get crumbs
    text = str(response.content)
    match = re.search(crumble_regex, text)
    crumbs = match.group(1)  
    # get cookie    
    cookie = session.cookies.get_dict()    
    url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumbs)
    r = requests.get(url, cookies=session.cookies.get_dict(), timeout=5, stream=True)
    out = r.text
    filename = '%s_start_date=%s_end_date=%s.csv' % (symbol, start_date_.replace('/','-'), end_date_.replace('/','-'))
    # Counting the rows for deleting the ones that not have the same than others.
    counting_rows[filename] = len(out.splitlines())
    with open('csv/' + filename,'w') as file:
        file.write(out)

# Deleting csv files
dict_symbol_name = dict()
number_of_rows = max(counting_rows.values())

for x in counting_rows.keys():
    if counting_rows[x] < number_of_rows:
        os.remove('csv/' + x)
    else:
        key = x.split('_')[0]
        dict_symbol_name[key] = full_dict_symbol_name[key]
        
with open('list_of_companies.json', 'w') as file:
    json.dumps(dict_symbol_name)    