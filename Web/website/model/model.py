import keras.models
import joblib

from keras.models import model_from_json
#Pipelines
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer

from sklearn.pipeline import Pipeline


def init(): 
	# Load the model
	estimator = model_from_json(open('website/model/model_architecture.json','r').read())
	estimator.load_weights('website/model/model_weights.h5')

	# Load Column Transformer 
	column_transformer = joblib.load('website/model/columnTransformer')

	METRICS = [ 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
]
	estimator.compile(loss='binary_crossentropy', optimizer='sgd', metrics = METRICS)
	pipe = Pipeline(steps=[
    ('preprocessing',column_transformer),
    ('classifier',estimator)])

	
	return pipe