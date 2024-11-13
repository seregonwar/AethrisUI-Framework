import webview
from typing import Dict, Any, Optional, Callable
from ..core import VirtualNode

class VueBridge:
    def __init__(self):
        self._webview = None
        self._components = {}
        self._callbacks = {}
    
    def create_component(self, vue_code: str, props: Dict[str, Any] = None) -> VirtualNode:
        component_id = f"vue-component-{len(self._components)}"
        
        html = f"""
        <div id="{component_id}"></div>
        <script src="https://unpkg.com/vue@3"></script>
        <script>
            {vue_code}
            
            const app = Vue.createApp({{
                template: `<App />`,
                components: {{ App }}
            }});
            
            app.config.globalProperties.$python = {{
                callback: function(name, ...args) {{
                    window.pywebview.api.handle_callback(name, args);
                }}
            }};
            
            app.mount('#{component_id}');
        </script>
        """
        
        self._components[component_id] = html
        
        return VirtualNode(
            component_type="web-view",
            props={
                "html": html,
                "callbacks": self._callbacks,
                "js_api": self
            },
            children=[]
        )
    
    def register_callback(self, name: str, callback: Callable):
        """Registra una callback Python che può essere chiamata dal Vue"""
        self._callbacks[name] = callback
    
    def handle_callback(self, name: str, args: list):
        """Gestisce le callbacks dal Vue al Python"""
        if name in self._callbacks:
            self._callbacks[name](*args)

class WebViewComponent:
    def __init__(self, props: Dict[str, Any]):
        self.props = props
        self._webview = None
        
    def render(self) -> VirtualNode:
        if not self._webview:
            self._webview = webview.create_window(
                "Web Component",
                html=self.props["html"],
                js_api=self.props["js_api"]
            )
            
        return VirtualNode(
            component_type="container",
            props={"style": {"width": "100%", "height": "100%"}},
            children=[self._webview]
        ) 