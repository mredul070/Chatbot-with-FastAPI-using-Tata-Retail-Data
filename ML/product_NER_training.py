import JSON
import spacy
import random
from spacy.training import Example

nlp = spacy.blank("en")


ner = nlp.add_pipe("ner", last=True)
ner.add_label("PRODUCT")


TRAIN_DATA = json.loads('NER_TRAINING.json')

nlp.begin_training()

for epoch in range(10):  
    random.shuffle(TRAIN_DATA)
    losses = {}
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], losses=losses)
    print("Epoch:", epoch, "Losses:", losses)


nlp.to_disk("custom_ner_model")
