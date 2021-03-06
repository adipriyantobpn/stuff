import time
import mosquitto
import httplib2
from urllib import urlencode
import json

cities = ["Portsmouth,UK", "Southampton,UK", "London,UK", "Oxford,UK"]
client = mosquitto.Mosquitto("test-client")
print client.connect("localhost")

def call_weather(city):

    h = httplib2.Http(); # disable_ssl_certificate_validation=True)
#    h.add_credentials(intro_username, intro_password)
    resp, content = h.request("http://api.openweathermap.org/data/2.5/weather?q="+city)

#    print resp            
    try:
       response=json.loads(content)
    
       main = response['main']
       temp = round(main['temp'] - 273.15,2)
       humidity = main['humidity']
       pressure = main['pressure']
       wind = response['wind']
       windspeed = wind['speed']
       winddirection = wind['deg']
       country = response['sys']['country']
       city = response['name']
	
       print temp, humidity, pressure, windspeed, winddirection, country, city

       data = dict(temp=temp, humidity=humidity, pressure=pressure, windspeed=windspeed, winddirection=winddirection, country=country,city=city)
       print data
       print client.publish("/weather/"+country+"/"+city, json.dumps(data), 0)
    except Exception as inst:
       print inst    
    
    client.loop()

while 1==1:
  for city in cities:
    call_weather(city)
  time.sleep(10)

