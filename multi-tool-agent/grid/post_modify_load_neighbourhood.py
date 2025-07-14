import os
import requests
from typing import Dict, Any

def post_modify_load_neighbourhood(neighbourhood: int, factor: float) -> Dict[str, Any]:
    """
    Modifies the load of a neighbourhood by sending a POST request to the OpenDSS endpoint.

    Args:
        neighbourhood (int): The neighbourhood identifier (not individual bus).
        factor (float): The factor by which to reduce the load.

    Returns:
        dict: {
            'status': 'success',
            'data': ...  # Response from the API
        }
        or
        dict: {
            'status': 'failure',
            'error': ...
        }
    """
    opendss_url = os.environ.get('OPENDSS_URL')
    if not opendss_url:
        return {'status': 'failure', 'error': 'OPENDSS_URL not set in environment'}

    url = f"{opendss_url}/modify_load_neighbourhood"
    payload = {
        "neighbourhood": neighbourhood,
        "factor": factor
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 