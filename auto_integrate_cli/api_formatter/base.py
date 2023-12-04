import requests

from auto_integrate_cli.settings.default import (
    AUTOGEN_RERUN_CONDITION,
    AUTOGEN_RERUN_LIMIT,
)
from .autogen import extract


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
        self.input_obj = input_obj

    def format(self):
        api1_details = self.input_obj["api1"]
        api2_details = self.input_obj["api2"]

        apis = []

        for obj in api1_details, api2_details:
            json_obj = {}
            if obj["type"] == "json_api":
                json_obj = self.get_json_api(obj["url"])
            if obj["type"] == "json_dict":
                json_obj = self.get_json(obj["data"])
            if obj["type"] == "api_doc":
                json_obj = obj["data"]
            if "doc_website" in obj:
                information = ""
                if json_obj:
                    information = f"""
                    This is the starting API structure from the GET request:
                    {json_obj}.
                    """

                information += f"""\nThis is the API documentation website:
                {obj["doc_website"]}. \n Now you need to extract information
                and structure the API.
                """
                # json_obj = extract(information)
                runs = 0
                result = None

                while runs < AUTOGEN_RERUN_LIMIT:
                    print()
                    print(f"----- STARTING AUTOGEN EXTRACT RUN {runs} -----")
                    print()
                    result = extract(information)
                    if result != AUTOGEN_RERUN_CONDITION:
                        break

                    runs += 1
                json_obj = result
            apis.append(json_obj)
        return apis

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
