import os
import requests

def get_meter_ds_data(dataset_id):
    """
    Sends a GET request to $STRAPI_URL/meter-datasets/{id} to fetch a specific meter dataset.

    Args:
        dataset_id (int): The unique ID of the meter dataset.

    Returns:
        dict: {
            'status': 'success',
            'data': {...}  # Meter dataset object
        }
        or
        dict: {
            'status': 'failure',
            'error': ...
        }
    """
    strapi_url = os.environ.get('STRAPI_URL')  # e.g., http://localhost:1337/meter-data-simulator
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/meter-datasets/{dataset_id}"

    try:
        response = requests.get(url)
        response_json = response.json()

        if response.status_code == 200:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}