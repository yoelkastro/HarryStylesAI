import tensorflow as tf
import numpy as np
import os
import time
import json

params = {}

with open('params.json') as js:
	data = json.load(js)

	params['batch_size'] = data['batch_size']
	params['embedding_dim'] = data['embedding_dim']
	params['rnn_units'] = data['rnn_units']
	params['vocab_size'] = data['vocab_size']
	params['vocab'] = data['vocab']


char2id= {u:i for i, u in enumerate(params['vocab'])}
id2char = np.array(params['vocab'])

def buildModel(vocabSize, embeddingDim, rnnUnits, batchSize):
	model = tf.keras.Sequential([
		tf.keras.layers.Embedding(vocabSize, embeddingDim, batch_input_shape=[batchSize, None]),
		tf.keras.layers.GRU(rnnUnits, return_sequences=True, stateful=True, recurrent_initializer='glorot_uniform'),
		tf.keras.layers.Dense(vocabSize)
	])
	return model


model = buildModel(params['vocab_size'], params['embedding_dim'], params['rnn_units'], 1)

checkpointDir = 'trainingCheckpoint'
checkpointPre = os.path.join(checkpointDir, 'chkp_{epoch}')

model.load_weights(tf.train.latest_checkpoint(checkpointDir))
model.build(tf.TensorShape([1, None]))

def generateText(model, startString):
	numGenerate=2000

	inputEval = [char2id[s] for s in startString]
	print(inputEval)
	inputEval = tf.expand_dims(inputEval, 0)

	textGenerated = []
	textGenerated.append(startString[0])

	temperature = 1.0 # Test

	model.reset_states()

	while(len(textGenerated) < numGenerate or textGenerated[-1] != '.'):
		predictions = model(inputEval)
		predictions = tf.squeeze(predictions, 0)

		predictions = predictions / temperature
		predictedId = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

		inputEval = tf.expand_dims([predictedId], 0)

		textGenerated.append(id2char[predictedId])

	return (''.join(textGenerated))

model.summary()

print(generateText(model, startString=u"H"))


#print(len(vocab))