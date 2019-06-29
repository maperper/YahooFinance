#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 20:12:37 2019

@author: miguel-angel
"""

from bs4 import BeautifulSoup
import requests
import re


company = input('Company symbol: ')
#company = 'OKE'
url = 'https://finance.yahoo.com/quote/%s/key-statistics?p=%s' % (company, company)

r = requests.get(url).text
soup = BeautifulSoup(r, 'lxml')

tables = soup.find_all('table', attrs = {'class','table-qsp-stats Mt(10px)'})



valuation_measure = f'''Market Cap (intraday)
Enterprise Value
Trailing P/E
Forward P/E
PEG Ratio (5 yr expected)
Price/Sales (ttm)
Price/Book (mrq)
Enterprise Value/Revenue
Enterprise Value/EBITDA'''.splitlines()

stock_price_history = f'''Beta (3Y Monthly)
52-Week Change
S&P500 52-Week Change
52 Week High
52 Week Low
50-Day Moving Average
200-Day Moving Average'''.splitlines()

share_statistics = f'''Avg Vol (3 month) 3	1.11M
Avg Vol (10 day)
Shares Outstanding
Float
% Held by Insiders
% Held by Institutions
Shares Short (Jun 14, 2019)
Short Ratio (Jun 14, 2019)
Short % of Float (Jun 14, 2019)
Short % of Shares Outstanding (Jun 14, 2019)
Shares Short (prior month May 15, 2019)'''.splitlines()

dividend_splits = f'''Forward Annual Dividend Rate
Forward Annual Dividend Yield
Trailing Annual Dividend Rate
Trailing Annual Dividend Yield
5 Year Average Dividend Yield
Payout Ratio
Dividend Date
Ex-Dividend Date
Last Split Factor (new per old)
Last Split Date'''.splitlines()

fiscal_year = f'''Fiscal Year Ends
Most Recent Quarter (mrq)'''.splitlines()

profitability = f'''Profit Margin
Operating Margin (ttm)'''.splitlines()

management_effectivienss = f'''Return on Assets (ttm)
Return on Equity (ttm)'''.splitlines()

income_statement = f'''Revenue (ttm)
Revenue Per Share (ttm)
Quarterly Revenue Growth (yoy)
Gross Profit (ttm)
EBITDA
Net Income Avi to Common (ttm)
Diluted EPS (ttm)
Quarterly Earnings Growth (yoy)'''.splitlines()

balance_sheet = f'''Total Cash (mrq)
Total Cash Per Share (mrq)
Total Debt (mrq)
Total Debt/Equity (mrq)
Current Ratio (mrq)
Book Value Per Share (mrq)'''.splitlines()

cash_flow_statement = f'''Operating Cash Flow (ttm)
Levered Free Cash Flow (ttm)'''.splitlines()


data_names_dict = {'Valuation Measures':valuation_measure, 'Stock Price History':stock_price_history,\
              'Share Statistics':share_statistics, 'Dividends & Splits':dividend_splits,\
              'Fiscal Year':fiscal_year, 'Profitability':profitability,\
         'Management Effectiveness':management_effectivienss,'Income Statement':income_statement,\
         'Balance Sheet':balance_sheet,'Cash Flow Statement':cash_flow_statement}

data_names = ['Valuation Measures','Stock Price History', 'Share Statistics','Dividends & Splits',\
              'Fiscal Year', 'Profitability','Management Effectiveness','Income Statement',\
         'Balance Sheet','Cash Flow Statement']

data_dict = dict()
data_dict_without_clean = dict()

for table, name in zip(tables, data_names):
    pattern_values = re.compile('\<td class="Fz\(s\) Fw\(500\) Ta\(end\) Pstart\(10px\) Miw\(60px\)" data-reactid="\d+">(.*?)\<\/td\>')
    # pattern_titles = re.compile('\<span data-reactid="\d+"\>(.*?)\<\/span>')
    values = pattern_values.findall(str(table))
    # titles = pattern_titles.findall(str(table))
    titles = data_names_dict[name]
    clean_values = list()
    for value in values:
        if '<span data-reactid=' in value:
            clean_values.append('N/A')
        else:
            clean_values.append(value)
    #print(dict(zip(titles,values)))
    data_dict[name] = dict(zip(titles, clean_values))
   # data_dict_without_clean[name] = dict(zip(titles, values)) 