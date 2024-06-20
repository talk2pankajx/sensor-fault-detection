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
### DAG Tutorial Documentation
This DAG is demonstrating an Extract -> Transform -> Load pipeline
"""

from __future__ import annotations

# [START tutorial]
# [START import_module]
import json
import textwrap

import pendulum

from sensor.pipeline.training_pipeline import TrainingPipeline
from sensor.entity.config_entity import TrainingPipelineConfig

# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
training_pipeline = TrainingPipeline(training_pipeline_config=TrainingPipelineConfig())

# [END import_module]

# [START instantiate_dag]
with DAG(
    "sensor_training_pipeline",
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={"retries": 2},
    # [END default_args]
    description="DAG tutorial",
    schedule="@weekly",
    start_date=pendulum.datetime(2024, 6, 16, tz="UTC"),
    catchup=False,
    tags=["machine_learning", "classification","sensor"],
) as dag:
    # [END instantiate_dag] 
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    # [START extract_function]
    def data_ingestion(**kwargs):
        ti = kwargs["ti"]
        data_ingestion_artifact = training_pipeline.start_data_ingestion()
        ti.xcom_push("data_ingestion_artifact", data_ingestion_artifact.__dict__)
    
    def data_validation(**kwargs):
        ti = kwargs["ti"]
        from sensor.entity.artifacts_entity import DataIngestionArtifact
        data_ingestion_artifact = ti.xcom_pull(task_ids="data_ingestion", key="data_ingestion_artifact")
        data_ingestion_artifact =DataIngestionArtifact(**(data_ingestion_artifact))
        data_validation_artifact = training_pipeline.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        ti.xcom_push("data_validation_artifact", data_validation_artifact.__dict__)
    
    def data_transformation(**kwargs):
        ti = kwargs["ti"]
        from sensor.entity.artifacts_entity import DataValidationArtifact
        data_validation_artifact = ti.xcom_pull(task_ids="data_validation", key="data_validation_artifact")
        data_validation_artifact =DataValidationArtifact(**(data_validation_artifact))
        data_transformation_artifact = training_pipeline.start_data_transformation(data_validation_artifact=data_validation_artifact)
        ti.xcom_push("data_transformation_artifact", data_transformation_artifact.__dict__)
    
    def model_training(**kwargs):
        ti = kwargs["ti"]
        from sensor.entity.artifacts_entity import DataTransformationArtifact
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation", key="data_transformation_artifact")
        data_transformation_artifact =DataTransformationArtifact(**(data_transformation_artifact))
        model_trainer_artifact = training_pipeline.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
        ti.xcom_push("model_trainer_artifact", model_trainer_artifact.__dict__)
    
    def model_evaluation(**kwargs):
        ti = kwargs["ti"]
        from sensor.entity.artifacts_entity import DataTransformationArtifact,DataValidationArtifact,ModelTrainerArtifact
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation", key="data_transformation_artifact")
        data_transformation_artifact = DataTransformationArtifact(**(data_transformation_artifact))
        
        data_validation_artifact = ti.xcom_pull(task_ids="data_validation", key="data_validation_artifact")
        data_validation_artifact = DataValidationArtifact(**(data_validation_artifact))
        
        model_trainer_artifact = ti.xcom_pull(task_ids="model_training", key="model_trainer_artifact")
        model_trainer_artifact = ModelTrainerArtifact(**(model_trainer_artifact))
        
        model_eval_artifact = training_pipeline.start_model_evaluation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact
        )
        ti.xcom_push("model_eval_artifact", model_eval_artifact.__dict__)

        
    def model_pusher(**kwargs):
        ti = kwargs["ti"]
        from sensor.entity.artifacts_entity import DataTransformationArtifact,DataValidationArtifact,ModelTrainerArtifact
        data_transformation_artifact = ti.xcom_pull(task_ids="data_transformation", key="data_transformation_artifact")
        data_transformation_artifact = DataTransformationArtifact(**(data_transformation_artifact))
        
        model_trainer_artifact = ti.xcom_pull(task_ids="model_training", key="model_trainer_artifact")
        model_trainer_artifact = ModelTrainerArtifact(**(model_trainer_artifact))
        
        model_pusher_artifact = training_pipeline.start_model_pusher(
            model_trainer_artifact = model_trainer_artifact,
            data_transformation_artifact = data_transformation_artifact
        )
        ti.xcom_push("model_pusher_artifact", model_pusher_artifact.__dict__)
        
        
    def push_data_to_s3(**kwargs):
        import os
        bucket_name = os.getenv("BUCKET_NAME")
        artifact_folder ="/app/artifact"
        saved_model_folder="/app/saved_models"
        print("Artifact Folder",artifact_folder)
        os.system(f"aws s3 sync {artifact_folder} s3://{bucket_name}/artifact")
        os.system(f"aws s3 sync {saved_model_folder} s3://{bucket_name}/saved_models")

        
    


    # [START main_flow]
    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )
    data_ingestion_task.doc_md = textwrap.dedent(
        """\
    #### Data Ingestion task
    A simple data ingestion task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    data_validation_task = PythonOperator(
        task_id="data_validation",
        python_callable=data_validation,
    )
    data_validation_task.doc_md = textwrap.dedent(
        """\
    #### Data validation task
    A simple validation task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )
    
    data_transformation_task = PythonOperator(
        task_id="data_transformation",
        python_callable= data_transformation,
    )
    data_transformation_task.doc_md = textwrap.dedent(
        """\
    #### Transformation task
    This helps in data transforming
    """
    )
    
    model_training_task = PythonOperator(
        task_id="model_training",
        python_callable= model_training,
    )
    model_training_task.doc_md = textwrap.dedent(
        """\
    #### Training the model task
    This helps in training the model
    """
    )
    
    model_evaluation_task = PythonOperator(
        task_id="model_evaluation",
        python_callable= model_evaluation,
    )
    model_evaluation_task.doc_md = textwrap.dedent(
        """\
    #### Evaluation of the model 
    This helps evaluation of the model of the current model
    """
    )
    
    model_pusher_task = PythonOperator(
        task_id="model_pusher",
        python_callable= model_pusher,
    )
    model_pusher_task.doc_md = textwrap.dedent(
        """\
    #### Model Pusher
    Pushing the model to the task
    """
    ) 
    
    push_data_to_s3_task= PythonOperator(
        task_id="push_data_to_s3",
        python_callable= push_data_to_s3,
    )
    push_data_to_s3_task.doc_md = textwrap.dedent(
        """\
    #### push data to s3
    Pushing the model to s3 bucket
    """
    ) 
    

    data_ingestion_task >> data_validation_task >> data_transformation_task >> model_training_task >> model_evaluation_task >> model_pusher_task >> push_data_to_s3_task 


# [END main_flow]

# [END tutorial]
