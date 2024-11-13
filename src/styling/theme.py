from typing import Dict, Any, Optional
from ..core.context import create_context, ContextProvider
from dataclasses import dataclass
from ..platform.color import Color

@dataclass
class ThemeColors:
    primary: Color = Color("#007AFF")
    secondary: Color = Color("#6C757D")
    success: Color = Color("#28A745")
    error: Color = Color("#DC3545")
    warning: Color = Color("#FFC107")
    info: Color = Color("#17A2B8")
    background: Color = Color("#FFFFFF")
    surface: Color = Color("#F8F9FA")
    text: Color = Color("#212529")
    
    def get(self, key: str, default: Color) -> Color:
        return getattr(self, key, default)

@dataclass
class ThemeSpacing:
    xs: int = 4
    sm: int = 8
    md: int = 16
    lg: int = 24
    xl: int = 32

@dataclass
class ThemeShadows:
    sm: str = "0 2px 4px rgba(0,0,0,0.1)"
    md: str = "0 4px 8px rgba(0,0,0,0.1)"
    lg: str = "0 8px 16px rgba(0,0,0,0.1)"

class Theme:
    _current = None
    
    def __init__(self, colors: Dict[str, str] = None):
        self.colors = ThemeColors()
        if colors:
            for key, value in colors.items():
                if hasattr(self.colors, key):
                    setattr(self.colors, key, Color(value))
    
    @classmethod
    def get_current(cls) -> 'Theme':
        if cls._current is None:
            cls._current = Theme()  # Tema di default
        return cls._current
    
    @classmethod
    def set_current(cls, theme: 'Theme'):
        cls._current = theme
    
    @property
    def current(self) -> 'Theme':
        return self.get_current()

class ThemeProvider:
    _current_theme: Optional[Theme] = None
    theme_context = create_context('theme')
    
    @classmethod
    def set_theme(cls, theme: Theme):
        cls._current_theme = theme
        ContextProvider.provide(cls.theme_context, theme)
    
    @classmethod
    def get_current_theme(cls) -> Theme:
        return cls._current_theme

def use_theme() -> Theme:
    from ..hooks import use_context
    return use_context(ThemeProvider.theme_context) 