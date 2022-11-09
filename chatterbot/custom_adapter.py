import json
import random
import re
import struct
from abc import ABCMeta, abstractmethod
from typing import List

import requests as requests
from chatterbot.conversation import Statement
from chatterbot.logic import LogicAdapter


class MyAdapter(LogicAdapter, metaclass=ABCMeta):
    @property
    @abstractmethod
    def pattern(self) -> re.Pattern:
        pass

    @property
    @abstractmethod
    def keywords(self) -> List[str]:
        pass

    def can_process(self, statement: Statement):
        return self.pattern.findall(statement.text)

    @abstractmethod
    def process(self, input_statement: Statement, additional_response_selection_parameters=None) -> Statement:
        pass

    def calculate_confidence(self, match: str, input_statement: Statement) -> float:
        match_index = len(match) / len(input_statement.text)
        keyword_index = self._contains_keyword(input_statement)
        return match_index * 0.4 + keyword_index * 0.6

    def _contains_keyword(self, input_statement: Statement):
        return any(
            keyword in [
                word.lower()
                for word in
                input_statement.text.split()
            ]
            for keyword
            in self.keywords
        )


class HexColorLogicAdapter(MyAdapter):
    pattern = re.compile(r'#([a-f\d]{6})', flags=re.IGNORECASE)
    keywords = ['hex', 'hexadecimal', 'color', 'colour', 'rgb']

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def process(self, input_statement: Statement, additional_response_selection_parameters=None):
        hex_number = self.pattern.findall(input_statement.text)[0]
        r, g, b = struct.unpack('BBB', bytes.fromhex(hex_number))

        text = 'RGB of your color is: Red: {}, Green: {}, Blue: {}'.format(r, g, b)
        response_statement = Statement(text=text)
        response_statement.confidence = self.calculate_confidence(hex_number, input_statement)

        return response_statement


class BinaryLogicAdapter(MyAdapter):
    pattern = re.compile(r'([01]{2,})', flags=re.IGNORECASE)
    keywords = ['binary', 'bin']

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def process(self, input_statement: Statement, additional_response_selection_parameters=None):
        binary = self.pattern.findall(input_statement.text)[0]
        text = f'Decimal value of {binary} is {int(binary, 2)}'

        response_statement = Statement(text=text)
        response_statement.confidence = self.calculate_confidence(binary, input_statement)

        return response_statement


class BiologyComplementaryLogicAdapter(MyAdapter):
    pattern = re.compile(r'([actg]{3,})', flags=re.IGNORECASE)
    keywords = ['gene', 'genes', 'genetic', 'genetics', 'code', 'sequence', 'complement', 'complementary']
    mapper = {
        ord('A'): 'U',
        ord('C'): 'G',
        ord('T'): 'A',
        ord('G'): 'C'
    }

    def replace(self, g):
        return ''.join(self.mapper[element] for element in g.group())

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def process(self, input_statement, additional_response_selection_parameters=None):
        codes: List[str] = self.pattern.findall(input_statement.text)
        text = ' '.join(
            code.translate(self.mapper)
            for code
            in codes
        )
        response_statement = Statement(text=text)
        response_statement.confidence = self.calculate_confidence(text, input_statement)

        return response_statement


class StandardConversationsAdapter(LogicAdapter):
    database = [
        [['hi', 'hello', 'cheers'], ['Welcome!', 'Bonjour!']],
        [['fuck', 'idiot', 'kys'], ["Don't say like that!", "It's not nice", "Apologize!"]],
        [['apologise', 'apologize', 'sorry'], ["Don't worry!", "That's okay!"]],
    ]

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.theme = None

    def can_process(self, input_statement: Statement):
        for i, line in enumerate(self.database):
            self.theme = i
            test = any(
                keyword in [
                    word.lower()
                    for word in
                    input_statement.text.split()
                ]
                for keyword
                in line[0]
            )
            if test:
                return True

    def process(self, statement, additional_response_selection_parameters=None):
        return Statement(text=random.choice(self.database[self.theme][1]))


class OutOfScopeAdapter(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.theme = None
        self.sid = '123123131'

    def can_process(self, input_statement: Statement):
        return True

    def rasa(self, text: str) -> str:
        payload = {
            "sender": str(self.sid),
            "message": text
        }

        try:
            request = requests.post('http://127.0.0.1:5005/webhooks/rest/webhook',
                                    data=json.dumps(payload))
            return request.json()[0]['text']
        except Exception:
            return "rasa connection failed"

    def process(self, input_statement, additional_response_selection_parameters=None):
        return Statement(text=self.rasa(input_statement.text))
