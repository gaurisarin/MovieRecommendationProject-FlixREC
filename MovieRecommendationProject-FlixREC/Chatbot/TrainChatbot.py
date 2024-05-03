# references: 
# https://www.kaggle.com/code/eyadgk/build-a-chatbot-with-bert-eda-vis/notebook

import pandas as pd
import json
import os 

from sklearn.model_selection import train_test_split

from transformers import BertForSequenceClassification
from transformers import BertTokenizer
from transformers import TrainingArguments, Trainer

import torch
from torch.utils.data import Dataset

def load_intents():
    '''
    Loads the intents.json file into a dataframe
    Returns:
        df: pd.DataFrame
    '''
    intents_file = 'chatbot/intents.json'
    intents = None; 
    try:
        with open(intents_file) as file:
            intents = json.load(file)
    except Exception as e:
        raise Exception('No file named "intents.json" found.') from e
    
    tup_intent = []
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            tup_intent.append((pattern, intent['tag']))
    
    return pd.DataFrame(tup_intent, columns =['Pattern', 'Tag'])

################ Preprocessing Data #########################
df = load_intents() 

# getting labels for the HuggingFace BERT model 
labels = list(df['Tag'].unique())
id2label = { id:label for (id,label) in list(enumerate(labels))} 
label2id = { label:id for (id,label) in list(enumerate(labels))} 


# Splitting into testing/ training using sklearn 
X = df['Pattern'].tolist()
y = [label2id[i] for i in df['Tag'].tolist()]
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state = 42)

# HuggingFace provides a tokenizer/embedding that is ideal for the pre-trained BERT model 
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", max_length=256)
train_encoding = tokenizer(X_train, truncation=True, padding=True)
test_encoding = tokenizer(X_test, truncation=True, padding=True)

# see pretrained models here: https://huggingface.co/transformers/v3.3.1/pretrained_models.html
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", 
                                                      num_labels=len(labels), 
                                                      id2label=id2label, 
                                                      label2id = label2id)

# pytorch dataloader 
class DataLoader(Dataset):
    
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataloader = DataLoader(train_encoding, y_train)
test_dataloader = DataLoader(test_encoding, y_test)

# HuggingFace Trainer 
training_args = TrainingArguments(
    output_dir='./output', 
    do_train=True,
    do_eval=True,
    num_train_epochs=100,              
    per_device_train_batch_size=32,  
    per_device_eval_batch_size=16,
    warmup_steps=100,                
    weight_decay=0.05,
    logging_strategy='steps',
    logging_dir='./multi-class-logs',            
    logging_steps=50,
    evaluation_strategy="steps",
    eval_steps=50,
    save_strategy="steps", 
    load_best_model_at_end=True
)
trainer = Trainer(
    model=model,
    args=training_args,                 
    train_dataset=train_dataloader,         
    eval_dataset=test_dataloader
)

######### Training #################
trainer.train()

######## Evaluation ################
print("Train set:")
print(trainer.evaluate(eval_dataset=train_dataloader))
print("Test set:")
print(trainer.evaluate(eval_dataset=test_dataloader))

########## Save Model ###############
model_path = "./data"
trainer.save_model(model_path)
tokenizer.save_pretrained(model_path)