import os
import requests
from typing import Dict, Any

def get_neighbourhood_of_transformer(transformer_name: str) -> Dict[str, Any]:
    """
    Retrieves the neighbourhood ID of a particular transformer from the OpenDSS endpoint.

    Args:
        transformer_name (str): The name of the transformer.

    Returns:
        dict: {
            'status': 'success',
            'data': ...  # The neighbourhood ID
        }
        or
        dict: {
            'status': 'failure',
            'error': ...
        }
    """
    opendss_url = os.environ.get('OPENDSS_URL')
    if not opendss_url:
        return {'status': 'failure', 'error': 'OPENDSS_URL not set in environment'}

    url = f"{opendss_url}/get_node_data"
    try:
        response = requests.get(url)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            neighborhood_details = response_json.get('results', {}).get('neighborhood_details', {})
            bus_details = response_json.get('results', {}).get('bus_details', [])
            # Map bus name to neighbourhood
            bus_to_neigh = {}
            for neighbourhood_id, buses in neighborhood_details.items():
                for b in buses:
                    bus_to_neigh[str(b)] = neighbourhood_id
            # Find all buses with this transformer
            buses_with_transformer = set()
            for bus in bus_details:
                for transformer in bus.get('Transformers', []):
                    if str(transformer.get('name', '')) == str(transformer_name):
                        buses_with_transformer.add(str(bus.get('Bus')))
            # Find neighbourhoods for these buses
            neighbourhoods = set()
            for bus in buses_with_transformer:
                if bus in bus_to_neigh:
                    neighbourhoods.add(bus_to_neigh[bus])
            if neighbourhoods:
                return {'status': 'success', 'data': list(neighbourhoods)}
            else:
                return {'status': 'failure', 'error': f'Transformer {transformer_name} not found in any neighbourhood'}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 