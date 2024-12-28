from predict_service_functions import predict_traffic_sign

image = '../app/data/test/00001.png'

response = predict_traffic_sign(image)

print(f"Class Index is {response['class_index']} and class name is {response['class_name']}")

