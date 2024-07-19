## Project Overview

The Sensor Fault Prediction project aims to predict faults in sensors using advanced machine learning techniques. This project leverages Apache Airflow for orchestrating data pipelines, ensuring efficient and reliable data processing workflows. After conducting seven experiments, the best model parameters were selected using XGBoost, a powerful and scalable gradient boosting framework. The final model is deployed on AWS to provide real-time predictions.

## Key Features

Data Pipelines with Airflow: Utilizes Apache Airflow to manage and automate data ingestion, preprocessing, and model training pipelines.
Model Selection: Conducted seven experiments to fine-tune and select the best model parameters using XGBoost.
Deployment on AWS: Deployed the trained model on AWS for scalable and reliable predictions.
Real-time Fault Prediction: Provides real-time predictions of sensor faults, enabling proactive maintenance and reducing downtime.
Project Structure
dags/: Contains Airflow DAGs for orchestrating data pipelines.
models/: Includes the trained XGBoost model and related scripts.
sensor/: Contains data preprocessing and model training pipelines.


## Getting Started

Prerequisites

Python 3.8+
Apache Airflow
AWS Account
Docker

## Installation

Clone the repository

git clone https://github.com/talk2pankajx/sensor-fault-prediction.git
cd sensor-fault-prediction


if you are using Conda please create an environment using conda

conda create -m envname -y

## Deploying the application

configure the AWS ec2 service
configure the ECR repository
create an S3 bucket in AWS with /app/input_files

configure a self hoster runner on the github



# To run this project locally

Please install docker desktop on your machine

open the command prompt and add this command 

## docker build -t imagename:tag . 

the connection string from the mongodb atlas or any other database

## mongodb+srv://username:password@cluster0.jg1j5zw.mongodb.net - Mongodb

Then run the following command to run the airflow locally

## docker run -p 8080:8080 -v %cd%\airflow\dags:/app/airflow/dags -e "MONGO_DB_URL = mongodb+srv://username:password@cluster0.jg1j5zw.mongodb.net" sensor:latest


# Contributing

Contributions are welcome! Please fork the repository and submit a pull request.


## Usage

Trigger the Airflow DAG to start the data pipeline.
Monitor the pipeline’s progress through the Airflow web interface.
Access real-time predictions via the deployed model on AWS.
