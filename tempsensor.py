import re
import subprocess
import time
from w1thermsensor import W1ThermSensor
from influxdb import InfluxDBClient

sensor = W1ThermSensor()

while True:
    client = InfluxDBClient('localhost', 8086, 'tempmonitor', 'J3kVTBEfKezsM9yQ3NGF', 'temperature')
    query = 'select temp from temperature where time > now()-1440m and time < now()-1435m'
    results = client.query(query)
    points = results.get_points()
    for point in points:
        temp_yesterday = point['temp']
        print(temp_yesterday)
        
    temp = sensor.get_temperature()
    
    temp_data = [
        {
            "measurement" : "temperature",
            "tags" : {
                "location": "back_garden"
            },
            "fields" : {
                "temp": float(temp),
                "temp_yesterday": float(temp_yesterday)
            }
        }
    ]
    print(temp_data)

    client.write_points(temp_data)
    client.close()

    time.sleep(300)

