import streamlit as st
from PIL import Image
# import custom module
from utils import append_message, setup_logger
from interface.ai_chat import get_ai_response
from config import ROLES

logger = setup_logger(__name__)


def setup_page_config():
    """Setup page config"""
    st.set_page_config(
        page_title="AI ChatBot",
        page_icon="🤖",
        layout="centered",
        # initial_sidebar_state="collapsed" # set the initial state of sidebar
    )


@st.cache_resource
def load_avatars():
    """Cache to load avatars"""
    try:
        avatar_user = Image.open("static/user_avatar.png")
        avatar_ai = Image.open("static/ai_avatar.png")
        return avatar_user, avatar_ai
    except FileNotFoundError as e:
        logger.error(f"Avatar image not found: {e}")
        return None, None

def render_chat_history(avatar_user, avatar_ai):
    """Render chat history messages"""

    chat_history_container = st.container()
    with chat_history_container:
        # Loop for all histories
        for message in st.session_state.messages:
            cols = st.columns([1, 6, 1]) if message["role"] == "user" else st.columns([1, 6, 1][::-1])
            with cols[2 if message["role"] == "user" else 0]:
                st.image(image = avatar_user if message["role"] == "user" else avatar_ai,
                         caption= "user" if message["role"] == "user" else "robot",
                         use_column_width=True,
                         width=40)
            with cols[1]:
                # create_message_bubble(content={message['content']})
                bubble_color = "#DCF8C6" if message["role"] == "user" else "#F1F0F0"
                logger.debug(f"Check the full message：{message}")
                st.markdown(
                    f"<div style='background-color:{bubble_color}; padding: 10px; border-radius: 10px;'>{message['content']}</div>",
                    unsafe_allow_html=True
                )


def render_single_message(message, avatar_user, avatar_ai):
    """Render single message"""
    is_user = message["role"] == "user"

    # Create columns
    cols = st.columns([1, 6, 1]) if is_user else st.columns([1, 6, 1][::-1])

    # Columns for avatar
    with cols[2 if is_user else 0]:
        avatar = avatar_user if is_user else avatar_ai
        caption = "user" if is_user else "robot"
        st.image(avatar, caption=caption, use_column_width=True, width=40)

    # Columns for history message
    with cols[1]:
        logger.debug(f"Check the full message：{message}")
        bubble_color = "#DCF8C6" if is_user else "#F1F0F0"
        st.markdown(
            f"<div style='background-color:{bubble_color}; padding: 10px; border-radius: 10px;'>{message['content']}</div>",
            unsafe_allow_html=True
        )

def render_chat_interface(avatar_user, avatar_ai):
    """Render chat interface"""
    # Create container to contain history message
    chat_history_container = st.container()

    with chat_history_container:
        # Render each single message
        for message in st.session_state.messages:
            render_single_message(message, avatar_user, avatar_ai)

    # Clean history bottom
    if st.session_state.messages:
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            st.caption(f"💬 Total conversations: {len(st.session_state.messages)} ")

        with col2:
            if st.button("🗑️ Clean",use_container_width=True): #  type="secondary", key="clear_chat",
                st.session_state.messages = []
                if "last_message_count" in st.session_state:
                    st.session_state.last_message_count = 0
                st.rerun()

    # Get user input
    user_input = st.chat_input("Type your question...", key="user_input")

    # Handle uer input
    if user_input:
        handle_user_input(user_input, avatar_user, avatar_ai, chat_history_container)

def initialize_session_state():
    """Initialize session state"""
    defaults = {
        "messages": [],
        "selected_role": ROLES[0] if ROLES else "👑 Dominating CEO",
        "temperature": 0.7,
        "model": "GLM-4-9B-0414",
        "last_message_count": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_sidebar():
    """Render sidebar"""
    # --- Set sidebar  ---
    with st.sidebar.expander("🛠 Advanced Setting"):
        st.session_state.temperature = st.slider("Temperature", 0.0, 1.2, 0.7, 0.1)
        st.session_state.model = st.selectbox(
            label="Choose Model",
            options=["GLM-4-9B-0414", "GLM-4.1V-9B-Thinking", "Qwen3-8B", "GLM-Z1-9B-0414",
                     "DeepSeek-R1-Distill-Qwen-7B"],
            index=0
        )
        st.session_state.role = st.selectbox(
            label="Choose Character",
            options=["👑 Dominating CEO", "🎀 Adorable Loli"],
            index=0
        )
        logger.info(f"User selecting role:{st.session_state.role}")

    # --- User manual ---
    with st.sidebar.expander("📖 Manual"):
        st.markdown("1. 1️⃣ Choose a Character\n 2. 2️⃣ Input your question\n 3. 3️⃣ Click the send bottom")


def handle_user_input(user_input, avatar_user, avatar_ai, chat_history_container):
    """Handle user input"""
    try:
        logger.info(f"Get input query: {user_input}")
        append_message("user", user_input)

        # Init a empty placeholder
        placeholder = chat_history_container.empty()
        with placeholder.container():
            cols = st.columns([1, 6, 1][::-1])
            with cols[0]:
                st.image(avatar_ai, width=40)
            with cols[1]:
                msg_area = st.empty()

            full_response = ""
            message_placeholder = st.empty()

            # Get response from AI model
            for chunk in get_ai_response(
                    user_query=user_input,
                    role=st.session_state.role,
                    model_name=st.session_state.model,
                    temperature=st.session_state.temperature
            ):
                full_response += chunk
                # Update the history message
                message_placeholder.markdown(
                    f"<div style='background-color:#F1F0F0; padding: 10px; border-radius: 10px;'>{full_response}</div>",
                    unsafe_allow_html=True
                )

            append_message("assistant", full_response)
            # Reload the page to show the full history message
            st.rerun()

    except Exception as e:
        logger.error(f"Call api error: {e}")
        st.error(f"Call api error: {e}")
