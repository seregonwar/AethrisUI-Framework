from src import Window, Container, Button, Text, Theme

def App():
    return Container({
        "children": [
            Text("Basic Example"),
            Button({
                "text": "Click Me!",
                "onClick": lambda: print("Button clicked!"),
                "style": {
                    "background": Theme.current.primary,
                    "padding": 10,
                    "border_radius": 5
                }
            })
        ],
        "direction": "vertical",
        "spacing": 15
    })

# Create and run the application
window = Window("Basic GUI Example", (400, 300))
window.render(App())
window.run() 