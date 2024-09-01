from w1thermsensor import W1ThermSensor
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# store data in influx database
def StoreInDatabase(p):
    influxdb_bucket = "xxxxxxxxxxxxx"
    influxdb_org = "xxxxxx"
    influxdb_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    influxdb_url = "xxxxxxxxxxxxxxxxxxxxxxxxx"

    client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)

    write_api = client.write_api(write_options = SYNCHRONOUS)

    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=p)

    client.close()

# ***************************************** MAIN ********************************************

sensor = W1ThermSensor()

temp = sensor.get_temperature()
temp = round(temp,1)

print("Temperature: {}".format(temp))

temp_data = influxdb_client.Point("backside")\
    .field("temp", float(temp))

StoreInDatabase(temp_data)