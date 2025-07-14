import os
import requests
from typing import Dict, Any

def delete_dfp(name: str) -> Dict[str, Any]:
    """
    Deletes a Demand Flexibility Program (DFP) by sending a DELETE request to the OpenDSS endpoint.

    Args:
        name (str): Name of the DFP to delete.

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

    url = f"{opendss_url}/delete_dfp"
    payload = {
        "name": name
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.delete(url, json=payload, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 