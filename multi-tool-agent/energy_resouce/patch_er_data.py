import os
import requests
import json
from typing import List

def patch_er_data(er_id: int, meter: int, appliances: List[str]) -> dict:
    """
    Sends a PATCH request to $STRAPI_URL/energy-resources/{er_id} to update an Energy Resource entry.

    Args:
        er_id (int): The ID of the energy resource to update.
        meter (int): Meter ID to update.
        appliances (List[str]): List of appliances to update.

    Returns:
        dict: {'status': 'success', 'data': ...} if update succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    update_fields = {
        "meter": meter,
        "appliances": appliances
    }
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/energy-resources/{er_id}"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'data': update_fields})

    try:
        response = requests.patch(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code == 200:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
