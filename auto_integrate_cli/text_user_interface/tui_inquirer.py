import inquirer
from inquirer.themes import GreenPassion
from inquirer.themes import BlueComposure

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, parent_dir)

from auto_integrate_cli.file_handler.json_handler import JSONHandler
from auto_integrate_cli.api_formatter.base import APIFormatter

import pandas as pd
import plotly.graph_objs as go


def prepareQuestions(api1, api2, mapping):
    """
    Prepare questions for inquirer to prompt user for mapping
    Args:
        api1: api1 from api_formatter
        api2: api2 from api_formatter
        mapping: JSON from mapping file

    Returns: list of questions for inquirer

    """
    mappedFields = mapping['mappedFields']
    unmappedFields = mapping['unmappedFields']

    api1Fields = [x for x in api1.keys()]
    api2Fields = [x for x in api2.keys()]

    questions = []

    # Questions for mapped fields
    for field in mappedFields:
        q = inquirer.Checkbox(name=field,
                          message=f"VERIFY mapping for {field} (Press <space> to select, <Enter> to submit)",
                          choices=api2Fields,
                          default=[mappedFields[field]],
                          ),
        questions.append(q)

    # Questions for unmapped fields
    for field in unmappedFields:
        q = inquirer.Checkbox(name=field,
                          message=f"CHOOSE mapping for UNMAPPED {field} (Press <space> to select, <Enter> to submit)",
                          choices=api2Fields,
                          ),
        questions.append(q)

    # Convert from list of tuple(inquirer) to list of inquirer
    questions = [x[0] for x in questions]
    return questions

def promptUser(questions):
    """
    Prompt user for verifying and choosing mapping for questions
    Args:
        questions: list of questions for inquirer

    Returns: Dict of answers from user, with key as api1 field name and values ad api2 field names

    """
    answers = inquirer.prompt(questions, theme=GreenPassion())
    return answers

def visualize(mappings):
    """
    Visualize the mapping, uses Plotly to plot a table
    Args:
        mappings: Dict returned from promptUser

    Returns: None

    """
    # testData = {'fullName': ['name', 'extraName'], 'emergencyContactNumber': ['emergencyContact'],
    #             'DoB': ['dateOfBirth'], 'city': ['city'], 'state': ['state'], 'street': ['address'],
    #             'score': ['grade'], 'honorStudent': ['honors'], 'created': ['createdAt'],
    #             'tt1': ['typeTest1'], 'tt2': ['typeTest2'], 'tt3': ['typeTest3']}

    for key in mappings:
        mappings[key] = ", ".join(mappings[key])

    df = pd.DataFrame(mappings.items(), columns=['Original Field Name', 'Mapped Field Name'])

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df['Original Field Name'], df['Mapped Field Name']],
                   fill_color='lavender',
                   align='left'))
    ])

    fig.show()


if __name__ == "__main__":
    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file, 'output.txt')
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    print(api1)
    print(api2)

    mappingPath = "../../sandbox/Llama2Sandbox/llamaLocalLang.json"
    mappingFile = JSONHandler(mappingPath, 'output.txt')

    mapping = mappingFile.read()

    questions = prepareQuestions(api1, api2, mapping)
    ans = promptUser(questions)
    print(ans)

    visualize(ans)
