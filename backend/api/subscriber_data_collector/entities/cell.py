from dataclasses import dataclass, field


@dataclass
class Cell:
    """
    Class representing an NodeB in a mobile network.
    """

    bts_name: str = field(
        default="",
        metadata={"description": "Name of the bts"}
    )
    bts_id: int = field(
        default=0,
        metadata={"description": "Bts id in decimal format"}
    )
    bsc_name: str = field(
        default="",
        metadata={"description": "Bsc name"}
    )
    bsc_id: int = field(
        default=0,
        metadata={"description": "bsc id in decimal format"}
    )
    bts_state: str = field(
        default="",
        metadata={"description": "State could be lock or unlocked"}
    )