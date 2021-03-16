from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Chatterbot',
trainer='chatterbot.trainers.CorpusTrainer', 
storage_adapter='chatterbot.storage.SQLStorageAdapter',
database_uri='sqlite:///database.db')

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train("TrainingDocs/intents.yml")
# trainer.train(
#     "chatterbot.corpus.english.greetings",
#     #"chatterbot.corpus.bangla.botprofile",
#     #"chatterbot.corpus.buses.route3",
#     #"chatterbot.corpus.buses.broute",
#     "chatterbot.corpus.english.conversations",

# )