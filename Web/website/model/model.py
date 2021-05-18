import keras.models
import joblib

from keras.models import model_from_json
#Pipelines
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

from sklearn.pipeline import Pipeline


def init(): 
	# Load the model
	estimatorv1 = model_from_json(open('website/model/v1model_architecture.json','r').read())
	estimatorv1.load_weights('website/model/v1model_weights.h5')

	# Load Column Transformer 
	column_transformerv1 = joblib.load('website/model/v1columnTransformer')

	METRICS = [ 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
]
	estimatorv1.compile(loss='binary_crossentropy', optimizer='sgd', metrics = METRICS)
	pipev1 = Pipeline(steps=[
    ('preprocessing',column_transformerv1),
    ('classifier',estimatorv1)])



# Load the model v2
	estimatorv2 = model_from_json(open('website/model/v2model_architecture.json','r').read())
	estimatorv2.load_weights('website/model/v2model_weights.h5')

	# Load Column Transformer 
	column_transformerv2 = joblib.load('website/model/v2columnTransformer')

	METRICS = [ 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
]
	estimatorv2.compile(loss='binary_crossentropy', optimizer='sgd', metrics = METRICS)
	pipev2 = Pipeline(steps=[
    ('preprocessing',column_transformerv2),
    ('classifier',estimatorv2)])
	
	return pipev1, pipev2