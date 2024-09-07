from w1thermsensor import W1ThermSensor
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

influxdb_bucket = "xxx"
influxdb_org = "xxx"
influxdb_token = "xxx-xxx"
influxdb_url = "xxxs"

# Store data in influx database
def StoreInDatabase(p):

    client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

    write_api = client.write_api(write_options = SYNCHRONOUS)

    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=p)

    client.close()

# Query influx database
def QueryDatabase():
    client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

    query_api = client.query_api()

    query = 'from(bucket: "tempsensor")\
        |> range(start: -24h)\
        |> filter(fn: (r) => r["_measurement"] == "backside")\
        |> filter(fn: (r) => r["_field"] == "temp")'

    result = query_api.query(org=influxdb_org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    
    day_avg = round(sum(results) / len(results),1)
    day_max = max(results)
    day_min = min(results)
    
    client.close()

    return day_avg,day_max,day_min

# ***************************************** MAIN ********************************************

sensor = W1ThermSensor()

temp = sensor.get_temperature()
temp = round(temp,1)

print("Temperature: {}".format(temp))

temp_data = influxdb_client.Point("backside")\
    .field("temp", float(temp))

StoreInDatabase(temp_data)

# Get 24h average, max and min temp 
day_avg,day_max,day_min = QueryDatabase()

print("24h Avg: {}".format(day_avg))
print("24h Max: {}".format(day_max))
print("24h Min: {}".format(day_min))

temp_data = influxdb_client.Point("backside")\
    .field("day_avg", float(day_avg))\
    .field("day_max", float(day_max))\
    .field("day_min", float(day_min))

StoreInDatabase(temp_data)