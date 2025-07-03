import os
import requests
import json

def control_meter(control_data):
    """
    Sends a POST request to $STRAPI_URL/meters/control to simulate meter control (e.g., load adjustment).

    Args:
        control_data (dict): Control payload to send.
            Example:
                {
                    "meter_id": "METER003",
                    "parent_meter_id": None,
                    "pincode": "",
                    "load_factor": 0.82,
                    "log_type": "CONSUMER"
                }

    Returns:
        dict: {'status': 'success', 'data': ...} if control action succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/meters/control"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(control_data)

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
