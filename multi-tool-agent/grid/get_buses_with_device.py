import os
import requests
from typing import Dict, Any, List

def get_buses_with_device(device_type: str) -> Dict[str, Any]:
    """
    Retrieves all buses (households) that have a device with a specific type (partial, case-insensitive match on device name).
    Args:
        device_type (str): The device type to search for (e.g., 'television').
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
                for device in bus.get('Devices', []):
                    if device_type.lower() in str(device.get('device_name', '')).lower():
                        bus_copy = dict(bus)
                        if 'Transformers' in bus_copy:
                            del bus_copy['Transformers']
                        matches.append(bus_copy)
                        break
            return {'status': 'success', 'data': matches}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 