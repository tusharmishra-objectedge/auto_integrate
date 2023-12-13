# Auto Integrate

## Description
Auto-Integrate is a tool that allows you to automatically integrate one of your APIs into another API. It utilizes the capabilities of GPT-4 models and Autogen powered multi-agent AI conversational frameworks to automate the process of ETL. Auto-Integrate can comprehend documentation of your APIs, map their attributes with required transformations and finally, integrate them by a POST request into your target API.

## Installation
Instructions on how to install and setup your application.

## Setting up the environment
Run the following commands to set up the environment:
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage
Examples of how to use the application, including all the available commands and their options.

## Running the program
The program needs to be run from the root directory of the repository. The following arguments are required:
- `-i` or `--input`: The path to the input file
- `-o` or `--output`: The path to the output file

The program can hence be run as follows:
```bash
python3 -m auto_integrate_cli -i <input_file> -o <output_file>
```

We have set a deafult working directory for the input and output files as `demo`, located in the root directory of the repository. This setting can be configured in the `settings/default.py` file. Hence, the program can also be run as follows:

For example:
```bash
python3 -m auto_integrate_cli -i inputs/input_file.json -o outputs/output_file.json
```

## Contributing
Instructions on how to contribute to the project can be found in the [CONTRIBUTING.md](CONTRIBUTING.md) file.
