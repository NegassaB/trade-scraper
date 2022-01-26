import json
import sys
import time

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import (expected_conditions as EC, ui)


browser_options = Options()
# browser_options.add_argument("--headless")
browser_options.add_argument("--incognito")

browser = webdriver.Chrome(options=browser_options)
browser.get("https://v3.aggr.trade/")
trade_dict = {}


def get_soup():
    try:
        elem_present = ui.WebDriverWait(browser, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'trade')))
    except Exception:
        print("page is not ready, retrying")
        time.sleep(1)
        get_soup()
    else:
        if elem_present:
            print("page is ready to be scrapped")
            return bs(browser.page_source, "html.parser")
        else:
            print("WHAT THE ACTUAL FUCK")


def save_2_file(trade_dict):
    with open('trade_watcher.json', 'w+') as trade_watcher:
        json.dump(trade_dict, trade_watcher)

    time.sleep(2)


def extract_trades():
    price = ""

    soup = get_soup()
    time.sleep(0.5)
    soup = get_soup()
    result = soup.find_all('div', class_='trades-list hide-scrollbar -logos')
    for outter_div in result:
        for li in outter_div:
            inner_divs = li.find_all('div')
            while len(inner_divs) > 0:
                div = inner_divs.pop(0)
                if 'trade__price' in div.attrs['class']:
                    price = div.text.strip()
                    trade_dict[price] = {'title': li.attrs['title']}
                if 'data-timestamp' in div.attrs:
                    trade_dict[price].update({'trade_timestamp': div.attrs['data-timestamp']})
                if 'trade__amount' in div.attrs['class']:
                    spans = div.find_all('span')
                    while len(spans) > 0:
                        span = spans.pop(0)
                        if 'class' not in span.attrs.keys():
                            pass
                        else:
                            if 'trade__amount__quote' in span.attrs['class']:
                                trade_dict[price].update({'trade_amount_quote': span.text.strip()})
                            if 'trade__amount__base' in span.attrs['class']:
                                trade_dict[price].update({'trade_amount_base': span.text.strip()})


def runner():
    while True:
        try:
            extract_trades()
            save_2_file(trade_dict)
        except Exception as e:
            print(e, exc_info=True)
            browser.close()
            sys.exit(1)


if __name__ == "__main__":
    runner()
