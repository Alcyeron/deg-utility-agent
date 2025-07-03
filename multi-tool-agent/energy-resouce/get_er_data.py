import os
import requests

def get_er_data(id):
    """
    Sends a GET request to $STRAPI_URL/energy-resources/{id}?populate[0]=meter.parent&populate[1]=meter.children&populate[2]=meter.appliances
    to retrieve a specific energy resource by id.
    Args:
        id (int): The unique identifier for the energy resource.
    Returns:
        A dictionary with:
            - 'status': 'success' if data is retrieved, else 'failure'
            - 'data': energy resource dictionary if successful, else None
                The energy resource dictionary contains:
                    - id (int): Unique identifier for the energy resource
                    - name (str): Name of the energy resource
                    - type (str): Type of the energy resource (e.g., 'CONSUMER')
                    - createdAt (str): ISO timestamp of creation
                    - updatedAt (str): ISO timestamp of last update
                    - publishedAt (str): ISO timestamp of publication
                    - meter (dict): Dictionary with the following fields:
                        - id (int): Unique identifier for the meter
                        - code (str): Meter code
                        - consumptionLoadFactor (int): Consumption load factor
                        - productionLoadFactor (int): Production load factor
                        - type (str): Type of the meter (e.g., 'SMART')
                        - city (str): City where the meter is located
                        - state (str): State where the meter is located
                        - latitude (float): Latitude coordinate
                        - longitude (float): Longitude coordinate
                        - pincode (str): Postal code
                        - createdAt (str): ISO timestamp of meter creation
                        - updatedAt (str): ISO timestamp of meter update
                        - publishedAt (str): ISO timestamp of meter publication
                        - max_capacity_KW (int): Maximum capacity in kilowatts
                        - dfp_subscription_id (any): DFP subscription ID or null
                        - children (list): List of child meters (could be empty)
                        - parent (dict or None): Parent meter or None
    Example success response:
        {
            "message": "Energy resource fetched successfully",
            "data": { ... }
        }
    Example error response:
        {
            "data": null,
            "error": {
                "status": 404,
                "name": "NotFoundError",
                "message": "Energy resource not found",
                "details": {}
            }
        }
    """
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment', 'data': None}

    url = f"{strapi_url}/energy-resources/{id}?populate[0]=meter.parent&populate[1]=meter.children&populate[2]=meter.appliances"
    try:
        response = requests.get(url)
        response_json = response.json()
        if response_json.get('message') == 'Energy resource fetched successfully' and 'data' in response_json and response_json['data']:
            return {'status': 'success', 'data': response_json['data']}
        else:
            error_msg = None
            if 'error' in response_json and 'message' in response_json['error']:
                error_msg = response_json['error']['message']
            return {'status': 'failure', 'data': None, 'error': error_msg}
    except Exception as e:
        return {'status': 'failure', 'error': str(e), 'data': None}
