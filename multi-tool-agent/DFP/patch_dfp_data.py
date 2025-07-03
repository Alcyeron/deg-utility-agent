import os
import requests
import json

def patch_dfp_data(input_dict):
    """
    Sends a PATCH request to $STRAPI_URL/dfp with the input_dict as JSON.
    Returns a dictionary with a 'status' field: 'success' if updated, else 'failure'.
    Args:
        input_dict: A dictionary containing the data to be patched.
            keys:
                id (int): The unique identifier for the DFP entry.
                is_active (bool): The active status to be set for the DFP entry.
    Returns:
        A dictionary with a 'status' field: 'success' if updated, else 'failure'.
    """
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/dfp"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.patch(url, data=json.dumps(input_dict), headers=headers)
        response_json = response.json()
        if response_json.get('message') == 'DFP updated successfully':
            return {'status': 'success'}
        else:
            return {'status': 'failure'}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
