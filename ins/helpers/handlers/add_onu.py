from time import sleep
from ins.helpers.utils.decoder import decoder, check
from ins.helpers.handlers.spid import calculate_spid
from ins.helpers.handlers.fail import fail_checker


def add_client(comm, command, data):
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(
        f'ont add {data["port"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]} {data["name_2"]} {data["contract"]}" '
    )
    sleep(5)
    value = decoder(comm)
    fail = fail_checker(value)
    if fail is not None:
        return (None, fail)
    (_, end) = check(value, "ONTID :").span()
    ID = value[end : end + 3].replace(" ", "").replace("\n", "").replace("\r", "")
    command(
        f'ont optical-alarm-profile {data["port"]} {ID} profile-name ALARMAS_OPTICAS'
    )
    command(f'ont alarm-policy {data["port"]} {ID} policy-name FAULT_ALARMS')
    command("quit")
    return (int(ID), fail)


def add_service(command, data):
    data["wan"][0]["spid"] = (
        calculate_spid(data)["I"]
        if "_IP" not in data["plan_name"]
        else calculate_spid(data)["P"]
    )

    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(2)
    command(
        f"ont port native-vlan {data['port']} {data['onu_id']} eth 1 vlan {data['wan'][0]['vlan']}"
    ) if data["device_type"] == "B" else None
    sleep(2)

    IPADD = data["assigned_public_ip"] if "_IP" in data["plan_name"] else None

    command(
        f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['wan'][0]['vlan']}"
    ) if "_IP" not in data["plan_name"] else command(
        f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 static ip-address {IPADD} mask 255.255.255.128 gateway 181.232.181.129 pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan 102"
    )

    sleep(2)
    command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 2")

    sleep(2)
    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 2")

    command("quit")
    sleep(2)
    command(
        f"""service-port {data['wan'][0]['spid']} vlan {data['wan'][0]['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data["wan"][0]['gem_port']} multi-service user-vlan {data['wan'][0]['vlan']} tag-transform transparent inbound traffic-table index {data["wan"][0]["plan_idx"]} outbound traffic-table index {data["wan"][0]["plan_idx"]}"""
    )
    sleep(2)

    sleep(2)
    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(2)
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0")
    sleep(2)
    command("quit")
