import os
import requests
import json

def create_meter(input_dict):
    """
    Sends a POST request to $STRAPI_URL/meters with the input_dict as JSON.
    Returns a dictionary with a 'status' field: 'success' if created, else 'failure'.

    Args:
        input_dict: A dictionary containing the meter data to be created.
            Example keys:
                code (str)
                parent (int or None)
                energyResource (int)
                consumptionLoadFactor (float)
                productionLoadFactor (float)
                type (str)
                city (str)
                state (str)
                latitude (float)
                longitude (float)
                pincode (str)

    Returns:
        dict: {'status': 'success', 'data': ...} if creation was successful,
              {'status': 'failure', 'error': ...} otherwise.
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/meters"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'data': input_dict})

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
