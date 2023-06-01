from time import sleep
from ins.helpers.decoder import decoder, check
from ins.helpers.fail_handler import failChecker
from ins.helpers.spid_check import spidCalc


def add_device(comm, command, client):
    command(f"interface gpon {client['frame']}/{client['slot']}")
    command(
        f'ont add {client["port"]} sn-auth {client["sn"]} omci ont-lineprofile-id {client["wan"][0]["line_profile"]} ont-srvprofile-id {client["wan"][0]["srv_profile"]} desc "{client["name_1"].upper().replace(" ","_")} {client["name_2"].upper().replace(" ","_")} {client["contract"]}" '
    )
    value = decoder(comm)
    fail = failChecker(value)
    if fail is None:
        (_, end) = check(value, "ONTID :").span()
        ID = value[end : end + 3].replace(" ", "").replace("\n", "").replace("\r", "")
        command(
            f'ont optical-alarm-profile {client["port"]} {ID} profile-name ALARMAS_OPTICAS'
        )
        command(f'ont alarm-policy {client["port"]} {ID} policy-name FAULT_ALARMS')
        command("quit")
        return (ID, fail)
    return (None, fail)


def add_service(comm, command, client):
    client["wan"][0]["spid"] = (
        spidCalc(client)["I"]
        if "_IP" not in client["plan_name"].upper()
        else spidCalc(client)["P"]
    )

    command(f"interface gpon {client['frame']}/{client['slot']}")

    if client["device_type"].upper() == "B":
        command(
            f" ont port native-vlan {client['port']} {client['onu_id']} eth 1 vlan {client['wan'][0]['vlan']} "
        )

    command(
        f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {client['wan'][0]['vlan']}"
    ) if "_IP" not in client["plan_name"] else command(
        f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 static ip-address {client['assigned_public_ip']} mask 255.255.255.128 gateway 181.232.181.129 pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan 102"
    )

    command(f"ont internet-config {client['port']} {client['onu_id']} ip-index 2")

    command(f"ont policy-route-config {client['port']} {client['onu_id']} profile-id 2")

    command("quit")

    command(
        f"""service-port {client['wan'][0]['spid']} vlan {client['wan'][0]['vlan']} gpon {client['frame']}/{client['slot']}/{client['port']} ont {client['onu_id']} gemport {client["wan"][0]['gem_port']} multi-service user-vlan {client['wan'][0]['vlan']} tag-transform transparent inbound traffic-table index {client["wan"][0]["dba_profile"]} outbound traffic-table index {client["wan"][0]["dba_profile"]}"""
    )

    sleep(7)
    command(f"interface gpon {client['frame']}/{client['slot']}")
    command(
        f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0"
    )
    command("quit")
