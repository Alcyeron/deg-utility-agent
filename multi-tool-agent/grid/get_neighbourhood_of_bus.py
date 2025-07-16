import os
import requests
from typing import Dict, Any

def get_neighbourhood_of_bus(bus_name: str) -> Dict[str, Any]:
    """
    Retrieves the neighbourhood ID of a particular bus from the OpenDSS endpoint.

    Args:
        bus_name (str): The name of the bus (household).

    Returns:
        dict: {
            'status': 'success',
            'data': ...  # The neighbourhood ID
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
            for neighbourhood_id, buses in neighborhood_details.items():
                if str(bus_name) in [str(b) for b in buses]:
                    return {'status': 'success', 'data': neighbourhood_id}
            return {'status': 'failure', 'error': f'Bus {bus_name} not found in any neighbourhood'}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 