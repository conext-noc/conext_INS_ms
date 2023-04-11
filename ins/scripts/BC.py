
from unittest import result
from sch.helpers.devices import devices
from sch.helpers.data_lookup import data_lookup
from sch.scripts.ssh import ssh
from sch.helpers.decoder import decoder
from sch.helpers.optical_finder import opticalValues
from sch.helpers.ont_type_finder import typeCheck
from sch.helpers.wan_finder import wan

def clientFinder(data):
    oltOptions = ["1", "2", "3"]
    if data['olt'] in oltOptions:
        ip = devices[f"OLT{data['olt']}"]
        (comm, command, quit) = ssh(ip)
        decoder(comm)
        client,fail = data_lookup(comm,command,data['contract']).values()
        
        if fail != None:
            data['error'] = fail
            quit()
            return {
            "error": True,
            "message":fail
            }
            
        client["olt"] = data["olt"]
        (client["temp"], client["pwr"]) = opticalValues(comm,command,client)
        client["type"] = typeCheck(comm,command,client)
        (client["ip_address"], client["wan"]) = wan(comm,command,client)
        quit()
        return client
    
    
    else:
        return {
            "error": True,
            "message":"OLT does not exist"
        }
