import sys
import os
from logging.handlers import RotatingFileHandler
import streamlit as st
import logging


def setup_logger(name: str = "app_logger", log_file: str = "./app.log", level=logging.DEBUG):
    """
    Set up a high-level logger that supports both file and console output and displays detailed error paths and function names.
    :param name: The name of the logger.
    :param log_file: The file path for saving logs.
    :param level: The log level, default is logging.INFO.
    :return: Returns the logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    #  Set Console Handler
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Set File Handler（auto rotating）
    if log_file and not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger(__name__)


def append_message(role: str, content: str):
    """
    Add the user's message or AI's response to Streamlit's session_state.
    """
    if "messages" not in st.session_state:
        # Make sure messages exist
        st.session_state.messages = []
    st.session_state.messages.append({"role": role, "content": content})
    # Show part of the message
    logger.debug(f"Appending role: {role}'s message: {content[:min(len(content), 50)]}...")
