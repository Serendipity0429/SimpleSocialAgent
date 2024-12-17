import random

class PersonalityGenerator(object):
    def __init__(self):
        pass
    
    def generate_traits(self, is_random=True):
        self.personality_traits = {
                "openness": 0.5,
                "conscientiousness": 0.5,
                "extraversion": 0.5,
                "agreeableness": 0.5,
                "neuroticism": 0.5
            }
        if is_random:
            for trait in self.personality_traits:
                self.personality_traits[trait] = random.random()
        return self.personality_traits
        