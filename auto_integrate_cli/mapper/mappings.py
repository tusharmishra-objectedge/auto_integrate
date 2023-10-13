from auto_integrate_cli.mapper.fuzzy import FuzzMapper
from auto_integrate_cli.mapper.jaccard import JaccardSimilarityMapper


def mappings(api1, api2, manual_L2R=None, manual_R2L=None):
    """
    Map API 1 to API 2

    This function uses multiple available classes to map API 1 to API 2.
    The classes used are:
    - FuzzMapper: Uses fuzzy string matching
    - JaccardSimilarityMapper: Uses Jaccard similarity

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
    fuzz_mapper = FuzzMapper(api1, api2)
    l2r_mapping, r2l_mapping = fuzz_mapper.map()
    output_obj["mappings"].append(
        {
            "type": "fuzzy",
            "L2R": l2r_mapping,
            "R2L": r2l_mapping,
        }
    )
    jaccard_mapper = JaccardSimilarityMapper(api1, api2)
    l2r_mapping, r2l_mapping = jaccard_mapper.map()
    output_obj["mappings"].append(
        {
            "type": "jaccard",
            "L2R": l2r_mapping,
            "R2L": r2l_mapping,
        }
    )
    return output_obj
