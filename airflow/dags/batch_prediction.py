#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""

from __future__ import annotations

# [START tutorial]
# [START import_module]
import textwrap
import os
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from sensor.entity.config_entity import BatchPredictionConfig
from sensor.pipeline.batch_prediction import BatchPrediction

# [END import_module]

config = BatchPredictionConfig()

# [START instantiate_dag]
with DAG(
    "batch_prediction",
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2,},
    # [END default_args]
    description="Sensor_fault_detection",
    schedule="@weekly",
    start_date=datetime(2024, 6, 16),
    catchup=False,
    tags=["Batch_prediction", "machine_learning", "classification","sensor"],
) as dag:
    def download_files(**kwargs):
        import os
        bucket_name = os.getenv("BUCKET_NAME")
        input_dir = "/app/input_files"
        # creating the directory if it does not exist
        os.makedirs(input_dir, exist_ok=True)
        os.system(f"aws s3 sync s3://{bucket_name}/inbox {config.inbox_dir}")
    def batch_prediction(**kwargs):
        config = BatchPredictionConfig()
        batch_prediction =BatchPrediction(batch_config=config)
        batch_prediction.initiate_batch_prediction()
    
    def upload_files(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync {config.archive_dir} s3://{bucket_name}/archive")
        os.system(f"aws s3 sync {config.outbox_dir} s3://{bucket_name}/outbox")
    
    
    download_files_task= PythonOperator(
        task_id="download_files",
        python_callable= download_files,
    )
    download_files_task.doc_md = textwrap.dedent()
    
    
    batch_prediction_task= PythonOperator(
        task_id="batch_prediction",
        python_callable= batch_prediction,
    )
    batch_prediction_task.doc_md = textwrap.dedent()
    
    
    upload_input_files= PythonOperator(
        task_id="upload_files",
        python_callable= upload_files,
    )
    upload_input_files.doc_md = textwrap.dedent()
    
    
    download_files_task >> batch_prediction_task >> upload_input_files