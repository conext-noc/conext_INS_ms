from time import sleep
from datetime import datetime
from ins.helpers.utils.decoder import check, check_iter, decoder

newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondFSPEnd = "ONT NNI type"
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "


def new_lookup(comm, command, SN_NEW):
    _ = decoder(comm)
    SN_FINAL = None
    FSP_FINAL = None
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
        data = {
            "fsp": aFSP.replace("\r", ""),
            "sn": aSN,
            "idx": ont + 1,
            "time": clientTime.days,
        }
        client.append(data)
    for ont in client:
        if SN_NEW == ont["sn"] and ont["time"] <= 10:
            SN_FINAL = ont["sn"]
            FSP_FINAL = ont["fsp"]
    return (SN_FINAL, FSP_FINAL)
