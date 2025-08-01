
from utils import  setup_logger
from ui.set_up import setup_page_config,load_avatars,initialize_session_state,render_sidebar,render_chat_interface

logger = setup_logger(__name__)

# --- Set page basic config ---
setup_page_config()

# --- Load avatar ---
avatar_user,avatar_ai =load_avatars()

# --- Initialize variables ---
initialize_session_state()

# --- Set sidebar ---
render_sidebar()

# --- Chat interface ---
render_chat_interface(avatar_user,avatar_ai)
