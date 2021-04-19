from flask import Blueprint, render_template, request, flash, jsonify
import json

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

@views.route('/modal', methods=['GET'])
def modal():
             
    #return request.args['data']
    return jsonify(id =2 , result = request.args['data'])
