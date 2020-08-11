import tensorflow as tf
import numpy as np
import os
import time
import json
import re

params = {}

BATCH_SIZE = 8
BUFFER_SIZE = 10000

#path_to_file = tf.keras.utils.get_file('shakespeare.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
path_to_file = '/Users/yoelkastro/Desktop/writeAI/data.txt'

text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
text = re.sub("[^\w]", " ",  text).split()

vocab = sorted(set(text))

params['vocab'] = vocab

char2id= {u:i for i, u in enumerate(vocab)}
id2char = np.array(vocab)

idText = np.array([char2id[c] for c in text])

seqLength = 5
examplesPerEpoch = len(text) // (seqLength + 1)

charDataset = tf.data.Dataset.from_tensor_slices(idText)

seqs = charDataset.batch(seqLength + 1, drop_remainder=True)

def splitTargetInput(chunk):
	inputText = chunk[:-1]
	targetText = chunk[1:]
	return inputText, targetText

dataset = seqs.map(splitTargetInput).shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder = True)

embeddingDim = 256
rnnUnits = 1024

def buildModel(vocabSize, embeddingDim, rnnUnits, batchSize):
	model = tf.keras.Sequential([
		tf.keras.layers.Embedding(vocabSize, embeddingDim, batch_input_shape=[batchSize, None]),
		tf.keras.layers.GRU(rnnUnits, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
		tf.keras.layers.Dense(vocabSize)
	])
	return model

model = buildModel(len(vocab), embeddingDim, rnnUnits, BATCH_SIZE)

params['batch_size'] = BATCH_SIZE
params['embedding_dim'] = embeddingDim
params['rnn_units'] = rnnUnits
params['vocab_size'] = len(vocab)

with open('/Users/yoelkastro/Desktop/writeAI/paramsWord.json', 'w') as outfile:
    json.dump(params, outfile)

def loss(labels, logits):
	return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits = True)

model.compile(optimizer='adam', loss=loss)

checkpointDir = '/Volumes/Elements/trainingCheckpointsWord'
checkpointPre = os.path.join(checkpointDir, 'chkp_{epoch}')

checkpointCallback = tf.keras.callbacks.ModelCheckpoint(
	filepath = checkpointPre,
	save_weights_only=True,
	save_freq=100
	)

EPOCHS = 10000
history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpointCallback], steps_per_epoch=10)
