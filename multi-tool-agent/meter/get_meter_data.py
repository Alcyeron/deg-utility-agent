import os
import requests

def get_meter_by_id(meter_id):
    """
    Sends a GET request to $STRAPI_URL/meters/{id} to fetch a single meter entry with populated relations.

    Args:
        meter_id (int): The unique identifier of the meter to retrieve.

    Returns:
        dict: {
            'status': 'success',
            'data': {...}  # Single meter object
        } 
        or 
        dict: {
            'status': 'failure',
            'error': ...  # Error message or response
        }
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = (
        f"{strapi_url}/meters/{meter_id}?"
        f"populate[0]=parent&populate[1]=energyResource&populate[2]=children"
        f"&populate[3]=appliances"
    )

    try:
        response = requests.get(url)
        response_json = response.json()

        if response.status_code == 200:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
