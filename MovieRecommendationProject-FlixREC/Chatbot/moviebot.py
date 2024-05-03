from transformers import BertForSequenceClassification, BertTokenizerFast
from transformers import pipeline
import os 
import json 

default_responses = {}

# loading intents 
def load_default_responses():
    intents_file = 'chatbot/intents.json'
    intents = None; 
    try:
        with open(intents_file) as file:
            intents = json.load(file)
    except Exception as e:
        raise Exception('No file named "intents.json" found.') from e
    

    for intent in intents['intents']:
            default_responses[intent['tag']] = intent['responses']

def load():
    ############## LOAD MODEL ###################
    MODEL_PATH = r"chatbot/data"
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer= BertTokenizerFast.from_pretrained(MODEL_PATH)
    global chatbot
    chatbot = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    load_default_responses()

def get_default_responses(): 
     return default_responses

def get_label(user_text):
    '''
    Gets the action label of the given text
    '''
    user_text = user_text.lower().strip()
    label, score = chatbot(user_text)[0].values() 
    if(score < .7):
        return "unknown"
    else: 
        return label

