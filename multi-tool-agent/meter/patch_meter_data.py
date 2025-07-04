import os
import requests
import json
from typing import Dict, Any

def patch_meter_data(meter_id: int, update_fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sends a PATCH request to $STRAPI_URL/meters/{id} with the update_fields as JSON.

    Args:
        meter_id (int): The ID of the meter to update.
        update_fields (dict): A dictionary of fields to update inside the "data" object.
            Example:
                {
                    "parent": None,
                    "energyResource": None,
                    "appliances": []
                }

    Returns:
        dict: {'status': 'success'} if update succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/meters/{meter_id}"
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
