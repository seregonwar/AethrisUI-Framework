import webview
from typing import Dict, Any, Optional, Callable
import json
import logging

logger = logging.getLogger(__name__)

class ReactBridge:
    def __init__(self):
        self._window = None
        self._callbacks = {}
        self._python_api = {}
    
    def expose_to_js(self, name: str, func: Callable):
        """Espose una funzione Python a JavaScript"""
        self._python_api[name] = func
    
    def create_component(self, react_code: str, props: Dict[str, Any] = None) -> None:
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>React Calculator</title>
            <script src="https://unpkg.com/react@17/umd/react.production.min.js"></script>
            <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js"></script>
            <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
            <style>
                body {
                    margin: 0;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    background: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }
            </style>
        </head>
        <body>
            <div id="root"></div>
            <script type="text/babel">
                // Bridge API
                const pythonBridge = {
                    async invoke(method, ...args) {
                        try {
                            const result = await window.pywebview.api.invoke(method, ...args);
                            return JSON.parse(result);
                        } catch (error) {
                            console.error('Error invoking Python method:', error);
                            throw error;
                        }
                    },
                    
                    subscribe(event, callback) {
                        window.pywebview.api.subscribe(event, (...args) => {
                            callback(...args.map(arg => JSON.parse(arg)));
                        });
                    },
                    
                    emit(event, ...args) {
                        window.pywebview.api.emit(event, ...args.map(arg => JSON.stringify(arg)));
                    }
                };

                // React Context per l'API Python
                const PythonContext = React.createContext(null);

                // Hook personalizzato per usare l'API Python
                function usePythonApi() {
                    const api = React.useContext(PythonContext);
                    if (!api) {
                        throw new Error('usePythonApi must be used within a PythonContext.Provider');
                    }
                    return api;
                }
        """ + f"\n{react_code}\n" + """
                
                // Wrapper component con il Provider
                function AppWrapper() {
                    return React.createElement(
                        PythonContext.Provider,
                        { value: pythonBridge },
                        React.createElement(App)
                    );
                }

                // Renderizza l'applicazione
                ReactDOM.render(
                    React.createElement(AppWrapper),
                    document.getElementById('root')
                );
            </script>
        </body>
        </html>
        """
        
        # Crea una nuova finestra webview
        self._window = webview.create_window(
            'React Calculator',
            html=html,
            js_api=self,
            width=360,
            height=600,
            resizable=True
        )
    
    def invoke(self, method: str, *args) -> str:
        """Invoca un metodo Python da JavaScript"""
        if method in self._python_api:
            try:
                result = self._python_api[method](*args)
                return json.dumps(result)
            except Exception as e:
                logger.error(f"Error invoking Python method {method}: {str(e)}")
                return json.dumps({"error": str(e)})
        return json.dumps(None)
    
    def subscribe(self, event: str, callback: str):
        """Registra una callback JavaScript per un evento Python"""
        self._callbacks[event] = callback
    
    def emit(self, event: str, *args):
        """Emette un evento da Python a JavaScript"""
        if event in self._callbacks:
            try:
                self._window.evaluate_js(f"{self._callbacks[event]}({','.join(args)})")
            except Exception as e:
                logger.error(f"Error emitting event {event}: {str(e)}")
    
    def run(self):
        """Avvia il loop principale di webview"""
        webview.start(debug=True)