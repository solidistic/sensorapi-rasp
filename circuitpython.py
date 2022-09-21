import adafruit_dht
import board
import time
import influxdb


def read():
    sensor = adafruit_dht.DHT11(board.D4)
    db = influxdb.Requests()

    while True:
        try:
            print(
                "Temperature {0}*C; Humidity {1}%".format(sensor.temperature, sensor.humidity))
            res = db.post_data(sensor.temperature, sensor.humidity)
            print("Response {0}".format(res))
        except Exception as e:
            print(e)

        time.sleep(60 * 5)


print("--- Initializing... ---")
read()
