# Import the necessary libraries
import os
import numpy as np
from PIL import Image

from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Variables
classes = 43

# This function creates a model

def create_model(input_shape=(32, 32, 3), learning_rate=0.0001):
    model = models.Sequential([
        # Input layer
        layers.Input(shape=input_shape),

        # Convolutional layer 1
        layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),

        # Pooling layer 1
        layers.MaxPooling2D((2,2)),

        # Convolutional layer 2
        layers.Conv2D(64, (3,3), activation='relu', input_shape=input_shape),
        
        # Pooling layer 2
        layers.MaxPooling2D((2,2)),
        
        # Convolutional layer 3
        layers.Conv2D(128, (3,3), activation='relu', input_shape=input_shape),
        
        # Flatten layer
        layers.Flatten(),
        
        # Dense layer 1
        layers.Dense(256, activation='relu'),
        
        # Dropout layer
        layers.Dropout(0.5),
        
        # Dense layer 2
        layers.Dense(43, activation='softmax')
    ])

    # Optimizer
    optimizer = keras.optimizers.Adam(learning_rate)
    
    # Loss
    loss = keras.losses.CategoricalCrossentropy()

    # Compile model
    model.compile(optimizer=optimizer, 
                  loss=loss,
                  metrics=['accuracy']
    )

    return model

# This function resizes the images

def resize_images(size=(32, 32)):
    for i in range(classes):
        input_directory = f"./data/train/{i}"
        output_directory = f"./data/train-r/{i}"
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    
        for filename in os.listdir(input_directory):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
    
            try:
                with Image.open(input_path) as img:
                    img = img.resize(size)
                    img.save(output_path)
                    print(f"Resized and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

# This function prepares the dataset

def load_images():
    
    sign_images = []
    sign_indexes = []

    for i in range(classes):
        
        input_directory = f"./data/train-r/{i}"
        
        for filename in os.listdir(input_directory):
            input_path = os.path.join(input_directory, filename)

            try:
                with Image.open(input_path) as img:
                    sign_images.append(np.array(img))
                    sign_indexes.append(i)
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

    sign_images = np.array(sign_images)
    sign_indexes = np.array(sign_indexes)

    return sign_images, sign_indexes

# This function trains the model

def train_model():
    # Resize images
    resize_images(size=(32, 32))
    
    # Prepare the dataset
    sign_images, sign_indexes = load_images()

    # Split the dataset into train and validation
    X_train, X_val, y_train, y_val = train_test_split(sign_images, sign_indexes, test_size=0.2, random_state=42)

    # Change target variables to categorical
    y_train = to_categorical(y_train)
    y_val = to_categorical(y_val)

    # Create model
    model = create_model(input_shape=(32, 32, 3), learning_rate=0.0001)

    # Create a checkpoint to be used while training
    checkpoint_filepath = './model/traffic_sign_classification_model.h5'
    
    checkpoint = keras.callbacks.ModelCheckpoint (
        checkpoint_filepath,
        save_best_only=True,
        monitor="val_accuracy"
    )

    # Train model
    model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val), callbacks=[checkpoint])

# This is the initialization function

def init():
    # Check if model file (traffic_sign_classification_model.bin) already exists
    if os.path.exists('./model/traffic_sign_classification_model.h5'):
        print('Model file already exists. Exiting init function...')
        return

    # Model not trained yet so let's train it
    train_model()

if __name__ == "__main__":
    init()