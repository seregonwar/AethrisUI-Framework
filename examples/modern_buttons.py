import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src import Window, Container, Button, Text, Theme
from src.styling.effects import ModernEffects

def App():
    return Container({
        "children": [
            Button({
                "text": "Gradient Button",
                "variant": "gradient",
                "onClick": lambda: print("Gradient clicked!")
            }),
            Button({
                "text": "Glass Button",
                "variant": "glass",
                "effect": "glow",
                "onClick": lambda: print("Glass clicked!")
            }),
            Button({
                "text": "Pulsing Button",
                "variant": "filled",
                "effect": "pulse",
                "onClick": lambda: print("Pulse clicked!")
            }),
            Button({
                "text": "Noise Button",
                "variant": "filled",
                "effect": "noise",
                "onClick": lambda: print("Noise clicked!")
            })
        ],
        "direction": "vertical",
        "spacing": 20,
        "style": ModernEffects.glass(0.05, 15)
    })

window = Window("Modern Buttons", (400, 500))
window.render(App())
window.run() 