from time import sleep
from ins.helpers.utils.decoder import check, decoder
from ins.helpers.handlers.fail import fail_checker
from ins.helpers.constants.definitions import ont_type_start, ont_type_end, ont_type_vendor


def type_finder(comm, command, data):
    ONT_TYPE = None
    FAIL = None
    value = decoder(comm)
    command(f"  interface  gpon  {data['frame']}/{data['slot']}  ")
    command(f"  display  ont  version  {data['port']}  {data['onu_id']}  ")
    sleep(5)
    command("quit")
    value = decoder(comm)
    FAIL = fail_checker(value)
    if FAIL is None:
        (_, tS) = check(value, ont_type_start).span()
        (tE, _) = check(value, ont_type_end).span()
        (_, sV) = check(value, ont_type_vendor).span()
        ONT_TYPE = value[tS:tE-1].replace("\n", "")
        ONT_VENDOR = value[sV:sV + 4]
    return (ONT_TYPE, ONT_VENDOR)
