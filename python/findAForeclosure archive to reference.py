from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from csv import reader
import requests
import sys
import datetime

foreclosureListFileName = 'foreclosureListFile.csv'
zipCodeWhiteList = []
writeHeaderRow = True

#    Bankruptcy (Erroneous Sale)
#    Bankruptcy (Extends Owner Redemption Period)
#    Bankruptcy (No Effect On Foreclosure)
#    Bankruptcy (To be continued)
#    Bankruptcy General
#    Bankruptcy Prior to NED
#    Bankruptcy Sale Stayed (Restart Needed)
#    Continued
#    Cured
#    Deeded
#    Deferred
#    Determine Agricultural Status
#    Intent to Cure Filed
#    Lienor Intent to Redeem Filed
#    Lienor Redemption
#    Motion to Set Aside Sale
#    NED Recorded
#    New Foreclosure
#    Original Sale
#    Owner Intent to Redeem Filed
#    Owner Redemption
#    Owner Redemption Figures Pending
#    Pending Continuance
#    Publication Partial
#    Redeemed by Owner
#    Rescinded
#    Restarted
#    Resumed After Set Aside or TRO
#    Sale Set Aside by Court Order
#    Sold
#    Temporary Restraining Order
#    To be Rescinded
#    To be Withdrawn
#    Unknown
#    Withdrawn
#    Withdrawn (Cured)

def writeRowToFile(rowColumnDataString):
    foreclosureListFile = open(foreclosureListFileName, "a")
    foreclosureListFile.write(rowColumnDataString)
    foreclosureListFile.close()

def getRowData(driver):
    global writeHeaderRow
    rows = driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_gvSearchResults"]/tbody/*')
    for row in rows:
        rowColumnData = row.find_elements("xpath", './*')
        if len(rowColumnData) == 7:
            if writeHeaderRow:
                rowColumnDataString = '"' + rowColumnData[0].text + '","' + rowColumnData[1].text + '","' + rowColumnData[2].text + '","' + rowColumnData[3].text + '","' + rowColumnData[4].text + '","' + rowColumnData[5].text + '","' + rowColumnData[6].text + '"\n'
                writeRowToFile(rowColumnDataString)
                writeHeaderRow = False
                
            else:
                rowColumnDataString = '"' + rowColumnData[0].text + '","' + rowColumnData[1].text + '","' + rowColumnData[2].text + '","' + rowColumnData[3].text + '","' + rowColumnData[4].text + '","' + rowColumnData[5].text + '","' + rowColumnData[6].text + '"\n'
                writeRowToFile(rowColumnDataString)
        

def getGridRows():
    driverPublicTrustee = webdriver.Chrome()
    driverPublicTrustee.get('https://elpasopublictrustee.com/GTSSearch/index.aspx')
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_txtZipCode"]').send_keys(zipCodeWhiteList[0])
    select = Select(driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_ddStatus"]'))

    # select by visible text
    select.select_by_visible_text('NED Recorded')

    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_btnSearch"]').click()
    
#    pagenationPageNumber = 1
#    while pagenationPageNumber < 11:
#        print('Searching page ' + str(pagenationPageNumber) + '...')
#        if pagenationPageNumber == 1:
#            print(driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_Label1"]').text)
#        else:
#            driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_gvSearchResults"]/tbody/tr[1]/td/table/tbody/tr/td['+str(pagenationPageNumber)+']/a').click()
        
#    if uncommented above then indent below but not .quit()
    WebDriverWait(driverPublicTrustee, timeout=8).until(EC.presence_of_element_located((By.CLASS_NAME, 'SearchResultsGridRow')))
    driverPublicTrustee.execute_script("window.scrollTo(0, 250)")
    getRowData(driverPublicTrustee)
#    pagenationPageNumber+=1
        
    driverPublicTrustee.quit()
    
def readInWhiteListZipCodes(whiteListName):
    whiteList = open(whiteListName, "r")
    with open(whiteListName, "r") as readWhiteList_obj:
        csv_reader = reader(readWhiteList_obj)
        for row in csv_reader:
            zipCodeWhiteList.append(row[0].rstrip())
            
def getZillowValue(addressStreetFormatted, addressZipcodeFormatted):
#    https://www.zillow.com/howto/api/APIOverview.htm
    driverZillow = webdriver.Chrome()
    driverZillow.get('https://www.zillow.com/homes/' + addressStreetFormatted + '-Colorado-Springs,-CO-' + addressZipcodeFormatted + '_rb')
    sold = 0.00
    price = 0.00
    zestimate = 0.00
    assessed = 0.00
    
def getElPasoCountyAssessorValue():


    searchUrl = 'https://property.spatialest.com/co/elpaso/data/search'
    myobj = {'filters[term]': '714 CLINTON WAY'}

    x = requests.post(searchUrl, data = myobj)

    print(x.text)
#    use the id field to search for the property card and then you can get all the needed info for the spreadsheet
    
        
        
    
#    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_txtZipCode"]').text
    
def getPropertyValues():
    with open(foreclosureListFileName, "r") as readForeclosureList_obj:
        csv_reader = reader(readForeclosureList_obj)
        for row in csv_reader:
#            print(row[2].replace(' ', '-') + ' ' + row[3][0:5])
#            getZillowValue(row[2].replace(' ', '-'),row[3][0:5])
            getElPasoCountyAssessorValue()
            input('enter')
            


#   Realtor.com (https://www.realtor.com) then search for property

#   El Paso County Assesor (https://property.spatialest.com/co/elpaso/#/) then search for property

userInput = input('Type 1 to search all foreclosures on the public trustee website.\nType 2 to search for property values.\nThen press ENTER.')
if userInput == '1':
    readInWhiteListZipCodes('whiteListZipCodes.csv')
    getGridRows()
    print('All records have been gathered!')

elif userInput == '2':
    getPropertyValues()
    print('All property data has been gathered!')


# let this create a csv and json file and then I can create a beta site in github to put the info in for Porter
