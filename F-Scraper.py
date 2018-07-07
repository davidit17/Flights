


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 
import sqlite3
from datetime import date
import datetime




# get all content from 2 pages

url = "https://www.gulliver.co.il/Content/SalePage.aspx?pageId=264&module=Flights"
r = requests.get(url)
c = r.content
soup=BeautifulSoup(c,"html.parser")
all = soup.find_all("ul")

url2 = 'https://www.gulliver.co.il/Content/SalePage.aspx?pageId=99&module=Flights'
r2 = requests.get(url2)
c2 = r2.content
soup2=BeautifulSoup(c2,"html.parser")
all2 = soup2.find_all("ul")  




# get relevan data from mivzaim page into array

sale = []

for i in range(len(soup.find_all("strong",{'style':'font-size:1em;'}))):
    m={}
    m['destination'] = soup.find_all("strong",{'style':'font-size:1em;'})[i].text.replace('\t', '')
    m['company'] = soup.find_all("span", {'class':'LastDeals_hotel'})[i].text.replace('\t', '')
    m['vacationDate'] = soup.find_all("span", {'class':'LastDeals_Date'})[i].text.replace('\t', '')
    m['PriceInDollars'] = int(soup.find_all("strong", {'class':'LastDeals_price'})[i].text.replace('$',''))
    m['offerDate'] = date.today()
    sale.append(m)




# get relevan data from last minute page into array

last = []

for i in range(len(all2)):
    m={}
    m['destination'] = soup2.find_all("strong",{'style':'font-size:1em;'})[i].text.replace('\t', '').split()[0]
    m['company'] = 'Last Minute'
    m['vacationDate'] = soup2.find_all("span", {'class':'LastDeals_Details'})[i].text.replace('מחיר לאדםתאריכי טיסה','') 
    m['PriceInDollars'] = int(soup2.find_all("strong", {'class':'LastDeals_price'})[i].text.replace('$','').replace('€',''))
    m['offerDate'] = date.today()
    last.append(m)




# insert arrays into dataframes

df=pd.DataFrame(sale)
cols = df.columns.tolist()
cols = [cols[3] , cols[2] , cols[1],cols[4],cols[0]]
df = df[cols] 

df2 = pd.DataFrame(last)
df2 = df2[cols]

#merge the 2 dfs
merged = df2.append(df,ignore_index=True)



# sql 


def create():
    conn=sqlite3.connect("flights.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS flights (id INTEGER PRIMARY KEY,offerDate INTEGER,destination TEXT,company TEXT,vacationDate TEXT,PriceInDollars INTEGER)")
    conn.commit()
    conn.close()
          
    
def gettable():
    conn = sqlite3.connect("flights.db")
    table = pd.read_sql_query("SELECT * FROM flightData", conn)
    return table
    conn.close()        
    

def drop_table():
    conn = sqlite3.connect("flights.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE flightData")
    conn.commit()
    conn.close()
    
def insert(merged) :  
    conn = sqlite3.connect("flights.db")   
    df = merged
    df.to_sql("flightData", conn, if_exists='append')
    conn.commit()
    conn.close()

    
def findLastDate():
    conn=sqlite3.connect("flights.db") 
    cur = conn.cursor()
    lastDate = cur.execute("SELECT distinct max(offerDate) FROM flightData").fetchone()[0]
    conn.close()
    return lastDate




# insert to db if offer date if offerdate is not exist

if  (datetime.datetime.strptime(findLastDate(),"%Y-%m-%d").date()) < max(merged.offerDate) :
    insert(merged)
    print("inserted")
else :
    print ("Already in database")
    print ("DB last date :" , findLastDate())
    print ("current date :" ,max(merged.offerDate))










