# sensor-fault-detection
Classification about the sensors fault using the sensor reading
source testing

docker run -p 8080:8080 -v ${PWD}\airflow\dags:/app/airflow/dags -e "MONGO_DB_URL = mongodb+srv://pankaj:gqdf1OutSO1zjfCT@cluster0.9l118e0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" sensor:latest




    - AWS_ACCESS_KEY = AKIAZQ3DQI7WN4OFR32S
    - AWS_SECRET_KEY = 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
    - AWS_REGION = ap-southeast-2
    - ECR_LOGIN_URI = 654654326764.dkr.ecr.ap-southeast-2.amazonaws.com
    - ECR_REPOSITORY_NAME = sensor
    - BUCKET_NAME = sensor-project-1112
    - MONG0_DB_URL = mongodb+srv://pankaj:gqdf1OutSO1zjfCT@cluster0.9l118e0.mongodb.net/?retryWrites=true&w=majority