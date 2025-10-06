from dataclasses import dataclass, field


@dataclass
class EnodeB:
    """
    Class representing an eNodeB (Evolved Node B) in a mobile network.
    """

    name: str = field(default="", metadata={"description": "Cell ID"})
    id: int = field(default=0, metadata={"description": "Enodeb ID in decimal format"})
    link_status: str = field(
        default="", metadata={"description": "Link status, normal status is connected"}
    )
    ip_address1: str = field(
        default="", metadata={"description": "eNodeB ID in decimal format"}
    )
    ip_address2: str = field(
        default="", metadata={"description": "eNodeB ID in hexadecimal format"}
    )
    port: int = field(default=0, metadata={"description": "eNodeB port"})
