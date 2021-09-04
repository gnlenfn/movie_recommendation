import numpy as np
from datetime import datetime
import os
import tensorflow as tf
from tensorflow.keras import models,layers, optimizers, losses, metrics
from tensorflow.keras.callbacks import EarlyStopping

# create model
def create_model():
        model = models.Sequential()
        model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        return model


if __name__ == "__main__":
        time = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')

        # data load
        X_train = np.load("./data/X_train.npy")
        X_test = np.load("./data/X_test.npy")
        y_train = np.load("./data/y_train.npy")
        y_test = np.load("./data/y_test.npy")


        # callbacks
        checkpoint_path = './checkpoints/training_checkpoints_{epoch:02d}_baseline.hdf5'
        checkpoint_dir = os.path.dirname(checkpoint_path)# Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                        save_weights_only=True,
                                        save_best_only=True,
                                        verbose=1)
        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience = 10)
        csv_logger = tf.keras.callbacks.CSVLogger(f'./log/baseline_{time}_log.csv', append=True, separator=';')

        # model compile
        model = create_model()
        model.compile(optimizer=optimizers.RMSprop(lr=0.001),
                loss=losses.binary_crossentropy,
                metrics=[metrics.binary_accuracy])

        # model training and test
        model.fit(X_train, y_train, epochs=30, 
                batch_size=512, validation_split=0.2, 
                callbacks=[es, cp_callback,csv_logger])

        results = model.evaluate(X_test, y_test)
        print(results)