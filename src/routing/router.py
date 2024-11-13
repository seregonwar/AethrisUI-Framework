from typing import Dict, Callable, Optional
from dataclasses import dataclass
from ..core import VirtualNode

@dataclass
class Route:
    path: str
    component: Callable[[], VirtualNode]
    
class Router:
    def __init__(self):
        self._routes: Dict[str, Route] = {}
        self._current_path: str = "/"
        
    def add_route(self, route: Route):
        self._routes[route.path] = route
        
    def navigate(self, path: str):
        if path in self._routes:
            self._current_path = path
            return self._routes[path].component() 