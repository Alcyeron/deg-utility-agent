import os
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

def search_dfp_by_range(
    min_power_kw_min: Optional[float] = None, min_power_kw_max: Optional[float] = None,
    target_pf_min: Optional[float] = None, target_pf_max: Optional[float] = None,
    registered_at_start: Optional[str] = None, registered_at_end: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves DFPs by range of min_power_kw, target_pf, and registration date.

    Args:
        min_power_kw_min (float, optional): Minimum value for min_power_kw.
        min_power_kw_max (float, optional): Maximum value for min_power_kw.
        target_pf_min (float, optional): Minimum value for target_pf.
        target_pf_max (float, optional): Maximum value for target_pf.
        registered_at_start (str, optional): Start date (inclusive) for registration, in 'YYYY-MM-DD' format.
        registered_at_end (str, optional): End date (inclusive) for registration, in 'YYYY-MM-DD' format.

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
                if min_power_kw_min is not None and dfp.get('min_power_kw', 0) < min_power_kw_min:
                    continue
                if min_power_kw_max is not None and dfp.get('min_power_kw', 0) > min_power_kw_max:
                    continue
                if target_pf_min is not None and dfp.get('target_pf', 0) < target_pf_min:
                    continue
                if target_pf_max is not None and dfp.get('target_pf', 0) > target_pf_max:
                    continue
                if registered_at_start or registered_at_end:
                    reg_date_str = dfp.get('registered_at', None)
                    if reg_date_str:
                        try:
                            reg_date = datetime.strptime(reg_date_str.split()[0], '%Y-%m-%d')
                        except Exception:
                            continue
                        if registered_at_start:
                            start_date = datetime.strptime(registered_at_start, '%Y-%m-%d')
                            if reg_date < start_date:
                                continue
                        if registered_at_end:
                            end_date = datetime.strptime(registered_at_end, '%Y-%m-%d')
                            if reg_date > end_date:
                                continue
                matches.append(dfp)
            return {'status': 'success', 'data': matches}
        else:
            return {'status': 'failure', 'error': response_json}
    except Exception as e:
        return {'status': 'failure', 'error': str(e)} 