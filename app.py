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

# Custom CSS for Responsiveness and Modern Look
st.markdown("""
    <style>
    /* Main Background and Text */
    .main { 
        background-color: #0e1117; 
    }
    
    /* Responsive Font Sizes */
    html {
        font-size: 16px;
    }
    @media (max-width: 768px) {
        html {
            font-size: 14px;
        }
        .stTitle {
            font-size: 1.8rem !important;
        }
    }

    /* Chat Message Styling */
    .stChatMessage { 
        border-radius: 12px; 
        margin-bottom: 15px;
        padding: 1rem;
        border: 1px solid #262730;
    }
    
    /* Improved Json and Code blocks */
    .stJson, code { 
        background-color: #1e1e1e !important; 
        padding: 12px !important; 
        border-radius: 8px !important; 
    }

    /* Token Counter - Fully Responsive */
    .token-counter {
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(145deg, #1e1e1e, #262730);
        border: 1px solid #4b4b4b;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    .token-value {
        color: #ff4b4b;
        font-size: 1.5rem;
        display: block;
        margin-top: 5px;
    }

    /* Sidebar Improvements */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        padding-top: 2rem;
    }
    
    /* Make buttons look better on mobile */
    .stButton button {
        width: 100%;
        border-radius: 8px;
    }
    
    /* Adjusting container for better mobile experience */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 800px;
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
        result = data.get("result")
        operation = data.get("operation", "Calculation")

        # Highlight the result if it exists
        if result is not None:
            st.markdown(f"### 🎯 Result: `{result}`")
        
        if explanation:
            st.markdown(f"**Explanation:**\n{explanation}")
        
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
            
            # Responsive container for chart
            with st.container():
                st.line_chart(df_plot, use_container_width=True)
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
    
    # Token Counter & Cost in Columns
    st.subheader("📊 Usage Statistics")
    
    col1, col2 = st.columns(2)
    
    # Cost estimation (rough)
    cost = (st.session_state.total_tokens / 1000) * 0.01
    
    with col1:
        st.markdown(f"""
            <div class="token-counter">
                Tokens
                <span class="token-value" style="font-size: 1.2rem;">{st.session_state.total_tokens}</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="token-counter">
                Cost
                <span class="token-value" style="font-size: 1.2rem;">${cost:.4f}</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Export History
    st.subheader("💾 Data Management")
    memory_data = get_memory()
    if memory_data:
        df = pd.DataFrame(memory_data)
        csv = df.to_csv(index=False).encode('utf-8')
        if st.download_button(
            label="📥 Export Chat History (CSV)",
            data=csv,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        ):
            st.toast("History exported successfully!", icon="✅")
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        clear_memory()
        st.session_state.total_tokens = 0
        st.toast("Memory cleared!", icon="🧹")
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
