import os
import requests
from typing import Dict, Any, List

def search_buses(attribute: str, value: str) -> Dict[str, Any]:
    """
    Searches buses (households) by any attribute, supporting partial and case-insensitive matches.
    Args:
        attribute (str): The attribute to search by (e.g., 'Bus', 'Load_kW').
        value (str): The value to search for (partial, case-insensitive).
    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of matching bus entries
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
            matches: List[Any] = []
            for bus in bus_details:
                attr_val = str(bus.get(attribute, '')).lower()
                if value.lower() in attr_val:
                    bus_copy = dict(bus)
                    if 'Transformers' in bus_copy:
                        del bus_copy['Transformers']
                    matches.append(bus_copy)
            return {'status': 'success', 'data': matches}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 