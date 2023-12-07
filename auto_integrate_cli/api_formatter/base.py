import requests
from time import sleep

from auto_integrate_cli.settings.default import (
    AUTOGEN_RERUN_CONDITION,
    AUTOGEN_RERUN_LIMIT,
)
from .autogen import extract
# from autogen import extract


from auto_integrate_cli.file_handler.json_handler import JSONHandler


class APIFormatter:
    def __init__(self, input_obj, logger=None):
        """
        Constructor

        This constructor initializes the APIFormatter object.

        Parameters:
            input_obj (dict): The input object

        Returns:
            None
        """
        self.input_obj = input_obj
        self.logger = logger

    def format(self):
        if self.logger:
            self.logger.append(f"Formatting APIs: {self.input_obj['api1']}\n{self.input_obj['api2']}")
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

            if inputType == "json_api":
                if self.logger:
                    self.logger.append(f'Getting API details from URL')
                json_obj = self.get_json_api(apiDetail["url"])
                apiDetailsDict[apiKey] = json_obj
                apiDetailsDict[fieldKey] = json_obj

            elif inputType == "json_dict":
                if self.logger:
                    self.logger.append(f'Getting API details from JSON')
                json_obj = self.get_json(apiDetail["data"])
                apiDetailsDict[apiKey] = json_obj
                apiDetailsDict[fieldKey] = json_obj


            elif inputType == "api_doc":
                if self.logger:
                    self.logger.append(f'Getting API details from API documentation')
                json_obj = apiDetail["data"]
                apiDetailsDict[apiKey] = json_obj
                for key, value in apiDetail["data"][0].items():
                    field = key
                    fieldType = value["type"]
                    sampleVal = value["sample_value"]
                    if field not in apiDetailsDict[fieldKey].keys():
                        apiDetailsDict[fieldKey][field] = {}
                    apiDetailsDict[fieldKey][field] = {"type": fieldType, "sample_value": sampleVal}

            if "doc_website" in apiDetail.keys():
                if self.logger:
                    self.logger.append(f"Starting document extract autogen for {apiDetail['doc_website']}")
                information = ""
                if json_obj:
                    information = f"""
                    This is the starting API structure from the GET request:
                    {json_obj}.
                    """

                information += f"""\nThis is the API documentation website:
                {apiDetail["doc_website"]}. \nNow you need to extract information and structure the API.
                """
                # json_obj = extract(information)
                runs = 0
                result = None

                while runs < AUTOGEN_RERUN_LIMIT:
                    if self.logger:
                        self.logger.append(f"Starting autogen extract run {runs}")
                    sleep(1)
                    print()
                    print(f"----- STARTING AUTOGEN EXTRACT RUN {runs} -----")
                    print()
                    result = extract(information, self.logger)
                    if result != AUTOGEN_RERUN_CONDITION:
                        if self.logger:
                            self.logger.append(f"Autogen extract run {runs} successful")
                        break
                    else:
                        if self.logger:
                            self.logger.append(f"Autogen extract run {runs} failed")

                    runs += 1
                json_obj = result
                apiKey = f"api{i + 1}"
                if apiKey not in apiDetailsDict:
                    apiDetailsDict[apiKey] = {}
                apiDetailsDict[apiKey] = json_obj

        if self.logger:
            self.logger.append(f"APIs formatted")
            self.logger.append(f"API1: {apiDetailsDict['api1']}")
            self.logger.append(f"API1 Fields: {apiDetailsDict['api1Fields']}")
            self.logger.append(f"API2: {apiDetailsDict['api2']}")
            self.logger.append(f"API2 Fields: {apiDetailsDict['api2Fields']}")
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
            print("GET JSON API: OK")
            data = response.json()
            api_data = {}

            if len(data) > 0:
                for key, value in data[0].items():
                    data_type = type(value).__name__
                    api_data[key] = {"type": data_type, "sample_value": value}
            return api_data
        else:
            print("JSON API GET: ERROR ", response.status_code)
            return {}

    def get_json(self, data):
        api_data = {}
        if len(data) > 0:
            for key, value in data[0].items():
                data_type = type(value).__name__
                api_data[key] = {"type": data_type, "sample_value": value}
        return api_data

if __name__ == "__main__":


    file_handler = JSONHandler("../../demo/inputs/nyc.json", "output.json")
    inputs = file_handler.read()

    apiFormatter = APIFormatter(inputs)

    apiDetailsDict = apiFormatter.format()
