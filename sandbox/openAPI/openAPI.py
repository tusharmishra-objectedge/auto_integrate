import openai
import json
import os

from app.file_handler.json_handler import JSONHandler
from app.api_formatter.base import APIFormatter

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")


def match_api_fields(api1, api2):
    print(f"api1: {api1}")
    print(f"api2: {api2}")
    print()

    prompt = f"Match the fields from api1 to those in api2. The data is \
        given in a JSON format, with the keys being the field and the values \
        the type of the data. api1: {api1} and api2: {api2}."

    print(prompt)

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3500,
        temperature=0.6,
    )

    generated_mapping = response.choices[0].text.strip()

    field_mapping = {}

    for line in generated_mapping.split("\n"):
        parts = line.split(":")
        if len(parts) == 2:
            field_mapping[parts[0].strip()] = parts[1].strip()

    return field_mapping


def calculate_metrics(api1, api2, resultFile):
    with open(resultFile) as f:
        data = json.load(f)

    num_fields1 = len(api1)
    num_fields2 = len(api2)
    print(f"api1 has {num_fields1} fields")
    print(f"api2 has {num_fields2} fields")

    api1_fields = {k.replace(" ", "").lower() for k in api1.keys()}
    api2_fields = {k.replace(" ", "").lower() for k in api2.keys()}

    print(f"api1_fields: {api1_fields}")
    print(f"api2_fields: {api2_fields}")
    print()

    matches = 0

    for api1res, api2res in data.items():
        api1resClean = api1res.replace(" ", "").lower()
        api2resClean = api2res.replace(" ", "").lower()
        print(f"{api1resClean}: {api2resClean}")
        if api1resClean in api1_fields and api2resClean in api2_fields:
            api1_fields.remove(api1resClean)
            api2_fields.remove(api2resClean)
            matches += 1

    print()
    print(
        f"For {num_fields1} in api1, and {num_fields2} in api2, \
        we got {matches} matches"
    )
    print(f"score: {matches/num_fields1}")


if __name__ == "__main__":
    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    print("Mapping api1 to api2")
    # print(api1)

    result = match_api_fields(api1, api2)

    print("OpenAI returned: ")
    print(result)

    if len(result) > 0:
        # save to output file
        with open("openAI_output.txt", "w+") as f:
            json.dump(result, f, indent=2)

        print("Wrote output to file")

        calculate_metrics(api1, api2, "openAI_output.txt")
    else:
        print("OpenAI returned no results, run again")

    # calculate_metrics(api1, api2, 'openAI_output.txt')
    # prompt = f"""
    #    Match the fields from the following two APIs:
    #    {api1}
    #    and
    #    {api2}
    #    """
    #
    # print(len(prompt))
