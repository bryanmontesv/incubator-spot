if __name__=='__main__':
    import sys
    from os import path

    sys.path.append(path.dirname(__file__))

from flask import Flask, Blueprint
from flask_graphql import GraphQLView
import os

from schema import OscSchema

app = Flask(__name__)

blueprint = Blueprint('osc_api', __name__)
blueprint.add_url_rule('/osc', strict_slashes=False, view_func=GraphQLView.as_view('osc', schema=OscSchema, graphiql=os.environ.get('SPOT_DEV') == '1'))

app.register_blueprint(blueprint)

if __name__=='__main__':
    port = int(sys.argv[1]) if len(sys.argv)>1 else 8889

    app.run(host='0.0.0.0', port=port)

def load_jupyter_server_extension(nb_app):
    import tornado.web
    import tornado.wsgi
    print ('Plugin is loading')
    from populate_options import populateWidget
    populateWidget()

    wsgi_app = tornado.wsgi.WSGIContainer(app)
    nb_app.web_app.add_handlers(r'.*', [
        (r'/osc.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))
    ])

    nb_app.log.info('Apache Spot osc extension loaded')
    if os.environ.get('SPOT_DEV')=='1':
        nb_app.log.warn('Apache Spot osc running in dev mode (environment var SPOT_DEV=1)')
