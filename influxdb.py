import requests
import os
from dotenv import load_dotenv

load_dotenv()


class Requests:
    organization = os.environ["ORG_ID"]
    bucket = os.environ["BUCKET_ID"]
    headers = {
        "Authorization": "Token {0}".format(os.environ["API_KEY"]),
        "Content-Type": "text/plain; charset=utf-8",
        "Accept": "application/json",
    }
    measurement = None
    sensor = None
    data_string = '{3},sensor_id={2} temp={0},hum={1}'

    def __init__(self, measurement="project", sensor_name="dht11"):
        self.measurement = measurement
        self.sensor = sensor_name

    def post_data(self, temp, hum):
        data = self.data_string.format(
            temp, hum, self.sensor, self.measurement)
        endpoint = "write"
        url = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/{2}?org={0}&bucket={1}&precision=ns".format(
            self.organization, self.bucket, endpoint)

        return requests.post(url, data=data, headers=self.headers)

    def get_data(self):
        endpoint = "query"
        self.headers["Content-Type"] = "application/vnd.flux"
        self.headers["Accept"] = "application/csv"
        url = "https://eu-central-1-1.aws.cloud2.influxdata.com/api/v2/{1}?org={0}".format(
            self.organization, endpoint)
        queryData = """from(bucket: "jannemulari's Bucket")
            |> range(start: -24h)
            |> filter(fn: (r) => r["_measurement"] == "test_measurement_4")"""
        print(url)
        print(self.headers)
        res = requests.post(url, headers=self.headers, data=queryData)

    def call(self, type, data):
        if type == "write":
            self.post_data(data)
        if type == "query":
            self.get_data()
