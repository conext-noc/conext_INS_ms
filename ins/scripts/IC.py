from helpers.utils.ssh import ssh
from helpers.handlers import request, spid, add_onu
from helpers.finder import optical, last_down_onu, device_type, new_onu
from helpers.constants import definitions

# FUNCTION IMPORT DEFINITIONS
db_request = request.db_request
add_service = add_onu.add_service
add_client = add_onu.add_client
optical_values = optical.optical_values
new_lookup = new_onu.new_lookup
calculate_spid = spid.calculate_spid
endpoints = definitions.endpoints
payload_add = definitions.payload_add
down_values = last_down_onu.down_values
client_place_holder = definitions.client_place_holder
client_payload = definitions.client_payload
type_finder = device_type.type_finder
olt_devices = definitions.olt_devices


def client_install(data):
    device = data["olt"]
    (comm, command, quit_ssh) = ssh(olt_devices[device])
    client = client_place_holder.copy()
    NEW_SN = data["sn"]
    (client["sn"], client["fsp"]) = new_lookup(comm, command, NEW_SN)
    if client["sn"] is None:
        quit_ssh()
        return {
            "error": True,
            "message": f"Serial {data['sn']} no esta conectado a la olt {device}",
            "client": None,
        }
    client["frame"] = int(client["fsp"].split("/")[0])
    client["slot"] = int(client["fsp"].split("/")[1])
    client["port"] = int(client["fsp"].split("/")[2])

    client["plan_name"] = data["plan_name"]

    db_plans = db_request(endpoints["get_plans"])["data"]
    plan_lists = [item["plan_name"] for item in db_plans]

    if client["plan_name"] not in plan_lists:
        quit_ssh()
        return {
            "error": True,
            "message": f"Plan {data['plan_name']} no esta registrado en la OLT",
            "client": None,
        }

    plan = next(
        (item for item in db_plans if item["plan_name"] == client["plan_name"]),
        None,
    )

    client["line_profile"] = plan["line_profile"]
    client["srv_profile"] = plan["srv_profile"]
    client["wan"][0] = plan

    client["name_1"] = data["name_1"]
    client["name_2"] = data["name_2"]
    client["contract"] = data["contract"].zfill(10)

    (client["onu_id"], client["fail"]) = add_client(comm, command, client)
    (client["temp"], client["pwr"]) = optical_values(comm, command, client, True)

    if float(client["pwr"]) <= -27.00:
        command(f'interface gpon {client["frame"]} {client["slot"]}')
        command(f'ont delete {client["port"]} {client["onu_id"]}')
        quit_ssh()
        return {
            "error": True,
            "message": f"Potencia de cliente excede limite de -27dBm, potencia @ {client['pwr']}, eliminando a cliente de OLT",
            "client": client,
        }

    client["device"] = type_finder(comm, command, client)

    add_service(command, client)

    for key in client_payload:
        client_payload[key] = client[key]

    client_payload["olt"] = device
    client_payload["fsp"] = f'{client["frame"]}/{client["slot"]}/{client["port"]}'
    client_payload[
        "fspi"
    ] = f'{client["frame"]}/{client["slot"]}/{client["port"]}/{client["onu_id"]}'
    client_payload["status"] = "online"
    client_payload["state"] = "active"
    client_payload["spid"] = client["wan"][0]["spid"]
    payload_add["data"] = client_payload.copy()
    req = db_request(endpoints["add_client"], payload_add)
    if req["error"]:
        print("an error occurred adding to db")
    else:
        print("successfully added client to db")

    quit_ssh()
    return {
        "error": False,
        "message": "success",
        "client": client,
    }
