import pandas as pd
import re
from dict_xpaths import paths
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import numpy as np
import warnings

# removing warning
warnings.filterwarnings("ignore", message="The frame.append method is deprecated and will be removed from pandas "
                                          "in a future version. Use pandas.concat instead.")

url = 'https://www.ycombinator.com/companies'


# defining function to scroll and then gather the companies that are showing in the page
names = []
df = pd.DataFrame(columns=['name', 'location', 'tag', 'status'])
def gather_companies(status):
    global df
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if driver.execute_script("return window.pageYOffset + window.innerHeight >= document.body.scrollHeight;"):
            break
    time.sleep(1)

    # defining companies, and take these hrefs to found information about them
    companies_hrefs = driver.find_elements(By.CSS_SELECTOR, "div.dsStC1AzZueqISZqfHLZ a.WxyYeI15LZ5U_DOM0z8F")
    for i in companies_hrefs:
        href = i.get_attribute("href")[27:]             # to cut the first part of the link

        name = driver.find_element(By.CSS_SELECTOR, f'a[href="{href}"] span.CBY8yVfV0he1Zbv9Zwjx').text

        locations_element = driver.find_element(By.CSS_SELECTOR, f'a[href="{href}"] span.eKDwirBf1zBn7I5MGAOb')
        locations = (re.split("[,;]", locations_element.text))

        tags = []
        tag_elements = driver.find_elements(By.CSS_SELECTOR, f'a[href$="{href}"] a.C_UZV5NvBs8V3ANHGSVs span')
        for tag in tag_elements:
            tags.append(tag.text)

        # create rows to insert in dataframe
        for i in range(len(locations)):
            row = pd.Series([name, locations[i], np.nan, status], index=df.columns)
            df = df.append(row, ignore_index=True)

        for i in range(len(tags)):
            row = pd.Series([name, np.nan, tags[i], status], index=df.columns)
            df = df.append(row, ignore_index=True)

# Set up the driver
chrome_path = Service(r"C:\Users\Daniele\Documents\Chrome_driver\chromedriver")
driver = webdriver.Chrome(service=chrome_path)

driver.get(url)

time.sleep(2)

# define all the elements to filter
open_filter = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section[2]/div/div[1]/div/div[9]/a")

splitter_act = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section[2]/div/div[1]/div/div[18]/div[2]/label/span[1]")
splitter_pub = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section[2]/div/div[1]/div/div[18]/div[3]/label/span[1]")
splitter_acq = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section[2]/div/div[1]/div/div[18]/div[4]/label/span[1]")
splitter_ina = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/section[2]/div/div[1]/div/div[18]/div[5]/label/span[1]")
splitter1 = driver.find_element(By.XPATH, paths["W23"])
splitter2 = driver.find_element(By.XPATH, paths["S22"])
splitter3 = driver.find_element(By.XPATH, paths["W22"])
splitter4 = driver.find_element(By.XPATH, paths["S21"])
splitter5 = driver.find_element(By.XPATH, paths["W21"])
splitter6 = driver.find_element(By.XPATH, paths["S20"])
splitter7 = driver.find_element(By.XPATH, paths["W20"])



# perform a click action on the filter element
time.sleep(1)
actions = ActionChains(driver)
actions.click(open_filter)
actions.perform()

splitter8 = driver.find_element(By.XPATH, paths["S19"])
splitter9 = driver.find_element(By.XPATH, paths["W19"])
splitter10 = driver.find_element(By.XPATH, paths["S18"])
splitter11 = driver.find_element(By.XPATH, paths["W18"])
splitter12 = driver.find_element(By.XPATH, paths["S17"])
splitter13 = driver.find_element(By.XPATH, paths["W17"])
splitter14 = driver.find_element(By.XPATH, paths["IK12"])
splitter15 = driver.find_element(By.XPATH, paths["S16"])
splitter16 = driver.find_element(By.XPATH, paths["W16"])
splitter17 = driver.find_element(By.XPATH, paths["S15"])
splitter18 = driver.find_element(By.XPATH, paths["W15"])
splitter19 = driver.find_element(By.XPATH, paths["S14"])
splitter20 = driver.find_element(By.XPATH, paths["W14"])
splitter21 = driver.find_element(By.XPATH, paths["S13"])
splitter22 = driver.find_element(By.XPATH, paths["W13"])
splitter23 = driver.find_element(By.XPATH, paths["S12"])
splitter24 = driver.find_element(By.XPATH, paths["W12"])
splitter25 = driver.find_element(By.XPATH, paths["S11"])
splitter26 = driver.find_element(By.XPATH, paths["W11"])
splitter27 = driver.find_element(By.XPATH, paths["S10"])
splitter28 = driver.find_element(By.XPATH, paths["W10"])
splitter29 = driver.find_element(By.XPATH, paths["S09"])
splitter30 = driver.find_element(By.XPATH, paths["W09"])
splitter31 = driver.find_element(By.XPATH, paths["S08"])
splitter32 = driver.find_element(By.XPATH, paths["W08"])
splitter33 = driver.find_element(By.XPATH, paths["S07"])
splitter34 = driver.find_element(By.XPATH, paths["W07"])
splitter35 = driver.find_element(By.XPATH, paths["S06"])



actions.click(splitter_act)
actions.click(splitter1)
actions.click(splitter2)
actions.click(splitter3)

actions.perform()


gather_companies("active")


actions.click(splitter4)
actions.click(splitter5)
actions.click(splitter6)
actions.click(splitter1)
actions.click(splitter2)
actions.click(splitter3)

actions.perform()

time.sleep(1)

gather_companies("active")

actions.click(splitter7)
actions.click(splitter8)
actions.click(splitter9)
actions.click(splitter10)
actions.click(splitter11)
actions.click(splitter12)
actions.click(splitter13)
actions.click(splitter14)
actions.click(splitter15)
actions.click(splitter16)
actions.click(splitter4)
actions.click(splitter5)
actions.click(splitter6)
actions.perform()

gather_companies("active")

actions.click(splitter7)
actions.click(splitter8)
actions.click(splitter9)
actions.click(splitter10)
actions.click(splitter11)
actions.click(splitter12)
actions.click(splitter13)
actions.click(splitter14)
actions.click(splitter15)
actions.click(splitter16)
actions.click(splitter17)
actions.click(splitter18)
actions.click(splitter19)
actions.click(splitter20)
actions.click(splitter21)
actions.click(splitter22)
actions.click(splitter23)
actions.click(splitter24)
actions.click(splitter25)
actions.click(splitter26)
actions.click(splitter27)
actions.click(splitter28)
actions.click(splitter29)
actions.click(splitter30)
actions.click(splitter31)
actions.click(splitter32)
actions.click(splitter33)
actions.click(splitter34)
actions.click(splitter35)
actions.perform()

gather_companies("active")

actions.click(splitter_acq)
actions.click(splitter17)
actions.click(splitter18)
actions.click(splitter19)
actions.click(splitter20)
actions.click(splitter21)
actions.click(splitter22)
actions.click(splitter23)
actions.click(splitter24)
actions.click(splitter25)
actions.click(splitter26)
actions.click(splitter27)
actions.click(splitter28)
actions.click(splitter29)
actions.click(splitter30)
actions.click(splitter31)
actions.click(splitter32)
actions.click(splitter33)
actions.click(splitter34)
actions.click(splitter35)
actions.click(splitter_pub)
actions.perform()

gather_companies("acquired")

actions.click(splitter_ina)
actions.click(splitter_acq)
actions.perform()

gather_companies("inactive")

actions.click(splitter_pub)
actions.click(splitter_ina)
actions.perform()

gather_companies("public")

driver.quit()

# I splitted the companies in batched less than 1000, because this was the limit that the website could display,
# and then by status, I inserted the status information because the website wasn't giving this information in the html
# then I saved the dataframe in a file and continued in another file to work easily with it

df.to_csv('my_data.csv', index=False)
