import os
import requests
from typing import Dict, Any

def put_update_dfp(name: str, min_power_kw: float, target_pf: float) -> Dict[str, Any]:
    """
    Modifies a Demand Flexibility Program (DFP) by sending a PUT request to the OpenDSS endpoint.

    Args:
        name (str): Name of the DFP to update.
        min_power_kw (float): New minimum power in kW for the DFP.
        target_pf (float): New target power factor for the DFP.

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

    url = f"{opendss_url}/update_dfp"
    payload = {
        "name": name,
        "min_power_kw": min_power_kw,
        "target_pf": target_pf
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.put(url, json=payload, headers=headers)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 