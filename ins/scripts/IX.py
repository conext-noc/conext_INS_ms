from ins.helpers.devices import devices
from ins.helpers.decoder import decoder
from ins.helpers.add_onu import add_device, add_service
from ins.helpers.data_lookup import data_lookup
from ins.scripts.ssh import ssh
from ins.helpers.mapper import PLANS


def confirm(client):
  oltOptions = ["1", "2", "3"]
  if client['olt'] in oltOptions:
    ip = devices[f"OLT{client['olt']}"]
    (comm, command, quit) = ssh(ip)
    _ = decoder(comm)
    
    # new lookup
    (client["sn"], client["frame"], client["slot"], client["port"]) = data_lookup(comm, command, client)
    print(client)
    '''
                "line_profile": 27,
            "srv_profile": 212,
            "vlan": 3102,
            "name": "OZ_MAX_1",
            "provider": "INTER",
            "dba_profile": 212,
            "gem_port": 22
    '''
    client["wan"] = [{}]
    client["wan"][0]["vlan"] = PLANS[client["plan_name"]]["vlan"]
    client["wan"][0]["gem_port"] = PLANS[client["plan_name"]]["gem_port"]
    client["wan"][0]["line_profile"] = PLANS[client["plan_name"]]["line_profile"]
    client["wan"][0]["dba_profile"] = PLANS[client["plan_name"]]["dba_profile"]
    client["wan"][0]["srv_profile"] = PLANS[client["plan_name"]]["srv_profile"]
    (client["onu_id"], client["fail"]) = add_device(comm,command, client)
    # add onu handler
    # if fail != None:
    #   data['error'] = fail
    #   quit()
    #   return {
    #   "error": True,
    #   "message":fail
    #   }
    
    
    # check optical values handler
    # (client["temp"], client["pwr"]) = opticalValues(comm,command,client)
    # (client["ip_address"], client["wan"]) = wan(comm,command,client)
    # client["type"] = typeCheck(comm,command,client)
    # if optical ok proceed otherwise return like manual installation
    # if fail != None:
    #   data['error'] = fail
    #   quit()
    #   return {
    #   "error": True,
    #   "message":fail
    #   }
    # add service if optical are ok
    
    # add to db ms
    quit()
    return client

  else:
      return {
          "error": True,
          "message":"OLT does not exist"
      }