from sch.helpers.decoder import decoder, check
from sch.helpers.fail_handler import failChecker

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "


def opticalValues(comm, command, data ):
    TEMP = None
    PWR = None
    command(f'  interface  gpon  {data["frame"]}/{data["slot"]}  ')
    command(f'  display  ont  optical-info  {data["port"]}  {data["onu_id"]}  |  no-more')
    command('quit')
    value = decoder(comm)
    fail = failChecker(value)
    rePwr = check(value, conditionPwr)
    reTemp = check(value, conditionTemp)
    if fail == None and rePwr != None:
        (_, eT) = reTemp.span()
        (_, eP) = rePwr.span()
        PWR = value[eP: eP + 6]
        TEMP = value[eT: eT + 4].replace("\n", "").replace(" ", "").replace("\r", "")
    return (TEMP, PWR)
