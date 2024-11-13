import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src import Window, Container, Button, Text, use_state, use_effect, Style, Theme

def Counter(props):
    count, set_count = use_state(0)
    
    use_effect(lambda: print(f"Count changed to: {count.get()}"), [count])
    
    return Container({
        "children": [
            Text(f"Count: {count.get()}"),
            ModernButton(),
            Button({
                "text": "Decrement",
                "onClick": lambda: set_count(count.get() - 1),
                "style": {
                    "background": Theme.current.secondary,
                    "padding": 10,
                    "border_radius": 5
                }
            })
        ],
        "direction": "vertical",
        "spacing": 15
    })

def ModernButton():
    return Button({
        "text": "Click Me",
        "variant": "primary",
        "style": {
            "background": Theme.current.colors["primary"],
            "color": "#FFFFFF",
            "padding": "12px 24px",
            "border_radius": "12px",
            "font_size": "16px",
            "font_weight": "600",
            "letter_spacing": "0.5px",
            "text_transform": "uppercase"
        }
    })

# Create and run the application
window = Window("Modern GUI Example", (400, 300))
window.render(Counter({}))
window.run() 