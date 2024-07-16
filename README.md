# sensor-fault-detection
Classification about the sensors fault using the sensor reading
source testing

docker run -p 8080:8080 -v %cd%\airflow\dags:/app/airflow/dags -e "MONGO_DB_URL = mongodb+srv://pankajx:qFA9vHeTs93HocdB@cluster0.jg1j5zw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" sensor:latest

