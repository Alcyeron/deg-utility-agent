import os
import requests
from typing import Dict, Any

def get_management_logs() -> Dict[str, Any]:
    """
    Retrieves management logs from the grid status endpoint.
    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of management log entries
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
            management_log = response_json.get('results', {}).get('management_status', {}).get('management_log', [])
            return {'status': 'success', 'data': management_log}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 