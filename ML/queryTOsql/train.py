import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

class DataLoader:
    def __init__(self, filename):
        self.filename = filename
    
    def load_data(self):
        data = pd.read_csv(self.filename)
        queries = data['user_query'].tolist()
        postgres_queries = data['postgres_query'].tolist()
        return queries, postgres_queries
    
    def preprocess_data(self, queries, postgres_queries):
        tokenizer_input = Tokenizer()
        tokenizer_output = Tokenizer()
        tokenizer_input.fit_on_texts(queries)
        tokenizer_output.fit_on_texts(postgres_queries)
        
        X = tokenizer_input.texts_to_sequences(queries)
        y = tokenizer_output.texts_to_sequences(postgres_queries)
        
        max_len_input = max(len(seq) for seq in X)
        max_len_output = max(len(seq) for seq in y)
        
        X = pad_sequences(X, maxlen=max_len_input, padding='post')
        y = pad_sequences(y, maxlen=max_len_output, padding='post')
        
        return tokenizer_input, tokenizer_output, X, y, max_len_input, max_len_output

class ModelBuilder:
    def __init__(self, max_len_input, input_vocab_size, max_len_output, output_vocab_size):
        self.max_len_input = max_len_input
        self.input_vocab_size = input_vocab_size
        self.max_len_output = max_len_output
        self.output_vocab_size = output_vocab_size
    
    def build_model(self):
        model = Sequential([
            Embedding(self.input_vocab_size, 256, input_length=self.max_len_input, mask_zero=True),
            LSTM(256),
            Dense(self.output_vocab_size, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

class Trainer:
    def __init__(self, model):
        self.model = model
    
    def train(self, X_train, y_train, X_val, y_val):
        early_stopping = EarlyStopping(patience=5, restore_best_weights=True)
        history = self.model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50, batch_size=32, callbacks=[early_stopping])
        return history

class Evaluator:
    def __init__(self, model):
        self.model = model
    
    def evaluate(self, X_val, y_val):
        loss, accuracy = self.model.evaluate(X_val, y_val)
        return loss, accuracy

class Plotter:
    def plot_history(self, history):
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Val Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    data_loader = DataLoader('your_dataset.csv')
    queries, postgres_queries = data_loader.load_data()
    tokenizer_input, tokenizer_output, X, y, max_len_input, max_len_output = data_loader.preprocess_data(queries, postgres_queries)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model_builder = ModelBuilder(max_len_input, tokenizer_input.num_words + 1, max_len_output, tokenizer_output.num_words + 1)
    model = model_builder.build_model()

    trainer = Trainer(model)
    history = trainer.train(X_train, y_train, X_val, y_val)


    evaluator = Evaluator(model)
    loss, accuracy = evaluator.evaluate(X_val, y_val)
    print("Model Loss:", loss)
    print("Model Accuracy:", accuracy)


    plotter = Plotter()
    plotter.plot_history(history)

