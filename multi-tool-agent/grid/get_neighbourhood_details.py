import os
import requests
from typing import Dict, Any

def get_neighbourhood_details() -> Dict[str, Any]:
    """
    Retrieves all neighbourhood details from the OpenDSS endpoint.

    Returns:
        dict: {
            'status': 'success',
            'data': ...  # The neighborhood_details field from the API
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

    url = f"{opendss_url}/get_node_data"
    try:
        response = requests.get(url)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            neighborhood_details = response_json.get('results', {}).get('neighborhood_details', {})
            return {'status': 'success', 'data': neighborhood_details}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 