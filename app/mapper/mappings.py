from mapper.fuzzy import FuzzMapper
from mapper.jaccard import JaccardSimilarityMapper

def mappings(api1, api2, manual_L2R, manual_R2L):
    print(f"\n API 1: {api1}\n")
    print(f"API 2: {api2}\n")

    print("Mapping API 1 to API 2 ...\n")
    print("Manual mapping ...\n")
    print(f"L2R: \n {manual_L2R}\n")
    print(f"R2L: \n {manual_R2L}\n")

    print("Fuzzy mapping ...\n")
    fuzz_mapper = FuzzMapper(api1, api2)
    l2r_mapping, r2l_mapping = fuzz_mapper.map()
    print(f"L2R: \n {l2r_mapping}\n")
    print(f"R2L: \n {r2l_mapping}\n")

    print("Jaccard mapping ...\n")
    jaccard_mapper = JaccardSimilarityMapper(api1, api2)
    l2r_mapping, r2l_mapping = jaccard_mapper.map()
    print(f"L2R: \n {l2r_mapping}\n")
    print(f"R2L: \n {r2l_mapping}\n")

