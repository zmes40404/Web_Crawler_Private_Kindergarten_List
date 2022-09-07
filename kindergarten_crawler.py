from lib2to3.pgen2 import driver
import re 
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from openpyxl import load_workbook

def typeSelect_click():     # type select 私立
    type_name_btn = driver.find_element(By.ID, "ckSPub1")
    type_name_btn.click()
    time.sleep(0.5)

def careService_click():    # 兼辦國民小學兒童課後照顧服務select 無
    care_service_btn = driver.find_element(By.ID, "rdChildSvc0")
    care_service_btn.click()
    time.sleep(0.5)

def cityMenu_click():   # 縣市select台北市
    #   option[value='01'] 基隆市、02 台北市、03 新北市、04 宜蘭縣、05 桃園市、06 新竹市、07 新竹縣
    #   08 苗栗縣、09 台中市、11 彰化縣、12 南投縣、13 雲林縣、14 嘉義市、15 嘉義縣
    #   16 台南市、18 高雄市、20 屏東縣、21 台東縣、22 花蓮縣、23 澎湖縣、24 金門縣
    #   25 連江縣
    city_menu = driver.find_element(By.CSS_SELECTOR, "option[value='01']")
    city_menu.click()
    time.sleep(0.5)

def searchBtn_click():  # 搜尋按鈕click
    search_btn = driver.find_element(By.NAME, "btnSearch")
    search_btn.click()
    time.sleep(5)

def nextPage_click():   # Click Next Page
    nextpage_btn = driver.find_element(By.ID, "PageControl1_lbNextPage")
    nextpage_btn.click()
    time.sleep(2)

# Setting Chrome webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-snadbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('chromedriver', options=chrome_options) #   Run on Colab need this line
driver = webdriver.Chrome()

search_page_url = "https://ap.ece.moe.edu.tw/webecems/pubSearch.aspx" # 全國幼保資訊網基本資料查詢
driver.get(search_page_url)

time.sleep(1)

# Selenium 模仿人類操作瀏覽器
# type select 私立
typeSelect_click()

# 兼辦國民小學兒童課後照顧服務select 無
careService_click()

# 縣市select台北市
cityMenu_click()

# 搜尋按鈕click
searchBtn_click()

html_source = driver.page_source # get page data
soup = BeautifulSoup(html_source, 'html.parser')

# Get result page number
pageNum = soup.find("span", id="PageControl1_lblTotalPage")  

# Define empty list
all_schname = []
all_city = []
all_telephone = []
all_charger = []
all_peopleNumber = []
all_add = []

# Get parser context
if pageNum is None: # if only one page ignore change page process
    # Get all school name
    for schname in soup.find_all('h4'):
        all_schname.append(schname.string)

    # Get all city info
    for city in soup.find_all("span", id=re.compile("^GridView1_lblCity")):
        all_city.append(city.string)

    # Get phone number
    for tele in soup.find_all("span", id=re.compile("^GridView1_lblTel")):
        all_telephone.append(tele.string)
    
    # Get charger name
    for charger in soup.find_all("span", id=re.compile("^GridView1_lblCharge")):
        all_charger.append(charger.string)

    for peoNum in soup.find_all("span", id=re.compile("^GridView1_lblGenStd")):
        all_peopleNumber.append(peoNum.string)

    # Get address
    for add in soup.find_all("a", id=re.compile("^GridView1_hlAddr")):
        all_add.append(add.string)

    nextPage_click()
    html_source = driver.page_source # get page data    
    soup = BeautifulSoup(html_source, 'html.parser')
    #print(soup.prettify())

else:               # if many pages run every page and get parser context
    for page in range(int(pageNum.string)):
        # Get all school name
        for schname in soup.find_all('h4'):
            all_schname.append(schname.string)

        # Get all city info
        for city in soup.find_all("span", id=re.compile("^GridView1_lblCity")):
            all_city.append(city.string)

        # Get phone number
        for tele in soup.find_all("span", id=re.compile("^GridView1_lblTel")):
            all_telephone.append(tele.string)
        
        # Get charger name
        for charger in soup.find_all("span", id=re.compile("^GridView1_lblCharge")):
            all_charger.append(charger.string)

        # Get people number
        for peoNum in soup.find_all("span", id=re.compile("^GridView1_lblGenStd")):
            all_peopleNumber.append(peoNum.string)

        # Get address
        for add in soup.find_all("a", id=re.compile("^GridView1_hlAddr")):
            all_add.append(add.string)
        
        nextPage_click()
        html_source = driver.page_source # get page data    
        soup = BeautifulSoup(html_source, 'html.parser')
        #print(soup.prettify())

driver.quit()

# Write crawler into excel
col1 = "School_Name"
col2 = "City"
col3 = "Charger"
col4 = "Telephone"
col5 = "People_number"
col6 = "Address"
data = pd.DataFrame({col1:all_schname, col2:all_city, col3:all_charger, col4:all_telephone, col5:all_peopleNumber,col6:all_add})
data.to_excel('基隆市私立幼兒園名單.xlsx', sheet_name='sheet1', index=False)
