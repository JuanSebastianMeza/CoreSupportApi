from dataclasses import dataclass, field
from .network import Network
from .output_logs import OutputLogs

@dataclass
class Subscriber:
    imsi: str = field(
        default="",
        metadata={"description": "International Mobile Subscriber Identity"}
    )
    msisdn: str = field(
        default="",
        metadata={"description": "Mobile Station International Subscriber Directory Number"},
    )
    vlr: str = field(
        default="",
        metadata={"description": "number of subscriber registered vlr"}
    )
    sgsn: str = field(
        default="",
        metadata={"description": "Current user's sgsn"}
    )
    mss: str = field(
        default="",
        metadata={"description": "Current user's sgsn"}
    )
    last_activity_cico: str = field(
        default="",
        metadata={"description": "Current user's sgsn"}
    )
    routing_category: str = field(
        default="",
        metadata={"description": "Current user's sgsn"}
    )
    services: str = field(
        default="",
        metadata={"description": "Current user's sgsn"}
    )
    last_activity_paco: str = field(
        default="",
        metadata={"description": "User last time activity saw from paco side"}
    )
    network: Network = field(
        default_factory=Network,
        metadata={"description": "Data of user current network technologies (LTE, UMTS, GSM)"},
    )
    output_logs: OutputLogs = field(
        default_factory=OutputLogs,
        metadata={"description": "Output logs of the commands"},
    )
