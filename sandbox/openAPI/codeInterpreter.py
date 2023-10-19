from codeinterpreterapi import CodeInterpreterSession, settings, File
from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
settings.OPENAI_API_KEY = os.getenv("OPENAI_KEY")

if __name__ == "__main__":
    with CodeInterpreterSession() as session:
        files = [
            # File.from_path("mockAPI1.json"),
            File.from_path("API_matched_test.json"),
        ]

        url1 = "https://651313e18e505cebc2e98c43.mockapi.io/students"
        url2 = "https://651313e18e505cebc2e98c43.mockapi.io/pupils"
        mapped_fields = {
            "emergencyContactNumber": "emergencyContact",
            "DoB": "dateOfBirth",
            "city": "city",
            "state": "state",
            "street": "address",
            "score": "grade",
            "honorStudent": "honors",
            "created": "createdAt",
            "id": "id",
        }

        # user_request = "Using python 3, write a function that takes in a url
        # for an API and returns the structure of the data from the API in a
        # JSON format, with keys = column name and value = column type."

        # user_request = "Analyze the JSON file and generate a python function
        # that creates a POST request for the fields from api1 to api2 using
        # the L2R under manual_map."

        # user_request = "First, analyze the JSON file. Second, generate a
        # python function that creates a POST request, for an API, the keys
        # in the JSON serve as the source field and the values the target
        # field."

        user_request = f"Write a python function that uses a GET request \
            to get data from {url1} in the JSON file, and a POST request \
            to post that data to {url2} in the JSON file. Second, the \
            data from url1 should be mapped to the fields of url2 as \
            mentioned in {mapped_fields} in the JSON file."

        response = session.generate_response(user_request, files=files)

        response.show()

        print("Got response")
