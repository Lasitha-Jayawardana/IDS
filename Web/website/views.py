from flask import Blueprint, render_template, request, flash, jsonify
import json
from io import StringIO
from website.model.model import init
import pandas as pd

global model
model = init()


views = Blueprint('views', __name__)


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

@views.route('/<name>')
def home(name):
    return f"Hello{name}"

@views.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@views.route('/predict', methods=['GET'])
def predict():
    cc = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes','dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell','su_attempted', 'num_root', 'num_file_creations', 
    'num_shells','num_access_files', 'num_outbound_cmds', 'is_host_login','is_guest_login', 'count', 'srv_count', 
    'serror_rate','srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate','diff_srv_rate', 'srv_diff_host_rate', 
    'dst_host_count','dst_host_srv_count', 'dst_host_same_srv_rate','dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate','dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate']
    
    str_data = StringIO(request.args['data'])
    df_tt = pd.read_csv(str_data,sep=",",names=cc)

    test_predictions = model.predict(df_tt)
    #print('Predicted value : ',test_predictions)
    

    if test_predictions>0.5:
        output = 'Anomaly'
    else:
        output = 'Normal'
            
    #print('Status : ',output)
         
    #return request.args['data']
    return jsonify(id =request.args['id'] , result = output)
