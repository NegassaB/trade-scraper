import time

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


browser_options = Options()
# browser_options.add_argument("--headless")
browser_options.add_argument("--incognito")

browser = webdriver.Chrome(options=browser_options)
browser.get("https://v3.aggr.trade/")
# time.sleep(60)
# browser.refresh()


def get_soup():
    try:
        # elem_present = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'trade')))
        elem_present = WebDriverWait(browser, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'trade')))
        # elem_present = WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'title'), 'BTCUSD '))
        # elem_present = WebDriverWait(browser, 10, 2).until(EC.presence_of_all_elements_located(By.TAG_NAME, 'li'))
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


soup = get_soup()
soup = get_soup()
if soup:
    result = soup.find_all('div', class_='trades-list hide-scrollbar -logos')

trade_dict = {}
for outter_div in result:
    print(type(outter_div))
    for li in outter_div:
        print(type(li))
        trade_dict[li.attrs['title']] = {'class': li.attrs['class']}
        inner_divs = li.find_all('div')
        while len(inner_divs) > 0:
            div = inner_divs.pop(0)
            print(type(div))
            if 'trade__price' in div.attrs['class']:
                trade_dict[li.attrs['title']].update({'trade_price': div.text.strip()})
            if 'data-timestamp' in div.attrs:
                trade_dict[li.attrs['title']].update({'trade_timestamp': div.attrs['data-timestamp']})
            if 'trade__amount' in div.attrs['class']:
                spans = div.find_all('span')
                while len(spans) > 0:
                    span = spans.pop(0)
                    if 'class' not in span.attrs.keys():
                        pass
                    else:
                        if 'trade__amount__quote' in span.attrs['class']:
                            trade_dict[li.attrs['title']].update({'trade_amount_quote': span.text.strip()})
                        if 'trade__amount__base' in span.attrs['class']:
                            trade_dict[li.attrs['title']].update({'trade_amount_base': span.text.strip()})
    #     break
    # break


print(trade_dict)
