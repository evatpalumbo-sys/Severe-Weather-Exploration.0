# Lab 3: Chatbot page
# TODO: Rename this file to fit your page. Keep the number at the front.
#
# A chatbot built with Pydantic AI (see the Pydantic AI pages on Canvas).
# It should:
#   - use a Pydantic AI Agent with instructions that fit your project's theme (no tools yet)
#   - use Streamlit's chat elements: st.chat_message and st.chat_input
#   - remember the conversation (message_history, saved in st.session_state)
#   - use try/except so an error shows a message instead of crashing the page
#   - stay on theme, without using any API or external data
#
# Your Gemini API key goes in .streamlit/secrets.toml as GOOGLE_API_KEY.

import streamlit as st
from pydantic_ai import Agent

st.title("WeatherBot")

st.write(
    "Ask questions about weather, storms, forecasting, "
    "hurricanes, tornadoes, clouds, and meteorology."
)

# Create the agent
agent = Agent(
    model="google-gla:gemini-2.0-flash",
    system_prompt="""
You are WeatherBot, a helpful meteorology assistant.

You can explain:
- thunderstorms
- tornadoes
- hurricanes
- weather forecasting
- clouds
- atmospheric science
- weather safety

Stay focused on meteorology topics.

Do not claim to provide real-time weather forecasts.
Do not make up current weather conditions.
Keep answers educational and easy to understand.
"""
)

# Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask a weather question...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        # Build conversation history
        conversation = ""

        for msg in st.session_state.messages:
            conversation += (
                f"{msg['role'].upper()}: "
                f"{msg['content']}\n"
            )

        result = agent.run_sync(conversation)

        response = result.output

    except Exception:
        response = (
            "Sorry, WeatherBot encountered an error. "
            "Please try again."
        )

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)