from ins.helpers.devices import devices
from ins.helpers.decoder import decoder
from ins.helpers.add_onu import add_device, add_service
from ins.helpers.data_lookup import data_lookup
from ins.helpers.optical_finder import opticalValues
from ins.helpers.ont_type_finder import typeCheck
from ins.scripts.ssh import ssh
from ins.helpers.add_db_client import add_to_db
from ins.helpers.mapper import PLANS


def confirm(client):
  oltOptions = ["1", "2", "3"]
  if client['olt'] in oltOptions:
    ip = devices[f"OLT{client['olt']}"]
    (comm, command, quit) = ssh(ip)
    _ = decoder(comm)
    
    (client["sn"], client["frame"], client["slot"], client["port"]) = data_lookup(comm, command, client)
    client["wan"] = [{}]
    client["wan"][0]["vlan"] = PLANS[client["plan_name"]]["vlan"]
    client["wan"][0]["gem_port"] = PLANS[client["plan_name"]]["gem_port"]
    client["wan"][0]["line_profile"] = PLANS[client["plan_name"]]["line_profile"]
    client["wan"][0]["dba_profile"] = PLANS[client["plan_name"]]["dba_profile"]
    client["wan"][0]["srv_profile"] = PLANS[client["plan_name"]]["srv_profile"]
    (client["onu_id"], client["fail"]) = add_device(comm,command, client)
    
    if client["fail"] != None:
      quit()
      return {
      "error": True,
      "message":client["fail"],
      "data": client
      }
    (client["temperature"], client["power"]) = opticalValues(comm,command,client)
    client["type"] = typeCheck(comm,command,client)
    if int(client["power"]) <= -27:
      quit()
      return {
      "error": True,
      "message":f"Optical Power exceeds threshold of -27dBm, power @ {client['power']}",
      "data":client
      }
    add_service(comm, command, client)
    add_to_db(client)
    quit()
    return {
      "error": False,
      "message":"Success",
      "data":client
      }

  else:
      return {
          "error": True,
          "message":"OLT does not exist",
          "data":client
      }