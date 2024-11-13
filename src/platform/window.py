from typing import Tuple, Optional, Callable
from .native_window import NativeWindow
from ..core import VirtualNode

class Window:
    _instance = None
    
    def __init__(self, title: str = "Modern GUI Window", size: Tuple[int, int] = (800, 600)):
        self._native_window = NativeWindow(title, size)
        self._current_component = None
        self._size = size
        Window._instance = self
    
    @classmethod
    def get_instance(cls) -> Optional['Window']:
        return cls._instance
    
    def render(self, root_component: VirtualNode | Callable[[], VirtualNode]):
        if callable(root_component):
            self._current_component = root_component
            root_component = root_component()
        else:
            self._current_component = lambda: root_component
            
        self._native_window.render(root_component)
    
    def run(self):
        self._native_window.run()
    
    def reload(self):
        """Reloads the application by re-rendering the current component"""
        if self._current_component:
            self.render(self._current_component)
    
    def resize(self, width: int, height: int):
        """Resizes the window"""
        self._size = (width, height)
        self._native_window.resize(width, height)
        if self._current_component:
            self.reload()
            
    def get_current_size(self) -> Tuple[int, int]:
        """Gets the current window size"""
        return self._size