from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from .state import State

@dataclass
class VirtualNode:
    component_type: str
    props: Dict[str, Any]
    children: List['VirtualNode']
    state: Optional[State] = None 