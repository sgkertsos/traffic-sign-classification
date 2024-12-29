# Import libraries
import requests
import numpy as np
import json
import pickle
from PIL import Image

def predict_traffic_sign(image):

    # The host where the gateway resides
    url = 'http://a8890f67a9ca24353a8c8b53653d442e-140471327.us-east-1.elb.amazonaws.com/predict_traffic_sign'

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