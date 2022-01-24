import csv
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


browser_options = Options()
# browser_options.add_argument("--headless")
browser_options.add_argument("--incognito")

browser = webdriver.Chrome(options=browser_options)
browser.get("https://v3.aggr.trade/")
time.sleep(30)

# 49800 -- trade__price
# 509K -- trade__amount__quote
# 29.8 -- trade__amount__base
# Sell -- li inside class attr
# BYBIT -- li inside class attr
# todo: write to json
# todo: no duplicates


def get_soup():
    return bs(browser.page_source, "html.parser")


def extract_save_csv():
    soup = get_soup()
    result = soup.select('.hide-scrollbar ul') # trades-list hide-scrollbar -logos
    with open('trade_watcher.csv', 'a', newline="") as trade_watcher:
        writeCSV = csv.writer(trade_watcher)
        for unorder_list in result:
            for list_item in unorder_list:
                writeCSV.writerow([f"{list_item.attrs['class'][1]}"])
                for content in list_item:
                    writeCSV.writerow([f"\t\t{content.attrs['class']}"])
                    if '-timestamp' in content.attrs['class']:
                        for val in content:
                            writeCSV.writerow([f"\t\t{val.text}"])
                    else:
                        writeCSV.writerow([f"\t\t{content.text}\n"])
        writeCSV.writerow(["\n"])


if __name__ == "__main__":
    while True:
        extract_save_csv()
        print("sleeping")
        time.sleep(2)
        print("DONE sleeping")
