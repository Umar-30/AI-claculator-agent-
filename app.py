import streamlit as st
import json
import pandas as pd
from agent import ask_agent
from memory import get_memory, clear_memory
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="AI Calculator Agent Pro",
    page_icon="🤖",
    layout="centered"
)

# Initialize Session State
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    .stJson { background-color: #1e1e1e; padding: 10px; border-radius: 5px; }
    .token-counter {
        padding: 10px;
        border-radius: 5px;
        background-color: #262730;
        border: 1px solid #4b4b4b;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def render_assistant_response(content):
    try:
        # If content is already a dict, use it, otherwise parse it
        if isinstance(content, str):
            # Try to extract JSON from the string if there's extra text
            if "{" in content and "}" in content:
                json_str = content[content.find("{"):content.rfind("}")+1]
                data = json.loads(json_str)
            else:
                data = json.loads(content)
        else:
            data = content

        explanation = data.get("explanation", "")
        if explanation:
            st.write(explanation)
        
        # Check for plot data
        plot_data = data.get("plot_data")
        if plot_data and isinstance(plot_data, dict) and "x" in plot_data and "y" in plot_data:
            # Create DataFrame
            df_plot = pd.DataFrame({
                "x": plot_data["x"],
                "y": plot_data["y"]
            })
            # Ensure x is the index for line_chart
            df_plot = df_plot.set_index("x")
            st.line_chart(df_plot)
            st.success(f"📈 Visualized: {data.get('expression', 'Function')}")

        with st.expander("🔍 View Technical Details"):
            st.json(data)
            
    except Exception as e:
        # Fallback for plain text
        st.write(content)

st.title("🤖 AI Calculator Agent Pro")
st.caption("Advanced calculations with Graphing & Enhanced Sidebar")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model Selection
    selected_model = st.selectbox(
        "Select Model",
        options=["command-r-plus-08-2024", "command-r-08-2024", "command-light"],
        index=0,
        help="Choose between powerful or fast models."
    )
    
    st.markdown("---")
    
    # Token Counter
    st.subheader("📊 Usage Statistics")
    st.markdown(f"""
        <div class="token-counter">
            Total Tokens Used: <br>
            <span style="color: #ff4b4b; font-size: 20px;">{st.session_state.total_tokens}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Cost estimation (rough)
    # Command R+ cost: ~$3 per 1M input, $15 per 1M output. Simplification: $0.01 per 1000 tokens
    cost = (st.session_state.total_tokens / 1000) * 0.01
    st.caption(f"Estimated Cost: ${cost:.4f}")
    
    st.markdown("---")
    
    # Export History
    st.subheader("💾 Data Management")
    memory_data = get_memory()
    if memory_data:
        df = pd.DataFrame(memory_data)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Chat History (CSV)",
            data=csv,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    
    if st.button("🗑️ Clear Conversation"):
        clear_memory()
        st.session_state.total_tokens = 0
        st.rerun()

    st.markdown("---")
    
    # Showcase Features
    st.subheader("🚀 Features & Capabilities")
    with st.expander("📈 Advanced Graphing", expanded=True):
        st.write("Ask me to 'plot' or 'visualize' functions!")
        st.info("**Try these examples:**\n"
                "- *Plot x squared*\n"
                "- *Visualize np.sin(x)*\n"
                "- *Graph x**3 - 5*x*")
    
    with st.expander("🔢 Math Agent"):
        st.write("I can solve multi-step math problems using tools.")
        st.caption("Add, subtract, multiply, divide, powers, and roots supported.")

# Display chat history
messages = get_memory()
for msg in messages:
    role = "user" if msg["role"] == "USER" else "assistant"
    with st.chat_message(role):
        if role == "assistant":
            render_assistant_response(msg["content"])
        else:
            st.write(msg["content"])

# Chat input
if prompt := st.chat_input("What would you like to calculate?"):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_json, tokens = ask_agent(prompt, model=selected_model)
            st.session_state.total_tokens += tokens
            render_assistant_response(response_json)
    
    # Force rerun to update token counter in sidebar
    st.rerun()
