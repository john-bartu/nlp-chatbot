import re
import struct

from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter


class HexColorLogicAdapter(LogicAdapter):
    pattern = re.compile(r'#([a-f\d]{6})', flags=re.IGNORECASE)

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement: Statement):
        return self.pattern.match(statement.text)

    def process(self, input_statement: Statement, additional_response_selection_parameters=None):
        hex_number = self.pattern.findall(input_statement.text)[0]
        r, g, b = struct.unpack('BBB', bytes.fromhex(hex_number))
        confidence = 0.0

        text = 'I see, you mention color in HEX! Red: {}, Green: {}, Blue: {}'.format(r, g, b)
        response_statement = Statement(text=text, confidence=confidence)

        return response_statement


class BinaryLogicAdapter(LogicAdapter):
    pattern = re.compile(r'([01]{2,})', flags=re.IGNORECASE)

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement: Statement):
        return self.pattern.match(statement.text)

    def process(self, input_statement: Statement, additional_response_selection_parameters=None):
        binary = self.pattern.findall(input_statement.text)[0]
        confidence = 0.0
        text = 'Gotcha! {}'.format(int(binary, 2))
        response_statement = Statement(text=text, confidence=confidence)

        return response_statement


class BiologyComplementaryLogicAdapter(LogicAdapter):
    pattern = re.compile(r'([actg]{3,})', flags=re.IGNORECASE)
    mapper = {
        'A': 'U',
        'C': 'G',
        'T': 'A',
        'G': 'C'
    }

    def replace(self, g):
        return ''.join(self.mapper[element] for element in g.group())

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return self.pattern.match(statement.text)

    def process(self, input_statement, additional_response_selection_parameters=None):
        text = self.pattern.sub(self.replace, input_statement.text)
        confidence = 0.0
        response_statement = Statement(text=text, confidence=confidence)

        return response_statement
