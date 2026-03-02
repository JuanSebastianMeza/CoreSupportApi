from dataclasses import dataclass
from dataclasses import field


@dataclass
class Oss:
    name: str = field(default='ImasterMae')
    hostname: str = field(default='10.178.10.101')
    port: int = field(default=31114)
    endline_char: str = field(default='\r')
    user_name: str = field(default='E09600')
    password: str = field(default='February.1987')