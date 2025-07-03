import os
import requests

def delete_energy_resource(er_id):
    """
    Sends a DELETE request to $STRAPI_URL/energy-resources/{id} to delete a specific Energy Resource.

    Args:
        er_id (int): The unique identifier of the energy resource to delete.

    Returns:
        dict: {
            'status': 'success',
            'message': 'Energy Resource deleted'
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

    url = f"{strapi_url}/energy-resources/{er_id}"

    try:
        response = requests.delete(url)
        if response.status_code in [200, 204]:
            return {'status': 'success', 'message': 'Energy Resource deleted'}
        else:
            return {'status': 'failure', 'error': response.json()}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
