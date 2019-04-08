import requests, json 
import time
import serial
import urllib
from firebase import firebase
import datetime

def get_api_data(url):
    now = datetime.datetime.now()
    response = requests.get(url) 
    x = response.json() 
    b = x[0]
    y = b['WeatherText']
    y1 = b['RealFeelTemperature']['Metric']['Value']
    y2 = b['RelativeHumidity']

    c =  str(y)+"|"+str(y1)+'|'+str(y2)+'|'+str(now.hour)
    print c
    return c

def get_moisture_data(port):
    ser = serial.Serial(port, 9600, timeout = 1)
    while True:
        ser.write('1')
        a = ser.readline()
        if(a > '0'):
           print a
           return a[:3]

def send_motor_reading(port,value):
    ser = serial.Serial(port, 9600, timeout = 1)
    ser.write(value)

def push_data(inputstr,port):
    firebase1 = firebase.FirebaseApplication('https://smart-irrigation-689e5.firebaseio.com/', None)
    firebase2 = firebase.FirebaseApplication('https://smart-irrigation-outer.firebaseio.com/',None)
    outputstr = "Wheater|Temperature|Humidity|Time|Moisture"
    inputlist = inputstr.split('|')
    outputlist = outputstr.split('|')
    a = calc_prob(inputlist,outputlist)
    print a
    output = a
    if output == "no need of water":
       v = 0
    elif output == "need only some water":
       v = 90
    elif output == "need water":
       v = 180
    print output
    send_motor_reading(port,v)
    inputlist.append(output)
    outputlist.append("output")
    dictionary = {}
    for i,j in zip(inputlist,outputlist):
        dictionary[j] = i
    result = firebase2.post('',dictionary)
    firebase2.put('/','present',result['name'])
    result = firebase2.get('', '')
    b  = result["present"]
    for i,j in result[b].items():
        result = firebase1.put('/',i,j)
    print result

def calc_prob(a,b):
    dictionary = {}
    for t,t1 in zip(a,b):
        dictionary[t1] = t
    if dictionary["Moisture"] == "wet":
        return "no need of water"
    elif dictionary["Wheater"] == "Rain" or dictionary["Wheater"] == "Snow":
        return "no need of water"
    elif int(dictionary["Humidity"]) > 55:
        return "need only some water" 
    elif float(dictionary["Temperature"]) < 25.0:
        return "need only some water"
    elif "cloudy" in dictionary["Wheater"]:
        return "need only some water"
    elif int(dictionary["Time"]) < 6 or int(dictionary["Time"]) > 20:
        return "need only some water"
    else:
        return "need water"

def main(url,port):
    api_data = get_api_data(url)
    moisture_data = get_moisture_data(port)
    total_data = api_data+'|'+moisture_data
    push_data(total_data,port)

