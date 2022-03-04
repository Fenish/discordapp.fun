from flask import Blueprint, request
from googletrans import Translator, LANGUAGES

server = Blueprint("translate_api", __name__)
base_url = "https://api.discordapp.fun/"


@server.route("/translate")
def currency():
    params = request.args
    from_lang = params.get("from")
    to_lang = params.get("to")
    text = params.get("text")
    if not from_lang or not to_lang or not text:
        return {
            "StatusCode": 400,
            "Message": "Invalid parameters",
            "Example": base_url + "translate?&from=EN&to=ES&text=Hello+how+are+you"
        }
    from_lang = from_lang.lower()
    to_lang = to_lang.lower()
    if not LANGUAGES.get(from_lang) or not LANGUAGES.get(to_lang):
        return {
            "StatusCode": 400,
            "Message": "Invalid language. You can get list of languages from " + base_url + "translate/languages",
        }
    translator = Translator()
    translation = translator.translate(text, dest=to_lang, src=from_lang)
    return {
        "StatusCode": 200,
        "From": from_lang,
        "To": to_lang,
        "Original": translation.origin,
        "Message": translation.text
    }


@server.route("/translate/languages")
def get_languages():
    return {
        "StatusCode": 200,
        "Languages": LANGUAGES
    }
