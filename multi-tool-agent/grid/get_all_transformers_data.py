import os
import requests
from typing import Dict, Any, List

def get_all_transformers_data() -> Dict[str, Any]:
    """
    Retrieves all transformer details as a flat list (not grouped by bus).
    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of transformer entries
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
            bus_details = response_json.get('results', {}).get('bus_details', [])
            transformers: List[Any] = []
            for bus in bus_details:
                transformers.extend(bus.get('Transformers', []))
            return {'status': 'success', 'data': transformers}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 