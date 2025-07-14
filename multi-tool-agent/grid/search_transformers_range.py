import os
import requests
from typing import Dict, Any, List, Optional

def search_transformers_range(
    current_kva_min: Optional[float] = None, current_kva_max: Optional[float] = None,
    rated_kva_min: Optional[float] = None, rated_kva_max: Optional[float] = None,
    loading_percent_min: Optional[float] = None, loading_percent_max: Optional[float] = None
) -> Dict[str, Any]:
    """
    Searches transformers for a range of values for current_kva, rated_kva, and loading_percent.
    All parameters are optional; if provided, they filter the results.

    Args:
        current_kva_min (float, optional): Minimum value for current_kVA.
        current_kva_max (float, optional): Maximum value for current_kVA.
        rated_kva_min (float, optional): Minimum value for rated_kVA.
        rated_kva_max (float, optional): Maximum value for rated_kVA.
        loading_percent_min (float, optional): Minimum value for loading_percent.
        loading_percent_max (float, optional): Maximum value for loading_percent.

    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of matching transformer entries
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
            matches: List[Any] = []
            for bus in bus_details:
                for transformer in bus.get('Transformers', []):
                    if current_kva_min is not None and transformer.get('current_kVA', 0) < current_kva_min:
                        continue
                    if current_kva_max is not None and transformer.get('current_kVA', 0) > current_kva_max:
                        continue
                    if rated_kva_min is not None and transformer.get('rated_kVA', 0) < rated_kva_min:
                        continue
                    if rated_kva_max is not None and transformer.get('rated_kVA', 0) > rated_kva_max:
                        continue
                    if loading_percent_min is not None and transformer.get('loading_percent', 0) < loading_percent_min:
                        continue
                    if loading_percent_max is not None and transformer.get('loading_percent', 0) > loading_percent_max:
                        continue
                    matches.append(transformer)
            return {'status': 'success', 'data': matches}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 