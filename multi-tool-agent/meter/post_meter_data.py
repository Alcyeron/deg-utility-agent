import os
import requests
import json
from typing import Optional

def create_meter(code: str, parent: Optional[int], energyResource: int, consumptionLoadFactor: float, productionLoadFactor: float, type: str, city: str, state: str, latitude: float, longitude: float, pincode: str) -> dict:
    """
    Sends a POST request to $STRAPI_URL/meters with the provided arguments as JSON.
    Returns a dictionary with a 'status' field: 'success' if created, else 'failure'.

    Args:
        code (str): Meter code.
        parent (Optional[int]): Parent meter ID or None.
        energyResource (int): Energy resource ID.
        consumptionLoadFactor (float): Consumption load factor.
        productionLoadFactor (float): Production load factor.
        type (str): Meter type.
        city (str): City.
        state (str): State.
        latitude (float): Latitude.
        longitude (float): Longitude.
        pincode (str): Postal code.

    Returns:
        dict: {'status': 'success', 'data': ...} if creation was successful,
              {'status': 'failure', 'error': ...} otherwise.
    """
    input_dict = {
        "code": code,
        "parent": parent,
        "energyResource": energyResource,
        "consumptionLoadFactor": consumptionLoadFactor,
        "productionLoadFactor": productionLoadFactor,
        "type": type,
        "city": city,
        "state": state,
        "latitude": latitude,
        "longitude": longitude,
        "pincode": pincode
    }
    strapi_url = os.environ.get('STRAPI_URL')
    if not strapi_url:
        return {'status': 'failure', 'error': 'STRAPI_URL not set in environment'}

    url = f"{strapi_url}/meters"
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({'data': input_dict})

    try:
        response = requests.post(url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code in [200, 201]:
            return {'status': 'success', 'data': response_json}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}
