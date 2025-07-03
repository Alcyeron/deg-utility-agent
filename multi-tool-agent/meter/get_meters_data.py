import os
import requests
from typing import Dict, Any

def get_all_meters(page: int = 1, page_size: int = 25) -> Dict[str, Any]:
    """
    Sends a GET request to $STRAPI_URL/meters to fetch all meters with populated relations.
    
    Args:
        page (int): The page number for pagination (default is 1).
        page_size (int): The number of items per page (default is 25).
    
    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of meter entries
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
        f"{strapi_url}/meters?"
        f"pagination[page]={page}&pagination[pageSize]={page_size}"
        f"&populate[0]=parent&populate[1]=energyResource&populate[2]=children"
        f"&populate[3]=appliances&sort[0]=children.code:desc"
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
