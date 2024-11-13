from src.web.react_bridge import ReactBridge
import json

# Crea un bridge React
react = ReactBridge()

# Funzioni Python esposte a React
def calculate(operation: str, a: float, b: float) -> float:
    try:
        a = float(a)
        b = float(b)
        if operation == '+':
            return a + b
        elif operation == '-':
            return a - b
        elif operation == '×':
            return a * b
        elif operation == '÷':
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        raise ValueError(f"Unknown operation: {operation}")
    except Exception as e:
        print(f"Error in calculate: {str(e)}")
        raise

def format_number(number: float) -> str:
    try:
        number = float(number)
        if number.is_integer():
            return str(int(number))
        return f"{number:.8f}".rstrip('0').rstrip('.')
    except Exception as e:
        print(f"Error in format_number: {str(e)}")
        raise

# Esponi le funzioni a JavaScript
react.expose_to_js('calculate', calculate)
react.expose_to_js('format_number', format_number)

# Definisci il componente React della calcolatrice
calculator_code = """
// Definizione degli stili
const styles = {
    calculator: {
        width: '330px',
        background: '#FFFFFF',
        border: '2px solid #E9ECEF',
        borderRadius: '24px',
        boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
        padding: '15px'
    },
    display: {
        width: '100%',
        height: '90px',
        background: '#F8F9FA',
        border: '2px solid #E9ECEF',
        borderRadius: '16px',
        margin: '15px 0',
        padding: '20px',
        display: 'flex',
        justifyContent: 'flex-end',
        alignItems: 'center',
        fontSize: '40px',
        fontFamily: 'Consolas',
        color: '#212529'
    },
    buttonBase: {
        width: '65px',
        height: '65px',
        margin: '4px',
        borderRadius: '12px',
        fontSize: '22px',
        border: 'none',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        outline: 'none'
    },
    numberButton: {
        background: '#F8F9FA',
        color: '#212529'
    },
    operatorButton: {
        background: '#0D6EFD',
        color: '#FFFFFF'
    },
    clearButton: {
        width: '100%',
        background: '#DC3545',
        color: '#FFFFFF',
        marginBottom: '10px'
    },
    equalsButton: {
        background: '#28A745',
        color: '#FFFFFF'
    },
    buttonGrid: {
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '8px'
    }
};

// Componente Calcolatrice
function Calculator() {
    const [display, setDisplay] = React.useState('0');
    const [firstNumber, setFirstNumber] = React.useState(null);
    const [operation, setOperation] = React.useState(null);
    const [newNumber, setNewNumber] = React.useState(true);
    
    const pythonApi = usePythonApi();

    const handleNumber = (num) => {
        const newDisplay = newNumber ? num : (display === '0' ? num : display + num);
        setDisplay(newDisplay);
        setNewNumber(false);
        pythonApi.emit('displayChange', newDisplay);
    };

    const handleOperation = (op) => {
        try {
            setFirstNumber(parseFloat(display));
            setOperation(op);
            setNewNumber(true);
            pythonApi.emit('operationSelected', op);
        } catch (error) {
            setDisplay('Error');
            pythonApi.emit('calculationError', error.message);
        }
    };

    const handleEquals = async () => {
        if (!operation || firstNumber === null) return;

        try {
            const secondNumber = parseFloat(display);
            const result = await pythonApi.invoke('calculate', operation, firstNumber, secondNumber);
            const formattedResult = await pythonApi.invoke('format_number', result);
            
            setDisplay(formattedResult);
            setOperation(null);
            setFirstNumber(null);
            setNewNumber(true);
            
            pythonApi.emit('calculationComplete', {
                firstNumber,
                operation,
                secondNumber,
                result: formattedResult
            });
        } catch (error) {
            setDisplay('Error');
            pythonApi.emit('calculationError', error.message);
        }
    };

    const handleClear = () => {
        setDisplay('0');
        setFirstNumber(null);
        setOperation(null);
        setNewNumber(true);
        pythonApi.emit('clear');
    };

    const handleDecimal = () => {
        if (!display.includes('.')) {
            const newDisplay = display + '.';
            setDisplay(newDisplay);
            setNewNumber(false);
            pythonApi.emit('displayChange', newDisplay);
        }
    };

    return React.createElement('div', { style: styles.calculator }, [
        React.createElement('div', { key: 'display', style: styles.display }, display),
        React.createElement('button', {
            key: 'clear',
            onClick: handleClear,
            style: { ...styles.buttonBase, ...styles.clearButton }
        }, 'C'),
        React.createElement('div', { key: 'keypad', style: styles.buttonGrid },
            [7, 8, 9, '÷', 4, 5, 6, '×', 1, 2, 3, '-', 0, '.', '=', '+'].map(item =>
                React.createElement('button', {
                    key: item,
                    onClick: () => {
                        if (typeof item === 'number' || item === '.') {
                            item === '.' ? handleDecimal() : handleNumber(item.toString());
                        } else if (item === '=') {
                            handleEquals();
                        } else {
                            handleOperation(item);
                        }
                    },
                    style: {
                        ...styles.buttonBase,
                        ...(typeof item === 'number' || item === '.'
                            ? styles.numberButton
                            : item === '='
                                ? styles.equalsButton
                                : styles.operatorButton)
                    }
                }, item)
            )
        )
    ]);
}

const App = () => React.createElement(Calculator);
"""

# Callbacks Python per gli eventi React
def on_display_change(display):
    print(f"Display changed to: {display}")

def on_operation_selected(operation):
    print(f"Operation selected: {operation}")

def on_calculation_complete(data):
    print(f"Calculation complete: {data['firstNumber']} {data['operation']} {data['secondNumber']} = {data['result']}")

def on_calculation_error(error):
    print(f"Calculation error: {error}")

def on_clear():
    print("Calculator cleared")

# Registra le callbacks
react.subscribe('displayChange', on_display_change)
react.subscribe('operationSelected', on_operation_selected)
react.subscribe('calculationComplete', on_calculation_complete)
react.subscribe('calculationError', on_calculation_error)
react.subscribe('clear', on_clear)

# Crea e mostra la finestra con il componente React
react.create_component(calculator_code)

# Avvia l'applicazione
react.run()