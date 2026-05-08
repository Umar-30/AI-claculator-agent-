import math
import numpy as np

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    return a ** b

def square_root(a):
    return math.sqrt(a)

def plot_function(expression, x_min=-10, x_max=10, points=100):
    """
    Generates x and y values for plotting a mathematical function.
    The expression should be in Python syntax (e.g., 'x**2 + 2*x + 1').
    """
    try:
        x = np.linspace(x_min, x_max, points)
        # Use a safe dict for eval
        safe_dict = {"x": x, "np": np, "math": math}
        # Replace common math symbols if needed, though user/agent should provide python syntax
        y = eval(expression, {"__builtins__": None}, safe_dict)
        
        # Convert numpy arrays to lists for JSON serialization
        return {
            "x": x.tolist(),
            "y": y.tolist() if isinstance(y, np.ndarray) else [float(y)] * points
        }
    except Exception as e:
        return {"error": str(e)}