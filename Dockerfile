FROM python:3.12
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW__CORE_DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE_ENABLE_XCOM_PICKLING=True
RUN airflow db init
RUN airflow users create -e talk2pankajx@gmail.com -f Pankaj -l Prasad -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN apt update -y && apt install awscli -y
ENTRYPOINT [ "/bin/sh" ]
CMD [ "start.sh" ]
