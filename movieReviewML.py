import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras import regularizers
import tensorflow_datasets as tfds
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download("stopwords")
nltk.download('wordnet')
import numpy as np

lem = WordNetLemmatizer()
stopwords = stopwords.words("english")
newstopwords = [',', '.', 'b', '<br /><br />', ]
stopwords.append(newstopwords)

def normalize(text, label):
    tokens = word_tokenize(text.decode("utf-8"))
    filtered = [word for word in tokens if word.lower() not in stopwords]
    lemmatized = [lem.lemmatize(word) for word in filtered]
    sentence = " ".join(lemmatized)
    return sentence, label

train_data, validation_data, test_data = tfds.load(
    name="imdb_reviews",
    split=('train[:80%]', 'train[80%:]', 'test'),
    as_supervised=True)

train_texts = np.array([text for text, _ in tfds.as_numpy(train_data)])
train_labels = np.array([label for _, label in tfds.as_numpy(train_data)])

val_texts = np.array([text for text, _ in tfds.as_numpy(validation_data)])
val_labels = np.array([label for _, label in tfds.as_numpy(validation_data)])

test_texts = np.array([text for text, _ in tfds.as_numpy(test_data)])
test_labels = np.array([label for _, label in tfds.as_numpy(test_data)])

vect = np.vectorize(normalize)
normalized_train_texts, normalized_train_labels = vect(train_texts, train_labels)
normalized_val_texts, normalized_val_labels = vect(val_texts, val_labels)
normalized_test_texts, normalized_test_labels = vect(test_texts, test_labels)

train_dataset = tf.data.Dataset.from_tensor_slices((normalized_train_texts, normalized_train_labels))
val_dataset = tf.data.Dataset.from_tensor_slices((normalized_val_texts, normalized_val_labels))
test_dataset = tf.data.Dataset.from_tensor_slices((normalized_test_texts, normalized_test_labels))

VOCAB_SIZE = 10000
encoder = tf.keras.layers.TextVectorization(max_tokens=VOCAB_SIZE)
encoder.adapt(train_dataset.map(lambda text, label: text))

model = tf.keras.Sequential([
    encoder,
    tf.keras.layers.Embedding(
        input_dim=len(encoder.get_vocabulary()),
        output_dim=64,
        mask_zero=True),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, activation='sigmoid', return_sequences=True)),
    tf.keras.layers.Conv1D(filters=64, kernel_size=3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(16, activation='relu', kernel_regularizer=regularizers.l1(0.01)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
              metrics=['accuracy'])

history = model.fit(x=normalized_train_texts,
                    y=normalized_train_labels,
                    epochs=3,
                    verbose=1,
                    validation_data=(normalized_val_texts, normalized_val_labels))

tf.saved_model.save(model, 'C:/Users/suhas/MovieReview')

test_loss, test_accuracy = model.evaluate(normalized_test_texts, normalized_test_labels)
print("Test Loss:", test_loss)
print("Test Accuracy:", test_accuracy)