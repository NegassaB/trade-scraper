import csv
import time

from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString, Tag

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


browser_options = Options()
browser_options.add_argument("--headless")
browser_options.add_argument("--incognito")

browser = webdriver.Chrome(options=browser_options)
browser.get("https://v3.aggr.trade/")
time.sleep(30)

soup = bs(browser.page_source, "html.parser")
result = soup.find_all('div', class_='trades-list hide-scrollbar -logos')

trade_list = {}
for res in result:
    for list_items in res:
        trade_list[list_items.attrs['title']] = {'class': list_items.attrs['class']}
        print(f"{list_items.attrs['class']} -- {list_items.attrs['title']}")
        divs = list_items.find_all('div')
        while len(divs) > 0:
            div = divs.pop(0)
            if 'trade__price' in div.attrs['class']:
                trade_list[list_items.attrs['title']].update({'trade_price': div.text.strip()})
            if 'data-timestamp' in div.attrs:
                trade_list[list_items.attrs['title']].update({'trade_timestamp': div.attrs['data-timestamp']})
            if 'trade__amount' in div.attrs['class']:
                spans = div.find_all('span')
                while len(spans) > 0:
                    span = spans.pop(0)
                    if 'class' not in span.attrs.keys():
                        pass
                    else:
                        if 'trade__amount__quote' in span.attrs['class']:
                            trade_list[list_items.attrs['title']].update({'trade_amount_quote': span.text.strip()})
                        if 'trade__amount__base' in span.attrs['class']:
                            trade_list[list_items.attrs['title']].update({'trade_amount_base': span.text.strip()})
        # break
    # break

print(trade_list)

{
    'BINANCE_FUTURES:btcusdt': {
        'class': ['trade', '-BINANCE_FUTURES', '-buy', '-level-0'],
        'trade_price': '36557',
        'trade_amount_quote': '167K',
        'trade_amount_base': '4.574',
        'trade_timestamp': '1643115788860'
    },
    'BYBIT:BTCUSD': {
        'class': ['trade', '-BYBIT', '-sell', '-level-0'],
        'trade_price': '36558.5',
        'trade_amount_quote': '120K',
        'trade_amount_base': '3.2851',
        'trade_timestamp': '1643115800000'
    },
    'BINANCE_FUTURES:btcusd_perp': {
        'class': ['trade', '-BINANCE_FUTURES', '-sell', '-level-0'],
        'trade_price': '36566.8',
        'trade_amount_quote': '145K',
        'trade_amount_base': '3.9544',
        'trade_timestamp': '1643115795237'
    },
    'BITMEX:XBTUSD': {
        'class': ['trade', '-BITMEX', '-sell', '-level-0'],
        'trade_price': '36551.0',
        'trade_amount_quote': '140K',
        'trade_amount_base': '3.8304',
        'trade_timestamp': '1643115815532'
    },
    'FTX:BTC-PERP': {
        'class': ['trade', '-FTX', '-sell', '-level-0'],
        'trade_price': '36599.0',
        'trade_amount_quote': '115K',
        'trade_amount_base': '3.1444',
        'trade_timestamp': '1643115795394'
    },
    'BYBIT:BTCUSDT': {
        'class': ['trade', '-BYBIT', '-sell', '-level-0'],
        'trade_price': '36542.0',
        'trade_amount_quote': '180K',
        'trade_amount_base': '4.939',
        'trade_timestamp': '1643115800000'
    }
}
