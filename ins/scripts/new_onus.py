from datetime import datetime
from time import sleep
from ins.helpers.utils.decoder import check, check_iter, decoder
from ins.helpers.utils.ssh import ssh
from ins.helpers.constants.definitions import olt_devices

condition = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondFSPEnd = "ONT NNI type"
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "


def new_onus(olt):
    (comm, command, quit_ssh) = ssh(olt_devices[olt])
    client = []
    command("display ont autofind all | no-more")
    sleep(5)
    value = decoder(comm)
    regex = check_iter(value, newCond)
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, sFSP) = check(result, newCondFSP).span()
        (eFSP, _) = check(result, newCondFSPEnd).span()
        (_, eSN) = check(result, newCondSn).span()
        (_, eT) = check(result, newCondTime).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[sFSP : eFSP - 1].replace("\n", "").replace(" ", "")
        aT = result[eT : eT + 19].replace("\n", "")
        t1 = datetime.strptime(aT, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.fromisoformat(str(datetime.now()))
        clientTime = t2 - t1
        client.append(
            {
                "fsp": aFSP.replace("\r", ""),
                "sn": aSN,
                "idx": ont + 1,
                "time": clientTime.days,
            }
        )
    quit_ssh()
    return {"data": client, "error": False, "message": "success"}
