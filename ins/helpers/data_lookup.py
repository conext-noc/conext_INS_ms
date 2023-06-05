from time import sleep
from datetime import datetime
from ins.helpers.decoder import check, checkIter, decoder

condition = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondFSPEnd = "ONT NNI type"
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "


def data_lookup(comm, command, data):
    SN_NEW = data["sn"]
    SN = None
    FRAME = None
    SLOT = None
    PORT = None
    client = []
    command("display ont autofind all | no-more")
    sleep(1)
    value = decoder(comm)
    regex = checkIter(value, newCond)
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, sFSP) = check(result, newCondFSP).span()
        (eFSP, _) = check(result, newCondFSPEnd).span()
        (_, eSN) = check(result, newCondSn).span()
        (_, eT) = check(result, newCondTime).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[sFSP:eFSP].replace("\n", "").replace(" ", "")
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

    for ont in client:
        if SN_NEW == ont["sn"] and ont["time"] <= 10:
            SN = ont["sn"]
            FRAME = ont["fsp"].split("/")[0]
            SLOT = ont["fsp"].split("/")[1]
            PORT = ont["fsp"].split("/")[2]
    return (SN, FRAME, SLOT, PORT)
