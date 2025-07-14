import os
import requests
from typing import Dict, Any, List

def get_households_by_dfp(dfp_index: int) -> Dict[str, Any]:
    """
    Retrieves all household (bus) details subscribed to a specific DFP by index.

    Args:
        dfp_index (int): The index of the DFP.

    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of bus details
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

    # Step 1: Get the list of bus names subscribed to the DFP
    url_dfp = f"{opendss_url}/get_dfp_details"
    try:
        response_dfp = requests.get(url_dfp)
        response_json_dfp = response_dfp.json()
        if response_dfp.status_code == 200 and response_json_dfp.get('status') == 'success':
            dfps = response_json_dfp.get('dfps', [])
            subscribed_buses = None
            for dfp in dfps:
                if dfp.get('index') == dfp_index:
                    subscribed_buses = set(str(b) for b in dfp.get('subscribed_buses', []))
                    break
            if subscribed_buses is None:
                return {'status': 'failure', 'error': f'DFP with index {dfp_index} not found'}
        else:
            return {'status': 'failure', 'error': response_json_dfp}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}

    # Step 2: Get all bus details and filter by subscribed bus names
    url_node = f"{opendss_url}/get_node_data"
    try:
        response_node = requests.get(url_node)
        response_json_node = response_node.json()
        if response_node.status_code == 200 and response_json_node.get('status') == 'success':
            bus_details = response_json_node.get('results', {}).get('bus_details', [])
            filtered_buses = [bus for bus in bus_details if str(bus.get('Bus')) in subscribed_buses]
            return {'status': 'success', 'data': filtered_buses}
        else:
            return {'status': 'failure', 'error': response_json_node}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 