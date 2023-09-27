# from fuzzywuzzy import fuzz

def calculate_jaccard_similarity(attr1, attr2):
    set1 = set(attr1.lower())
    set2 = set(attr2.lower())
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return intersection / union if union != 0 else 0

def map_attributes(api1, api2, similarity_threshold=0.8):
    l2r_mapping = {}
    r2l_mapping = {}

    for attr1, data_type1 in api1.items():
        max_similarity = -1
        matching_attr = None

        for attr2, data_type2 in api2.items():
            similarity = calculate_jaccard_similarity(attr1, attr2)
            if similarity > max_similarity:
                max_similarity = similarity
                matching_attr = attr2

        if max_similarity >= similarity_threshold and data_type1 == api2[matching_attr]:
            l2r_mapping[attr1] = matching_attr
            r2l_mapping[matching_attr] = attr1

    return l2r_mapping, r2l_mapping

api1 = {'fullName': 'str', 'emergencyContactNumber': 'str', 'DoB': 'str', 'city': 'str', 'state': 'str', 'street': 'str', 'score': 'int', 'honorStudent': 'bool', 'created': 'str', 'id': 'str'}

api2 = {'createdAt': 'str', 'name': 'str', 'dateOfBirth': 'str', 'address': 'str', 'state': 'str', 'city': 'str', 'honors': 'bool', 'grade': 'int', 'emergencyContact': 'str', 'id': 'str'}

l2r_mapping, r2l_mapping = map_attributes(api1, api2)

print("L2R mapping:")
print(l2r_mapping)

print("\nR2L mapping:")
print(r2l_mapping)



