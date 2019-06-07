import requests
import json
import boto3
import os
import logging
import time

# Set up Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Boto3
s3 = boto3.client('s3')
KITTY_BUCKET = os.environ['KITTY_BUCKET']

# API Settings
KITTY_TOKEN = os.environ['KITTY_TOKEN']
payload = "{\n \"dappName\": \"KittyFarm\"\n}"
headers = {
        'x-api-token': KITTY_TOKEN}

# Get All Kitties
url = 'https://public.api.cryptokitties.co/v1/kitties'
logger.info("calling CryptoKitties API - getAllKitties")

# initial call to get total
response = requests.request('GET', url, headers = headers,
       data = payload, allow_redirects=False)
logger.info("response status - {}".format(response.status_code))
result = json.loads(response.text)
total = result["total"]

# start with offset = 0, increment by 5000, get all kitties
offset = 0
increment = 5000
cntr = 1

while offset < total:

    url = 'https://public.api.cryptokitties.co/v1/kitties?' + "offset=" + str(offset) + "&limit=" + str(increment)
    logger.info("calling CryptoKitties API - getAllKitties")
    response = requests.request('GET', url, headers = headers,
           data = payload, allow_redirects=False)
    logger.info("response status - {}".format(response.status_code))

    result = json.loads(response.text)
    out = json.dumps(result,indent=2)
    key = "kitties" + str(cntr) + ".json"

    s3.put_object(Bucket=KITTY_BUCKET,Key=key,Body=out)

    offset = offset + increment
    logger.info("finished call # " + str(cntr))
    cntr = cntr + 1
    time.sleep(.01)

logger.info("FINISHED ALL KITTIES PROCESS")




