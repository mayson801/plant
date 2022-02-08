import os
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import tweeter
from datetime import date


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

def get_prices(shop_name,url, element_type, class_value,headless=True):
    options = Options()
    failcount=0
    if headless == True:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    driver.get(url)

    while True:
        time.sleep(1)
        try:
            html = driver.page_source

            soup = BeautifulSoup(html,features="html.parser")

            find_price_element = soup.findAll(element_type, {"class": class_value})
            find_price_text = find_price_element[0].text.strip()

            driver.close()
            print(shop_name+" done")
            break
        except:
            failcount=failcount+1
            print(soup)
            print("try again")
            if failcount>10:
                find_price_text="null"
                driver.close()
                break
    return shop_name,find_price_text

def get_all_super_markets():
    tesco_price = get_prices("tesco","https://www.tesco.com/groceries/en-GB/products/296734865","span","value",False)
    asda_price = get_prices("asda","https://groceries.asda.com/product/pringles-tube-snacks/pringles-original-sharing-crisps/910003062100","strong","co-product__price pdp-main-details__price")
    morrisons_price = get_prices("morrisons","https://groceries.morrisons.com/products/pringles-original-372817011", "h2", "bop-price__current")
    sainsburys_price = get_prices("sainsburys","https://www.sainsburys.co.uk/gol-ui/product/pringles-original-190g","div","pd__cost__total undefined",False)
    if sainsburys_price[1] =="null":
        sainsburys_price = get_prices("sainsburys","https://www.sainsburys.co.uk/gol-ui/product/pringles-original-190g","div","pd__cost__total--promo undefined", False)
    coop_price = get_prices("coop","https://www.coop.co.uk/products/pringles-original-200g","p","coop-c-card__price")


    list_of_shop_prices=[tesco_price,asda_price,morrisons_price,sainsburys_price,coop_price]

    return list_of_shop_prices
def add_iteam(shop,price,date):
    dynamodb = boto3.resource('dynamodb',region_name='eu-west-2')
    table = dynamodb.Table('pringle_prices')
    table.put_item(
    Item= {
        'date': date,
        'shop': shop,
        'price': price
    })

def create_pringal_tweet():
    #change_these
    CONSUMER_KEY =  '6Gcj1k8KsqU083WLbsBVtlsE3'
    CONSUMER_SECRET = 'Wnq3A6sq4jt8yUWdJxJ4zZsFB1pRsOWpBJWtTETS8g3hZ1WOqd'
    ACCESS_TOKEN = '1352749264892530688-E7bSHpr9Ij4Oc5CsGto3n3Ck95hi1D'
    ACCESS_TOKEN_SECRET = 'VcwdphWF3YZGeKUZqycruYf7krUapED7Qjn6IEyYWipih'
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
    os.remove("temp.txt")
create_pringal_tweet()
#data = get_all_super_markets()
#print(data)
#i=0
#date = date.today().strftime("%d/%m/%Y")
#while i < len(data):
 #   shop=data[i][0]
  #  price=data[i][1]
   # #add_iteam(shop,price,date)
    #i=i+1