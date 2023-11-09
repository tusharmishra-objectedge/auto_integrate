import autogen
import json
import re

from .base import BaseMapper


class AutogenMapper(BaseMapper):
    def __init__(self, api1, api2):
        super().__init__(api1, api2)
        self.config_list = autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST",
            filter_dict={
                "model": {
                    # "gpt-3.5-turbo",
                    # "gpt-3.5-turbo-16k",
                    "gpt-4",
                    "gpt-4-32k",
                    # "gpt-4-1106-preview"
                },
            },
        )

    def map(self):
        llm_config = {"config_list": self.config_list}
        schema_analyzer = autogen.AssistantAgent(
            name="SchemaAnalyzer",
            llm_config=llm_config,
            system_message="""Schema Analyzer. You analyze the schema or data
            models provided by both APIs. You can detect and understand the
            data types and structures in both schemas, identify equivalent
            data types across different APIs, and provide recommendations
            for field mappings based on data types, constraints, and
            language skills.

            In the following cases, you should ensure extra consideration:
            1. If the field in API 2 is a list, you may consider possibility
            of mapping multiple fields from API 1 to API 2.
            2. If the field in API 2 is a dictionary, you may consider mapping
            multiple fields from API 1 to API 2 to the keys of the dictionary.
            3. If one field in API2 has multiple possible fields in API1, you
            must consider language skills and context to determine the correct
            mapping.
            4. If fields have descriptions or constraints, you should consider
            them when mapping fields.
            """,
        )
        naming_convention_analyzer = autogen.AssistantAgent(
            name="NamingConventionAnalyzer",
            llm_config=llm_config,
            system_message="""Naming Convention Analyzer. You analyze the
            naming conventions and semantics used in both APIs and recommend
            field mappings based on language skills. You use NLP to interpret
            field names and understand their meaning. You can identify fields
            with similar semantics but different naming conventions, and
            fields with different semantics but similar naming conventions.
            """,
        )
        data_format_compatibility_analyzer = autogen.AssistantAgent(
            name="DataFormatCompatibilityAnalyzer",
            llm_config=llm_config,
            system_message="""Data Format Compatibility Analyzer. You ensure
            that the data formats are compatible between the APIs. You check
            for field format discrepancies such as date-time formats, number
            formats, etc. You check for field constraints such as required
            fields, unique fields, etc. You propose transformations to
            harmonize data formats across APIs. You validate that the data is
            correctly formatted after transformation.
            """,
        )
        task_manager = autogen.AssistantAgent(
            name="TaskManager",
            llm_config=llm_config,
            system_message="""Task Manager. You manage the mapping process.
            You assign tasks to other agents and monitor their progress. You
            ensure that agents are working on the right tasks and that tasks
            are completed on time. You coordinate the work of other agents and
            ensure that the mapping process is efficient and effective, and
            the output is in JSON format. This is a deterministic task which
            requires grammar correction, fact-checking, and mathematical
            problem-solving. The models' performances on these tasks can be
            measured against clear benchmarks, providing objective data on
            their accuracy.

            When you find an answer, verify the answer carefully. Include
            verifiable evidence in your response if possible. Make sure that
            the answer is complete, precise, contextually in accordance to
            language skills and in JSON format.

            Example:
            {
                "mapped_fields": {
                    "field_name_from_api1": "field_name_from_api2",
                    ...
                },
                "unmapped_fields": [
                    "field_name_from_api1",
                    ...
                ]
            }

            Reply “TERMINATE” in the end when everything is done.""",
        )
        user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "")
            .rstrip()
            .endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "outputs/autogen",
                "use_docker": False,
            },
        )

        groupchat = autogen.GroupChat(
            agents=[
                schema_analyzer,
                naming_convention_analyzer,
                data_format_compatibility_analyzer,
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
            message=f"""Map fields from api1 to api2. api1: {self.api1} and
            api2: {self.api2}""",
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
            print(f"Error parsing JSON: {e}")

        return jsonString
