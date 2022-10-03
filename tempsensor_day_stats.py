from influxdb import InfluxDBClient

tempdata = 0
datapoints = 0
temp_max = 0
temp_min = 40

client = InfluxDBClient('localhost', 8086, 'tempmonitor', 'J3kVTBEfKezsM9yQ3NGF', 'temperature')

query = 'select temp from temperature where time > now() - 1d'

results = client.query(query)
points = results.get_points()

for point in points:
    tempdata = tempdata + point['temp']
    datapoints += 1
    if point['temp'] > temp_max:
        temp_max = point['temp']
    if point['temp'] < temp_min:
        temp_min = point['temp']
        
temp_avg = tempdata / datapoints
print(tempdata)
print(datapoints)

temp_avg = round(temp_avg,1)
temp_max = round(temp_max,1)
temp_min = round(temp_min,1)

temp_data = [
    {
        "measurement" : "temp_day_stats",
        "tags" : {
            "location": "back_garden"
        },
        "fields" : {
            "temp_avg": float(temp_avg),
            "temp_max": float(temp_max),
            "temp_min": float(temp_min)
        }
    }
]

print(temp_data)

client.write_points(temp_data)
client.close()