from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import etl

DRIVER_PATH = '/path/to/chromedriver'
links_to_scrape=[]
df=pd.DataFrame()

for page in range(1, 3):
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://asunnot.oikotie.fi/myytavat-asunnot/helsinki?pagination='+ str(page))

    time.sleep(2)
    ##all_links = driver.find_element(By.XPATH, '//a[@href]')
    ##print(all_links)

    lnks = driver.find_elements(By.CLASS_NAME, "ot-card-v2")
    # traverse list
    for lnk in lnks:
        links_to_scrape.append(lnk.get_attribute("href"))
        print(lnk.get_attribute("href"))
    ##driver.quit()

for link in links_to_scrape:
    ## append dict to df
    data=pd.DataFrame([etl.extract(link)])

    data_transformed=etl.transform(data, link)

    df==df.append(data_transformed)