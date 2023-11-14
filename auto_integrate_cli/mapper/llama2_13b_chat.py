import json
import os
import re

from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from auto_integrate_cli.settings.default import MODELS_DIR

from .base import BaseMapper


class LLama2Mapper(BaseMapper):
    def __init__(self, api1, api2):
        super().__init__(api1, api2)
        self.model_path = os.path.join(
            MODELS_DIR, "llama-2-13b-chat.Q4_0.gguf"
        )
        # Callbacks support token-wise streaming
        self.callback_manager = CallbackManager(
            [StreamingStdOutCallbackHandler()]
        )
        self.n_gpu_layers = 1
        self.n_batch = 512
        self.max_tokens = 4096
        self.load_model()
        self.set_prompt()

    def load_model(self):
        """
        Loads the Llama 2 model from the modelPath
        """
        print("Loading LLama 2 model...")
        llm = LlamaCpp(
            model_path=self.model_path,
            n_gpu_layers=self.n_gpu_layers,
            n_batch=self.n_batch,
            n_ctx=2048,
            f16_kv=True,
            callback_manager=self.callback_manager,
            verbose=True,
            # grammar_path=GRAMMARS_JSON_PATH,
            max_tokens=self.max_tokens,
        )
        print("Model loaded!")
        self.model = llm

    def set_prompt(self):
        system_message = """Assistant's response is always in JSON."""
        user_prompt = f"""Match field names from api1 to api2 depending on the\
        meaning from field names and data type integration feasibility.\
        api1: {self.api1} and api2: {self.api2}. Answer in JSON format: \
        field_name_from_api1: field_name_from_api2, ...\
        Mapped fields should be under the key "mapped_fields", while unmapped\
        fields should be a JSON array under the key "unmappedFields".
        """
        self.prompt = f"""
        <s>[INST]<<SYS>> {system_message} <</SYS>> {user_prompt} [/INST]
        """

    def map(self):
        response = self.model(self.prompt)
        print(f"Response: {response}")

        response = response.replace("\n", "")

        # Use Regex to clean response and capture the JSON output even if
        # result not in desired format

        pattern = r"\{(.*)\}"
        matches = re.search(pattern, response, re.MULTILINE)

        jsonString = ""

        if matches:
            jsonString += matches.group(0)

        try:
            jsonString = json.loads(jsonString)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

        return jsonString
