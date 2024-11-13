from .theme import Theme

# Inizializza il tema di default
Theme(
    name="light",
    colors={
        "primary": "#1976D2",      # Blu
        "secondary": "#FF4081",     # Rosa
        "background": "#F5F5F5",    # Grigio chiaro
        "surface": "#FFFFFF",       # Bianco
        "text": "#212121",          # Quasi nero
        "border": "#E0E0E0",        # Grigio
        "error": "#D32F2F",         # Rosso
        "warning": "#FFA000",       # Arancione
        "success": "#388E3C",       # Verde
        "info": "#0288D1"           # Blu chiaro
    },
    fonts={
        "primary": "Arial",
        "secondary": "Helvetica",
        "monospace": "Consolas"
    }
)

from .core import VirtualNode, State
from .platform import Window
from .styling import Style
from .widgets import (
    Button, 
    Text, 
    Container, 
    Input, 
    Checkbox, 
    RadioButton, 
    Select, 
    Slider, 
    Switch
)

__all__ = [
    'Window',
    'Button',
    'Text',
    'Container',
    'Input',
    'Checkbox',
    'RadioButton',
    'Select',
    'Slider',
    'Switch',
    'Theme',
    'Style',
    'VirtualNode',
    'State'
] 