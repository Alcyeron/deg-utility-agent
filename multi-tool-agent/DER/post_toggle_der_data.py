import os
import requests
import json

def post_toggle_der_data(id, input_dict):
    """
    Sends a POST request to $STRAPI_URL/toggle-der/{id} to toggle a DER resource.
    Args:
        id (int): The unique identifier for the DER resource to be toggled (used in the URL).
        input_dict (dict): Dictionary containing the request body with the following keys:
            - der_id (str): The DER resource identifier (as a string)
            - switched_on (bool): Whether the DER should be switched on
    Returns:
        A dictionary with:
            - 'status': 'success' if toggled successfully, 'failure' otherwise
            - 'data': The response data if successful, else None
            - 'error': Error message if failure, else None
    Example request body:
        {
            "der_id": "8",
            "switched_on": true
        }
    Example error response:
        {
            "data": null,
            "error": {
                "status": 400,
                "name": "BadRequestError",
                "message": "DER not found"
            }
        }
    """
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment', 'data': None}

    url = f"{strapi_url}/toggle-der/{id}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(input_dict), headers=headers)
        response_json = response.json()
        if response_json.get('error'):
            return {
                'status': 'failure',
                'error': response_json['error'].get('message', 'Unknown error'),
                'data': None
            }
        else:
            return {
                'status': 'success',
                'data': response_json.get('data'),
                'error': None
            }
    except Exception as e:
        return {'status': 'failure', 'error': str(e), 'data': None}
