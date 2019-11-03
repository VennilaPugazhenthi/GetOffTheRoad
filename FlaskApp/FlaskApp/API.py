import json
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
from twilio.rest import Client

APIKEY = "qEDtcGHcyGVGAcUKA9NbSFcNTkWPPnyU"
def getWeatherText(data):
    value=data['WeatherText']
    return value
def getHasPrecipitation(data):
    value2=data['HasPrecipitation']
    return value2
def getPrecipitationType(data):
    value3=data['PrecipitationType']
    return value3
def getIsDayTime(data):
    temp=data['IsDayTime']
    return temp
def getTemperature_Metric_Value(data):
    value4=data['Temperature']['Metric']['Value']
    return value4
def getRelativeHumidity(data):
    value5=data['RelativeHumidity']
    return value5
def getWind_Speed_Metric_Value(data):
    value6=data['Wind']['Speed']['Metric']['Value']
    return value6
def getWindGust_Speed_Metric_Value(data):
    value7=data['WindGust']['Speed']['Metric']['Value']
    return value7
def getVisibility_Metric_Value(data):
    value8=data['Visibility']['Metric']['Value']
    return value8
def getPast24HourTemperatureDeparture_Metric_Value(data):
    value9=data['Past24HourTemperatureDeparture']['Metric']['Value']
    return value9
def getApparentTemperature_Metric_Value(data):
    value10=data['ApparentTemperature']['Metric']['Value']
    return value10
def getPrecipitationSummary_Past24Hours_Metric_Value(data):
    value11=data['PrecipitationSummary']['Past24Hours']['Metric']['Value']
    return value11
def getTemperatureSummary_Past24HourRange_Minimum_Metric_Value(data):
    value12=data['TemperatureSummary']['Past24HourRange']['Minimum']['Metric']['Value']
    return value12

def get_history_values(LOC_KEY): 
    URL3 = "http://dataservice.accuweather.com/currentconditions/v1/%s/historical/24" % str(LOC_KEY)
    a=['WeatherText','HasPrecipitation','PrecipitationType','IsDayTime','Temperature_Metric_Value','RelativeHumidity','Wind_Speed_Metric_Value','WindGust_Speed_Metric_Value','Visibility_Metric_Value','Past24HourTemperatureDeparture_Metric_Value','ApparentTemperature_Metric_Value','PrecipitationSummary_Past24Hours_Metric_Value','TemperatureSummary_Past24HourRange_Minimum_Metric_Value']
    important={}
    #important[a[0]]=getWeatherText(result)
    #important[a[3]]=getIsDayTime(result)
    #important[a[1]]=getPrecipitationType(result)
    #important[a[2]]=getPrecipitationType(result)
    #important[a[8]]=getVisibility_Metric_Value(result)
    PARAMS = {'apikey':APIKEY, 'details':'true', 'metric' :'true'}

    r3 = requests.get(url = URL3, params = PARAMS)

    data3 = r3.json()
    temperature = list(map(lambda x: x['Temperature']['Metric']['Value'], data3))
    minimum=min(temperature)
    maximum=max(temperature)
    normalize=[]
    for each in temperature:
        norm= (each-minimum)/(maximum-minimum)
        normalize.append(norm)
    #print (normalize)
    important[a[4]]=normalize
    #print(important)
    
    
    visibility = list(map(lambda x: x['Visibility']['Metric']['Value'], data3))
    minimum=min(visibility)
    maximum=max(visibility)
    normalize=[]
    if(maximum==minimum):
        maximum=maximum+1
        for each in visibility:
            norm= (each-minimum)/(maximum-minimum)
            normalize.append(norm)
    #print (normalize)
    important[a[8]]=normalize
    #print(important)
    
    
    precipitation = list(map(lambda x: x['PrecipitationSummary']['Past24Hours']['Metric']['Value'], data3))
    minimum=min(temperature)
    maximum=max(temperature)
    normalize=[]
    for each in temperature:
        norm= (each-minimum)/(maximum-minimum)
        normalize.append(norm)
    #print (normalize)
    important[a[11]]=normalize
    
    #list_element=[]
    for elements in important:
        list_element=(important[elements])
        count=len(list_element)
        sum=0
        for ele in list_element:
            sum=sum+ele
        avg=sum/count
        important[elements]=avg
    #print(important)
    threshold=0
    for elements in important:
        num=important[elements]
        weight=0.33
        threshold=threshold+weight*num
    threshold=threshold*33
    
    return threshold
    #return 1
    #print(important)
    #print(data3)
    #df3 = json_normalize(data3)
    #df3.columns = df3.columns.map(lambda x: x.split(".")[-1])
    #print(df3)
    #valuesDF = df3.loc[1:24,['Value']]
    #print(valuesDF.describe())
    #print(df3.get('CloudCover'))



def sendText(name, receiverNumber, locationKey, reportType=2, locationName="State College"):
    if(len(str(receiverNumber)) == 10):
        account_sid = 'ACbe30297e8f40d647f772ef6c6abcf4c3'
        auth_token = '986bfbb54066801bf7a2a3f2c39c3e99'
        client = Client(account_sid, auth_token) 
        #get weather information
        APIKEY = "qEDtcGHcyGVGAcUKA9NbSFcNTkWPPnyU"
        URL = "http://dataservice.accuweather.com/currentconditions/v1/" + str(locationKey)
        PARAMS1 = {'apikey': APIKEY, 'language': 'en-us', 'details': 'true'}
        weatherData = requests.get(url = URL , params = PARAMS1)
        data1 = weatherData.json()
        #add weather information precipitation type,visibility, and 
        for result in data1:
            precipType = getPrecipitationType(result)
            vis = getVisibility_Metric_Value(result)
            temp = getTemperature_Metric_Value(result)
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
            
            drivability = get_history_values(locationKey)
            
            
            
            if(drivability > 4):
                bodyStr = bodyStr + "%s is currently drivable with a score of %s" %(locationName,drivability)
            else:
                bodyStr = bodyStr + "Get Off The Road! Drivability score is %s" %(drivability)
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
