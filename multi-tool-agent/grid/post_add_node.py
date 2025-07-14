import os
import requests
from typing import Dict, Any, List

def post_add_node(
    bus_name: str,
    neighborhood_id: int,
    coordinates: Dict[str, float],
    load_kw: float,
    load_kvar: float,
    connections: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Adds a new household (bus/node) by sending a POST request to the OpenDSS endpoint.

    Args:
        bus_name (str): Name of the new bus/node.
        neighborhood_id (int): ID of the neighborhood.
        coordinates (dict): Dictionary with 'x' and 'y' coordinates.
        load_kw (float): Load in kW.
        load_kvar (float): Load in kVAR.
        connections (list): List of connection dicts, each with 'to_bus', 'linecode', and 'length'.

    Returns:
        dict: {
            'status': 'success',
            'data': ...  # Response from the API
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

    url = f"{opendss_url}/add_node"
    payload = {
        "bus_name": bus_name,
        "neighborhood_id": neighborhood_id,
        "coordinates": coordinates,
        "load_kw": load_kw,
        "load_kvar": load_kvar,
        "connections": connections
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 