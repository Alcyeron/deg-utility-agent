import os
import requests
from typing import Dict, Any

def get_all_buses_data() -> Dict[str, Any]:
    """
    Sends a GET request to the OpenDSS endpoint to retrieve all bus (household) details (excluding transformer details).
    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of bus (household) entries
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
            # Exclude transformer details from each bus
            for bus in bus_details:
                if 'Transformers' in bus:
                    del bus['Transformers']
            return {'status': 'success', 'data': bus_details}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 