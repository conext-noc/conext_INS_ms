from ins.helpers.add_onu import add_device, add_service
from ins.helpers.devices import devices
from ins.helpers.decoder import decoder
from ins.helpers.data_lookup import data_lookup
from ins.helpers.mapper import PLANS
from ins.helpers.optical_finder import opticalValues
from ins.helpers.ont_type_finder import typeCheck
from ins.scripts.ssh import ssh


def confirm(client):
    fail = None
    oltOptions = ["1", "2", "3"]
    if client["olt"] in oltOptions:
        ip = devices[f"OLT{client['olt']}"]
        (comm, command, quit_ssh) = ssh(ip)
        _ = decoder(comm)

        (client["sn"], client["frame"], client["slot"], client["port"]) = data_lookup(
            comm, command, client
        )

        if client["sn"] is None or client["frame"] is None or client["slot"] is None:
            quit_ssh()
            return {"error": True, "message": "ONT NOT FOUND", "data": client}
        client["wan"] = [{}]
        client["wan"][0]["vlan"] = PLANS[client["plan_name"].upper()]["vlan"]
        client["wan"][0]["gem_port"] = PLANS[client["plan_name"].upper()]["gem_port"]
        client["wan"][0]["line_profile"] = PLANS[client["plan_name"].upper()][
            "line_profile"
        ]
        client["wan"][0]["dba_profile"] = PLANS[client["plan_name"].upper()][
            "dba_profile"
        ]
        client["wan"][0]["srv_profile"] = PLANS[client["plan_name"].upper()][
            "srv_profile"
        ]
        (client["onu_id"], client["fail"]) = add_device(comm, command, client)

        if client["fail"] is not None:
            quit_ssh()
            return {"error": True, "message": client["fail"], "data": client}

        (client["temperature"], client["power"], fail) = opticalValues(
            comm, command, client
        )
        client["type"] = typeCheck(comm, command, client)

        if client["power"] is None:
            quit_ssh()
            return {"error": True, "message": fail, "data": client}
        if float(client["power"]) <= -27.00:
            quit_ssh()
            return {
                "error": True,
                "message": f"Optical Power exceeds threshold of -27dBm, power @ {client['power']}",
                "data": client,
            }
        add_service(comm, command, client)

        quit_ssh()
        return {"error": False, "message": "Success", "data": client}

    return {"error": True, "message": "OLT does not exist", "data": client}
