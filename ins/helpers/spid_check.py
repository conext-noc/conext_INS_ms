from time import sleep
from sch.helpers.decoder import decoder, check, checkIter
from sch.helpers.fail_handler import failChecker
from sch.helpers.file_handler import data_to_dict

conditionSpidOnt = "CTRL_C to break"
condition = "-----------------------------------------------------------------------------"
spidHeader = "SPID,ID,ATT,PORT_TYPE,F/S,/P,VPI,VCI,FLOW_TYPE,FLOW_PARA,RX,TX,STATE,"
conditionSPID = """Next valid free service virtual port ID: """
spidCheck = {
    "index": "Index               : ",
    "id": "VLAN ID             : ",
    "attr": "VLAN attr           : ",
    "endAttr": "Port type",
    "plan": "Outbound table name : ",
    "adminStatus": "Admin status        : ",
    "status": "State               : ",
    "endStatus": "Label               :",
}


def ontSpid(comm, command, client):
    command(
        f"display service-port port {client['frame']}/{client['slot']}/{client['port']} ont {client['onu_id']}  |  no-more")
    sleep(2)
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        limits = checkIter(value, condition)
        (_, s) = limits[1]
        (e, _) = limits[2]
        data = data_to_dict(spidHeader, value[s: e - 2])
        return (data, None)
    else:
        return (None, fail)