import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array

from flask import Flask
from flask import request
from flask import jsonify
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins="http://localhost:5000", supports_credentials=True)

def getModel():
    global model 
    model = load_model('VGG16_cats_and_dogs.h5')
    print(" * Model loaded!")

def preprocessImage(image, targetSize):
    if (image.mode != "RGB"):
        image = image.convert("RGB")
    image = image.resize(targetSize)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image 

print(" * Loading Keras model...")
getModel()

@app.route("/predict", methods=["POST"])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processedImage = preprocessImage(image, targetSize=(224, 224))

    prediction = model.predict(processedImage).tolist()

    response = {
        'prediction': {
            'dog': prediction[0][0],
            'cat': prediction[0][1]
        }
    }
    return jsonify(response)
