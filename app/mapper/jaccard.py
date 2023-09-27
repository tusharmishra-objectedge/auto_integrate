from .base import BaseMapper

class JaccardSimilarityMapper(BaseMapper):
    
    def __init__(self, api1, api2):
        super().__init__(api1, api2)
        self.similarity_threshold = 0.5
    
    def calculate_similarity(self, attr1, attr2):
        set1 = set(attr1.lower())
        set2 = set(attr2.lower())
        return len(set1.intersection(set2)) / len(set1.union(set2))
    
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
    
            if max_similarity >= self.similarity_threshold and data_type1 == self.api2[matching_attr]:
                l2r_mapping[attr1] = matching_attr
                r2l_mapping[matching_attr] = attr1
    
        return l2r_mapping, r2l_mapping