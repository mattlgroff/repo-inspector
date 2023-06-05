from flask import Flask, jsonify, Response, request, send_from_directory
from git import Repo
import os
import shutil

app = Flask(__name__, static_folder='public')

@app.route('/')
def hello():
    return jsonify(message="Repo Inspector is live!")

@app.route('/logo.png', methods=['GET', 'OPTIONS'])
def get_logo():
    if request.method == 'OPTIONS':
        return ('', 204, {})
    return send_from_directory(app.static_folder, 'logo.png')

@app.route('/legal')
def legal():
    return jsonify(message="MIT License. This comes with no warranty. Use at your own risk. No data is saved. All data is deleted after each request.")

@app.route('/.well-known/ai-plugin.json', methods=['GET', 'OPTIONS'])
def get_plugin_json():
    if request.method == 'OPTIONS':
        return ('', 204, {})

    with open('./public/.well-known/ai-plugin.json', 'r') as f:
        json_data = f.read()
        return Response(json_data, mimetype='text/json')

@app.route('/openapi.yaml', methods=['GET', 'OPTIONS'])
def get_openapi_yaml():
    if request.method == 'OPTIONS':
        return ('', 204, {})

    with open('./public/openapi.yaml', 'r') as f:
        yaml_data = f.read()
        return Response(yaml_data, mimetype='text/yaml')

def clone_repo(repo_url):
    """Clone a Git repository to a temporary directory and return the path."""
    temp_path = repo_url.split('://')[-1].replace('/', '_')  # create a unique temporary path
    if not os.path.exists(temp_path):
        Repo.clone_from(repo_url, temp_path)
    return temp_path

@app.route('/inspect_folder', methods=['POST', 'OPTIONS'])
def inspect_folder():
    if request.method == 'OPTIONS':
        return ('', 204, {})

    json_data = request.get_json()
    if not json_data or 'repo_to_clone' not in json_data:
        return jsonify(message="Bad Request"), 400

    repo_url = json_data['repo_to_clone']
    folder_path = json_data.get('folder_path', '')  # Default to root directory if not provided

    if not repo_url.startswith('https://'):
        return jsonify(message="Bad Request, please provide an https Git link"), 400

    try:
        temp_path = clone_repo(repo_url)
        full_path = os.path.join(temp_path, folder_path)

        filenames = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

        shutil.rmtree(temp_path)

        return jsonify(filenames=filenames), 200
    except Exception as e:
        return jsonify(message=str(e)), 404


@app.route('/inspect_file', methods=['POST', 'OPTIONS'])
def inspect_file():
    if request.method == 'OPTIONS':
        return ('', 204, {})

    json_data = request.get_json()
    if not json_data or 'repo_to_clone' not in json_data or 'file_path' not in json_data:
        return jsonify(message="Bad Request"), 400

    repo_url = json_data['repo_to_clone']
    file_path = json_data['file_path']

    if not repo_url.startswith('https://'):
        return jsonify(message="Bad Request, please provide an https Git link"), 400

    try:
        temp_path = clone_repo(repo_url)

        with open(os.path.join(temp_path, file_path), 'r') as f:
            content = f.read()

        shutil.rmtree(temp_path)

        return jsonify(content=content), 200
    except FileNotFoundError:
        return jsonify(message="File not found"), 404
    except Exception as e:
        return jsonify(message=str(e)), 500

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://chat.openai.com'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response