import cohere
import json
import tools

from config import COHERE_API_KEY
from memory import save_message, get_memory
from schemas import CalculatorResponse

co = cohere.Client(COHERE_API_KEY)

# Define tools for Cohere
TOOLS = [
    {
        "name": "add",
        "description": "Adds two numbers",
        "parameter_definitions": {
            "a": {"description": "First number", "type": "float", "required": True},
            "b": {"description": "Second number", "type": "float", "required": True}
        }
    },
    {
        "name": "subtract",
        "description": "Subtracts b from a",
        "parameter_definitions": {
            "a": {"description": "Number to subtract from", "type": "float", "required": True},
            "b": {"description": "Number to subtract", "type": "float", "required": True}
        }
    },
    {
        "name": "multiply",
        "description": "Multiplies two numbers",
        "parameter_definitions": {
            "a": {"description": "First number", "type": "float", "required": True},
            "b": {"description": "Second number", "type": "float", "required": True}
        }
    },
    {
        "name": "divide",
        "description": "Divides a by b",
        "parameter_definitions": {
            "a": {"description": "Dividend", "type": "float", "required": True},
            "b": {"description": "Divisor", "type": "float", "required": True}
        }
    },
    {
        "name": "power",
        "description": "Raises a to the power of b",
        "parameter_definitions": {
            "a": {"description": "Base", "type": "float", "required": True},
            "b": {"description": "Exponent", "type": "float", "required": True}
        }
    },
    {
        "name": "square_root",
        "description": "Calculates the square root of a number",
        "parameter_definitions": {
            "a": {"description": "Number to find the square root of", "type": "float", "required": True}
        }
    },
    {
        "name": "plot_function",
        "description": "Generates data points for plotting a mathematical function (e.g., y = x^2).",
        "parameter_definitions": {
            "expression": {"description": "The mathematical expression in Python syntax (e.g., 'x**2', 'np.sin(x)')", "type": "string", "required": True},
            "x_min": {"description": "Minimum x value", "type": "float", "required": False},
            "x_max": {"description": "Maximum x value", "type": "float", "required": False}
        }
    }
]

SYSTEM_PROMPT = """
You are an AI Calculator Agent Pro.

Your tasks:
1. Solve mathematical expressions accurately using the provided tools.
2. Use conversation memory to understand context.
3. If a calculation is needed, use the appropriate tool.
4. If a user asks to "plot", "graph", or "visualize" a function, use the 'plot_function' tool.
5. After getting the tool result, return a JSON response.

CRITICAL JSON RULE:
Return ONLY these fields:
{
  "operation": "string",
  "expression": "string",
  "result": number or null,
  "explanation": "string"
}
DO NOT include 'plot_data' in your JSON. The system will add it automatically. Keep your response short.
"""

def ask_agent(user_input, model="command-r-plus-08-2024"):
    save_message("USER", user_input)

    chat_history = []
    memory = get_memory()
    for msg in memory[:-1]:
        role = "CHATBOT" if msg["role"] == "ASSISTANT" else msg["role"]
        chat_history.append({"role": role, "message": msg["content"]})

    total_tokens = 0
    last_plot_data = None

    response = co.chat(
        model=model,
        message=user_input,
        tools=TOOLS,
        preamble=SYSTEM_PROMPT,
        chat_history=chat_history,
        temperature=0
    )

    if response.meta and response.meta.tokens:
        total_tokens += response.meta.tokens.input_tokens + response.meta.tokens.output_tokens

    if response.tool_calls:
        extended_history = chat_history + [
            {"role": "USER", "message": user_input},
            {"role": "CHATBOT", "message": response.text, "tool_calls": response.tool_calls}
        ]

        tool_results = []
        for call in response.tool_calls:
            func = getattr(tools, call.name)
            try:
                result = func(**call.parameters)
                if call.name == "plot_function":
                    last_plot_data = result
                    # Tell the model the data is ready so it doesn't try to generate it
                    tool_output = "Plot data generated and stored in system memory. DO NOT include it in your next message."
                else:
                    tool_output = result

                tool_results.append({
                    "call": call,
                    "outputs": [{"result": tool_output}]
                })
            except Exception as e:
                tool_results.append({
                    "call": call,
                    "outputs": [{"error": str(e)}]
                })

        final_response = co.chat(
            model=model,
            message="", 
            tools=TOOLS,
            tool_results=tool_results,
            preamble=SYSTEM_PROMPT,
            chat_history=extended_history,
            temperature=0
        )

        if final_response.meta and final_response.meta.tokens:
            total_tokens += final_response.meta.tokens.input_tokens + final_response.meta.tokens.output_tokens

        raw_output = final_response.text
    else:
        raw_output = response.text

    # CLEANUP: Final assembly of the response
    try:
        # Extract JSON even if there's conversational filler
        if "{" in raw_output and "}" in raw_output:
            json_str = raw_output[raw_output.find("{"):raw_output.rfind("}")+1]
            parsed = json.loads(json_str)
        else:
            parsed = json.loads(raw_output)
    except:
        # If model failed to give JSON, create it
        parsed = {
            "operation": "plot" if last_plot_data else "conversation",
            "expression": user_input,
            "result": None,
            "explanation": raw_output
        }

    # Inject plot data manually (Foolproof)
    if last_plot_data:
        parsed["plot_data"] = last_plot_data
        if "operation" not in parsed or parsed["operation"] == "conversation":
            parsed["operation"] = "plot"

    final_output = json.dumps(parsed, indent=2)
    save_message("ASSISTANT", final_output)

    return final_output, total_tokens