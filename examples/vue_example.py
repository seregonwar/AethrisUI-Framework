from src import Window, Container
from src.web.vue_bridge import VueBridge

vue = VueBridge()

vue_code = """
const App = {
    data() {
        return {
            count: 0
        }
    },
    methods: {
        increment() {
            this.count++;
            this.$python.callback('onCountChange', this.count);
        }
    },
    template: `
        <div style="padding: 20px">
            <h1>Vue Counter: {{ count }}</h1>
            <button 
                @click="increment"
                style="padding: 10px 20px; font-size: 16px; border-radius: 8px; 
                       border: none; background: #42b883; color: white; cursor: pointer"
            >
                Increment
            </button>
        </div>
    `
}
"""

def on_count_change(new_count):
    print(f"Count changed to: {new_count}")

vue.register_callback('onCountChange', on_count_change)
vue_component = vue.create_component(vue_code)

window = Window("Vue Example", (400, 300))
window.render(Container({
    "children": [vue_component],
    "style": {"width": "100%", "height": "100%"}
}))
window.run() 