from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CalculatorResponse(BaseModel):
    operation: str
    expression: str
    result: Optional[float] = None
    explanation: Optional[str] = None
    plot_data: Optional[Dict[str, Any]] = None