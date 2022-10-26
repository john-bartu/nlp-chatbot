import os
import time

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

time.clock = time.time

# Clear database - fresh train
os.remove('db.sqlite3')

# Create a new chatbot named Charlie
chatbot = ChatBot(
    'Neo',
    logic_adapters=[
        {
            'import_path': 'custom_adapter.BinaryLogicAdapter'
        },
        {
            'import_path': 'custom_adapter.HexColorLogicAdapter'
        },
        {
            'import_path': 'custom_adapter.BiologyComplementaryLogicAdapter'
        },
        {
            'import_path': 'custom_adapter.StandardConversationsAdapter'
        },
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Could you repeat please?',
            'maximum_similarity_threshold': 0.9
        }
    ])

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot_corpus/train_basic.yml")


def ask(question):
    response = chatbot.get_response(question)
    print(f'> {question}\n{response}')


# ask('What is binary value for #010011?')
# ask('What is RGB value for #010011?')
# ask('Could you show complementary sequence for "ATG CTA AGC ATA"?')

while True:
    try:
        # os.system('clear')
        print("> ", end='')
        user_input = input()

        bot_response = chatbot.get_response(user_input)

        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
