#import from accuweatherapi written by vennila
import import_ipynb
import Accuweather_API as API

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import pandas as pd
#from pymongo import MongoClient

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACbe30297e8f40d647f772ef6c6abcf4c3'
auth_token = '986bfbb54066801bf7a2a3f2c39c3e99'
client = Client(account_sid, auth_token)




#setup for accuweather api
import requests

#
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".



receiverNumber = 7177365578



#Get location information
URL2 = "http://dataservice.accuweather.com/locations/v1/cities/search"

PARAMS2 = {'apikey':APIKEY,
          'q':'State College PA'
         }

r = requests.get(url = URL2, params = PARAMS2)

data = r.json()

LOC_KEY = ''

for result in data:
    #print (result)
    key = result['Key']
    locationName = result['LocalizedName']
    postal = result['PrimaryPostalCode']
    state = result['AdministrativeArea']['LocalizedName']
    LOC_KEY = key # Use last in list

    print("%s:\n  Location Key: %s\n  Postal Code: %s\n  State: %s"
          %(locationName, key, postal,state))

locationName = str(locationName)


name = "Peter"
reportType = 2
precip="percipitation"

    
def sendText(receiverNumber,location,reportType):
    if(len(str(receiverNumber)) == 10):
        
        
        #get weather information
        locationKey = 335315
        APIKEY = "qEDtcGHcyGVGAcUKA9NbSFcNTkWPPnyU"
        URL = "http://dataservice.accuweather.com/currentconditions/v1/" + str(locationKey)
        PARAMS1 = {'apikey': APIKEY, 'language': 'en-us', 'details': 'true'}
        weatherData = requests.get(url = URL , params = PARAMS1)
        data1 = weatherData.json()
        #add weather information precipitation type,visibility, and 
        for result in data1:
            precipType = API.getPrecipitationType(result)
            vis = API.getVisibility_Metric_Value(result)
            temp = API.getTemperature_Metric_Value(result)
        print("ok")
        print(precipType)
        print("ok")
        
        #convert null precipitation type to readable format
        precipString="None"
        if(str(precipType) == "None"):
            precipString = "no precipitation"
            
        else:
            precipString = str(precipType)
        print(precipString)
        #create messages to send to user
        #
        if(reportType == 1):
            message = client.messages \
                        .create(
                             body="Hello "+ name +" " + str(data.get('WeatherText')),
                             from_='+18636228008',
                             to='+17177365578' #+ str(receiverNumber)
                    
                        )
        #daily report
        elif(reportType == 2):
            print(precipString)
            bodyStr = "Hello %s, there will be %s in " %(name,precipString)
            bodyStr = bodyStr + locationName + " today."
            bodyStr = bodyStr + " It is currently %s degrees Celcius."%(temp)
            bodyStr = bodyStr + "\nVisibility is " + str(vis) + " meters. "
            if(drivable):
                bodyStr = bodyStr + "%s is currently drivable!" %(locationName)
            else:
                bodyStr = bodyStr + "Get Off The Road!"
            print(bodyStr)
            message = client.messages \
                        .create(
                             body=bodyStr,
                             from_='+18636228008',
                             to='+17177365578' #+ str(receiverNumber)
                    # 17177365578
                         )
            
        #Print out the drivability score
        else:
            message = client.messages \
                        .create(
                             body = "Hello " + name + " the drivability in " + locationName + " will be .",
                             from_='+18636228008',
                             to='+1' + str(receiverNumber)
                        )
        print(message.sid)
    else:
        print('bad number')
    return 1

if __name__ == "__main__":
    sendText(receiverNumber,locationKey,reportType)
print("Success!")
