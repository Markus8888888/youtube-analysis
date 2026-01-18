import streamlit as st

def render_chat_interface():
    """
    Renders a premium chat interface.
    """
    st.markdown("### 💬 Chat with your Comments")
    st.markdown("")
    
    # Initialize chat history if not present
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I've analyzed the comments. Ask me anything about the audience sentiment or specific feedback."}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ex: 'What are people saying about the audio quality?"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate AI response
        response = f"Based on the analyzed comments, regarding **'{prompt}'**: I found that 78% of viewers had positive feedback, with specific praise for production quality. However, some users mentioned concerns about pricing. Would you like me to dive deeper into specific sentiment patterns?"
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})