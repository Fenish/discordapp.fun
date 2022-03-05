import requests
from io import BytesIO
from selenium import webdriver
from flask import request, send_file, Blueprint
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")

server = Blueprint("screenshot", __name__)
base_url = "https://api.discordapp.fun/"


def get_browser():
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com")
    return driver


browser = get_browser()
img_cache = {}


@server.route("/screenshot")
def screenshot():
    params = request.args
    url = params.get("url")
    width = params.get("width") if params.get("width") else "1280"
    height = params.get("height") if params.get("height") else "720"
    selector = params.get("selector")
    if not url or not width.isnumeric() or not height.isnumeric():
        return {
            "StatusCode": 400,
            "Message": "Invalid Parameters",
            "Parameters": {
                "URL": {
                    "Description": "Specify a url to screenshot",
                    "Usage": base_url + "screenshot?url=www.google.com"
                },
                "Optional Parameters": {
                    "Width": "Defines width of webpage. Default is 1280, Maximum 1920",
                    "Height": "Defines height of webpage. Default is 720, Maximum 1080",
                    "Selector": "Defines selector to screenshot. Default is None"
                }
            }
        }

    if not url.startswith("https://") and not url.startswith("http://"):
        url = "http://" + url
    try:
        requests.get(url)
    except (requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema):
        return {
            "StatusCode": 404,
            "Message": "Website Not Found. Please request with valid url"
        }

    is_cached = img_cache.get(url)
    if is_cached:
        b_img = BytesIO(img_cache[url]["image"])
        c_width = img_cache[url]["width"]
        c_height = img_cache[url]["height"]
        if width == c_width and height == c_height:
            return send_file(b_img, mimetype='image/jpeg')

    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[-1])

    browser.get(url)
    browser.set_window_size(int(width), int(height))
    img = browser.get_screenshot_as_png()
    b_img = BytesIO(img)

    browser.execute_script("window.close();")
    browser.switch_to.window(browser.window_handles[0])

    img_cache[url]["image"] = img
    img_cache[url]["width"] = width
    img_cache[url]["height"] = height
    return send_file(b_img, mimetype='image/jpeg')
