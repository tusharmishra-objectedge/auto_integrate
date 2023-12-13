import logging
import os
import sys
import inquirer
from inquirer.themes import GreenPassion
from auto_integrate_cli.file_handler.json_handler import JSONHandler


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, parent_dir)


class TUIInquirer:
    def __init__(self, mapping, api1Fields, api2Fields):
        """
        Initialize the TUIInquirer class

        This function initializes the TUIInquirer class with a file path.
        Gets the directory of the file from settings
        """
        self.mapping = mapping
        self.api1Fields = api1Fields
        self.api2Fields = api2Fields
        self.questions = []

    def prepareQuestions(self):
        """
        Verify mapping for user

        Returns:
            answers (dict): key-value of api1 field name and api2 field name
        """
        logging.info("Verifying mapping using Text User Interface")
        questions = []

        for field in self.mapping:
            fieldConditions = "NO CONDITIONS"
            if "conditions" in self.mapping[field].keys():
                fieldConditions = self.mapping[field]["conditions"][0][
                    "condition"
                ]
                print(fieldConditions)
            q = (
                inquirer.Checkbox(
                    name=field,
                    message=f"""{field} - {self.mapping[
field]['source_fields']}\nTransformation: {self.mapping[
field]['transformation']}\nConditions: {fieldConditions}\n(Press <space> to
select, <Enter> to submit)""",
                    choices=["correct", "incorrect"],
                    default=["correct"],
                ),
            )
            questions.append(q)

        # Convert from list of tuple(inquirer) to list of inquirer
        questions = [x[0] for x in questions]
        self.questions = questions

    def promptUser(self):
        """
        Prompt user for verifying and choosing mapping for questions.

        Returns:
            answers (dict): key-value of api1 field name and api2 field name
        """
        self.prepareQuestions()
        logging.info(
            "Prompting user for verifying and choosing mapping for questions"
        )
        answers = inquirer.prompt(self.questions, theme=GreenPassion())

        return answers


if __name__ == "__main__":
    mappingPath = "../../demo/pipelineTest.json"
    mappingFile = JSONHandler(mappingPath, "output.txt")

    mapping = mappingFile.read()

    api1Fields = {
        "Location_Id": {"type": "int", "sample_value": 98459},
        "Business_Account_number": {"type": "int", "sample_value": 24493},
        "Ownership_Name": {"type": "str", "sample_value": "Quigley Inc"},
        "DBA_Name": {"type": "str", "sample_value": "Collins - Goodwin"},
        "Street_Address": {"type": "str", "sample_value": "2759 Alta Rapid"},
        "City": {"type": "str", "sample_value": "Port Toreymouth"},
        "State": {"type": "str", "sample_value": "Alaska"},
        "Source_Zipcode": {"type": "str", "sample_value": "09052-5081"},
        "Business_Start_Date": {
            "type": "str",
            "sample_value": "2023-02-28T17:10:34.836Z",
        },
        "Business_End_Date": {
            "type": "str",
            "sample_value": "2023-12-06T18:53:08.192Z",
        },
        "Locations_Start_Date": {
            "type": "str",
            "sample_value": "2023-09-23T17:46:44.783Z",
        },
        "Location_End_Date": {
            "type": "str",
            "sample_value": "2023-12-06T23:07:00.311Z",
        },
        "Mail_Address": {"type": "str", "sample_value": "Suite 788"},
        "Mail_City": {"type": "str", "sample_value": "New Emelybury"},
        "Mail_Zipcode": {"type": "str", "sample_value": "87243-1557"},
        "Mail_State": {"type": "str", "sample_value": "Washington"},
        "NAICS_Code": {"type": "int", "sample_value": 39993},
        "NAICS_Code_Description": {"type": "str", "sample_value": "Health"},
        "Parking_Tax": {"type": "bool", "sample_value": True},
        "Transient_Occupancy_Tax": {"type": "bool", "sample_value": True},
        "LIC_Code": {"type": "int", "sample_value": 54644},
        "LIC_Code_Description": {"type": "str", "sample_value": "Computers"},
        "Supervisor_District": {"type": "int", "sample_value": 25611},
        "Neighbourhoods-Analysis_Boundaries": {
            "type": "str",
            "sample_value": "Leuschke Course",
        },
        "Business_Corridor": {"type": "str", "sample_value": "Clothing"},
        "Business_Location": {
            "type": "list",
            "sample_value": ["-25.5596", "-12.0084"],
        },
        "id": {"type": "str", "sample_value": "1"},
    }
    api2Fields = {
        "name": {"type": "str", "sample_value": "Kilback - Hansen"},
        "domain": {"type": "str", "sample_value": "elderly-extent.com"},
        "city": {"type": "str", "sample_value": "Lavonworth"},
        "industry": {"type": "str", "sample_value": "Computers"},
        "state": {"type": "str", "sample_value": "Delaware"},
        "phone": {"type": "str", "sample_value": "1-702-410-8247 x47697"},
        "id": {"type": "str", "sample_value": "1"},
    }

    mapping = mapping["mapped"]

    tui = TUIInquirer(mapping, api1Fields, api2Fields)
    ans = tui.promptUser()
    print(ans)
