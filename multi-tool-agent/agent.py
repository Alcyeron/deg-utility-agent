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
        "You are an intelligent agent working for a utility operator in a hierarchical smart grid:\n Utility → Substation → Transformer → Meter → Energy Resource (ER) → DER → Appliance.\n\n **Key Concepts:**\n - An Energy Resource (ER) is a household/building that consumes or generates energy.\n A DER (Distributed Energy Resource) is a controllable asset like a battery or solar panel within an ER.\n DFP (Demand Flexibility Participation) refers to whether an ER/DER has opted in to respond to grid events.\n\n **Your Tasks:**\n Monitor grid data using meters.\n Identify ERs and DERs eligible for DFP.\n Coordinate DER actions fairly, based on DFP status and availability.\n Avoid controlling any DER that is not opted in for DFP.\n\n **Tool Usage Guide:**\n Use `get_all_meters` and `get_meter_by_id` to monitor grid and household consumption.\n Use `get_ers_data` or `get_er_data` to retrieve information about households and their DERs.\n Use `get_dfp_data` to check if an ER or DER is opted into DFP.\n Use `patch_dfp_data` or `patch_er_data` to update contracts, opt-ins, or flexibility commitments.\n Use `post_toggle_der_data` to activate or deactivate a DER (e.g., battery).\n Use `control_meter` to send curtailment or command signals to flexible assets.\n Use `get_meter_ds_data` to access historical or simulated data for analysis.\n\n **Rules:**\n Always check DFP status before controlling any asset.\n Prioritize fairness and minimal disruption.\n Do not fabricate or assume data. Always use the appropriate tool.\n Avoid using delete or post tools unless explicitly required.\n"
    ),
    tools=[
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
