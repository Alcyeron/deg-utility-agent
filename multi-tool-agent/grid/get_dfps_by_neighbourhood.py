import os
import requests
from typing import Dict, Any
from collections import Counter, defaultdict

def get_dfps_by_transformer(transformer_name: str) -> Dict[str, Any]:
    """
    Retrieves DFPs by the neighbourhood of a given transformer, ranked by the number of households subscribed.

    Args:
        transformer_name (str): The name of the transformer.

    Returns:
        dict: {
            'status': 'success',
            'data': [
                {
                    'dfp_details': {...},
                    'subscribed_households': int
                },
                ...
            ]
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

    # Step 1: Get all bus and neighbourhood details
    url_node = f"{opendss_url}/get_node_data"
    try:
        response_node = requests.get(url_node)
        response_json_node = response_node.json()
        if response_node.status_code == 200 and response_json_node.get('status') == 'success':
            neighborhood_details = response_json_node.get('results', {}).get('neighborhood_details', {})
            bus_details = response_json_node.get('results', {}).get('bus_details', [])
        else:
            return {'status': 'failure', 'error': response_json_node}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}

    # Step 2: Find the bus that contains this transformer
    bus_name = None
    for bus in bus_details:
        for transformer in bus.get('Transformers', []):
            if str(transformer.get('name', '')) == str(transformer_name):
                bus_name = str(bus.get('Bus'))
                break
        if bus_name:
            break
    if not bus_name:
        return {'status': 'failure', 'error': f'Transformer {transformer_name} not found in any bus'}

    # Step 3: Find the neighbourhood for this bus
    neighbourhood_id = None
    for neigh_id, buses in neighborhood_details.items():
        if bus_name in [str(b) for b in buses]:
            neighbourhood_id = neigh_id
            break
    if not neighbourhood_id:
        return {'status': 'failure', 'error': f'Bus {bus_name} not found in any neighbourhood'}

    # Step 4: Get all buses in the neighbourhood
    bus_list = neighborhood_details.get(str(neighbourhood_id), [])
    if not bus_list:
        return {'status': 'failure', 'error': f'No buses found for neighbourhood {neighbourhood_id}'}

    # Step 5: Fetch all DFP details
    url_dfps_by_household = f"{opendss_url}/get_dfp_details"
    try:
        response_dfp = requests.get(url_dfps_by_household)
        response_json_dfp = response_dfp.json()
        if response_dfp.status_code == 200 and response_json_dfp.get('status') == 'success':
            all_dfps = response_json_dfp.get('dfps', [])
        else:
            return {'status': 'failure', 'error': response_json_dfp}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)}

    # For each DFP, count how many of its subscribed_buses are in the neighbourhood's bus list
    dfp_results = []
    bus_set = set(str(b) for b in bus_list)
    for dfp in all_dfps:
        subscribed_buses = set(str(b) for b in dfp.get('subscribed_buses', []))
        count = len(bus_set & subscribed_buses)
        if count > 0:
            dfp_results.append({
                'dfp_details': dfp,
                'subscribed_households': count
            })
    # Sort by subscribed_households descending
    dfp_results.sort(key=lambda x: x['subscribed_households'], reverse=True)
    return {'status': 'success', 'data': dfp_results} 