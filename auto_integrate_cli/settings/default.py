import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CWD = "demo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ORG_ID = os.getenv("OPENAI_API_ORG_ID")
MODELS_DIR = "../models"
AVAILABLE_MODELS = {
    "LLAMA-2-13B-Chat": "llama-2-13b-chat.Q4_0.gguf",
}
AUTOGEN_RERUN_CONDITION = "***RERUN_AUTOGEN***"
AUTOGEN_RERUN_LIMIT = 3
