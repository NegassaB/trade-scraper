import json
import time

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


browser_options = Options()
browser_options.add_argument("--headless")
browser_options.add_argument("--incognito")

browser = webdriver.Chrome(options=browser_options)
browser.get("https://v3.aggr.trade/")
time.sleep(30)


def get_soup():
    return bs(browser.page_source, "html.parser")


def save_2_file(trade_dict):
    with open('trade_watcher.json', 'a') as trade_watcher:
        json.dump(trade_dict, trade_watcher)

    print(trade_dict)


def extract_trades():
    trade_dict = {}
    soup = get_soup()
    result = soup.find_all('div', class_='trades-list hide-scrollbar -logos')
    for res in result:
        for list_items in res:
            trade_dict[list_items.attrs['title']] = {'class': list_items.attrs['class']}
            divs = list_items.find_all('div')
            while len(divs) > 0:
                div = divs.pop(0)
                if 'trade__price' in div.attrs['class']:
                    trade_dict[list_items.attrs['title']].update({'trade_price': div.text.strip()})
                if 'data-timestamp' in div.attrs:
                    trade_dict[list_items.attrs['title']].update({'trade_timestamp': div.attrs['data-timestamp']})
                if 'trade__amount' in div.attrs['class']:
                    spans = div.find_all('span')
                    while len(spans) > 0:
                        span = spans.pop(0)
                        if 'class' not in span.attrs.keys():
                            pass
                        else:
                            if 'trade__amount__quote' in span.attrs['class']:
                                trade_dict[list_items.attrs['title']].update({'trade_amount_quote': span.text.strip()})
                            if 'trade__amount__base' in span.attrs['class']:
                                trade_dict[list_items.attrs['title']].update({'trade_amount_base': span.text.strip()})
    save_2_file(trade_dict)


if __name__ == "__main__":
    while True:
        extract_trades()
        print("sleeping")
        browser.refresh()
        time.sleep(2)
        print("DONE sleeping")
