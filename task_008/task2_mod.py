# task 2
#V5
#text = 'AT Course 2024'


class StringOperations:
    @staticmethod
    def get_length(text):
        return len(text)

    @staticmethod
    def get_substring(text, start, end):
        return text[start:end]

    @staticmethod
    def find_index(text, substring):
        return text.index(substring)

    @staticmethod
    def convert_to_upper(text):
        return text.upper()

    @staticmethod
    def convert_to_lower(text):
        return text.lower()

