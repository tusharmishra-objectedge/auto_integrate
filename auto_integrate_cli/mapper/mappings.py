from auto_integrate_cli.mapper.fuzzy import FuzzMapper
from auto_integrate_cli.mapper.jaccard import JaccardSimilarityMapper
from auto_integrate_cli.mapper.openai import OpenAIAPIMapper
from auto_integrate_cli.mapper.llama2_13b_chat import LLama2Mapper
from auto_integrate_cli.mapper.autogen import AutogenMapper


def map_fuzzy(api1, api2):
    """
    Map API 1 to API 2 using fuzzy string matching
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
    Map API 1 to API 2 using Jaccard similarity
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
    Map API 1 to API 2 using OpenAI API
    """
    openai_mapper = OpenAIAPIMapper(api1, api2)
    return {
        "type": f"openai_{engine}",
        "mapped": openai_mapper.map(engine=engine),
    }


def map_llama2(api1, api2):
    """
    Map API 1 to API 2 using LLama2
    """
    llama2_mapper = LLama2Mapper(api1, api2)
    return {
        "type": "llama2",
        "mapped": llama2_mapper.map(),
    }


def map_autogen(api1, api2):
    """
    Map API 1 to API 2 using Autogen
    """
    autogen_mapper = AutogenMapper(api1, api2)
    return {
        "type": "autogen",
        "mapped": autogen_mapper.map(),
    }


def mappings(api1, api2, manual_L2R=None, manual_R2L=None):
    """
    Map API 1 to API 2

    This function uses multiple available classes to map API 1 to API 2.
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
