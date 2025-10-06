from dataclasses import dataclass, field
from .enodeB import EnodeB
from .nodeB import NodeB
from .cell import Cell

@dataclass
class Network:
    technology: str = field(
        default="",
        metadata={"description": "User current network technologie (LTE, UMTS, GSM)"},
    )
    enodeb: EnodeB = field(
        default_factory=EnodeB,
        metadata={"description": "If user is in 4g it shows the nodeb id"},
    )
    nodeb: NodeB = field(
        default_factory=NodeB,
        metadata={"description": "If user is in 3g it shows the nodeb data"},
    )
    cell: Cell = field(
        default_factory=Cell,
        metadata={"description": "If user is in 2g it shows the cell data"},
    )
