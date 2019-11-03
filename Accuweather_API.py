import json
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

APIKEY = "qEDtcGHcyGVGAcUKA9NbSFcNTkWPPnyU"
  
URL = "http://dataservice.accuweather.com/locations/v1/cities/search"

PARAMS = {'apikey':APIKEY,
          'q':'State College PA'
         }

r = requests.get(url = URL, params = PARAMS)

data = r.json()

LOC_KEY = ''

for result in data:
    #print (result)
    key = result['Key']
    name = result['LocalizedName']
    postal = result['PrimaryPostalCode']
    state = result['AdministrativeArea']['LocalizedName']
    LOC_KEY = key # Use last in list

 def get_values(): 
    URL = "http://dataservice.accuweather.com/currentconditions/v1/%s" % LOC_KEY

    PARAMS = {'apikey':APIKEY, 'details':'true'}

    r = requests.get(url = URL, params = PARAMS)
    actualdict={}
    thisdict={}
    important={}

    data = r.json()
    a=['WeatherText','HasPrecipitation','PrecipitationType','IsDayTime','Temperature_Metric_Value','RelativeHumidity','Wind_Speed_Metric_Value','WindGust_Speed_Metric_Value','Visibility_Metric_Value','Past24HourTemperatureDeparture_Metric_Value','ApparentTemperature_Metric_Value','PrecipitationSummary_Past24Hours_Metric_Value','TemperatureSummary_Past24HourRange_Minimum_Metric_Value']
    #print(len(a))
    for result in data:
        #print(result)
        actualdict[a[0]]=getWeatherText(result)
        actualdict[a[1]]=(getHasPrecipitation(result))
        actualdict[a[2]]=(getPrecipitationType(result))
        actualdict[a[3]]=getIsDayTime(result)
        actualdict[a[4]]=(getTemperature_Metric_Value(result))
        actualdict[a[5]]=(getRelativeHumidity(result))
        actualdict[a[6]]=(getWind_Speed_Metric_Value(result))
        actualdict[a[7]]=(getWindGust_Speed_Metric_Value(result))
        actualdict[a[8]]=(getVisibility_Metric_Value(result))
        actualdict[a[9]]=(getPast24HourTemperatureDeparture_Metric_Value(result))
        actualdict[a[10]]=(getApparentTemperature_Metric_Value(result))
        actualdict[a[11]]=(getPrecipitationSummary_Past24Hours_Metric_Value(result))
        actualdict[a[12]]=(getTemperatureSummary_Past24HourRange_Minimum_Metric_Value(result))
        
        important[a[0]]=getWeatherText(result)
        important[a[3]]=getIsDayTime(result)
        important[a[1]]=getPrecipitationType(result)
        important[a[2]]=getPrecipitationType(result)
        important[a[11]]=getPrecipitationSummary_Past24Hours_Metric_Value(result)
        important[a[4]]=getTemperature_Metric_Value(result)
        important[a[12]]=getTemperatureSummary_Past24HourRange_Minimum_Metric_Value(result)
        important[a[8]]=getVisibility_Metric_Value(result)
    print(important)
    print(actualdict)
    for word in a:
        thisdict[word]=1
    print(thisdict)
    #print(getWeatherText(data))
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
    
def get_history_values(): 
    URL3 = "http://dataservice.accuweather.com/currentconditions/v1/%s/historical/24" % LOC_KEY
    a=['WeatherText','HasPrecipitation','PrecipitationType','IsDayTime','Temperature_Metric_Value','RelativeHumidity','Wind_Speed_Metric_Value','WindGust_Speed_Metric_Value','Visibility_Metric_Value','Past24HourTemperatureDeparture_Metric_Value','ApparentTemperature_Metric_Value','PrecipitationSummary_Past24Hours_Metric_Value','TemperatureSummary_Past24HourRange_Minimum_Metric_Value']
    important={}
    #important[a[0]]=getWeatherText(result)
    #important[a[3]]=getIsDayTime(result)
    #important[a[1]]=getPrecipitationType(result)
    #important[a[2]]=getPrecipitationType(result)
    important[a[11]]=getPrecipitationSummary_Past24Hours_Metric_Value(result)
    important[a[4]]=getTemperature_Metric_Value(result)
    important[a[8]]=getVisibility_Metric_Value(result)
    PARAMS = {'apikey':APIKEY, 'details':'true', 'metric' :'true'}

    r3 = requests.get(url = URL, params = PARAMS)

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
    
    for elements in important:
        list_element=(important[elements])
        count=len(list_element)
        if(count==0):
            count=1
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
