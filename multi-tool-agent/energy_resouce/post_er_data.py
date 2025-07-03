import os
import requests
import json
from typing import List, Optional

def post_er_data(name: str, type: str, meter: Optional[int], appliances: List[str]) -> dict:
    """
    Sends a POST request to $STRAPI_URL/energy-resources to create a new Energy Resource.

    Args:
        name (str): Name of the energy resource.
        type (str): Type of the energy resource.
        meter (int or None): Meter ID or None.
        appliances (List[str]): List of appliances.

    Returns:
        dict: {'status': 'success', 'data': ...} if creation succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    er_data = {
        "name": name,
        "type": type,
        "meter": meter,
        "appliances": appliances
    }
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/energy-resources"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'data': er_data})

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
