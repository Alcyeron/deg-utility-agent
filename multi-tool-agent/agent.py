import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
# DER
from .DER.post_toggle_der_data import post_toggle_der_data

# DFP
from .DFP.get_dfp_data import get_dfp_data
from .DFP.patch_dfp_data import patch_dfp_data

# energy_resouce
from .energy_resouce.get_er_data import get_er_data
from .energy_resouce.get_ers_data import get_ers_data
from .energy_resouce.del_er_data import del_er_data
from .energy_resouce.patch_er_data import patch_er_data
from .energy_resouce.post_er_data import post_er_data

# meter
from .meter.del_meter_data import delete_meter
from .meter.get_meter_data import get_meter_by_id
from .meter.get_meters_data import get_all_meters
from .meter.patch_meter_data import patch_meter_data
from .meter.post_meter_control_data import control_meter
from .meter.post_meter_data import create_meter

# meter_dataset
from .meter_dataset.get_meter_ds_data import get_meter_ds_data

root_agent = Agent(
    name="utility_dashboard_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the utility dashboard."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[
        post_toggle_der_data,
        get_dfp_data,
        patch_dfp_data,
        get_er_data,
        get_ers_data,
        del_er_data,
        patch_er_data,
        post_er_data,
        delete_meter,
        get_meter_by_id,
        get_all_meters,
        patch_meter_data,
        control_meter,
        create_meter,
        get_meter_ds_data,
    ],
)