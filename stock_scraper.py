#Stock Market Historical Price Quote Scraper v1
#Copyright 2018 Rakesh Bhatia

#This scraper demonstrates the use of Python with BeautifulSoup,
#requests, and the alpha_vantage API (which stores historical OHLC
#stock price data)

import os
import sys
import math
import csv
import time
import itertools
import bisect
import bs4
from bs4 import BeautifulSoup
import string
import requests
import random
import requests
import alpha_vantage
import json

def main():
    if len(sys.argv) < 3:
        print('Usage: python scrape_stock_data.py <stock symbol> <daily/weekly/monthly>')

    API_URL = "https://www.alphavantage.co/query"

    data = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": "NVDA",
        "outputsize": "compact",
        "datatype": "csv",
        "apikey": "WTX6IKTWWR57LOIQ"
        }

    data = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_' + sys.argv[2].upper() + '&symbol=' + sys.argv[1] + '&apikey=WTX6IKTWWR57LOIQ&datatype=csv')

    output_file = sys.argv[1] + '-' + sys.argv[2] + '.csv'
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            writer.writerow(row)
    #response = requests.get(API_URL, data)
    #print(response.json())
    #weekly_ohlc = json.loads(response.json())
    #print(weekly_ohlc)
    #[/code]

if __name__ == '__main__':
    sys.exit(main())
