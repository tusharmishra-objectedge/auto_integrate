import logging

from auto_integrate_cli.mapper.fuzzy import FuzzMapper
from auto_integrate_cli.mapper.jaccard import JaccardSimilarityMapper
from auto_integrate_cli.mapper.openai import OpenAIAPIMapper
from auto_integrate_cli.mapper.llama2_13b_chat import LLama2Mapper
from auto_integrate_cli.mapper.autogen import AutogenMapper

from auto_integrate_cli.settings.default import (
    AUTOGEN_RERUN_CONDITION,
    AUTOGEN_RERUN_LIMIT,
)


def map_fuzzy(api1, api2):
    """
    (Deprecated) Map API 1 to API 2 using fuzzy string matching.

    Note: This function is not used in the current version.
    """
    fuzz_mapper = FuzzMapper(api1, api2)
    l2r_mapping, r2l_mapping = fuzz_mapper.map()
    return {
        "type": "fuzzy",
        "L2R": l2r_mapping,
        "R2L": r2l_mapping,
    }


def map_jaccard(api1, api2):
    """
    (Deprecated) Map API 1 to API 2 using Jaccard similarity.

    Note: This function is not used in the current version.
    """
    jaccard_mapper = JaccardSimilarityMapper(api1, api2)
    l2r_mapping, r2l_mapping = jaccard_mapper.map()
    return {
        "type": "jaccard",
        "L2R": l2r_mapping,
        "R2L": r2l_mapping,
    }


def map_openai(api1, api2, engine="text-davinci-003"):
    """
    (Deprecated) Map API 1 to API 2 using OpenAI API.

    Note: This function is not used in the current version.
    """
    openai_mapper = OpenAIAPIMapper(api1, api2)
    return {
        "type": f"openai_{engine}",
        "mapped": openai_mapper.map(engine=engine),
    }


def map_llama2(api1, api2):
    """
    (Deprecated) Map API 1 to API 2 using LLama2.

    Note: This function is not used in the current version.

    Parameters:
        api1: api1 from api_formatter
        api2: api2 from api_formatter

    Returns:
        output_obj: output object containing the mappings
    """
    llama2_mapper = LLama2Mapper(api1, api2)
    return {
        "type": "llama2",
        "mapped": llama2_mapper.map(),
    }


def map_autogen(api1, api2):
    """
    Map API 1 to API 2 using Autogen AI multi-agent conversational framework.

    This function runs upto AUTOGEN_RERUN_LIMIT times, which value is defined
    in settings.default.py. If AUTOGEN_RERUN_CONDITION is not met, then it
    returns None. Otherwise, it returns the result of the mapping.

    Parameters:
        api1: api1 from api_formatter
        api2: api2 from api_formatter

    Returns:
        None or result of the mapping
    """
    logging.info("Starting autogen mapper")
    autogen_mapper = AutogenMapper(api1, api2)
    runs = 0
    result = None

    while runs < AUTOGEN_RERUN_LIMIT:
        logging.info(f"Starting autogen mapping run {runs}")
        print()
        print(f"----- STARTING AUTOGEN RUN {runs} -----")
        print()
        result = autogen_mapper.map()
        if result != AUTOGEN_RERUN_CONDITION:
            logging.info(f"Autogen mapping run {runs} successful")
            break
        else:
            logging.critical(f"Autogen mapping run {runs} failed")

        runs += 1

    return {
        "type": "autogen",
        "mapped": result,
    }


def mappings(api1, api2, manual_L2R=None, manual_R2L=None):
    """
    Map API 1 to API 2

    This function uses multiple available classes to map API 1 to API 2.

    Note: This function is not used in the current version.

    Parameters:
        api1: api1 from api_formatter
        api2: api2 from api_formatter
        manual_L2R: manually mapped L2R mapping
        manual_R2L: manually mapped R2L mapping

    Returns:
        output_obj: output object containing the mappings
    """
    output_obj = {}
    output_obj["api1"] = api1
    output_obj["api2"] = api2
    output_obj["mappings"] = []
    if manual_L2R and manual_R2L:
        output_obj["mappings"].append(
            {
                "type": "manual",
                "L2R": manual_L2R,
                "R2L": manual_R2L,
            }
        )
    output_obj["mappings"].append(map_autogen(api1, api2))
    return output_obj
