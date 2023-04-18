from flask import Flask, request
import cv2
import base64
import numpy as np
from PIL import Image
import json

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    encoded_data = request.data
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (32,32), interpolation = cv2.INTER_AREA)
    pil_image = Image.fromarray(resized)
    img_norm = (np.sum(np.expand_dims(np.array(pil_image), axis=-1)/3, axis=-1, keepdims=True) - 128) / 128
    return json.dumps(img_norm.reshape(1, 32, 32, 1).tolist())

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

app.run(port=5000)
