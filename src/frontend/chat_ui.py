import streamlit as st

def render_chat_interface():
    """
    Renders the chat history and input box.
    """
    st.markdown("### 💬 Chat with your Comments")
    
    # Initialize chat history if not present
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I've analyzed the comments. Ask me anything about the audience sentiment or specific feedback."}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ex: 'What are people saying about the audio quality?'"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- PLACEHOLDER FOR AI BRAIN CONNECTION ---
        # In a real scenario, you would call `get_gemini_response(prompt)` here.
        # For UI demo purposes, we echo a dummy response.
        response = f"I noticed you asked about: '{prompt}'. (AI Brain not connected yet)"
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})