import cv2
import qrcode
import requests
import numpy as np

from io import BytesIO
from urllib.request import Request, urlopen
from flask import request, send_file, Blueprint


server = Blueprint("qr_api", __name__)
base_url = "https://api.discordapp.fun/"


@server.route("/qr")
def qr_api():
    params = request.args
    param_create = params.get("create")
    param_read = params.get("read")

    if not param_create and not param_read:
        return {
            "StatusCode": 400,
            "Message": "Invalid parameters",
            "Parameters": {
                "Create QR Code": base_url + "qr?create=https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "Read QR code": base_url + "qr?read=qrcode_url"
            }
        }
    if param_read:
        qr_code = read_qr(param_read)
        return qr_code
    elif param_create:
        qr_code = create_qr(param_create)
        return send_file(qr_code, mimetype='image/jpeg')


def read_qr(image_url):
    if image_url:
        image_formats = ("image/png", "image/jpeg", "image/gif")
        try:
            site = requests.get(image_url)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.ConnectionError,
                requests.exceptions.InvalidSchema):
            return {
                "StatusCode": 400,
                "Message": "Please request with valid url"
            }
        headers = site.headers
        content_type = headers.get("Content-Type")
        if content_type not in image_formats:
            return {
                "StatusCode": 400,
                "Message": "Please request with valid image url"
            }

        req = Request(image_url, headers={'User-Agent': "Magic Browser"})
        resource = urlopen(req)
        img_bytes = BytesIO(resource.read())
        file_bytes = np.asarray(bytearray(img_bytes.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        det = cv2.QRCodeDetector()
        val, pts, st_code = det.detectAndDecode(img)
        if not val:
            return {
                "StatusCode": 400,
                "Message": "Please request with valid qr code"
            }
        return {
            "StatusCode": 200,
            "Message": val
        }


def create_qr(text):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=1)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io
