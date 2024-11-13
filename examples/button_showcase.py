from src import Window, Container, Button, Theme
from src.platform.color import Color

# Definisci un tema personalizzato
theme = Theme({
    "colors": {
        "primary": Color("#1976D2"),
        "secondary": Color("#424242"),
        "success": Color("#4CAF50"),
        "error": Color("#F44336"),
        "warning": Color("#FFC107")
    }
})

def ButtonShowcase():
    return Container({
        "children": [
            Button({
                "text": "Primary Button",
                "variant": "primary"
            }),
            Button({
                "text": "Secondary Button",
                "variant": "secondary"
            }),
            Button({
                "text": "Success Button",
                "variant": "success"
            })
        ],
        "style": {
            "gap": "16px",
            "padding": "24px"
        }
    })

# Crea e avvia l'applicazione
window = Window("Button Showcase", (400, 300))
Theme.set_current(theme)
window.render(ButtonShowcase())
window.run() 