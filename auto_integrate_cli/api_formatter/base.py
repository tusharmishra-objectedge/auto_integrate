import logging
import requests
from time import sleep

from auto_integrate_cli.settings.constants import (
    JSON_API,
    JSON_DICT,
    API_DOC,
)
from auto_integrate_cli.settings.default import (
    AUTOGEN_RERUN_CONDITION,
    AUTOGEN_RERUN_LIMIT,
)
from .autogen import extract

from auto_integrate_cli.file_handler.json_handler import JSONHandler


class APIFormatter:
    def __init__(self, input_obj):
        """
        Constructor

        This constructor initializes the APIFormatter object.

        Parameters:
            input_obj (dict): The input object

        Returns:
            None
        """
        logging.info("Initializing APIFormatter")
        self.input_obj = input_obj

    def format(self):
        """
        Format APIs from distinct sources into a standard format.

        This function formats the APIs from various available sources into a
        standard format. The distinct sources for the JSON API are:
        - JSON_API: gets API information from URL of the GET request
        - JSON_DICT: gets API information from a dictionary object
        - API_DOC: gets API information from structured standardized API
        data in dictionary format, containing the documentation information.

        The standard format generated just using the above defined sources is:
        ```json
        {
            "attribute_name": {"type": "type", "sample_value": "sample_value"}
        }
        ```
        Here, the `attribute_name` is the name of the attribute in the API
        response, `type` is the data type of the attribute, and `sample_value`
        is the sample value of the attribute, typically the first value in the
        API response.

        If the api detail contains the `doc_website` key, then the recently
        structured API is passed to the `extract` function in the `autogen`
        module to extract information from the API documentation and aggregate
        it with the structured API.

        """
        logging.info(
            f"Formatting APIs: {self.input_obj['api1']}\n\
            {self.input_obj['api2']}"
        )
        api1_details = self.input_obj["api1"]
        api2_details = self.input_obj["api2"]

        apiDetails = [api1_details, api2_details]
        apiDetailsDict = {}

        for i, apiDetail in enumerate(apiDetails):
            fieldKey = f"api{i + 1}Fields"
            apiKey = f"api{i + 1}"

            if apiKey not in apiDetailsDict:
                apiDetailsDict[apiKey] = {}

            if fieldKey not in apiDetailsDict:
                apiDetailsDict[fieldKey] = {}

            inputType = apiDetail["type"]
            json_obj = {}

            if inputType == JSON_API:
                logging.info("Getting API details from URL")
                json_obj = self.get_json_api(apiDetail["url"])
                apiDetailsDict[apiKey] = json_obj
                apiDetailsDict[fieldKey] = json_obj

            elif inputType == JSON_DICT:
                logging.info("Getting API details from JSON")
                json_obj = self.get_json(apiDetail["data"])
                apiDetailsDict[apiKey] = json_obj
                apiDetailsDict[fieldKey] = json_obj

            elif inputType == API_DOC:
                logging.info("Getting API details from API documentation")
                json_obj = apiDetail["data"]
                apiDetailsDict[apiKey] = json_obj
                for key, value in apiDetail["data"][0].items():
                    field = key
                    fieldType = value["type"]
                    sampleVal = value["sample_value"]
                    if field not in apiDetailsDict[fieldKey].keys():
                        apiDetailsDict[fieldKey][field] = {}
                    apiDetailsDict[fieldKey][field] = {
                        "type": fieldType,
                        "sample_value": sampleVal,
                    }

            if "doc_website" in apiDetail.keys():
                logging.info(
                    f"Starting document extract autogen for \
                    {apiDetail['doc_website']}"
                )
                information = ""
                if json_obj:
                    information = f"""This is the starting API structure from
the GET request: {json_obj}."""
                information += f"""\nThis is the API documentation website:
{apiDetail["doc_website"]}. \nNow you need to extract information and
structure the API."""
                runs = 0
                result = None

                while runs < AUTOGEN_RERUN_LIMIT:
                    logging.info(f"Starting autogen extract run {runs}")
                    sleep(1)
                    print()
                    print(f"----- STARTING AUTOGEN EXTRACT RUN {runs} -----")
                    print()
                    result = extract(information)
                    if result != AUTOGEN_RERUN_CONDITION:
                        logging.info(f"Autogen extract run {runs} successful")
                        break
                    else:
                        logging.critical(f"Autogen extract run {runs} failed")

                    runs += 1
                json_obj = result
                apiKey = f"api{i + 1}"
                if apiKey not in apiDetailsDict:
                    apiDetailsDict[apiKey] = {}
                apiDetailsDict[apiKey] = json_obj

        logging.info("APIs formatted")
        logging.info(f"API1: {apiDetailsDict['api1']}")
        logging.info(f"API1 Fields: {apiDetailsDict['api1Fields']}")
        logging.info(f"API2: {apiDetailsDict['api2']}")
        logging.info(f"API2 Fields: {apiDetailsDict['api2Fields']}")
        return apiDetailsDict

    def get_json_api(self, url):
        """
        Get JSON API

        This function gets the JSON API data from the URL.

        Parameters:
            url (str): The URL of the JSON API

        Returns:
            list: The list of dictionaries from the JSON API
        """
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("GET JSON API: OK")
            data = response.json()
            return self.get_json(data)
        else:
            logging.error("JSON API GET: ERROR ", response.status_code)
            return {}

    def get_json(self, data):
        api_data = {}
        if len(data) > 0:
            for key, value in data[0].items():
                data_type = type(value).__name__
                api_data[key] = {"type": data_type, "sample_value": value}
        return api_data


if __name__ == "__main__":
    """
    Isolated manual test of the APIFormatter class.
    """
    file_handler = JSONHandler("../../demo/inputs/nyc.json", "output.json")
    inputs = file_handler.read()

    apiFormatter = APIFormatter(inputs)

    apiDetailsDict = apiFormatter.format()
