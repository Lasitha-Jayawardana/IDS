from flask import Blueprint, render_template, request, flash, jsonify
import json
from io import StringIO
from website.model.model import init
import pandas as pd
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields
from http import HTTPStatus

global model
model1,model2 = init()


views = Blueprint('views', __name__)
apiend = Blueprint('apiend', __name__)

api = Api(app = apiend, 
		  version = "1.0", 
		  title = "Intrusion Prediction System", 
		  description = "Provide open source API functionality for Intrusion Detection",doc='/doc')




v1Namespace = api.namespace('v1', description='APIs which suppored for all KDD-NSL features')
v2Namespace = api.namespace('v2', description='APIs which suppored for subset of KDD-NSL features')

           

# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == 'POST':
#         note = request.form.get('note')

#         if len(note) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note, user_id=current_user.id)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')

#     return render_template("home.html", user=current_user)


 
@views.route('/')
def index():
    return render_template("index.html")

# @views.route('/<name>')
# def home(name):
#     return f"Hello{name}"

@views.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

v1model = v1Namespace.model('v1', { #error handling in response
    'id': fields.String(
        #readonly=True,
        description='Identifier for featureVec which was given as input'
    ),
    'result': fields.String(
        required=True,
        description='The predicted result'
    )
})

@v1Namespace.route("/")
class v1Class(Resource):
    @v1Namespace.doc(responses={ 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Identifier for the featureVec. It will return with results',
             'featureVec': '''Specify the features associated with the NSL-KDD dataset. 
             
Ex : 
duration , protocol_type , service , flag , src_bytes , dst_bytes , land , wrong_fragment , urgent , hot , num_failed_logins , logged_in , num_compromised , root_shell , su_attempted , num_root , num_file_creations , num_shells , num_access_files , num_outbound_cmds , is_host_login , is_guest_login , count , srv_count , serror_rate , srv_serror_rate , rerror_rate , srv_rerror_rate , same_srv_rate , diff_srv_rate , srv_diff_host_rate , dst_host_count , dst_host_srv_count , dst_host_same_srv_rate , dst_host_diff_srv_rate , dst_host_same_src_port_rate , dst_host_srv_diff_host_rate , dst_host_serror_rate , dst_host_srv_serror_rate , dst_host_rerror_rate , dst_host_srv_rerror_rate' '''})

    @v1Namespace.marshal_with(v1model) #validity check with response format as v1model
    #@v1Namespace.expect(v1model, validate=True) #validate inputs with v1model
    def get(self):
        '''Api version 1 endpoint'''
        try:
            cc = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes','dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell','su_attempted', 'num_root', 'num_file_creations', 
    'num_shells','num_access_files', 'num_outbound_cmds', 'is_host_login','is_guest_login', 'count', 'srv_count', 
    'serror_rate','srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate','diff_srv_rate', 'srv_diff_host_rate', 
    'dst_host_count','dst_host_srv_count', 'dst_host_same_srv_rate','dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate','dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate']

            str_data = StringIO(request.args['featureVec'])
            df_tt = pd.read_csv(str_data,sep=",",names=cc)

            test_predictions = model1.predict(df_tt)
            #print('Predicted value : ',test_predictions)
            

            if test_predictions>0.5:
                output = 'Anomaly'
            else:
                output = 'Normal'
                    
            #print('Status : ',output)
                
            #return request.args['data']
            return {
                'id': request.args['id'],
                'result': output
            }
            #return jsonify(id =request.args['id'] , result = output)
                    
        except KeyError as e:
            v1Namespace.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
            
        except Exception as e:
            v1Namespace.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

v2model = v1Namespace.model('v2', { #error handling in response
    'id': fields.String(
        #readonly=True,
        description='Identifier for featureVec which was given as input'
    ),
    'result': fields.String(
        required=True,
        description='The predicted result'
    )
})

@v2Namespace.route("")
class v2Class(Resource):
    @v2Namespace.doc(responses={ 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Identifier for the featureVec. It will return with results',
             'featureVec': '''Specify the features associated with subset of the NSL-KDD dataset which are shown below.
             
Ex : 
duration, protocol_type , service ,flag , src_bytes , dst_bytes , land , wrong_fragment , urgent , count , srv_count , serror_rate , srv_serror_rate , rerror_rate , srv_rerror_rate , same_srv_rate , diff_srv_rate , srv_diff_host_rate , dst_host_count , dst_host_srv_count , dst_host_same_srv_rate , dst_host_diff_srv_rate , dst_host_same_src_port_rate , dst_host_srv_diff_host_rate , dst_host_serror_rate , dst_host_srv_serror_rate , dst_host_rerror_rate , dst_host_srv_rerror_rate ''' })

    @v2Namespace.marshal_with(v2model) #validity check with response format as v1model
    #@v1Namespace.expect(v1model, validate=True) #validate inputs with v1model
    def get(self):
        '''Api version 2 endpoint'''
        try:
            cc = ['duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent',
                'count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate',
                'diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count','dst_host_same_srv_rate',
                'dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate',
                'dst_host_srv_serror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate']

            str_data = StringIO(request.args['featureVec'])
            df_tt = pd.read_csv(str_data,sep=",",names=cc)

            test_predictions = model2.predict(df_tt)
            #print('Predicted value : ',test_predictions)
            

            if test_predictions>0.5:
                output = 'Anomaly'
            else:
                output = 'Normal'
                    
            #print('Status : ',output)
                
            #return request.args['data']
            return {
                'id': request.args['id'],
                'result': output
            }
            #return jsonify(id =request.args['id'] , result = output)
                    
        except KeyError as e:
            v2Namespace.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
            
        except Exception as e:
            v2Namespace.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")




# @views.route('/predict', methods=['GET'])
# def predict():
#     cc = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes','dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
#     'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell','su_attempted', 'num_root', 'num_file_creations', 
#     'num_shells','num_access_files', 'num_outbound_cmds', 'is_host_login','is_guest_login', 'count', 'srv_count', 
#     'serror_rate','srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate','diff_srv_rate', 'srv_diff_host_rate', 
#     'dst_host_count','dst_host_srv_count', 'dst_host_same_srv_rate','dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
#     'dst_host_srv_diff_host_rate', 'dst_host_serror_rate','dst_host_srv_serror_rate', 'dst_host_rerror_rate',
#     'dst_host_srv_rerror_rate']
    
#     str_data = StringIO(request.args['data'])
#     df_tt = pd.read_csv(str_data,sep=",",names=cc)

#     test_predictions = model.predict(df_tt)
#     #print('Predicted value : ',test_predictions)
    

#     if test_predictions>0.5:
#         output = 'Anomaly'
#     else:
#         output = 'Normal'
            
#     #print('Status : ',output)
         
#     #return request.args['data']
#     return jsonify(id =request.args['id'] , result = output)
