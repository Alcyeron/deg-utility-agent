import os
import requests
from typing import Dict, Any

def get_transformer_data(transformer_name: str) -> Dict[str, Any]:
    """
    Retrieves details for a specific transformer by name.
    Args:
        transformer_name (str): The name of the transformer to retrieve.
    Returns:
        dict: {
            'status': 'success',
            'data': {...}  # Transformer entry
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
            bus_details = response_json.get('results', {}).get('bus_details', [])
            for bus in bus_details:
                for transformer in bus.get('Transformers', []):
                    if str(transformer.get('name', '')).lower() == transformer_name.lower():
                        return {'status': 'success', 'data': transformer}
            return {'status': 'failure', 'error': f'Transformer {transformer_name} not found'}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 