from enum import Enum

class Networks(Enum):
    LTE = "4G"
    UMTS = "3G"
    GSM = "2G"
    UNREGISTER = "Not registered in any sgsn"