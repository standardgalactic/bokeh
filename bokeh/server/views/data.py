from flask import jsonify, request
from werkzeug.utils import secure_filename
import json

from ..app import bokeh_app
from ..views import make_json
from ... import protocol
from ..crossdomain import crossdomain


@bokeh_app.route("/bokeh/data/<username>", methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", headers=['BOKEH-API-KEY', 'Continuum-Clientid'])
def list_sources(username):
    bokehuser = bokeh_app.authentication.current_user()
    request_username = bokehuser.username
    sources = bokeh_app.datamanager.list_data_sources(request_username, 
                                                      username)
    return jsonify(sources=sources)

    
@bokeh_app.route("/bokeh/data/<username>/<path:data_url>", methods=['GET', 'OPTIONS'])
@crossdomain(origin="*", headers=['BOKEH-API-KEY', 'Continuum-Clientid'])
def get_data(username, data_url):
    bokehuser = bokeh_app.authentication.current_user()
    request_username = bokehuser.username
    #handle docid later...
    parameters = json.loads(request.values.get('resample_parameters'))
    plot_size = json.loads(request.values.get('plot_size'))
    result = bokeh_app.datamanager.get_data(request_username, None, data_url, parameters, plot_size)
    result = make_json(protocol.serialize_json(result))
    return result


@bokeh_app.route("/bokeh/data/upload/<username>/<name>", methods=['POST'])
def upload(username, name):
    bokehuser = bokeh_app.authentication.current_user()
    request_username = bokehuser.username
    f = request.files['file']
    url = bokeh_app.datamanager.write(request_username, name, f)
    return url
