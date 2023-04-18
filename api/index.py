from flask import Flask, request
import cv2
import base64
import numpy as np
from PIL import Image
import json
from uuid import uuid4

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert():
    decoded = base64.b64decode(request.data)
    id = str(uuid4())
    f = open(id + ".png", "wb")
    f.write(decoded)
    f.close()
    img = cv2.imread(id + ".png", cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (32,32), interpolation = cv2.INTER_AREA)
    pil_image = Image.fromarray(resized)
    img_norm = (np.sum(np.expand_dims(np.array(pil_image), axis=-1)/3, axis=-1, keepdims=True) - 128) / 128
    return json.dumps(img_norm.reshape(1, 32, 32, 1).tolist())

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

@app.route('/classes', methods=['GET'])
def classes():
    return json.dumps({0: 'Speed limit (20km/h)',
              1: 'Speed limit (30km/h)',
              2: 'Speed limit (50km/h)',
              3: 'Speed limit (60km/h)',
              4: 'Speed limit (70km/h)',
              5: 'Speed limit (80km/h)',
              6: 'End of speed limit (80km/h)',
              7: 'Speed limit (100km/h)',
              8: 'Speed limit (120km/h)',
              9: 'No passing',
              10: 'No passing for vehicles over 3.5 metric tons',
              11: 'Right-of-way at the next intersection',
              12: 'Priority road',
              13: 'Yield',
              14: 'Stop',
              15: 'No vehicles',
              16: 'Vehicles over 3.5 metric tons prohibited',
              17: 'No entry',
              18: 'General caution',
              19: 'Dangerous curve to the left',
              20: 'Dangerous curve to the right',
              21: 'Double curve',
              22: 'Bumpy road',
              23: 'Slippery road',
              24: 'Road narrows on the right',
              25: 'Road work',
              26: 'Traffic signals',
              27: 'Pedestrians',
              28: 'Children crossing',
              29: 'Bicycles crossing',
              30: 'Beware of ice/snow',
              31: 'Wild animals crossing',
              32: 'End of all speed and passing limits',
              33: 'Turn right ahead',
              34: 'Turn left ahead',
              35: 'Ahead only',
              36: 'Go straight or right',
              37: 'Go straight or left',
              38: 'Keep right',
              39: 'Keep left',
              40: 'Roundabout mandatory',
              41: 'End of no passing',
              42: 'End of no passing by vehicles over 3.5 metric tons'})

app.run(port=5003)
