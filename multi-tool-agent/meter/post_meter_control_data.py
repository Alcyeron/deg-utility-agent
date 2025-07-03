import os
import requests
import json
from typing import Optional

def control_meter(meter_id: str, parent_meter_id: Optional[str], pincode: str, load_factor: float, log_type: str) -> dict:
    """
    Sends a POST request to $STRAPI_URL/meters/control to simulate meter control (e.g., load adjustment).

    Args:
        meter_id (str): Meter ID.
        parent_meter_id (Optional[str]): Parent meter ID or None.
        pincode (str): Postal code.
        load_factor (float): Load factor.
        log_type (str): Log type (e.g., 'CONSUMER').

    Returns:
        dict: {'status': 'success', 'data': ...} if control action succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    control_data = {
        "meter_id": meter_id,
        "parent_meter_id": parent_meter_id,
        "pincode": pincode,
        "load_factor": load_factor,
        "log_type": log_type
    }
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/meters/control"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(control_data)

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
