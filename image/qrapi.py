import cv2
import qrcode
import requests
import numpy as np

from io import BytesIO
from flask import request, send_file, Blueprint
from urllib.request import Request, urlopen

server = Blueprint("qr_api", __name__)
base_url = "https://api.discordapp.fun/"


@server.route("/qr")
def qr_api():
    args = request.args
    if not args.get("text") and not args.get("qrcode"):
        return {
            "StatusCode": 400,
            "Message": "Invalid parameters",
            "Parameters": {
                "Text": base_url + "qr?&text=https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "Qrcode": base_url + "qr?&qrcode=image_url"
            }
        }
    if args.get("text"):
        qr_text = args["text"]
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=1)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

    if args.get("qrcode"):
        qr_url = args["qrcode"]
        image_formats = ("image/png", "image/jpeg", "image/gif")
        try:
            site = requests.get(qr_url)
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

        req = Request(qr_url, headers={'User-Agent': "Magic Browser"})
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
