import requests


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

        api_attr = []

        for obj in api1_details, api2_details:
            if obj['type'] == 'json_api':
                api_attr.append(self.get_json_api(obj['url']))

        return api_attr

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
                    api_data[key] = data_type
            return api_data

        else:
            print("JSON API GET: ERROR ", response.status_code)
            return {}
