import os
import requests
from typing import Dict, Any

def get_bus_data(bus_id: str) -> Dict[str, Any]:
    """
    Retrieves details for a specific bus (household) by Bus ID, excluding transformer details.
    Args:
        bus_id (str): The Bus ID to retrieve.
    Returns:
        dict: {
            'status': 'success',
            'data': {...}  # Bus (household) entry
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
            for bus in bus_details:
                if str(bus.get('Bus')) == str(bus_id):
                    bus = dict(bus)  # Copy to avoid mutating original
                    if 'Transformers' in bus:
                        del bus['Transformers']
                    return {'status': 'success', 'data': bus}
            return {'status': 'failure', 'error': f'Bus ID {bus_id} not found'}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 