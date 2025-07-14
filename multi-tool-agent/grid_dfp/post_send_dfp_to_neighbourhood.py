import os
import requests
from typing import Dict, Any

def post_send_dfp_to_neighbourhood(neighbourhood: int, dfp_name: str) -> Dict[str, Any]:
    """
    Sends a DFP to a neighbourhood by sending a POST request to the OpenDSS endpoint.

    Args:
        neighbourhood (int): The neighbourhood identifier.
        dfp_name (str): The name of the DFP to send.

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

    url = f"{opendss_url}/send_dfp_to_neighbourhood"
    payload = {
        "neighbourhood": neighbourhood,
        "dfp_name": dfp_name
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