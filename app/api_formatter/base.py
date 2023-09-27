import requests

class APIFormatter():

    def __init__(self, input_obj):
        """
        Constructor

        This constructor initializes the APIFormatter object with the input object.

        Parameters:
            input_obj (dict): The input object

        Returns:
            None
        """
        self.input_obj = input_obj

    def format(self):
        api1_details = self.input_obj['api1']
        api2_details = self.input_obj['api2']

        api_attr = []
        
        for obj in api1_details, api2_details:
            if obj['type'] == 'mock_api':
                api_attr.append(self.get_mock_api(obj['url']))

        return api_attr

    def get_mock_api(self, url):
        """
        Get mock API

        This function gets the mock API data from the URL.

        Parameters:
            url (str): The URL of the mock API

        Returns:
            list: The list of dictionaries from the mock API
        """
        response = requests.get(url)
        if response.status_code == 200:
            print("GET mock API: OK")
            data = response.json()
            api_data = {}
        
            if len(data) > 0:
                for key, value in data[0].items():
                    data_type = type(value).__name__
                    api_data[key] = data_type
            return api_data
            
        else:
            print("MockAPI GET: ERROR ", response.status_code)
            return {}
