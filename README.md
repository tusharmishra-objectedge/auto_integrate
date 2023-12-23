# Auto Integrate

## Description
Auto-Integrate is a tool that allows you to automatically integrate one of your APIs into another API. It utilizes the capabilities of GPT-4 models and Autogen powered multi-agent AI conversational frameworks to automate the process of ETL. Auto-Integrate can comprehend documentation of your APIs, map their attributes with required transformations and finally, integrate them by a POST request into your target API.

## Installation
Instructions on how to install and setup your application.

## Setting up the environment
Run the following commands to set up the environment:

For the first time when the project is set up locally, run the following to create a virtuall
environment named `venv`:
```bash
python -m venv venv
```

Activate the virtual environment and up-date the dependencies every time by the following
commands:
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

## Setting up environment variables

### Dotenv
Create a `.env` file in the `auto_integrate_cli` directory of the project.

You can set variables defined in `settings/default.py` in this file for development purposes.

Additionally, you can set the following variables if you chose to use the standalone OPENAI mapper
present in `mapper/openai.py`:
- `OPENAI_API_KEY`: The OpenAI API key.
- `OPENAI_API_ORG_ID`: The OpenAI API Organisation ID to use for the API key.

### Environment variables for Autogen
Create a `OAI_CONFIG_LIST` file in the root directory of the project.

This file contains a list of objects that contain the following keys:
- `model`: The OPENAI model to use
- `api_key`: The OPENAI API key to use with the specific model

This list is used by Autogen to run the models and is aggregately dependent on all the autogen configurations, such as in the `api_formatter/autogen.py` and `mapper/autogen.py` file. See the `filter_dict` in the config for the list of `model` keys that can be set.

Example `OAI_CONFIG_LIST` file:
```
[
  {
    "model": "gpt-4",
    "api_key": "<KEY>"
  },
  {
    "model": "gpt-4-1106-preview",
    "api_key": "<KEY>"
  }
]
```

## Usage
Examples of how to use the application, including all the available commands and their options.

## Running the program
The program needs to be run from the root directory of the repository.

The following arguments are accepted:
- `-i` or `--input`: The path to the input file. Required.
- `-o` or `--output`: The path to the output file. Not required, it will default to output.txt if not provided.

By default, `demo` folder in the root directory is used to acess input and output files. This is set in the `settings/default.py` file. Ideally, add a dotenv setting modification if required in future.

The program can hence be run as follows:
```bash
python3 -m auto_integrate_cli -i <input_file> -o <output_file>
```

We have set a deafult working directory for the input and output files as `demo`, located in the root directory of the repository. This setting can be configured in the `settings/default.py` file. Hence, the program can also be run as follows:

For example:
```bash
python3 -m auto_integrate_cli -i inputs/input_file.json -o outputs/output_file.json
```
## Running the tests
We support unit tests using PyTest.
To run the tests:
```bash
python3 -m auto_integrate_cli -i <input_file> --runTests
```

## Contributing
Instructions on how to contribute to the project can be found in the [CONTRIBUTING.md](CONTRIBUTING.md) file.
