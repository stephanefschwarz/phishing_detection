import pandas as pd
import numpy as np
import tensorflow

import tensorflow as tf
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
from keras.utils.np_utils import to_categorical

# To read paper https://arxiv.org/pdf/1901.08688.pdf
# Code based on https://github.com/cerlymarco/MEDIUM_NoteBook/blob/master/OneClass_NeuralNetwork/OneClass_NeuralNetwork.ipynb

class OnePhishi():
    """docstring for OneClassNN."""

    def __init__(self, input_shape:int, n_class:int=2, learning_rate:flaot=0.01):
        super(OneClassNN, self).__init__()

        self.model = oneClassNN(input_shape, n_class, learning_rate)

    def oneClassNN(self, input_shape, n_class, learning_rate):

        input_url_emb = Input(shape=self.input_shape)

        output = Dense(units=128, activation='relu')(input_url_emb)
        output = Dense(units=52, activation='relu')(output)
        output = Dense(units=self.n_class, activation='relu')(output)

        model = Model(inputs=input_url_emb, outputs=output)

        opt = Adam(learning_rate=self.learning_rate)

        return model.compile(optimizer=opt, loss='categorical_crossentropy',
                            metrics=['accuracy'])

# if __name__ == '__main__':
#
#     from sklearn.model_selection import train_test_split
#     from sklearn.metrics import confusion_matrix, accuracy_score
#
#     embs = np.load(ROOT_FOLDER + 'url_embeddings.npy')
#     labels = np.load(ROOT_FOLDER + 'url_embeddings_labels.npy')
#
#     X_train, X_test, y_train, y_test = train_test_split(embs, labels, test_size=0.20, random_state=42)
#
#     # Training with only safe URLs
#     X_train = X_train[y_train==0]
#     y_train = y_train[y_train ==0]
#
#     y_train = to_categorical(y_train, num_classes=2)
#     y_test = to_categorical(y_test, num_classes=2)
#
#     url_embed_shape = X_train.shape[1]
#     phishi_model = OneClassNN(input_shape=url_embed_shape)
#
#     model.fit(x=X_train, y=y_train, batch_size=100, epochs=3)
#
#     preds = model.predict(X_test)
#
#     confusion_matrix(np.argmax(y_test, axis=1), np.argmax(preds, axis=1))
