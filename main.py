import streamlit as st
# from streamlit_gsheets import GSheetsConnection
# import streamlit_shadcn_ui as ui



# my_range = ui.date_picker(label='Select Date Range', mode='range', key='my_range', default_value=None)

# st.selectbox('Publication',(
#     'Sun Star Online',
#     'Other'
#     ), key='selectbox_pub')



# link = 'https://docs.google.com/spreadsheets/d/1eCYzx8VaIi8jE1tLYXBb7KF5eq_bg2_zcnNxbXd_bnI/edit?usp=sharing'

# conn = st.connection('gsheets', type=GSheetsConnection)

# data = conn.read(spreadsheet=link, usecols=[0,2])
# st.dataframe(data)


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime
import pandas as pd
from os import getcwd
import random

def create_driver():

    userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36	'
    ]

    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') # 
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument(f'user-agent={random.choice(userAgents)}')

    return webdriver.Chrome(options=options)

def main(_site):

    _dir = getcwd()

    # df_archive = pd.read_excel(f'{_dir}/pna_archive.xlsx')
    # url_list = df_archive['URL'].to_list()

    _links = []
    _dates = []
    _timescraped = []
    url_list = []

    print(f'----Scraping GMA News Online----')
    print('----Gathering New Links----')
    for i in range(1, 6):
        _page = f'{_site}{i}'
        driver = create_driver()
        driver.get(_page)
        
        container = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, 'category-content')))
        _articles = container.find_elements(By.CLASS_NAME, 'flex-1')
        for _article in _articles:
            _datestr = _article.find_element(By.CSS_SELECTOR, 'span[class="ms-1.5 block"]').text
            if 'Updated on' in _datestr:
                _datestr = _datestr.split(' Updated on ')[-1]
            _date = datetime.strptime(_datestr, '%B %d, %Y, %I:%M %p')
            datediff = (datetime.today() - _date).days

            if datediff > 60:
                break
            else:
                _url = _article.find_element(By.TAG_NAME, 'a').get_attribute('href')

                if _url not in url_list:
                    url_list.append(_url)
                    _links.append(_url)
                    _dates.append(_date)
                    _timescraped.append(datetime.now())
                    st.write(_url)
        

        driver.close()

    # print('----Exporting Data to Excel File----')
    # df_extracted = pd.DataFrame({'DATE_SCRAPED':_timescraped, 'ARTICLE_DATE':_dates, 'URL':_links})
    
    # merged_df = []
    # if df_archive.empty:
    #     df_extracted.sort_values(by=['DATE_SCRAPED'], ascending=False, inplace=True)
    #     df_extracted.to_excel(f'{_dir}/pna_archive.xlsx', index=False)
    # elif df_extracted.empty:
    #     pass
    # else:
    #     merged_df.append(df_extracted)
    #     merged_df.append(df_archive)

    #     # combine archive and new extacted links
    #     df_new = pd.concat(merged_df)
    #     df_new.sort_values(by=['DATE_SCRAPED'], ascending=False, inplace=True)
    #     df_new.to_excel(f'{_dir}/pna_archive.xlsx', index=False)
    
    # print('----PROCESS DONE----')
    
    return




# x = st.button('Process')

# if x:
#     main('https://www.pna.gov.ph/articles/search?q=&p=')

# import streamlit as st
import os, sys

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')


_ = installff()
# from selenium import webdriver
# from selenium.webdriver import FirefoxOptions
# opts = FirefoxOptions()
# opts.add_argument("--headless")
# browser = webdriver.Firefox(options=opts)

options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized') # 
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
# options.add_argument(f'user-agent={random.choice(userAgents)}')
driver = webdriver.Chrome(options=options)

driver.get('https://businessmirror.com.ph/')
st.write(driver.page_source)

st.write(1)



    

