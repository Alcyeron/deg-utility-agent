import os
import requests
from typing import Dict, Any

def get_grid_summary() -> Dict[str, Any]:
    """
    Retrieves the overall grid summary (power_summary and voltage_profile).
    Returns:
        dict: {
            'status': 'success',
            'data': {
                'power_summary': {...},
                'voltage_profile': {...}
            }
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
            results = response_json.get('results', {})
            power_summary = results.get('power_summary', {})
            voltage_profile = results.get('voltage_profile', {})
            return {'status': 'success', 'data': {'power_summary': power_summary, 'voltage_profile': voltage_profile}}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 