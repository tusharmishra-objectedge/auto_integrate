import replicate
import os
from app.file_handler.json_handler import JSONHandler
from app.api_formatter.base import APIFormatter

os.environ["REPLICATE_API_TOKEN"] = "r8_QYWVuQFgraS9EELRwOy60Fe3aNkoEvp2oanCC"


def prompt_llama2API(api1, api2):
    """
    Prompts Llama2 70B Chat to match the fields from api1 to those in api2. Uses Replicate for the API call.
    Args:
        api1: the source api
        api2: the target api

    Returns: the output from Llama2
    """
    output = replicate.run(
        "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
        input={
            "prompt": f'Match the fields from api1 to those in api2. The data is given in a JSON format, with the keys being the field and the values the type of the data. api1: {api1} and api2: {api2}. Return the result as a json. With the unmapped fields as a JSON array under the key "unmappedFields"'}
    )

    return output


if __name__ == "__main__":



    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()



    output = replicate.run(
        "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
        input={"prompt": f'Match the fields from api1 to those in api2. The data is given in a JSON format, with the keys being the field and the values the type of the data. api1: {api1} and api2: {api2}. Return a JSON object, with the mapped fields under "mappedFields" and unmapped fields as a JSON array under "unmappedFields". The key in "mappedFields" must be a field from api1 and the value must be a field from api2.'}
    )
    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    # print(output)
    with open('llamaOutput.json', 'w+') as f:
        for item in output:
            f.write(item)

    print('Wrote output to file')
