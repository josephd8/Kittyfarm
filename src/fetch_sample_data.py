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

# API Settings
KITTY_TOKEN = os.environ['KITTY_TOKEN']
payload = "{\n \"dappName\": \"KittyFarm\"\n}"
headers = {
        'x-api-token': KITTY_TOKEN}

sample = 1000

# Get All Kitties
url = 'https://public.api.cryptokitties.co/v1/kitties?' + "limit=" + str(sample)
logger.info("calling CryptoKitties API - getAllKitties")

# initial call to get total
response = requests.request('GET', url, headers = headers,
       data = payload, allow_redirects=False)
logger.info("response status - {}".format(response.status_code))
result = json.loads(response.text)

out = json.dumps(result,indent=2)
key = "kittySample.json"
s3.put_object(Bucket='jdc-nu',Key=key,Body=out)

logger.info("finished api call to get sample of " + str(sample) + " kitties")
logger.info("FINISHED SAMPLE KITTIES PROCESS")




