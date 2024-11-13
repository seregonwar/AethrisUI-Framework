from typing import Any, Dict, Type, Union
from dataclasses import dataclass

@dataclass
class PropType:
    type: Type
    required: bool = False
    default: Any = None

def validate_props(props: Dict[str, Any], prop_types: Dict[str, PropType]) -> bool:
    for name, prop_type in prop_types.items():
        if name not in props:
            if prop_type.required:
                raise ValueError(f"Missing required prop: {name}")
            props[name] = prop_type.default
        elif not isinstance(props[name], prop_type.type):
            raise TypeError(f"Invalid type for prop {name}")
    return True 