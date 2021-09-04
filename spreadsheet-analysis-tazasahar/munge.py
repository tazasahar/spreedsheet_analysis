from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import csv
URL = "https://finance.yahoo.com/quote/%5EIXIC/history?period1=34560000&period2=1614470400&interval=1wk&filter=history&frequency=1wk&includeAdjustedClose=true"

driver = webdriver.Chrome(executable_path = r"/usr/local/bin/chromedriver.exe")

#Hit the URL of the Web page 
driver.get(URL)
time.sleep(2)

# Driver scrolls down fifty times to load the table.
for i in range(0,50):
 driver.execute_script("window.scrollBy(0,5000)")
 time.sleep(2)

# Fetching the webpage and store in a variable.
webpage = driver.page_source

#writing the raw data to a file
raw_data = open("raw_data", 'w')
raw_data.write(webpage)
raw_data.close()

# Web page fetched from driver is parsed using Beautiful Soup.
HTMLPage = BeautifulSoup(driver.page_source, 'html.parser')

# Table is searched using class and stored in another variable.
Table = HTMLPage.find('table', class_='W(100%) M(0)')

# List of all the rows is store in a variable 'Rows'.
Rows = Table.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')

# Empty list is created to store the data
extracted_data = []

# Loop to go through each row of table
for i in range(0, len(Rows)):
    try:
        # Empty dictionary to store data present in each row
        RowDict = {}
        # Extracted all the columns of a row and stored in a variable
        Values = Rows[i].find_all('td')

        # Values (Open, High, Close etc.) are extracted and stored in dictionary
        if len(Values) == 7:
            RowDict["Date"] = Values[0].find('span').text.replace(',', '')
            RowDict["Open"] = Values[1].find('span').text.replace(',', '')
            RowDict["High"] = Values[2].find('span').text.replace(',', '')
            RowDict["Low"] = Values[3].find('span').text.replace(',', '')
            RowDict["Close"] = Values[4].find('span').text.replace(',', '')
            RowDict["Adj Close"] = Values[5].find('span').text.replace(',', '')
            RowDict["Volume"] = Values[6].find('span').text.replace(',', '')

        # Dictionary is appended in list
        extracted_data.append(RowDict)
    except:
        # To check the exception caused
        print("Row Number: " + str(i))
    finally:
    # To move to the next row
        i = i + 1


#Converted list of dictionaries to a Dataframe.
extracted_data = pd.DataFrame(extracted_data)
extracted_data.to_csv("clean_data.csv", index = False, encoding='utf-8' )

#print(extracted_data)

