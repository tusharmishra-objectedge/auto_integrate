from .base import BaseMapper
from fuzzywuzzy import fuzz


class FuzzMapper(BaseMapper):
    def __init__(self, api1, api2):
        super().__init__(api1, api2)
        self.max_similarity = 50

    def calculate_similarity(self, attr1, attr2):
        return fuzz.ratio(attr1.lower(), attr2.lower())

    def map(self):
        l2r_mapping = {}
        r2l_mapping = {}

        for attr1, data_type1 in self.api1.items():
            max_similarity = -1
            matching_attr = None

            for attr2, data_type2 in self.api2.items():
                similarity = self.calculate_similarity(attr1, attr2)
                if similarity > max_similarity:
                    max_similarity = similarity
                    matching_attr = attr2

            if (
                max_similarity >= self.max_similarity
                and data_type1 == self.api2[matching_attr]
            ):
                l2r_mapping[attr1] = matching_attr
                r2l_mapping[matching_attr] = attr1

        return l2r_mapping, r2l_mapping
