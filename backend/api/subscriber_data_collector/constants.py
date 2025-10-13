class HuaweiCommands:
    """Class for constants related to Huawei commands."""

    CURRENT_ALARMS = "LST ALMAF:;"
    ALARMS_HISTORY = "LST ALMLOG:;"
    EXTERNALS_ALARMS_HISTORY = "LST ALMLOG:ALMTP=ALL,STARTAID=65041,ENDAID=65055;"
    DSP_MMCTX_IMSI = 'DSP MMCTX:QUERYOPT=BYIMSI,IMSI="{}";'
    DSP_MMCTX_MSISDN = 'DSP MMCTX: QUERYOPT=BYMSISDN,MSISDN="{}";'
    DSP_S1APLNK = "DSP S1APLNK: OUTPUTTYPE=SCREEN,ENODEBID={};"
    DSP_UPPDPCHGINFO = "DSP UPPDPCHGINFO: SUBSCRIBERID=MSISDN,MSISDN={};"


class NokiaCommands:
    """Class for constants related to Nokia commands."""

    ZMVO = "ZMVO:MSISDN={}:;"
    ZEPO_3G = "ZEPO:TYPE=SA,NO={}:;"
    ZEPO_2G = "ZEPO:NO={},;"


class RemoteDataSourceConstants:
    """Class for constants related connections network elements."""

    SOCKET_ERROR = "Failed to stablish connection, please check if there issues with internet service. Error: /n"
    LOGIN_COMMAND = ""


class RegexPatterns:
    """Class for constants related to regex patterns."""

    # Connection
    CHECK_CONNECTION = r"RETCODE\s+=\s(0\s+Success)"
    CHECK_VNFC_CONNECTION = r"REG VNFC:NAME.*\nRETCODE\s=\s0\s+(Success)"
    KEY_END_DATA = r"---.*(END)"
    # subscriber
    IMSI = r"IMSI\s+=\s+(\d+)"
    VLR = r"VLR\sNO.\s+=\s+(\d+)"
    ACTIVITY_TIME_PACO = r"Lastest\sUE\sactivity\stime.*\s=\s\s(.*\d+)"
    ACTIVITY_DATE_CICO = r"LAST\sACTIVATE\sDATE\s.*\s(\d+-\d+\s\d+:\d+)"
    ROUTING_CATEGORY = r"ROUTING CATEGORY\s+\.+\s+(\d+)"
    SERVICES = r"BASIC\sSERVICES:\s+(\w+.*\w+)"
    # Commands validation
    CHECK_S1APLNK = r"(Number of results = 1).*\n.*---\s+END"
    CHECK_ZEPO = r"/.*(DX\sERROR):\s235.*"
    CHECK_ZMVO = r"COMMAND\sEXECUTION\sFAILED"
    CHECK_MMCTX_FAILED = r"Problems\sgathering\smmctx\sdata"
    # 3g data
    SERVICE_AREA_ID = r"Service\sarea\sof\suser\s\s=\s\s.*(\w\w\w\w)"
    SA_NAME = r"SA\s+NAME\s:(\w+)"
    LAC_ID = r"LAC\s+:(\d+)"
    ADMINISTRATIVE_STATE = r"ADMINISTRATIVE STATE\s+.*:(\w+)"
    ZEPO_ERROR = r"/.*(DX\sERROR):\s235.*"
    # 4g data
    ENODEB_ID = r"Global eNodeB ID\s+=\s+\w+(\w\w\w\w)"
    ENODEB_PRIMARY_IP = r"eNodeB\sIP\saddress1\s+=\s+(\w+.\w+.\w+.\w+|\w+)"
    ENODEB_SECONDARY_IP = r"eNodeB\sIP\saddress2\s+=\s+(\w+.\w+.\w+.\w+|\w+)"
    ENODEB_LINK_STATUS = r"Link\sstatus\s+=\s+(\w+)"
    ENODEB_NAME = r"eNodeB\sName\s+=\s+(\w+.*\w+)"
    ENODEB_PORT = r"eNodeB\sport\s+=\s+(.*\w+)"
    # 2g data
    CELL_ID = r"Cell\sId\s+=\s+0x(\w\w\w\w)"
    BTS_NAME_ID = r"BTS\s+NAME\s:(\w+)\s+NUMBER\s+:(\d+)"
    BSC_NAME_ID = r"BSC\s+NAME\s:(\w+)\s+NUMBER\s+:(\d+)"
    BTS_STATE = r"BTS\sADMINISTRATIVE\sSTATE.*:(\w+)"


class Vnfcs:
    """Class for constants related to vnfcs of network elements."""

    CGW = "cgw"
    OMO = "omo"


class OutputMessages:
    MMCTX_NOT_FOUND = "Subscriber is not registered in any SGSN"
    MMCTX_ERROR = "Problems gathering mmctx data"
    S1APLNK_ERROR = "Problems gathering S1APLNK data. Error:"
    TIMER_ERROR_MSS = "Timer expired error while getting data from nokia central:"
    ZEPO_ERROR_MSS = "Problems gathering ZEPO data. Error:"
    ZMVO_ERROR_MSS = "Problems gathering ZMVO data. Error:"
    MSISDN_FORMAT_ERROR = """Check if the MSISDN is in the correct format.
    The MSISDN should be max 15 digits long and contain only digits.
    The first 3 digits are the country code (CC), the next 3 digits are the
    subscriber number (SN), and the last 6 digits are the national destination code (NDC).

    CC + NDC + SN

    Country code (CC)
    National Destination Code (NDC)
    Subscriber number (SN)

    Examples:

    CC: 34 (Spain)
    NDC: 123 (Madrid)
    SN: 4567890 (subscriber number)

    CC: 58 (Venezuela)
    NDC: 414 (Caracas)
    SN: 1234567 (subscriber number)
    MSISDN: 584141963786"""
    


