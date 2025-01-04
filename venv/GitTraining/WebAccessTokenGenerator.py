import json
import requests
import pandas as pd

print('program is starting')

# Update the Parameters
server = '' # sisense url in format: https://myserver.sisense.com
token = '' # sisense admin authentication token
secret = '' # web access token secret key - generate one time while creating the token name
kid = '' # token name key id
sub = '' # Viewer user id which behalf on this user the token is created
dashboard_oid = '' # dashboard id for the token creation

# Optional Parameters - example for Datasecurity and apply filters

# Apply dashboard filter
flt = [
    {
        "jaql": {
            "dataSourceTitle": "Sample Retail",
            "table": "DimCountries",
            "column": "CountryName",
            "dim": "[DimCountries.CountryName]",
            "datatype": "text",
            "filter": {
                "members": []
            },
            "title": "CountryName"
        }
    }
]

# Apply Data Security

acl = [
    {
        "dataSourceTitle": "Sample Retail",
        "table": "DimCountries",
        "column": "Region",
        "allMembers": None,
        "datatype": "text",
        "members": [
            "Europe"
        ],
        "exclusionary": False
    }
]

def web_access_token_generator(server,token,secret,kid,sub,dashboard_oid,flt,acl):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    endpoint = '/api/v1/wat/generate'
    url = f'{server}{endpoint}'

    payload = {
        "header": {
            "typ": "JWT",
            "kid": kid,
            "alg": "RSA-OAEP-256",
            "enc": "A128GCM",
            "zip": "DEF"
        },
        "payload": {
            "sub": sub,
            "grants": {
                "flt": flt,
                "acl": acl
            }
        },
        "secret": secret
    }

    json_payload = json.dumps(payload)

    try:
        response = requests.post(url=url, headers=headers, data=json_payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        wat_token = response.content.decode('utf-8')
        dashboard_link = f'{server}/wat/{wat_token}/app/main#/dashboards/{dashboard_oid}?embed=true&l=false&r=true'
        return dashboard_link
    except Exception as e:
        # Handle any unexpected exceptions, including network issues, JSON parsing errors, and others
        print(f"An error occurred: {e}")
        result = json.loads(response.content)
        print(f"error reason - {result['error']['message']}")
        return None


dashboard_link = web_access_token_generator(server,token,secret,kid,sub,dashboard_oid,flt,acl)
print(dashboard_link)





