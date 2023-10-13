import time
import copy
import asyncio
import requests
import os

from fastapi import FastAPI, Request
from llama_cpp import Llama
from sse_starlette import EventSourceResponse

from app.file_handler.json_handler import JSONHandler
from app.api_formatter.base import APIFormatter

LLAMA_13B_LOCAL_PATH = '/Users/aditya/Llama2/llama-2-13b-chat.gguf.q4_1.bin'
LLAMA_7B_LOCAL_PATH = '/Users/aditya/Llama2/llama-2-7b-chat.Q4_K_M.gguf'

# Conversion script if model is ggml, llama.cpp now needs gguf
# python ./convert-llama-ggmlv3-to-gguf.py --eps 1e-5 --input /Users/aditya/Llama2/llama-2-13b-chat.ggml.q4_1.bin --output /Users/aditya/Llama2/llama-2-13b-chat.gguf.q4_1.bin

# uvicorn script to run fastapi server with llama2 model
# uvicorn llama2local:app --host localhost --port 8080

#Load the model
def load_model(path):

    llama_local_path = os.path.abspath(path)
    print(os.path.isfile(llama_local_path))
    print(f'Model path: {llama_local_path}')
    print('Loading model...')

    try:
        llm = Llama(model_path=llama_local_path)
        print('Model loaded!')
    except Exception as e:
        print(f'Error loading model: {e}')

    return llm


def generate_text(
    prompt="Who is the CEO of Apple?",
    max_tokens=256,
    temperature=0.1,
    top_p=0.5,
    echo=False,
    stop=["#"],
):
    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        echo=echo,
        stop=stop,
    )
    output_text = output["choices"][0]["text"].strip()
    return output_text

if __name__ == "__main__":
    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    llm = load_model(LLAMA_7B_LOCAL_PATH)

    prompt = f"""[INST] <<SYS>> Match the fields from api1 to those in api2. The data is given in a JSON format, with the keys being the field and the values the type of the data. api1: {api1} and api2: {api2}. Return the result as a json. With the unmapped fields as a JSON array under the key "unmappedFields". <</SYS>>[/INST]"""

    # stream = llm(
    #             prompt,
    #             max_tokens=500,
    #             stop=["\n", " Q:"],
    #             stream=True,
    #         )
    print('Prompting model...')
    st = time.time()
    output = llm(prompt,
                 max_tokens=350,
                 echo=True)
    print('Generated output!')
    et = time.time()
    print(f'Time taken: {et-st}')
    output_text = output["choices"][0]["text"].split('[/INST]')[-1]
    print(f'Output: {output_text}')

    with open('llamaLocal_Output.json', 'w+') as f:
        for item in output_text:
            f.write(item)

    print('Wrote output to file')