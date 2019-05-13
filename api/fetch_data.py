import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import boto3
import os
import logging
import time


# def requests_retry_session(
#     retries=3,
#     backoff_factor=0.3,
#     status_forcelist=(500, 502, 504),
#     session=None,
# ):

#     """Retry requests at least 3 times before failing"""

#     session = session or requests.Session()
#     retry = Retry(
#         total=retries,
#         read=retries,
#         connect=retries,
#         backoff_factor=backoff_factor,
#         status_forcelist=status_forcelist,
#     )
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount('http://', adapter)
#     session.mount('https://', adapter)
#     return session

# Set up Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Boto3
s3 = boto3.client('s3')

# Start requests session
# s = requests.Session()
# s.headers.update({'x-api-token': '07HVm340iA9pO8iu0I3lMMniT21DaNZPVU6chOE7nD8'})

# API Settings
payload = "{\n \"dappName\": \"KittyFarm\"\n}"
headers = {
        'x-api-token': '07HVm340iA9pO8iu0I3lMMniT21DaNZPVU6chOE7nD8'}

# Get All Kitties
url = 'https://public.api.cryptokitties.co/v1/kitties'
logger.info("calling CryptoKitties API - getAllKitties")

# initial call to get total
response = requests.request('GET', url, headers = headers,
       data = payload, allow_redirects=False)
logger.info("response status - {}".format(response.status_code))
result = json.loads(response.text)
total = result["total"]

# # final call to get all
# url = 'https://public.api.cryptokitties.co/v1/kitties?' + "limit=" + str(total)
# response = requests.request('GET', url, headers = headers,
#        data = payload, allow_redirects=False)
# logger.info("response status - {}".format(response.status_code))
# result = json.loads(response.text)

# start with offset = 0, increment by 10000, get all kitties
offset = 1375000
increment = 5000
cntr = 160

while offset < total:

    url = 'https://public.api.cryptokitties.co/v1/kitties?' + "offset=" + str(offset) + "&limit=" + str(increment)
    logger.info("calling CryptoKitties API - getAllKitties")
    response = requests.request('GET', url, headers = headers,
           data = payload, allow_redirects=False)
    logger.info("response status - {}".format(response.status_code))

    result = json.loads(response.text)
    out = json.dumps(result,indent=2)
    key = "kitties" + str(cntr) + ".json"

    s3.put_object(Bucket='jdc-nu',Key=key,Body=out)

    offset = offset + increment
    logger.info("finished call # " + str(cntr))
    cntr = cntr + 1
    time.sleep(.01)

# transform kitty list to json
# out = json.dumps(kittyList,indent=2)

# # Method 1: Object.put()
# s3 = boto3.resource('s3')
# object = s3.Object('jdc-nu', 'allKittiesV2.json')
# object.put(Body=out)

# # Method 2: Client.put_object()
# client = boto3.client('s3')
# client.put_object(Body=more_binary_data, Bucket='my_bucket_name', Key='my/key/including/anotherfilename.txt')

# upload json to s3
# s3.put_object(Bucket='jdc-nu',Key='allKitties' + str(cntr) + '.json',Body=out)
# logger.info("uploaded allKitties to S3")

logger.info("FINISHED ALL KITTIES PROCESS")

# # Get Cattributes
# url = 'https://public.api.cryptokitties.co/v1/cattributes'
# logger.info("calling CryptoKitties API - getCattributes")
# response = requests.request('GET', url, headers = headers,
#        data = payload, allow_redirects=False)
# logger.info("response status - {}".format(response.status_code))

# result = json.loads(response.text)

# with open('cattributes.json', 'w') as outfile:
#     json.dump(result, outfile)
# logger.info("wrote cattributes to json")

# s3.upload_file("cattributes.json","kittyfarm", "cattributes.json")
# logger.info("uploaded cattributes.json to S3")

# os.remove("cattributes.json")
# logger.info("removed cattributes.json from local")



