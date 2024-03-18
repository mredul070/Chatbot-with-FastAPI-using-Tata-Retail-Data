import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

class QueryPredictor:
    def __init__(self, model, tokenizer_input, tokenizer_output, max_len_input, max_len_output):
        self.model = model
        self.tokenizer_input = tokenizer_input
        self.tokenizer_output = tokenizer_output
        self.max_len_input = max_len_input
        self.max_len_output = max_len_output
    
    def predict_query(self, user_query):
        seq = self.tokenizer_input.texts_to_sequences([user_query])
        padded_seq = pad_sequences(seq, maxlen=self.max_len_input, padding='post')
        pred = self.model.predict(padded_seq)[0]
        idxs = np.argmax(pred, axis=-1)
        predicted_query = self.tokenizer_output.sequences_to_texts([idxs])[0]
        return predicted_query

if __name__ == "__main__":

    query_predictor = QueryPredictor(model, tokenizer_input, tokenizer_output, max_len_input, max_len_output)
    sample_query = "Where is my product now, My product ID 123"
    predicted_postgres_query = query_predictor.predict_query(sample_query)
    print("Predicted PostgreSQL Query:", predicted_postgres_query)
