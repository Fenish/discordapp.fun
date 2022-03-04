import os
import importlib
from flask import Flask, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


folders = [folder.name for folder in os.scandir() if folder.is_dir() and folder.name[0].isalpha()]
for folder in folders:
    files = [file for file in os.listdir(folder) if file.endswith(".py")]
    for file in files:
        module = importlib.import_module(f"{folder}.{file.replace('.py', '')}")
        app.register_blueprint(module.server)

base_url = "https://api.discordapp.fun"


@app.route("/")
def welcome():
    map = app.url_map.iter_rules()
    endpoints = []
    for endpoint in list(map)[:-2]:
        endpoints.append(f"{base_url}{endpoint.rule}")
    return {
        "StatusCode": 200,
        "Message": "Welcome to home of useless shits.You cannot find anything if you are not developer.Haha good luck 🍀",
        "Endpoints": endpoints
    }


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
