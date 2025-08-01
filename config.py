import os

# Get env variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1")

# Set default url as silicon flow's url
SILICON_FLOW_API_KEY = os.getenv("SILICON_FLOW_API_KEY")
SILICON_FLOW_API_URL = os.getenv("SILICON_FLOW_API_URL", "https://api.siliconflow.cn/v1")

#Check whether if the api key exists
if not OPENAI_API_KEY and not SILICON_FLOW_API_KEY:
    raise ValueError("BOTH OPENAI_API_KEY OR SILICON_FLOW_API_KEY IS EMPTY PLEASE RESET IT！！")

# Default temperature
TEMPERATURE = 0.7

# Call API retry times
RETRY_TIME = 3

# TODO: "🎩 Gentleman Scholar", "🧙‍♂️ Magic Girl"
ROLES = ["👑 Dominating CEO", "🎀 Adorable Loli"],

ROLES_SHOT_NAME_DICT = {"👑 Dominating CEO":"domineering_ceo",
                        "🎀 Adorable Loli":"loli"}

# Set up the available models of Silicon flow's platform for user to choose
MODEL_MAP = {"DeepSeek-R1-Distill-Qwen-7B":"deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
             "GLM-4-9B-0414":"THUDM/GLM-4-9B-0414",
             "GLM-Z1-9B-0414":"THUDM/GLM-Z1-9B-0414",
             "Qwen3-8B":"Qwen/Qwen3-8B",
             "GLM-4.1V-9B-Thinking":"THUDM/GLM-4.1V-9B-Thinking"}