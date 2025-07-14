import os
import requests
from typing import Dict, Any, List

def search_dfp_by_attribute(attribute: str, value: str) -> Dict[str, Any]:
    """
    Retrieves DFP details that match a given attribute (case-insensitive, partial match).

    Args:
        attribute (str): The attribute to search by (e.g., 'name', 'description').
        value (str): The value to search for (partial, case-insensitive).

    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of matching DFP entries
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

    url = f"{opendss_url}/get_dfp_details"
    try:
        response = requests.get(url)
        response_json = response.json()
        if response.status_code == 200 and response_json.get('status') == 'success':
            dfps = response_json.get('dfps', [])
            matches: List[Any] = []
            for dfp in dfps:
                attr_val = str(dfp.get(attribute, '')).lower()
                if value.lower() in attr_val:
                    matches.append(dfp)
            return {'status': 'success', 'data': matches}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 