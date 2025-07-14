import os
import requests
from typing import Dict, Any, List

def get_dfps_by_household(bus_name: str) -> Dict[str, Any]:
    """
    Retrieves all DFP details subscribed by a specific household (bus).

    Args:
        bus_name (str): The name of the bus (household).

    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of DFP details
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

    # Step 1: Get DFP indices for the household
    url_node = f"{opendss_url}/get_node_data"
    try:
        response_node = requests.get(url_node)
        response_json_node = response_node.json()
        if response_node.status_code == 200 and response_json_node.get('status') == 'success':
            bus_details = response_json_node.get('results', {}).get('bus_details', [])
            dfp_indices = None
            for bus in bus_details:
                if str(bus.get('Bus')) == str(bus_name):
                    dfp_indices = set(bus.get('DFPs', []))
                    break
            if dfp_indices is None:
                return {'status': 'failure', 'error': f'Bus {bus_name} not found'}
        else:
            return {'status': 'failure', 'error': response_json_node}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}

    # Step 2: Get all DFP details and filter by indices
    url_dfp = f"{opendss_url}/get_dfp_details"
    try:
        response_dfp = requests.get(url_dfp)
        response_json_dfp = response_dfp.json()
        if response_dfp.status_code == 200 and response_json_dfp.get('status') == 'success':
            dfps = response_json_dfp.get('dfps', [])
            filtered_dfps = [dfp for dfp in dfps if dfp.get('index') in dfp_indices]
            return {'status': 'success', 'data': filtered_dfps}
        else:
            return {'status': 'failure', 'error': response_json_dfp}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 