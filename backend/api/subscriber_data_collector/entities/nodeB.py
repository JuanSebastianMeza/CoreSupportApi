from dataclasses import dataclass, field


@dataclass
class NodeB:
    """
    Class representing an NodeB in a mobile network.
    """

    sa_name: str = field(
        default="",
        metadata={"description": "Name of the NodeB"}
    )
    sa_id: int = field(
        default=0,
        metadata={"description": "NodeB ID in decimal format"}
    )
    lac_id: int = field(
        default=0,
        metadata={"description": "LAC in decimal format"}
    )
    administrative_state: str = field(
        default="",
        metadata={"description": "State could be lock or unlocked"}
    )