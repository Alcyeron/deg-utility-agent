import os
import requests
import json

def patch_er_data(er_id, update_fields):
    """
    Sends a PATCH request to $STRAPI_URL/energy-resources/{id} to update an Energy Resource entry.

    Args:
        er_id (int): The ID of the energy resource to update.
        update_fields (dict): A dictionary of fields to update inside the "data" object.
            Example:
                {
                    "meter": 1,
                    "appliances": [
                        "Ceiling Fan",
                        "Solar Panel (production)",
                        "Air Conditioner (1.5 Ton)"
                    ]
                }

    Returns:
        dict: {'status': 'success', 'data': ...} if update succeeded,
              {'status': 'failure', 'error': ...} otherwise.
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
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
