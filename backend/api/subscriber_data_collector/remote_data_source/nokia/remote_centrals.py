from ...entities.network_element import NetworkElement

MSSCAN02_IP = "10.187.249.100"
MSSVAL02_IP = "10.187.245.228"
MSSMBO02_IP = "10.187.247.212"
MSSMPLC02_IP = "10.187.203.212"

Centrales_Nokia_List = [
    NetworkElement(
        name="MSSCAN02",
        hostname=MSSCAN02_IP,
        username="PRTGCV",
        password="NOKIA1234",
    ),
    NetworkElement(
        name="MSSVAL02",
        hostname=MSSVAL02_IP,
        username="PRTGCV",
        password="HGFDSO856ZI",
    ),
    NetworkElement(
        name="MSSMBO02", hostname=MSSMBO02_IP, username="PRTGCV", password="HGFDSO856ZI"
    ),
    NetworkElement(
        name="MSSPLC02",
        hostname=MSSMPLC02_IP,
        username="PRTGCV",
        password="HGFDSO856ZI",
    ),
]


def get_NetworkElement(name: str) -> NetworkElement:
    return [
        NetworkElement
        for NetworkElement in Centrales_Nokia_List
        if NetworkElement.name == name
    ][0]
