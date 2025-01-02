# Import libraries
import requests
import numpy as np
import json
import pickle
from PIL import Image

def predict_traffic_sign(image):

    # The host where the gateway resides
    url = 'http://aef4e0135fc674e079b622e215972265-452051357.us-east-1.elb.amazonaws.com/predict_traffic_sign'

    # Load image
    img = Image.open(image)
    img = img.resize((32,32))

    # Create image matrix
    x = np.array(img)

    # Serialize the created matrix
    serialized = pickle.dumps(x)

    # Send request to web service
    response = requests.post(url, data=serialized).json()

    # return house price
    return response