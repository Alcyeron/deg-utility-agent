import os
import requests
from typing import Dict, Any

def post_register_dfp(name: str, description: str, min_power_kw: float, target_pf: float) -> Dict[str, Any]:
    """
    Registers a new Demand Flexibility Program (DFP) by sending a POST request to the OpenDSS endpoint.

    Args:
        name (str): Name of the DFP.
        description (str): Description of the DFP.
        min_power_kw (float): Minimum power in kW for the DFP.
        target_pf (float): Target power factor for the DFP.

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

    url = f"{opendss_url}/register_dfp"
    payload = {
        "name": name,
        "description": description,
        "min_power_kw": min_power_kw,
        "target_pf": target_pf
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