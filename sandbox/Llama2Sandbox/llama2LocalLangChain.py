import re
import json

from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import os
from app.file_handler.json_handler import JSONHandler
from app.api_formatter.base import APIFormatter

from llama_cpp.llama_grammar import LlamaGrammar

LLAMA_13B_LOCAL_PATH = '/Users/aditya/Llama2/llama-2-13b-chat.gguf.q4_1.bin'
LLAMA_7B_LOCAL_PATH = '/Users/aditya/Llama2/llama-2-7b-chat.Q4_K_M.gguf'
GRAMMARS_JSON_PATH = '/Users/aditya/Desktop/USF/Fall 2023/AutoIntegrate/auto-integrate/sandbox/Llama2Sandbox/llama.cpp/grammars/json.gbnf'

template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = 1  # Metal set to 1 is enough.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
# Make sure the model path is correct for your system!

def loadModel(modelPath):
    """
    Loads the Llama 2 model from the modelPath
    Args:
        modelPath: Path to model file

    Returns: LlamaCpp object

    """

    print('Loading model...')

    llm = LlamaCpp(
        model_path=modelPath,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
        # grammar_path=GRAMMARS_JSON_PATH,
    )

    print('Model loaded!')

    return llm

def promptModel(api1, api2):
    """
    Prompts the Llama 2 model with the api1 and api2 and returns the response. Api1 and api2 must be formatted using api_formatter.format()
    Args:
        api1: api1
        api2: api2

    Returns:JSON response from Llama 2 model. Mapped fields under "mappedFields" and unmapped fields as a JSON array under the key "unmappedFields"

    """

    print('Prompting model...')

    system_message = f"""Assistant's response is always in a JSON format.
        """

    instruction_message = f"""Respond to the following in JSON with 'mappedFields' and 'unmappedFields' values "
        """

    user_message = f"""Map the fields from api1 to the fields in api2. api1: {api1} and api2: {api2}. Mapped fields should be under "mappedFields". Unmapped fields as a JSON array under the key "unmappedFields". The output must be in the JSON format."""

    prompt = f"""<s>[INST]<<SYS>>
           {system_message} <</SYS>>

           {user_message}[/INST]"""

    result = llm(prompt)

    print('Prompt returned, cleaning prompt...')

    resultClean = result.replace("\n", "")

    """
    Use Regex to clean response and capture the JSON output even if result not in desired format
    """
    pattern = r"\{(.*)\}"
    matches = re.search(pattern, resultClean, re.MULTILINE)

    jsonString = ""

    if matches:
        jsonString += matches.group(0)

    try:
        parsed_json = json.loads(jsonString)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

    return parsed_json


if __name__ == "__main__":
    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    llm = loadModel(LLAMA_13B_LOCAL_PATH)

    parsed_json = promptModel(api1, api2)

    print(parsed_json)

    # Specify the file path where you want to save the JSON data
    # Write the captured JSON data to the file
    with open('llamaLocalLang.json', "w+") as json_file:
        json.dump(parsed_json, json_file, indent=4)

    print(f"Captured data has been written to llamaLocalLang.json")