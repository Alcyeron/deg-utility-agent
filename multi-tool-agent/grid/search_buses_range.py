import os
import requests
from typing import Dict, Any, List, Optional

def search_buses_range(
    gen_kw_min: Optional[float] = None, gen_kw_max: Optional[float] = None,
    load_kw_min: Optional[float] = None, load_kw_max: Optional[float] = None,
    net_power_kw_min: Optional[float] = None, net_power_kw_max: Optional[float] = None,
    vangle_min: Optional[float] = None, vangle_max: Optional[float] = None,
    vmag_pu_min: Optional[float] = None, vmag_pu_max: Optional[float] = None
) -> Dict[str, Any]:
    """
    Searches buses (households) for a range of values for gen_kw, load_kw, net_power_kw, vangle, and vmag_pu.
    All parameters are optional; if provided, they filter the results.

    Args:
        gen_kw_min (float, optional): Minimum value for Gen_kW.
        gen_kw_max (float, optional): Maximum value for Gen_kW.
        load_kw_min (float, optional): Minimum value for Load_kW.
        load_kw_max (float, optional): Maximum value for Load_kW.
        net_power_kw_min (float, optional): Minimum value for Net_Power_kW.
        net_power_kw_max (float, optional): Maximum value for Net_Power_kW.
        vangle_min (float, optional): Minimum value for VAngle.
        vangle_max (float, optional): Maximum value for VAngle.
        vmag_pu_min (float, optional): Minimum value for VMag_pu.
        vmag_pu_max (float, optional): Maximum value for VMag_pu.

    Returns:
        dict: {
            'status': 'success',
            'data': [ ... ]  # List of matching bus entries
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
                # Check all filters
                if gen_kw_min is not None and bus.get('Gen_kW', 0) < gen_kw_min:
                    continue
                if gen_kw_max is not None and bus.get('Gen_kW', 0) > gen_kw_max:
                    continue
                if load_kw_min is not None and bus.get('Load_kW', 0) < load_kw_min:
                    continue
                if load_kw_max is not None and bus.get('Load_kW', 0) > load_kw_max:
                    continue
                if net_power_kw_min is not None and bus.get('Net_Power_kW', 0) < net_power_kw_min:
                    continue
                if net_power_kw_max is not None and bus.get('Net_Power_kW', 0) > net_power_kw_max:
                    continue
                if vangle_min is not None and bus.get('VAngle', 0) < vangle_min:
                    continue
                if vangle_max is not None and bus.get('VAngle', 0) > vangle_max:
                    continue
                if vmag_pu_min is not None and bus.get('VMag_pu', 0) < vmag_pu_min:
                    continue
                if vmag_pu_max is not None and bus.get('VMag_pu', 0) > vmag_pu_max:
                    continue
                bus_copy = dict(bus)
                if 'Transformers' in bus_copy:
                    del bus_copy['Transformers']
                matches.append(bus_copy)
            return {'status': 'success', 'data': matches}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 