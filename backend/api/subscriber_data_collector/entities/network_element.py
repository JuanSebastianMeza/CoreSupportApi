from dataclasses import dataclass, field


@dataclass
class NetworkElement():
    username: str = field(default='E09600')
    password: str = field(default='Abril.1987')
    hostname: str = field(default='10.178.10.101')
    vnfc_name: str = field(default='omo')
    name: str = field(default='')
    port: int = field(default=22)
    endline_char: str = field(default='\r')

    NE_NAMES = {"vSGSNCAN01", "vCGCAN01", "vGGSNCAN_CGW_01", " vGGSCAN_DGW_01"}
    VNFC_NAMES = {"csdb", "cslb", "fac", "gb", "gsc", "link", "omo", "usn", "VNFP", "vnrs"}