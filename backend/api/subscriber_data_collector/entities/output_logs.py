from dataclasses import dataclass, field


@dataclass
class OutputLogs:
    """
    Class representing an NodeB in a mobile network.
    """

    mmctx: str = field(
        default="",
        metadata={"description": "Output log of mmctx command"}
    )
    zepo: str = field(
        default="",
        metadata={"description": "Output log of zepo command"}
    )
    s1aplnk: str = field(
        default="",
        metadata={"description": "Output log of s1aplnk command"}
    )
    zmvo: str = field(
        default="",
        metadata={"description": "Output log of zmvo command"}
    )
