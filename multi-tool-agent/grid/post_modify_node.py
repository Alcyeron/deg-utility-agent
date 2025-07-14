import os
import requests
from typing import Dict, Any

def post_modify_node(bus_name: str, load_kw: float, load_kvar: float) -> Dict[str, Any]:
    """
    Modifies the details of a household (bus/node) by sending a POST request to the OpenDSS endpoint.

    Args:
        bus_name (str): Name of the bus/node to modify.
        load_kw (float): New load in kW.
        load_kvar (float): New load in kVAR.

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

    url = f"{opendss_url}/modify_node"
    payload = {
        "bus_name": bus_name,
        "load_kw": load_kw,
        "load_kvar": load_kvar
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