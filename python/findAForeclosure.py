from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from csv import reader
import requests
import urllib
import json
import requests
import sys
import time
import datetime
from datetime import timedelta, date
currentDateTime = datetime.datetime.now()
dateSuffix = '_'+str(currentDateTime.month)+'-'+str(currentDateTime.day)+'-'+str(currentDateTime.year)
foreclosureListFileName = 'foreclosureListFile'+dateSuffix+'.csv'
propertyValuesFileName = 'propertyValuesFile'+dateSuffix+'.csv'
propertyDetailsFileName = 'propertyDetailsFile'+dateSuffix+'.csv'
dataJsonFileName = '../js/data.js'
zipCodeWhiteList = []
zillowAccessToken = '6baca547742c6f96a6ff71b138424f21'

def writeRowToForeclosureListFile(rowColumnDataString, zipcodeIndex):
    foreclosureListFile = open(foreclosureListFileName, "a")
    if 'FC #' in rowColumnDataString:
        if zipcodeIndex == 0:
            foreclosureListFile.write(rowColumnDataString)
    else:
        foreclosureListFile.write(rowColumnDataString)
    foreclosureListFile.close()

def getRowData(driver, zipcodeIndex):
    rows = driver.find_elements("xpath", '//*[@id="ctl00_ContentPlaceHolder1_gvSearchResults"]/tbody/*')
    print(str(len(rows)-1) + ' property foreclosures.')
    for row in rows:
        rowColumnData = row.find_elements("xpath", './*')
        if len(rowColumnData) == 7:
            rowColumnDataString = '"' + rowColumnData[0].text + '","' + rowColumnData[1].text + '","' + rowColumnData[2].text + '","' + rowColumnData[3].text + '","' + rowColumnData[4].text + '","' + rowColumnData[5].text + '","' + rowColumnData[6].text + '"\n'
            writeRowToForeclosureListFile(rowColumnDataString, zipcodeIndex)
        

def getGridRows(zipcode, zipcodeIndex):
    driverPublicTrustee = webdriver.Chrome()
    driverPublicTrustee.get('https://elpasopublictrustee.com/GTSSearch/index.aspx')
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_txtZipCode"]').send_keys(zipcode)
    select = Select(driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_ddStatus"]'))
    # select by visible text
    select.select_by_visible_text('NED Recorded')
    
    tomorrow = date.today() + timedelta(days=1)
    nextWeek = tomorrow + timedelta(days=7)
    
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_txtCurrentScheduledSaleDateFrom"]').send_keys(tomorrow.strftime("%m/%d/%y"))
    
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_txtCurrentScheduledSaleDateTo"]').send_keys(nextWeek.strftime("%m/%d/%y"))

    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_btnSearch"]').click()
    
    try:
        WebDriverWait(driverPublicTrustee, timeout=8).until(EC.presence_of_element_located((By.CLASS_NAME, 'SearchResultsGridRow')))
        driverPublicTrustee.execute_script("window.scrollTo(0, 250)")
        getRowData(driverPublicTrustee, zipcodeIndex)
    except:
        print('Could not get records for zipcode: ' + zipcode + ', status: NED Recorded, Date From: ' + tomorrow.strftime("%m/%d/%y") + ' - ' + nextWeek.strftime("%m/%d/%y"))
    
    driverPublicTrustee.quit()
    
def cycleThroughZipcodes():
    for idx, zipcode in enumerate(zipCodeWhiteList):
        getGridRows(zipcode, idx)
        print(str(idx+1) + ' out of ' + str(len(zipCodeWhiteList)) + ' zipcodes gathered.')
    
def readInWhiteListZipCodes(whiteListName):
    with open(whiteListName, "r") as readWhiteList_obj:
        csv_reader = reader(readWhiteList_obj)
        for row in csv_reader:
            zipCodeWhiteList.append(row[0].rstrip())
            
def cycleThroughForeclosureNumbersForPropertyDetails(foreclosureListName):
    with open(propertyValuesFileName, "r") as propertyValuesCountFile:
        for count, line in enumerate(propertyValuesCountFile):
            pass
        lineCount = count
    propertyValuesCountFile.close()
    
    propertyDetailsFile = open(propertyDetailsFileName, "a")
    with open(propertyValuesFileName, "r") as readPropertyValuesList_obj:
        csv_reader_property_values = reader(readPropertyValuesList_obj)
        for idx,row in enumerate(csv_reader_property_values):
            if 'FC #' not in row:
                print('Searching ' + str(idx) + ' out of ' + str(lineCount))
                resultArray = readPropertyDetailsPublicTrustee(row[0].rstrip())
                rowToWrite = ""
                for column in row:
                    rowToWrite += '"' + column + '",'
                rowToWrite += '"' + resultArray[0] + '","' + resultArray[1] + '","' +  resultArray[2] + '","' + resultArray[3] + '"\n'
                print(rowToWrite)
                propertyDetailsFile.write(rowToWrite)
    propertyDetailsFile.close()
                
            
def readPropertyDetailsPublicTrustee(foreclosureNumber):
    driverPublicTrustee = webdriver.Chrome()
    driverPublicTrustee.get('https://elpasopublictrustee.com/GTSSearch/index.aspx')
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_txtForeclosureNumber"]').send_keys(foreclosureNumber)
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_btnSearch"]').click()
    
    try:
        WebDriverWait(driverPublicTrustee, timeout=8).until(EC.presence_of_element_located((By.CLASS_NAME, 'SearchResultsGridRow')))
        driverPublicTrustee.execute_script("window.scrollTo(0, 250)")
        driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_gvSearchResults"]/tbody/tr[2]/td[1]/a').click()
    except:
        print('Could not click on record.')

    input('Press Enter when on the past CAPTCHA\n')
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_btnChallengeResponse"]').click()
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_wizDetails_SideBarContainer_SideBarList_ctl02_SideBarButton"]').click()
    WebDriverWait(driverPublicTrustee, timeout=8).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_wizDetails_txtBasicsActualSaleDate')))
    currentlyScheduledSaleDate = driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_wizDetails_txtBasicsActualSaleDate"]').get_attribute('value')
    
    driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_wizDetails_SideBarContainer_SideBarList_ctl10_SideBarButton"]').click()
    WebDriverWait(driverPublicTrustee, timeout=8).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_wizDetails_txtCopPendingBid')))
    holdersInitialBid = driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_wizDetails_txtCopPendingBid"]').get_attribute('value')
    if len(holdersInitialBid) == 0:
        holdersInitialBid = 'N/A'
        
    deficiencyAmount = driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_wizDetails_txtCopDeficiencyAmount"]').get_attribute('value')
    if len(deficiencyAmount) == 0:
        deficiencyAmount = 'N/A'
    
    totalIndebtedness = driverPublicTrustee.find_element("xpath", '//*[@id="ctl00_ContentPlaceHolder1_wizDetails_txtCopTotalIndebtedness"]').get_attribute('value')
    if len(totalIndebtedness) == 0:
        totalIndebtedness = 'N/A'
    
    driverPublicTrustee.quit()
    return [currentlyScheduledSaleDate, holdersInitialBid, deficiencyAmount, totalIndebtedness]
    
            
#def getZillowValue(address, fcNumber):
#    https://www.zillow.com/howto/api/APIOverview.htm
#   https://api.bridgedataoutput.com/api/v2/zestimates_v2/zestimates?access_token=access_token&address="123 Main Street"
#    driverZillow = webdriver.Chrome()
#    input('Press Enter')
#    driverZillow.get('https://www.zillow.com/homes/' + address.replace(" ","-") + '_rb')
#    time.sleep(5)
#    src = driverZillow.find_element("xpath", '//*[@id="__next"]/div/div/div[1]/div[2]/div[1]/div/div[1]/div/ul/li[1]/button/picture/img').get_attribute('src')
#    urllib.request.urlretrieve(str(src),"../photos/fcNumber{}.jpg".format(fcNumber))
#    input('WAITING FOR DEVELOPER')
#    sold = 0.00
#    price = 0.00
#    zestimate = 0.00
#    assessed = 0.00
#    driverZillow.quit()

#def getZillowValue(address):
#   Need to get the access token for my account, register account
#   https://api.bridgedataoutput.com/api/v2/zestimates_v2/zestimates?access_token=access_token&address="123 Main Street"
#    zillowAccessToken
#    searchUrl = 'https://api.bridgedataoutput.com/api/v2/zestimates_v2/zestimates?access_token=6baca547742c6f96a6ff71b138424f21&address="' + address + '"'
#    myobj = {}
#    x = requests.post(searchUrl, data = myobj)
#    print(x.text)
#    json_object = json.loads(x.text)

def getRealtorComValue(row):
    driverRealtor = webdriver.Chrome()
    driverRealtor.get('https://www.realtor.com/')
    driverRealtor.find_element("xpath", '//*[@id="search-bar"]').send_keys(row[2] + ', Colorado Springs, CO, ' + row[3])
    driverRealtor.find_element("xpath", '//*[@id="__next"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div/div/header/div/div/button[2]').click()

    
def cleanAddress(addressToClean):
    result = addressToClean
    if 'DRIVE' in result:
        result = result.replace("DRIVE","Dr")
    if 'TERRACE' in result:
        result = result.replace("TERRACE","Ter")
    if 'LANE' in result:
        result = result.replace("LANE","Ln")
    if 'ROAD' in result:
        result = result.replace("ROAD","Rd")
    if 'NORTH' in result:
        result = result.replace("NORTH","N")
    if 'SOUTH' in result:
        result = result.replace("SOUTH","S")
    if 'EAST' in result:
        result = result.replace("EAST","E")
    if 'WEST' in result:
        result = result.replace("WEST","W")
    if 'CIRCLE' in result:
        result = result.replace("CIRCLE","CIR")
    return result
        
    
def getElPasoCountyAssessorValue(row):
    searchUrl = 'https://property.spatialest.com/co/elpaso/data/search'
    address = cleanAddress(row[2].upper())
    myobj = {'filters[term]': address}  # 'filters[term]': '714 CLINTON WAY'
    x = requests.post(searchUrl, data = myobj)
#    print(x.text)
    json_object = json.loads(x.text)
    try:
        print(json_object["id"])
        print(address)
#       use the id field to search for the property card and then you can get all the needed info for the spreadsheet
        driverAssessor = webdriver.Chrome()
        driverAssessor.get('https://property.spatialest.com/co/elpaso/#/property/' + json_object["id"])
        WebDriverWait(driverAssessor, timeout=8).until(EC.presence_of_element_located((By.ID, 'prccontent')))
        totalValue = driverAssessor.find_element("xpath", '//*[@id="prccontent"]/div/section/div/div[1]/div[2]/header/div/div/div[2]/div/div[2]/span').text
        isSinglePhotoPresent = len(driverAssessor.find_elements(By.ID,'prccontent')) > 0
        areMultiplePhotosPresent = len(driverAssessor.find_elements(By.ID,'slick-slide00')) > 0
        photoPath = None
        
        if isSinglePhotoPresent:
            photoPath = '//*[@id="prccontent"]/div/section/div/div[2]/div/div/div[1]/div/div/div/div/img'
        elif areMultiplePhotosPresent:
            photoPath = '//*[@id="slick-slide00"]/div/div/img'
        src = driverAssessor.find_element("xpath", photoPath).get_attribute('src')
        
        urllib.request.urlretrieve(str(src),"../photos/fcNumber{}.jpg".format(row[0]))
        return [totalValue,"../photos/fcNumber{}.jpg".format(row[0])]
        
    except KeyError:
        print("id does not exist for: " + address)
        return "Could Not Find"
    
def getPropertyValues():
    lineCount = -1
    with open(foreclosureListFileName, "r") as foreclosureListLineCountFile:
        for count, line in enumerate(foreclosureListLineCountFile):
            pass
        lineCount = count
    foreclosureListLineCountFile.close()
    
    propertyValuesFile = open(propertyValuesFileName, "a")
    with open(foreclosureListFileName, "r") as readForeclosureList_obj:
        csv_reader = reader(readForeclosureList_obj)
        assessorValue = 0.00
        for idx, row in enumerate(csv_reader):
            if 'FC #' not in row[0]:
                print('Searching ' + str(idx) + ' out of ' + str(lineCount))
# todo          print(row[2].replace(' ', '-') + ' ' + row[3][0:5])
# todo          getZillowValue(row[2].replace(' ', '-'),row[3][0:5])

                # Realtor.com (https://www.realtor.com) then search for property
# todo           getRealtorComValue(row)

                # El Paso County Assesor (https://property.spatialest.com/co/elpaso/#/) then search for property
                assessorResults = getElPasoCountyAssessorValue(row)
                rowToWrite = ""
                for column in row:
                    rowToWrite += '"' + column + '",'
                rowToWrite += '"' + assessorResults[0] + '",' + '"' + assessorResults[1] + '"\n'
                propertyValuesFile.write(rowToWrite)
        
        propertyValuesFile.close()
        
def createDataJson():
    with open(propertyDetailsFileName, "r") as readPropertyDetailsFile_obj:
        csv_reader = reader(readPropertyDetailsFile_obj)
        dataJsonFile = open(dataJsonFileName,"w")
        dataJsonFile.write('const data = [')
        for idx, row in enumerate(csv_reader):
            if 'FC #' not in row[0]:
                rowObj = {
                    "FC":row[0],
                    "GRANTOR":row[1],
                    "STREET":row[2],
                    "ZIP":row[3],
                    "SUBDIVISION":row[4],
                    "BALANCEDUE":row[5],
                    "STATUS":row[6],
                    "ASSESSORVALUE":row[7],
                    "PHOTOPATH":row[8],
                    "SALEDATE":row[9],
                    "LENDERSINITIALBID":row[10],
                    "DEFICIENCYAMOUNT":row[11],
                    "TOTALINDEBTEDNESS":row[12]
                }
                dataJsonFile.write(json.dumps(rowObj)+',')
        dataJsonFile.write(']')
        dataJsonFile.close()
    
            
# for O and E order https://www.etcos.com/o-and-e-order-form or https://www.etcos.com/empower-property-search-and-o-and-e-orders ask David

userInput = input('Type 1 to search all foreclosures on the public trustee website.\nType 2 to search for property values.\nType 3 for property details.\nThen press ENTER.\n')
if userInput == '1':
    foreclosureListFile = open(foreclosureListFileName, "a")
    foreclosureListFile.write('"FC #","Grantor","Street","Zip","Subdivision","Balance Due","Status"\n')
    foreclosureListFile.close()
    readInWhiteListZipCodes('whiteListZipCodes.csv')
    cycleThroughZipcodes()
    print('All records have been gathered!\n')

elif userInput == '2':
    propertyValuesFile = open(propertyValuesFileName, "w")
    propertyValuesFile .write('"FC #","Grantor","Street","Zip","Subdivision","Balance Due","Status","Assessor Market Value","Photo Path"\n')
    propertyValuesFile.close()
    getPropertyValues()
    print('All property data has been gathered!\n')
    
elif userInput == '3':
    propertyDetailsFile = open(propertyDetailsFileName, "w")
    propertyDetailsFile.write('"FC #","Grantor","Street","Zip","Subdivision","Balance Due","Status","Assessor Market Value","Photo Path","Currently Scheduled Sale Date","Lenders Initial Bid","Deficiency Amount","Total Indebtedness"\n')
    propertyDetailsFile.close()
    cycleThroughForeclosureNumbersForPropertyDetails(foreclosureListFileName)
    print('All property details data has been gathered!\n')
    createDataJson()
    print('Json data.json Created\n')
    
#elif userInput == 'test':
#    getZillowValue(input('Enter Address: '), 123)
    

# let this create a csv and json file and then I can create a beta site in github to put the info in for Porter

