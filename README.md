# 🤖 AI Calculator Agent Pro

A professional-grade AI Agent that goes beyond simple arithmetic. Powered by **Cohere's Command R+** model and **Streamlit**, this agent can solve complex multi-step math problems and generate real-time interactive graphs.

## 🚀 Key Features

- **Accurate Calculations:** Unlike standard LLMs, this agent uses specialized tools (Python logic) to ensure 100% mathematical accuracy.
- **📈 Advanced Graphing:** Visualize functions instantly! Just ask to "plot x^2" or "visualize a sine wave".
- **📊 Pro Sidebar:**
    - **Model Selection:** Switch between different Cohere models (Powerful vs. Fast).
    - **Token Counter:** Real-time tracking of API usage and estimated costs.
    - **Export History:** Download your entire conversation history as a CSV file.
- **💾 Conversation Memory:** Remembers previous calculations for context-aware problem solving.
- **🌑 Sleek Dark UI:** A modern, user-friendly interface built with Streamlit.

## 🛠️ Tech Stack

- **Language:** Python 3.14+
- **AI Orchestration:** Cohere API (Tool Use/Function Calling)
- **Frontend:** Streamlit
- **Data Handling:** Pandas, NumPy
- **Visuals:** Native Streamlit Charting (Line Charts)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai-calculator-agent
   ```

2. **Set up environment variables:**
   Create a `.env` file in the root directory and add your Cohere API key:
   ```env
   COHERE_API_KEY=your_api_key_here
   ```

3. **Install dependencies using `uv`:**
   ```bash
   uv sync
   ```

## 🏃 Usage

Run the application using Streamlit:

```bash
uv run streamlit run app.py
```

### 💡 Example Prompts to Try:
- "What is 15% of 2500?"
- "Solve for x: 2x + 10 = 50"
- "Plot the function x^2 - 4"
- "Visualize a sine wave from -10 to 10"

## 🏗️ Architecture

- **`app.py`**: The main Streamlit interface and UI logic.
- **`agent.py`**: AI logic, tool orchestration, and response assembly.
- **`tools.py`**: Pure Python functions for math and graphing.
- **`memory.py`**: Manages persistent chat history in `memory.json`.
- **`schemas.py`**: Pydantic models for structured AI responses.

## 🛡️ License

This project is open-source and available under the MIT License.

---
*Developed as part of an advanced AI development internship.*
