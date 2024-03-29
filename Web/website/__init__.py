from flask import Flask

#system level operations (like loading files)
#import sys 
#for reading operating system data
#import os
#tell our app where our saved model is
#sys.path.append(os.path.abspath("./model"))

# from website.model.model import *
# m = init()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0     #without cache
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    # from website.model.model import init
    # model = init()
    
    from .views import views,apiend
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(apiend, url_prefix='/api')

    return app