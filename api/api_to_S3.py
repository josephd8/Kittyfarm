import requests
import json
import boto3
import os
import logging

# Set up Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Set up Boto3
s3 = boto3.client('s3')

# API Settings
payload = "{\n \"dappName\": \"KittyFarm\"\n}"
headers = {
        'x-api-token': '07HVm340iA9pO8iu0I3lMMniT21DaNZPVU6chOE7nD8'}

# Get All Kitties
url = 'https://public.api.cryptokitties.co/v1/kitties?'
logger.info("calling CryptoKitties API - getAllKitties")
response = requests.request('GET', url, headers = headers,
       data = payload, allow_redirects=False)
logger.info("response status - {}".format(response.status_code))

result = json.loads(response.text)

with open('allKitties.json', 'w') as outfile:
    json.dump(result, outfile)
logger.info("wrote allKitties to json")

s3.upload_file("allKitties.json","kittyfarm", "allKitties.json")
logger.info("uploaded allKitties.json to S3")

os.remove("allKitties.json")
logger.info("removed allKitties.json from local")

# Get Cattributes
url = 'https://public.api.cryptokitties.co/v1/cattributes'
logger.info("calling CryptoKitties API - getCattributes")
response = requests.request('GET', url, headers = headers,
       data = payload, allow_redirects=False)
logger.info("response status - {}".format(response.status_code))

result = json.loads(response.text)

with open('cattributes.json', 'w') as outfile:
    json.dump(result, outfile)
logger.info("wrote cattributes to json")

s3.upload_file("cattributes.json","kittyfarm", "cattributes.json")
logger.info("uploaded cattributes.json to S3")

os.remove("cattributes.json")
logger.info("removed cattributes.json from local")


