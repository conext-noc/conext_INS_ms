from time import sleep
import paramiko
from ins.helpers.handlers.request import db_request
from ins.helpers.constants.definitions import endpoints


def ssh(ip):
    count = 1
    delay = 0.2
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm = None
    cont = True
    creds = db_request(endpoints["get_creds"], {})

    # Handling multiple SSH sessions
    while cont and count <= 3:
        try:
            username = creds["data"][count]["user_name"]
            password = creds["data"][count]["password"]
            port = 22
            conn.connect(ip, port, username, password)
            comm = conn.invoke_shell()
            cont = False
        except paramiko.ssh_exception.AuthenticationException:
            cont = True
            count += 1
            continue
        break

    def enter():
        comm.send(" \n")
        comm.send(" \n")
        sleep(delay)

    def command(cmd):
        print(cmd)
        comm.send(cmd)
        sleep(delay)
        enter()

    def quit_ssh():
        conn.close()

    command("enable")
    command("config")
    return (comm, command, quit_ssh)
