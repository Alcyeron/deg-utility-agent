import os
import requests
import json

def patch_dfp_data(id: int, is_active: bool) -> dict:
    """
    Patch DFP data.

    Args:
        id (int): The unique identifier.
        is_active (bool): The active status.

    Returns:
        dict: Status of the operation.
    """
    input_dict = {"id": id, "is_active": is_active}
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
