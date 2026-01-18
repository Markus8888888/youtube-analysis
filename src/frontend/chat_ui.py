import streamlit as st


def render_chat_interface():
    """
    Renders a premium chat interface with actual AI responses.
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
    if prompt := st.chat_input("Ex: 'What are people saying about the audio quality?'"):
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response from backend
        try:
            from src.backend.backend_service import BackEndService
            
            # Get or create backend service
            if "backend_service" not in st.session_state:
                st.session_state.backend_service = BackEndService()
            
            backend = st.session_state.backend_service
            
            # Generate AI response
            with st.spinner("Thinking..."):
                response = backend.get_ai_chat_response(prompt)
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except ImportError:
            # Fallback if backend not available
            response = "I'm sorry, the AI backend is not available. Please check your configuration."
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            with st.chat_message("assistant"):
                st.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})