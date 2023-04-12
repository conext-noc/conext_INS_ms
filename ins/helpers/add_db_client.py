import requests
import os
from dotenv import load_dotenv
load_dotenv()

def add_to_db(data):
  url = os.environ["DB_API_URI"]
  payload = {
    "name_1": data["name_1"],
    "name_2": data["name_2"],
    "contract": data["contract"],
    "olt": int(data["olt"]),
    "frame": int(data["frame"]),
    "slot": int(data["slot"]),
    "port": int(data["port"]),
    "onu_id": int(data["onu_id"]),
    "gem_port": int(data["wan"][0]["gem_port"]),
    "dba_profile": int(data["wan"][0]["dba_profile"]),
    "srv_profile": int(data["wan"][0]["srv_profile"]),
    "line_profile": int(data["wan"][0]["line_profile"]),
    "vlan": int(data["wan"][0]["vlan"]),
    "admin_status": "active"
}
  headers = {'content-type': 'application/json', 'conext-key':os.environ['CONEXT_KEY']}
  requests.post(url, json=payload, headers=headers)