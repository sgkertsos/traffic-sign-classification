### Description
This is the capstone project for the DataTalks Club ML Zoomcamp 2024.

In this project we will build a traffic sign classification web service.

This web service will take images of traffic signs and classify them. This kind of service could also be used in a self driven car. The car cameras could scan the road for traffic signs and when they find one, the system can classify the sign so that the car could decide what to do. For example if the cameras find a STOP sign, the car would stop.

### Dataset

We will use the **GTSRB - German Traffic Sign Recognition Benchmark** dataset from Kaggle. The dataset can be found in the URL below:

https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign

The two folders we are interested in, are:

* **Train**. All traffic sign images are stored here. You can find 43 folders, and in each folder you can find the images for a specific traffic sign. We will use this folder for model training.
* **Test**. We will use the images in this folder to test our model after it is trained.

### Tecnologies used

#### Jupyter notebook
![image info](./images/Jupyter_logo.png)  
Jupyter notebook is used run the **notebook.ipynb** file. We use this file for **Exploratory Data Analysis** and also for model evaluation and model selection.

#### Gunicorn
![image info](./images/gunicorn.png)  
Gunicorn is s a Python WSGI (Web Server Gateway Interface) HTTP Server. The Flask application runs on this server.

### Flask
![image info](./images/flask.png)  
Flask is the framework which we use to create the prediction web service. 

#### Streamlit
![image info](./images/streamlit.png)  
Streamlit is used to create the user interface (UI). The user selects a traffic sign image file by using the **** button or by just dragging the file and the output is displayed.

#### Docker
![image info](./images/docker.png)  
We use docker to create the containers for our app. We actually have two containers. One which contains the user interface and the script that allows us to connect to the predict service, and one which is actually our predict service.

#### Scikit-learn
![image info](./images/scikit-learn.png)  
We use the **scikit-learn** python library to handle data splitting.

#### Tensorflow
![image info](./images/tf.png)  
We use the **tensorflow** library to perform the model training.

### Application flow

Below you can see the application flow diagram.  

![image info](./images/app_flow_diagram.png)  

The user opens a r and accesses a simple form which is actually a streamlit app. All the user has to do is select the desired traffic sign image **(png/jpg)** by using the **Browse files** button or by just dragging the file. The streamlit app uses a function from the **predict_service_functions.py** file to connect to the web service **(predict_service.py)**. The connection is made by using the **/predict_traffic_sign** endpoint. The **predict** function uses the model **(traffic_sign_classification_model.h5)** to predict a traffic sign class. The traffic sign class with a short description is then returned to the user and displayed below the image selection box. The **init.py** script runs when the application starts. You can read more about this script in the **Run the application** section.

### Application structure

The following folders/files are included in the application:

* **app** folder. This folder contains all the files needed for the application to run.
* **data** folder. The application data file is stored here.
* **model** folder. The trained model **(traffic_sign_classification_model.h5)** is stored here.
* **docker-compose.yaml, Dockerfile.gunicorn** and **Dockerfile.streamlit** are used by docker to create the **UI** and **Predict Web Service** application containers.
* **requirements.streamlit.txt**. All python libraries with their versions, used by the UI container are stored here.
* **app.py**. This is the application entry point. It is the file that is loaded when the UI container starts.
* **predict_service_functions.py** This file contains the necessary functions to connect to the traffic sign classification web service.
* **requirements.gunicorn.txt**. All python libraries with their versions, used by the predict service container are stored here.
* **init.py**. This file is used to perform data preparation, to split the data into train and validation datasets, to train and finally save the model.
* **predict_service.py** This is the traffic sign classification web service. This service receives a traffic sign image in png/jpg format and returns a predicted traffic sign class.
* **notebook.ipynb** This is a Jupyter notebook file which was used for Exploratory Data Analysys and also for model evaluation and model final selection. After the best model is selected, this model is then used in the application.
* **README.md**. This file.

### Install Jupyter Notebook and Docker

#### Install Jupyter Notebook
To install Jupyter Notebook you can use the following link:

https://docs.jupyter.org/en/latest/install/notebook-classic.html

#### Install Docker and Docker Compose 
To install Docker and Docker Compose you can use the following links:

https://docs.docker.com/engine/install/  
https://docs.docker.com/compose/install/

### Run the application

#### Clone the github repository
Open a terminal, navigate to a folder where you want the repository files to be stored and then type:  

```console
git clone https://github.com/sgkertsos/traffic-sign-classification.git
```

#### Download the dataset
Download the **archive.zip** file from the link below:

https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign

and save it in the **app/data** folder.

In your terminal type:

```console
cd traffic-sign-classification/app/data
unzip archive.zip
```

#### Start the application

There are two possibilities here:

* Use the already trained model **(traffic_sign_classification_mode.h5)**  
  In **Dockerfile.gunicorn** comment out the following lines:

  ![image info](./images/comment_out_data.png)

  **NOTE**
  This is the selected method to run the application because it saves you time, training the model.
  
* Train the model again. The training may take some time.
  In **Dockerfile.gunicorn** comment out the following line:
  
  ![image info](./images/comment_out_model.png)  

Start the application by typing the following commands:

```console
cd traffic-sign-classification/app
docker compose up
```
Wait for the application to load. 

After the application loading is done we have two docker containers running simultaneously:

* Gunicorn on port 9696    
* Streamlit on port 8501

When the Gunicorn docker container starts for the first time, the **init.py** script runs. If you have selected the second option, to train the model again the following happen:

* Images are loaded
* Images are resized to 32x32 pixels and stored in the **app/data/train-r** folder.
* Dataset is split into train and validation data
* A model with specific parameters is trained. The specific model and the specific parameters were selected after model evaluation was performed by using the **notebook.ipynb** Jupyter Notebook file.
* The model is saved under the filename **traffic_sign_classification_model.h5** in the **app/model** folder.

This model is then loaded by the traffic sign classification web service to classify traffic signs. 

**Note**  
The script checks if the model file **(traffic_sign_classification_model.h5)** file exists. If the file exists, the script will not perform the initialization process again.

### Access the user interface
Open your preferred browser and navigate to the following address:

http://localhost:8501

The application loads and you are presented with the traffic sign image selection button.  

![image info](./images/app.png)  

Select a traffic sign image by clicking the **Browse files** button or by just dragging the image on the gray area.  

The traffic sign class index and description appear below the gray area.  

![image info](./images/app_classification_made.png)  

### Run notebook.ipynb Jupyter Notebook
If you want to check how the model evaluation was made, you can do it by opening the **notebook.ipynb** file in Jupyter Notebook and execute the code in each cell.

To start Jupyter Notebook make sure that you are in the **traffic-sign-classification** folder and then type the following in your terminal:

```console
jupyter notebook
```
Copy the URL that is shown in your terminal and paste it in your preferred browser. The following picture appears. 

![image info](./images/jupyter.png)  

Double click on the **notebook.ipynb** file. The file is opened in a different tab. In this file we do the following:

* We perform Exploratory Data Analysis. 
* We train and evaluate different models.

Each notebook cell has a short description of what is actually done.

### AWS Elastic Kubernetes Service
A Kubernetes cluster with this traffic sign classification service runs on AWS. You can access it by doing the following:

* Open a terminal and navigate to the **eks** folder. Then type:
 ```console
docker build -t streamlit_eks -f Dockerfile.streamlit .
```
to build the streamlit app, the eks version.
* After the image is built you can run it by typing:
```console
docker run -p 8501:8501 --name streamlit_eks -t streamlit_eks
```
* Finally open your preferred browser and type the following:
```console
http://localhost:8501
```
So now you can upload images to the traffic sign classification service to get a classification as you did with the local version.
But now the classification takes place on the EKS cluster.

### Build your own AWS EKS cluster for the traffic sign classification service
In this section we will show you how you can build your own AWS EKS cluster with the
traffic sign classification service.

#### Prerequisities

* An AWS account

* Install AWS CLI
You can see how to install AWS CLI in the following link:  
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html  

* Install kubectl and eksctl
You can see how to install kubectl and eksctl in the following link
https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

Open your terminal and access the **eks** folder.

Follow the next steps one by one:  

* Configure **AWS CLI**. Type:
```console
aws configure
```
Provide:  

AWS Access Key ID  
AWS Secret Access Key  
Default region name  
Default output format  

* Build the **TF serving** image. Type:
```console
docker build -t tf-serving-traffic-sign-classification-model -f Dockerfile.tfserving .
```

* Build the **gateway** image. Type:
```console
docker build -t serving-gateway -f Dockerfile.gateway .
```

* Create an **ECR repository**. Type:
```console
aws ecr create-repository --repository-name model-serving
```

It returns the following:  
**ACCOUNT**.dkr.ecr.**REGION**.amazonaws.com/model-serving

Where **ACCOUNT** is your ACCOUNT ID and **REGION** is your region.

**In the instructions that follow you have to replace the ACCOUNT ID and the REGION with those two values.**

* Authenticate with ECR. Type:  
```console
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <ACCOUNT ID>.dkr.ecr.<REGION>.amazonaws.com
```
It must return  
Login Succeeded

* Tag images. Type:
```console
docker tag serving-gateway <ACCOUNT ID>.dkr.ecr.<REGION>.amazonaws.com/model-serving:serving-gateway
docker tag tf-serving-traffic-sign-classification-model <ACCOUNT ID>.dkr.ecr.<REGION>.amazonaws.com/model-serving:tf-serving-traffic-sign-classification-model
```

* Push images to ECR. Type:
```console
docker push <ACCOUNT ID>.dkr.ecr.<REGION>.amazonaws.com/model-serving:serving-gateway
docker push <ACCOUNT ID>.dkr.ecr.<REGION>.amazonaws.com/model-serving:tf-serving-traffic-sign-classification-model
```

* Create kubernetes cluster. Type:
```console
eksctl create cluster -f cluster.yaml
```

* Make kubectl access the newly created cluster. Type:
```console
aws eks --region <REGION> update-kubeconfig --name tsc-eks
```

* Add **tf-serving** container to kubernetes cluster. Type:
```console
kubectl apply -f tf-serving-traffic-sign-classification-deployment.yaml
```

* Add **tf-serving** service to kubernetes cluster. Type:
```console
kubectl apply -f tf-serving-traffic-sign-classification-service.yaml
```

* Add **serving-gateway** to kubernetes cluster. Type:
```console
kubectl apply -f serving-gateway-deployment.yaml
```

* Add **serving-gateway** service to kubernetes cluster. Type:
```console
kubectl apply -f serving-gateway-service.yaml
```

* Find service external URL. Type:
```console
kubectl describe service serving-gateway
```
we see the value in the LoadBalancer Ingress line, eg  
a8890f67a9ca24353a8c8b53653d442e-140471327.us-east-1.elb.amazonaws.com

The kubernetes cluster is created. You can check it by typing the following commands:  

 * Check deployments. Type:
```console
kubectl get deployments
```

* Check pods. Type:
```console
kubectl get pods
```

* Check services. Type:
```console
kubectl get services
```

**The newly created kubernetes cluster cannot be used for free and it is charged. So if you want to delete it you can type the following:**  

```console
eksctl delete cluster --name tsc-eks
```

### Notes

#### Access docker container terminal
First you have to find the docker container id.

Type:

```console
docker ps
```
and note the container id, eg 68967bc26fc0

Copy the container id and then type:

```console
docker exec -it 68967bc26fc0 bash
```
You are now in the **/app** folder and you are ready to interact with the application files. If for example you are in the Gunicorn/Flask container, you can take a look at the **data** or **model** folders mentioned earlier, but you could also experiment with the communication between the containers by using such commands as **curl** and **ping**.  



