from predict_service_functions import predict_traffic_sign

image = './data/test/00000.png'

response = predict_traffic_sign(image)

print(f"Class Index is {response['class_index']} and class name is {response['class_name']}")

