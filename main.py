import os
import importlib
from flask import Flask

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/")
def welcome():
    return {
        "StatusCode": 200,
        "Message": "Welcome to home of useless shits.You cannot find anything if you are not developer.Haha good luck 🍀"
    }


folders = [folder.name for folder in os.scandir() if folder.is_dir() and folder.name[0].isalpha()]
for folder in folders:
    files = [file for file in os.listdir(folder) if file.endswith(".py")]
    for file in files:
        importlib.import_module(f"{folder}.{file.replace('.py', '')}")

if __name__ == "__main__":
    app.run()
