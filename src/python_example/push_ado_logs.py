import json
import requests
import datetime
import hashlib
import hmac
import base64

from constants import Constants
from env_var import Env

e = Env()

# The log type is the name of the event that is being submitted
log_type = "$(LogType)"

# An example JSON web monitor object
json_data = [{
    "DeploymentID": "$(Release.DeploymentID)",
    "ReleaseName": "$(Release.DefinitionName)",
    "AgentName": "$(Agent.Name)",
    "Time":"$CurrentTime",
    "Action":"$(Action)",
    "StoreName": "$(StoreName)"
  }
]
body = json.dumps(json_data)
print(body)

# Build the API signature
def build_signature(la_workspace_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, encoding='utf8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest())
    authorization = "SharedKey {}:{}".format(la_workspace_id,encoded_hash)
    return authorization

# Build and send a request to the POST API
def post_data(la_workspace_id, shared_key, body, log_type):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(la_workspace_id, shared_key, rfc1123date, content_length, method, content_type, resource)

    uri = 'https://' + la_workspace_id + Constants.LOG_ANALYTICS_ENDPOINT + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        print('Accepted')
    else:
        print("Response code: {}".format(response.status_code))

post_data(e.la_workspace_id, e.la_secret_key, body, log_type)