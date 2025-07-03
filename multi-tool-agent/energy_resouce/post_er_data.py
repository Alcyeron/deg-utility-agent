import os
import requests
import json

def post_er_data(er_data):
    """
    Sends a POST request to $STRAPI_URL/energy-resources to create a new Energy Resource.

    Args:
        er_data (dict): A dictionary of fields to create the energy resource.
            Example:
                {
                    "name": "ABC's Home",
                    "type": "PROSUMER",
                    "meter": None,
                    "appliances": ["Air Conditioner (1.5 Ton)"]
                }

    Returns:
        dict: {'status': 'success', 'data': ...} if creation succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/energy-resources"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'data': er_data})

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
