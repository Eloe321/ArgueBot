import random

class WouldYouRatherGame:
    def __init__(self):
        self.questions = [
            {"option_a": "be able to fly", "option_b": "be able to read minds"},
            {"option_a": "have unlimited money", "option_b": "have unlimited time"},
            {"option_a": "be invisible", "option_b": "be super strong"},
            {"option_a": "always be 10 minutes late", "option_b": "always be 20 minutes early"},
            {"option_a": "live in the past", "option_b": "live in the future"},
            {"option_a": "have a photographic memory", "option_b": "have an IQ of 200"},
            {"option_a": "win the lottery", "option_b": "live twice as long"},
            {"option_a": "speak all languages", "option_b": "be able to talk to animals"},
            {"option_a": "never have to sleep", "option_b": "never have to eat"},
            {"option_a": "be famous", "option_b": "be anonymous but rich"},
        ]

    def get_random_question(self):
        return random.choice(self.questions)