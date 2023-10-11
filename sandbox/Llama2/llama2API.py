import replicate
import os

if __name__ == "__main__":
    os.environ["REPLICATE_API_TOKEN"] = "r8_QYWVuQFgraS9EELRwOy60Fe3aNkoEvp2oanCC"


    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()



    output = replicate.run(
        "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
        input={"prompt": f'Match the fields from api1 to those in api2. The data is given in a JSON format, with the keys being the field and the values the type of the data. api1: {api1} and api2: {api2}.'}
    )
    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    for item in output:
        print(item)


