import openai
import json
import os
from app.settings.default import DEFAULT_CWD

from keys import openai_key
from app.file_handler.json_handler import JSONHandler
from app.api_formatter.base import APIFormatter

openai.api_key = openai_key

def match_api_fields(api1, api2):
    print(f'api1: {api1}')
    print(f'api2: {api2}')
    print()

    prompt = f"""
    Match the fields from the following two APIs:
    {api1} 
    and 
    {api2}
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    generated_mapping = response.choices[0].text.strip()

    field_mapping = {}

    for line in generated_mapping.split('\n'):
        parts = line.split(':')
        if len(parts) == 2:
            field_mapping[parts[0].strip()] = parts[1].strip()

    return field_mapping



if __name__ == "__main__":

    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    # file1 = JSONHandler("../demo/inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()
    # print(inputs)

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    # print(f"\nAPI 1: {api1}\n")
    # print(f"API 2: {api2}\n")

    result = match_api_fields(api1, api2)


    print('OpenAI returned: ')
    print(result)
