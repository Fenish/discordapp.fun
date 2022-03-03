import os
import importlib
from flask import Flask, request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


folders = [folder.name for folder in os.scandir() if folder.is_dir() and folder.name[0].isalpha()]
for folder in folders:
    files = [file for file in os.listdir(folder) if file.endswith(".py")]
    for file in files:
        importlib.import_module(f"{folder}.{file.replace('.py', '')}")


@app.route("/")
def welcome():
    map = app.url_map.iter_rules()
    endpoints = []
    for endpoint in list(map)[:-2]:
        endpoints.append(f"{request.base_url}{endpoint.rule.replace('/','')}")
    return {
        "StatusCode": 200,
        "Message": "Welcome to home of useless shits.You cannot find anything if you are not developer.Haha good luck 🍀",
        "Endpoints": endpoints
    }

if __name__ == "__main__":
    app.run()
