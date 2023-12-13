import autogen
import json
import re

from auto_integrate_cli.settings.default import AUTOGEN_RERUN_CONDITION


def extract(information, logger=None):
    """
    Extract information from the API documentation.

    This function extracts information from the API documentation.
    The information is extracted using an AI multi-agent conversational
    framework. The agents set up for the task are:

    - InformationExtractor: Extracts information from the API documentation,
    such as the Base URL of the API and its endpoints, supported methods,
    authentication methods, and response codes. It also extracts information
    about the fields in the response of the API, such as the field name,
    field type, field description, and field constraints by the method of
    scrapping the API documentation.
    - DataFormatAnalyzer: Analyzes the data format of the API response. It
    assesses the data format of the API response and provides insights on the
    field names, field types, field descriptions, and field constraints.
    - TaskManager: Manages the conversation between the agents. It assigns
    the tasks to the agents and assesses the agents' performance. It also
    ensures that the information provided by the agents is correct and in the
    desired output format.
    - UserProxy: It initializes the chat and provides the starting prompt for
    the group conversation.

    Parameters:
        information (str): The API documentation information.

    Returns:
        jsonString (str): The JSON string of the API structure.
    """
    llm_config = {
        "config_list": autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST",
            filter_dict={
                "model": {
                    # "gpt-3.5-turbo",
                    # "gpt-3.5-turbo-16k",
                    # "gpt-4",
                    # "gpt-4-32k",
                    "gpt-4-1106-preview"
                },
            },
        )
    }
    information_extractor = autogen.AssistantAgent(
        name="InformationExtractor",
        llm_config=llm_config,
        system_message="""Information Extractor. You extract information
from the APIs. You know how to use the API documentation to extract
information about the API. You should reply after your documentation lookup.
You can scrape the documentation HTML content or take help from other agents
to extract relevant information which can include the following:
1. Base URL of the API and the API endpoints
2. HTTP methods supported for each endpoint
3. Authentication mechanisms required
4. Sample request and response
5. Descriptions, data types, sample values, and constraints for each field.
6. Any additional information or documentation that can be useful.

In the following cases, you should ensure extra consideration:
1. If the field type is an Object, you should add a new key-value pair to the
field description to describe the children fields under the key "children".
2. If the field type is a list, you should add a new key-value pair to the
field description to describe the list items under the key "items".
3. If the field is self-generated, that is, the field is assigned a value
automatically by the API, you should set the constraint "ignore" to true.
4. If the field is not required, you should set the constraint "required" to
false.

Kindly note that the task is of a real-world nature and requires you to use
your skills to find the right information. You should not make up information.
You should reply after your documentation lookup.""",
        code_execution_config={
            "work_dir": "web",
        },
    )
    data_format_analyzer = autogen.AssistantAgent(
        name="DataFormatAnalyzer",
        llm_config=llm_config,
        system_message="""Data Format Analyzer. You analyze the data
models from the extracted information. You can identify the data types and
structures in the data models. You can identify equivalent data types across
different APIs. You can identify constraints on fields and classify them if
they are required, unique, or can be ignored for mapping. You can identify the
right description for each field.

Kindly note that the task is of a real-world nature and requires you to use
your skills to find the right information. You should not make up information.
You should reply after your documentation lookup.""",
    )
    task_manager = autogen.AssistantAgent(
        name="TaskManager",
        llm_config=llm_config,
        system_message="""Task Manager. You manage the process of structuring
the API information. You assign tasks to other agents and monitor their
progress. You ensure that agents are working on the right tasks and that tasks
are completed on time. You coordinate the work of other agents and ensure that
the structuring process is efficient and effective, and the output is in JSON
format. This is a deterministic task which requires fact-checking, and
mathematical problem-solving. The models' performances on these tasks can be
measured against clear benchmarks, providing objective data on their accuracy.

When you find an answer, verify the answer carefully. Include verifiable
evidence in your response if possible. Make sure that the answer is complete,
precise, contextually in accordance to language skills. The answer must be in
a valid JSON format without any character, symbol or comments that is not
allowed in JSON. Do not abstract or concatenate the answer. Do not make up any information.

Example:
{
    "base_url": "https://api.example.com",
    "authentication": {
        "type": "auth_type",
        "required": "true",
        "details": {
            "username": "username",
            "password": "password",
            "token": "token"
            ...
        }
        ...
    },
    endpoints: {
        "endpoint_name1": {
            "method": "http_method",
            "description": "endpoint_description",
            "parameters": {
                "field_name1": {
                    "type": "field_type",
                    "sample_value": "field_value",
                    "description": "field_description",
                    "constraints": {
                        "required": true,
                        "unique": false,
                        "ignore": false
                    }
                    ...
                },
                "field_name2": {
                    "type": "Object",
                    "sample_value": "field_value",
                    "description": "field_description",
                    "constraints": {
                        "required": true,
                        "unique": false,
                        "ignore": false
                    },
                    children: {
                        "child_field_name1": {
                            ...
                        },
                        ...
                    }
                    ...
                },
            },
        },
        ...
    },
}

Reply with the final JSON output and write “TERMINATE” in the end when
everything is done with full satisfaction.""",
        code_execution_config={
            "work_dir": "web",
            "use_docker": False,
        },
    )
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "web",
        },
    )

    groupchat = autogen.GroupChat(
        agents=[
            information_extractor,
            data_format_analyzer,
            task_manager,
            user_proxy,
        ],
        messages=[],
        max_round=50,
    )
    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )
    user_proxy.initiate_chat(
        manager,
        message=f"""Following is the information for an API that must be
used to retrieve relevant information about the APIs to structure the
information. {information}""",
    )
    response = user_proxy.last_message()["content"]
    response = response.replace("\n", "")

    # Use Regex to clean response and capture the JSON output even if
    # result not in desired format

    pattern = r"\{(.*)\}"
    matches = re.search(pattern, response, re.MULTILINE)

    jsonString = ""

    if matches:
        jsonString += matches.group(0)

    try:
        jsonString = json.loads(jsonString)
    except json.JSONDecodeError as e:
        if logger:
            logger.append(
                f"Error parsing extract Task Manager output JSON: {e}"
            )
            logger.append(
                "Checking for valid JSON in previous Task Manager messages"
            )

        # Parse through TaskManager messages if JSON format fails
        messages = user_proxy._oai_messages.values()
        tm_messages = [
            message
            for messages_list in messages
            for message in messages_list
            if message.get("name") == "TaskManager"
        ]

        tm_messages.reverse()

        for idx, message in enumerate(tm_messages):
            msg_content = message["content"]
            msg_content = msg_content.replace("\n", "")
            matches = re.search(pattern, msg_content, re.MULTILINE)

            jsonStringInternal = ""

            if matches:
                jsonStringInternal += matches.group(0)
            try:
                msg_json = json.loads(jsonStringInternal)
                if logger:
                    logger.append(
                        f"Found the valid JSON at TaskManager message {idx}"
                    )
                return msg_json
            except json.JSONDecodeError as e:
                if logger:
                    logger.append(
                        f"Error parsing JSON from TaskManager message {idx}: {e}"
                    )
                continue

        return AUTOGEN_RERUN_CONDITION

    return jsonString
