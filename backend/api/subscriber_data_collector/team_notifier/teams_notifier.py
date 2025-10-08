import requests
import json
import base64

SOPORTE_CORE_CHANNEL_ID = "19:c89c06a00ead4116be0ad11739188fda@thread.tacv2"

FILE_FLOW_URL = "https://prod-37.westeurope.logic.azure.com:443/workflows/1666269ff6e54e0ba7ba27e4156803bd/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=OjcaDklhttqhDMdwwUmKSlUzzL6lN1WAHTGP_Fjy7Ag"
MESSAGE_FLOW_URL = "https://prod-204.westeurope.logic.azure.com:443/workflows/53e6f79bbdbf4ea9b3301462e9419074/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=FObRGWWjvQNQrWq_JqAMUsCBbD7NfV7Vy3CuRHF-U-c"


def send_teams_notification(message, channel_id=SOPORTE_CORE_CHANNEL_ID):

    payload = {
    "channel": channel_id,
    "message": message}

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(MESSAGE_FLOW_URL, data=json.dumps(payload), headers=headers, timeout=5)

    if response.status_code != 200 | 202:
        print(f"Failed to send message. Status code: {response.status_code}")
        return
    print(f"Message sent successfully! {response.status_code}")

def send_teams_file(log_file):
    PROXIES = {
    'http': 'http://e10356:Jcbb-2390-2009@10.162.64.36:8080',
    'https': 'http://e10356:Jcbb-2390-2009@10.162.64.36:8080'
    }

    with open(log_file,"rb") as txt:

        file_content = txt.read()
        encoded_file = base64.b64encode(file_content).decode('utf-8')

    data = {
        'nombre': 'log_outputs.log',
        'binario': encoded_file,
        'canal': SOPORTE_CORE_CHANNEL_ID
    }

    http_data = {
    'url': FILE_FLOW_URL,
    'json': data,
    'proxies': PROXIES
    }

    #send post
    session = requests.Session()
    session.trust_env = False
    response = session.post(**http_data)

    # Check the response status
    if response.status_code == 200 | 202:
        print(f"Message sent successfully! {response.status_code}")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")



