import requests

def get_data (url,payload="",header={},verify=False):
    method="GET"
    response = requests.request(method, url=url, data=payload, headers=header,verify=verify)
    return (response)