import requests
from bs4 import BeautifulSoup
from datetime import date
import sqlite3
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np
import random



def get_number_of_pages(url):
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    num_pages=soup.select(".ng-binding").text
    num_pages=num_pages.partition('/')[1]

    return num_pages


def get_links():

    DRIVER_PATH = '/path/to/chromedriver'
    links_to_scrape=[]
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    for page in range(1, 4):
        
        driver.get('https://asunnot.oikotie.fi/myytavat-asunnot/helsinki?pagination='+ str(page))

        time.sleep(0.5)

        lnks = driver.find_elements(By.CLASS_NAME, "ot-card-v2")
        # traverse list
        for lnk in lnks:
            links_to_scrape.append(lnk.get_attribute("href"))
            print(lnk.get_attribute("href"))
    
    driver.quit()
    
    return links_to_scrape
    

# Making a GET request
def get_data(link, headers):


    r = requests.get(link, headers= headers)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    data=soup.select(".info-table__row")

    items={}
    for item in data:
        for i,j in zip(item.find_all("dt"), item.find_all("dd")):
            title=i.text.strip()
            value=j.text.strip()
            items[title]=value
            items['link']=link
    print(items)
    print(r)
    return items


def transform(df):

    columns_selected=["Sijainti",
                "Kaupunginosa",
                "link",
                "Kerros",
                "Asuinpinta_ala",
                "Huoneiston_kokoonpano",
                "Huoneita",
                "Kunto",
                "Parveke",
                "Velaton_hinta",
                "Myyntihinta",
                "Neliohinta",
                "Rahoitusvastike",
                "Hoitovastike",
                "Yhtiovastike",
                "Rakennuksen_tyyppi",
                "Rakennusvuosi",
                "Rakennusmateriaali",
                "Energialuokka",
                "Tontin_omistus",
                "Kerroksia",
                "Hissi",
                "Asumistyyppi",
                "Asunnossa_sauna",
                "pvm",
                "id",
                "status",
                "myyntikesto"]

    columns_to_float=['Velaton_hinta', 'Myyntihinta', 'Neliohinta', 'Rahoitusvastike', 'Hoitovastike', 'Yhtiovastike']


    df["pvm"]=date.today()
    df["id"]=df['link'].astype(str).str[-8:]
    df["status"]="aktiivinen"
    df["myyntikesto"]="NaN"

    df.columns = df.columns.str.replace('ä', 'a')
    df.columns = df.columns.str.replace('ö', 'o')
    df.columns = df.columns.str.replace('[-," "]', '_')
    
    for col in columns_selected:
        if col not in df.columns:
            df[col] = np.NaN

    df=to_float(df, columns_to_float)

    df=df[columns_selected]

    df=df.loc[df["Asumistyyppi"]!="Asumisoikeus"]
    df=df.loc[df["Huoneita"]<4]

    df["Hoitovastike_m2"]=df["Hoitovastike"]/df["Asuinpinta_ala"]

    return df


def extract(links_to_scrape):

    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    df=pd.DataFrame()
    countt=0
    errors=0
    for link in links_to_scrape:
    ## append dict to df

        time.sleep(random.randint(1,2))
        try:
            data=pd.DataFrame([get_data(link, headers)])

            df=df.append(data)
            countt+=1
            print(countt)
        except Exception as e:
            print(e)
            errors+=1
            print(f'errors {errors}')
    return df


def load(df):
    conn=sqlite3.connect('oikotie.db')

    df.to_sql("oikotie_asunnot", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


def upsert():
    conn=sqlite3.connect('oikotie.db')
    c=conn.cursor()

    c.execute('''UPDATE asunnot
                SET (status, myyntikesto) =('myyty', datetime('now')-pvm)
                WHERE asunnot.id IN (select a.id as id from oikotie_asunnot a
                left join stg_asunnot sa on a.id=sa.id
                where sa.id IS NULL);''')

    c.execute('''INSERT INTO asunnot
                WITH RECURSIVE uudet as (select sa.* from stg_oikotie_asunnot sa 
                left join oikotie_asunnot a on sa.id=a.id
                where a.id IS NULL)
                SELECT * FROM uudet;''')

    conn.commit()
    conn.close()

def load_aggregates(df):

    df_aggregates=df.describe()
    df_aggregates.reset_index(inplace=True)
    df_aggregates=df_aggregates.rename(columns = {'index':'metric'})
    df_aggregates["pvm"]=date.today()
    conn=sqlite3.connect('oikotie.db')

    df.to_sql("asunnot_history", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()




##Utils

def to_float(df, columns):

    replacement = {
        "/m2": "",
        "€": "",
        '\s+': '',
        ',':'.',
        '/kk': '',
        ' ': ''
        }

    for column in columns:
        
        df[column] = pd.to_numeric(df[column].astype(str).str.replace(' ', '').replace(replacement, regex=True), errors='coerce').fillna(np.NaN).astype(float)

    df['Kerros']=df['Kerros'].astype(str).str.split('/').str[0].astype(float)
    df['Asuinpinta_ala']=df['Asuinpinta_ala'].astype(str).str.split(' ').str[0].str.replace(',', '.').astype(float)

    return df

   

    

    



