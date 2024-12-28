import grpc
import tensorflow as tf

from PIL import Image
import numpy as np
import pickle

from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc

from flask import Flask
from flask import request
from flask import jsonify

# Class descriptions
class_descriptions = {
    0: 'Speed limit (20km/h)',
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
    42: 'End of no passing by vehicles over 3.5 metric'
}

# Variables used by gRPC communication
host = 'tf-serving-traffic-sign-classification-model:8500'
channel = grpc.insecure_channel(host)
stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)


# This function gets a traffic sign image as an input and makes a prediction
def make_prediction(x):
    
    # Create image matrix
    X = np.array([x])
    X = np.float32(X)

    # Make prediction
    pb_request = predict_pb2.PredictRequest()
    pb_request.model_spec.name = 'traffic_sign_classification_model'
    pb_request.model_spec.signature_name = 'serving_default'
    pb_request.inputs['input_1'].CopyFrom(tf.make_tensor_proto(X, shape=X.shape))
    pb_result = stub.Predict(pb_request, timeout=20.0)   
    preds = pb_result.outputs['dense_1'].float_val

    # Get class info
    class_index = np.argmax(preds)
    class_name = class_descriptions[class_index]

    # Return info
    return class_index, class_name

# Create Flask app
app = Flask('predict_service')

# Create predict function
@app.route('/predict_traffic_sign', methods=['POST'])
def predict():
    # Get serialized image
    serialized_image = request.data

    # Create matrix
    x = pickle.loads(serialized_image)

    # Make prediction
    class_index, class_name = make_prediction(x)

    result = {
        'class_index': int(class_index),
        'class_name': class_name
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)