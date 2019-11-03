import json
import requests
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

APIKEY = "qEDtcGHcyGVGAcUKA9NbSFcNTkWPPnyU"


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

