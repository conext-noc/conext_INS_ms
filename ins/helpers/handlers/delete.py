from time import sleep


def delete_onu(comm, command, client):
    command(f"interface gpon {client['frame']}/{client['slot']}")
    command(f"ont delete {client['port']} {client['onu_id']}")
    sleep(1)
    command("quit")
