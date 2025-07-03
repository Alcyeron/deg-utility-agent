import os
import requests

def get_er_data():
    """
    Sends a GET request to $STRAPI_URL/energy-resources?sort[0]=createdAt:desc&pagination[page]=1&populate[0]=meter&pagination[pageSize]=100
    to retrieve energy resource data.
    Returns:
        A dictionary with:
            - 'status': 'success' if data is retrieved, else 'failure'
            - 'data': list of energy resource dictionaries if successful, else None
                Each energy resource dictionary contains:
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
    """
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment', 'data': None}

    url = f"{strapi_url}/energy-resources?sort[0]=createdAt:desc&pagination[page]=1&populate[0]=meter&pagination[pageSize]=100"
    try:
        response = requests.get(url)
        response_json = response.json()
        if response_json.get('message') == 'Energy resources fetched successfully' and 'data' in response_json and 'results' in response_json['data']:
            return {'status': 'success', 'data': response_json['data']['results']}
        else:
            return {'status': 'failure', 'data': None}
    except Exception as e:
        return {'status': 'failure', 'error': str(e), 'data': None}
