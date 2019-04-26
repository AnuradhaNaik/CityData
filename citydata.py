from lxml import html
import requests
import csv
from bs4 import BeautifulSoup

def getLatLng(address,city,state):
    address.replace(' ','+')
    newadd=address+','+city+','+state
    url='http://www.mapquestapi.com/geocoding/v1/address?key=2cwkchRNOx1tEhmNVSWwwgKF3j2hpmfZ&location='+newadd
    response = requests.get(url)

    #resp_json_payload = response.json()
    re=response.json()
    re=re['results'][0]
    re=re['locations'][0]
    re=re['latLng']
    
    return re

def cityDataWebpageToCSV(url,city,state,filename):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    all_ = soup.find(class_='tabBlue')
    all_rows= all_.find_all('tr')
    it=0
    t=""


    with open(filename, mode='w') as _file:
        _writer = csv.writer(_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


        for a in all_rows:
            dates = a.contents[1]
            loc=a.contents[2]
            veh=a.contents[3]
            dp=a.contents[4]
            fat=a.contents[5]
            per=a.contents[6]
            ped=a.contents[7]
            loc=loc.contents[0]
            print('processing')
            if(it>0):
                ob=getLatLng(loc.contents[0],city,state)
                _writer.writerow([dates.contents[0],loc.contents[0],ob['lat'],ob['lng'],veh.contents[0],dp.contents[0],fat.contents[0],per.contents[0],ped.contents[0]])
            else:
                _writer.writerow([dates.contents[0],loc,'Latitude','Longitude',veh.contents[0],dp.contents[0],fat.contents[0],per.contents[0],ped.contents[0]])
            it=it+1

    return 0



cityDataWebpageToCSV('http://www.city-data.com/accidents/acc-Cincinnati-Ohio.html','Cincinnati','OH','f.csv')
        
    
    


