import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import tweeter


def close(self):
        # Remove specific tmp dir of this "run"
        shutil.rmtree(self._tmp_folder)

        # Remove possible core dumps
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if 'core.headless-chromi' in file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

def get_prices(shop_name,url, element_type, class_value,):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url)
    time.sleep(10)

    html = driver.page_source

    soup = BeautifulSoup(html,features="html.parser")

    find_price_element = soup.findAll(element_type, {"class": class_value})
    find_price_text = find_price_element[0].text.strip()

    driver.close()
    print(shop_name+" done")
    return shop_name,find_price_text

def get_all_super_markets():
    tesco_price = get_prices("tesco","https://www.tesco.com/groceries/en-GB/products/296734865","span","value")
    asda_price = get_prices("asda","https://groceries.asda.com/product/pringles-tube-snacks/pringles-original-sharing-crisps/910003062100","strong","co-product__price pdp-main-details__price")
    morrisons_price = get_prices("morrisons","https://groceries.morrisons.com/products/pringles-original-372817011", "h2", "bop-price__current")
    sainsburys_price = get_prices("sainsburys","https://www.sainsburys.co.uk/gol-ui/product/pringles-original-190g","div","pd__cost__total undefined")
    coop_price = get_prices("coop","https://www.coop.co.uk/products/pringles-original-200g","p","coop-c-card__price")

    list_of_shop_prices=[tesco_price,asda_price,morrisons_price,sainsburys_price,coop_price]
    return list_of_shop_prices

def create_pringal_tweet():
    #change_these
    CONSUMER_KEY = '###############'
    CONSUMER_SECRET = '##################'
    ACCESS_TOKEN = '#################'
    ACCESS_TOKEN_SECRET = '#############'
    list_of_shop_prices = get_all_super_markets()
    with open('temp.txt', 'w') as f:
        for shop in list_of_shop_prices:
          if '£' in shop[1]:
                    f.write(shop[0] +" " + shop[1] + "\n")
          else:
                    f.write(shop[0] +" £" + shop[1]+ "\n")
    with open('temp.txt', 'r') as f:
        #tweeter.tweet(f.read(),CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        print(f.read())