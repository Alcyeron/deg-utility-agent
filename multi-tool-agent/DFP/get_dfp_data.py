import os
import requests
from typing import Dict, Any

def get_dfp_data() -> Dict[str, Any]:
    """
    Sends a GET request to $STRAPI_URL/dfp to retrieve DFP data.
    Returns:
        A dictionary with:
            - 'status': 'success' if data is retrieved, else 'failure'
            - 'data': list of dictionaries, each representing a DFP entry, or None on failure
                Each DFP entry dictionary contains:
                    - id (int): Unique identifier for the DFP entry
                    - name (str): Name of the DFP entry
                    - intent (str): Intent description
                    - is_active (bool): Whether the DFP entry is active
                    - subscriptions (list of dict): List of subscription dictionaries, each with:
                        - participating (bool): Participation status
                        - energy_resource_name (str): Name of the energy resource
                    - utilities (list of str): List of utility company names
    """
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/dfp"
    try:
        response = requests.get(url)
        response_json = response.json()
        if 'data' in response_json:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'data': None}
    except Exception as e:
        return {'status': 'failure', 'error': str(e), 'data': None}
