from .base import BaseMapper
from fuzzywuzzy import fuzz


class FuzzMapper(BaseMapper):
    """
    Map API 1 to API 2 using fuzzy string matching.
    """

    def __init__(self, api1, api2):
        """
        Initialize the FuzzMapper class.

        This function initializes the FuzzMapper class with two APIs.

        Parameters:
            api1: api1 from api_formatter
            api2: api2 from api_formatter

        Returns: None
        """
        super().__init__(api1, api2)
        self.max_similarity = 50

    def calculate_similarity(self, attr1, attr2):
        """
        Calculate similarity between two strings.

        This function calculates the similarity between two strings using the
        fuzzywuzzy library.

        Parameters:
            attr1: first string, typically an attribute name
            attr2: second string, typically an attribute name

        Returns: similarity between the two strings
        """
        return fuzz.ratio(attr1.lower(), attr2.lower())

    def map(self):
        """
        (Deprecated) Map two APIs using fuzzy string matching.

        This function maps two APIs using fuzzy string matching. It returns two
        dictionaries, one mapping from API 1 to API 2 and the other mapping
        from API 2 to API 1.
        """
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
