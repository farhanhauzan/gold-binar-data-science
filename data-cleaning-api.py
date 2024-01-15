import re

from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from


class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: "API Documentation for Data Processing and Modeling"),
        'version' : LazyString(lambda: "1.0.0"),
        'description' : LazyString(lambda: " API untuk Data Text Processing dan Modeling Level Gold"),
    },
    host = LazyString(lambda: request.host)
)


swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint": "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config = swagger_config)

@swag_from("docs/welcome.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def welcome():
    json_response = {
        'status_code': 200,
        'description': "Welcome to data processing api",
        'data': "please input your data",
    }

    response_data = jsonify(json_response)
    return response_data


@swag_from("docs/text_processing.yml", methods= ['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    
    json_response = {
        'status_code': 200,
        'description': "hasil text yang telah di proses",
        
        # mengcovert menjadi lowercase
        
        # menghilangkan http
        # menghilangkan random url
        # menghilangkan symbol    
        
        # menghilangkan user tag    
        'data': re.sub('user', ' ', text),
        # menghilangkan "rt" tag    
        'data': re.sub('rt', ' ', text),   
        # menghilangkan tab
        'data': re.sub('\t', ' ', text),
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text), 
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/csv_processing.yml", methods= ['POST'])
@app.route('/csv-processing', methods=['POST'])
def csv_processing():

    file = request.files.get['file']    
    json_response = {
        'status_code': 200,
        'description': "Csv file yang telah di proses",
        'data': 'file',
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()