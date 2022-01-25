import csv
import time

from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString, Tag

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


soup = bs(browser.page_source, "html.parser")
result = soup.find_all('div', class_='trades-list hide-scrollbar -logos')

trade_list = {}
for res in result:
    for list_items in res:
        print(f"{list_items.attrs['class']} -- {list_items.attrs['title']}") 
        divs = list_items.find_all('div')
        while len(divs) > 0:
            div = divs.pop(0)
            if 'trade__price' in div.attrs['class']:
                trade_list[f"{list_items.attrs['class']} -- {list_items.attrs['title']}"] = {'trade__price': div.text}
            elif 'data-timestamp' in div.attrs:
                trade_list[f"{list_items.attrs['class']} -- {list_items.attrs['title']}"] = {'trade__timestamp': div.text}
            elif 'trade__amount' in div.attrs['class']:
                spans = div.find_all('span')
                print(spans)
                while len(spans) > 0:
                    span = spans.pop(0)
                    if isinstance(span, NavigableString):
                        pass
                    else:
                        if 'trade__amount__quote' in span.attrs['class']:
                            trade_list[f"{list_items.attrs['class']} -- {list_items.attrs['title']}"] = {'trade__amount__quote': span.text}
                        elif 'trade__amount__base' in span.attrs['class']:
                            trade_list[f"{list_items.attrs['class']} -- {list_items.attrs['title']}"] = {'trade__amount__base': span.text}
                        else:
                            pass
            else:
                pass
        break
    break


for res in result:
    for list_items in res:
        print(f"{list_items.attrs['class']} -- {list_items.attrs['title']}")
        for content in list_items:
            if isinstance(content, NavigableString):
                pass
            else:
                print(f"{content.attrs}\n")
                # print(f"{content.contents}")
                # print(f"{content.children}\n")
                if "trade__amount" in content.attrs:
                    print(content.span.next_sibling)
                for child in content:
                    if isinstance(child, Tag):
                        for sib in child:
                            # type(sib)
                            if isinstance(sib, NavigableString):
                                pass
                            else:
                                print(f"{sib.attrs} {sib.text.strip()}")
                            # print(sib.attrs)
                    print(f"{content.attrs['class']} {content.text.strip()}")
                # if 'data-timestamp' in content.attrs:
                #     print(content.attrs['data-timestamp'])
            # print(content.class)
        break
    break


def get_soup():
    return bs(browser.page_source, "html.parser")


def extract_save_csv():
    soup = get_soup()
    result = soup.find_all('div', class_='trades-list hide-scrollbar -logos')
    with open('trade_watcher.csv', 'a', newline="") as trade_watcher:
        writeCSV = csv.writer(trade_watcher)
        for res in result:
            for list_item in res:
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
