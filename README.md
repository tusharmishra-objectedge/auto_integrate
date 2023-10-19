# auto-integrate

### Updates:

| Tasks                                           | Date  |
|-------------------------------------------------|-------|
| Local deployment of llama2 models               | 10/13 |
| Updated project repository with dev environment |       |
| Api calls for Llama2 70B model                  | 10/10 |
|                                                 |       |


## Setting up the environment
Run the following commands to set up the environment:
```
source venv/bin/activate
pip3 install -r requirements.txt
```

## Running the program
The program needs to be run from the root directory of the repository. The following arguments are required:
- `-i` or `--input`: The path to the input file
- `-o` or `--output`: The path to the output file

The program can hence be run as follows:
```
python3 -m auto_integrate_cli -i <input_file> -o <output_file>
```

For example:
```
python3 -m auto_integrate_cli -i inputs/mockAPI1.json -o outputs/o.txt
```

### API Pricing Chart

| Model Name  | Technical Name  | Price for 1000 tokens (prompt) | Price for 1000 tokens (completions | Price for 500 tokens for 100 executions |
|-------------|-----------------|------------------------------|------------------------------------|:---------------------------------------:|
| GPT-4 32K   | gpt-4-32k       | USD 0.0600                   | USD 0.1200                         |                  $4.50                  |
| GPT-4 8k	   | gpt-4           | USD 0.0300	                | USD 0.0600	                        |                  $2.25                  |
|   GPT-3.5 16k  | gpt-3.5-turbo-16k |   USD 0.0030   | USD 0.0040                         |                $0.18                    |
|  GPT-3.5  | gpt-3.5-turbo  | USD 0.0015       | USD 0.0020     | $0.09 |
|Davinci             | text-davinci-003     |USD 0.0200                            |  USD 0.0200   | $1.00         |



## Installing Llama2 Locally

#### Download Model
Download model from HuggingFace. 
We used the 4-bit quantized model for the 13B model. Found here: https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/blob/main/llama-2-13b-chat.Q4_0.gguf

### Install Dependencies
**Langchain**
`pip install langchain`

**Llama.cpp**
If using M1/M2 macs:

`CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install llama-cpp-python`

If already installed a cpu version of the package, reinstall with Metal:

`CMAKE_ARGS="-DLLAMA_METAL=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir`

May need to install additional dependencies:

`pip install typing-inspect==0.8.0 typing_extensions==4.5.0`



### Calling the Model
See llama2LocalLangChain.py in sandbox/Llama2Sandbox directory for example code

**Import langchain**
```
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
```


**To enable GPU with M1/M2 macs:**

**Make sure the model path is correct for your system!** (Should be path to model downloaded above)

n_gpu_layers = 1  # Metal set to 1 is enough.

n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.

```
llm = LlamaCpp(
    model_path="LLama_Model_Path",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=True, # Verbose is required to pass to the callback manager
)
```

Refer to this document for more details: https://python.langchain.com/docs/integrations/llms/llamacpp
